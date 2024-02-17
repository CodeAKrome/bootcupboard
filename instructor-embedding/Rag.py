from segtok.segmenter import split_single
from flair.data import Sentence
import mmap
import fire
import re
import flair
import torch
from tqdm import trange, tqdm
import chromadb
from chromadb.utils import embedding_functions
from flair.models import SequenceTagger
from time import time
# import spacy
# from litellm import token_counter
from flair.models import SequenceTagger
from flair.data import Sentence
from flair.nn import Classifier
from flair.splitter import SegtokSentenceSplitter


"""
Requirements:
pip install fire flair torch chromadb tqdm InstructorEmbedding sentence_transformers litellm
"""

"""
Pip install command:

Poetry install command:

Run chroma in server mode:
chroma run --path /db_path

Client connection:
chroma_client = chromadb.HttpClient(host='localhost', port=8000)

Docker image with NLP libraries installed:
https://github.com/poteha/docker-nlp

Example commands:
For Merry Wives of Windsor
python Rag.py playrag --file=docs/merry.txt --collection_name=merry
python Rag.py query --q="Falstaff" --where='{"role":"PAGE."}' --where_document='{"$contains":"disguise"}'
"""

# ----- OUTSIDE CLASS -----



def runtime(func):
    """Time function execution."""

    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


# ----- OUTSIDE CLASS -----

DEFAULT_CHUNK_SIZE = 512
DEFAULT_DOCUMENT = "artofwar.txt"
DEFAULT_QUERY = "What are the seven considerations?"
DEFAULT_INSTRUCTION = "Represent the sentences for retrieval"
DEFAULT_COLLECTION_NAME = "default"
DEFAULT_DB_PATH = "db/chroma/default"
DEFAULT_MODEL_NAME = "hkunlp/instructor-xl"
DEFAULT_RESULTS = 3
DEFAULT_SEQUENCE_TAGGER = "flair/ner-english-large"
# Used for lemmatization
#DEFAULT_SPACY_MODEL_NAME = 'en_core_web_sm'

# Change this to use a different CUDA device or devices like 'cuda:0,1'
if torch.cuda.is_available():
    flair.device = torch.device("cuda:0")
    device_name = "cuda"
else:
    if torch.backends.mps.is_available():
        flair.device = torch.device("mps")
        device_name = "mps"
    else:
        flair.device = torch.device("cpu")
        device_name = "cpu"


class Rag(object):
    """Vector similarity search with chromadb and NER using flair."""

    def __init__(
        self,
        collection_name=DEFAULT_COLLECTION_NAME,
        instruction=DEFAULT_INSTRUCTION,
        database_path=DEFAULT_DB_PATH,
        model_name=DEFAULT_MODEL_NAME,
        device_name=device_name,
        chunk_size=DEFAULT_CHUNK_SIZE,
#        spacy_model_name = DEFAULT_SPACY_MODEL_NAME,
    ):
        self.instruction = instruction
        self.collection_name = collection_name
        self.database_path = database_path
        self.model_name = model_name
        self.device_name = device_name
        self.client = chromadb.PersistentClient(path=self.database_path)
        self.embedding_function = embedding_functions.InstructorEmbeddingFunction(
            model_name=self.model_name,
            device=self.device_name,
            instruction=self.instruction,
        )
        self.coll = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
            metadata={"instruction": self.instruction},
        )
        # Load the spaCy English model
        # if not spacy.util.is_package(spacy_model_name):
        #     spacy.cli.download(spacy_model_name)
        # self.nlp = spacy.load(spacy_model_name)
        # self.spacy_model_name = spacy_model_name
#        self.sequence_tagger = SequenceTagger.load(DEFAULT_SEQUENCE_TAGGER)
        self.splitter = SegtokSentenceSplitter()
        self.link_tagger = Classifier.load('linker')
                

    def tokens(self, text: str):
        messages = [{"user": "role", "content": text}]
        return token_counter(model=self.model_name, messages=messages)


    def lemmatized(self, text:str) -> str:
        """Lemmatize the text using spaCy."""
        doc = self.nlp(text)
        lemmatized_tokens = [token.lemma_ for token in doc]
        return ' '.join(lemmatized_tokens)


    def mmap_file(self, filepath):
        """Use memory mapping to MAINLINE an entire file."""
        with open(filepath, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            return mm.read().decode()

    def sentences(self, file=DEFAULT_DOCUMENT):
        """Break a file into lines by sentence."""
        print(f"Reading: {file}")
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text)
        sents = split_single(text)
        sents = [sent for sent in sents if sent]
        sentences = [Sentence(sent, use_tokenizer=True) for sent in sents]
        for sent in sentences:
            yield sent

    def sents(self, file=DEFAULT_DOCUMENT, block_size=3):
        """Break a file into lines by sentence."""
        print(f"Reading: {file} Block: {block_size}")
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text)
        sents = split_single(text)
        sents = [sent for sent in sents if sent]
        sentences = [Sentence(sent, use_tokenizer=True) for sent in sents]
        block_num = 0
        block_text = []
        for sent in sentences:
            block_text.append(sent.text)
            block_num += 1
            if block_num % block_size == 0:
                out = " ".join(block_text)
                block_text = []
                yield out
        if block_text:
            yield " ".join(block_text)

    def psents(self, file=DEFAULT_DOCUMENT, block_size=3):
        for block in self.sens(file, block_size):
            print(block)

    def play(self, file=DEFAULT_DOCUMENT):
        """Break a play into lines.
        Concatenate next line to this if this line starts with capitals."""
        buf = ""
        for sentence in self.sentences(file):
            txt = sentence
            if re.match(r"^\w+\.$", txt):
                buf = txt
                continue
            if buf:
                txt = f"{buf} {txt}"
                buf = ""
            yield txt

    def psentences(self, file=DEFAULT_DOCUMENT):
        """Print a file by sentences."""
        for sentence in self.sentences(file):
            print(sentence)

    def pplay(self, file=DEFAULT_DOCUMENT):
        """Print a play by sentences."""
        for sentence in self.play(file):
            print(sentence)

    def playrag(self, file=DEFAULT_DOCUMENT, collection_name=False):
        """Break a play into lines.
        Concattenate next line to this if this line starts with capitals.
        Remove the role names from embedding, use as metadata"""
        if collection_name:
            self.get_collection(collection_name)
        role = ""
        i = 0
        for sentence in tqdm(self.sentences(file)):
            txt = sentence
            if re.match(r"^[A-Z]+\.?$", txt):
                role = re.sub(r"\.", "", txt)
                continue
            self.coll.upsert(
                ids=[f"{file}:{i}"], metadatas=[{"role": role}], documents=[txt]
            )
            i += 1
        print(f"Upserted {i} records.")

    @runtime
    def playraghog(self, file=DEFAULT_DOCUMENT, collection_name=False, batch_size=5):
        """This requires boatloads of memory.
        It will probably blow up.🕸️
        You have been warned! 💀
        Break a play into lines.
        Concatenate next line to this if this line starts with capitals.
        Remove the role names from embedding, use as metadata"""
        if collection_name:
            self.get_collection(collection_name)
        role = ""
        i = 0
        ids = []
        metadatas = []
        documents = []
        for sentence in tqdm(self.sentences(file)):
            txt = str(sentence)
            # pretxt = txt
            # pretoke = self.tokens(txt)
            # txt = self.lemmatized(txt)
            # posttoke = self.tokens(txt)
            # print(f"pre post: {pretoke} {pretxt}  {posttoke} {txt}")
            
            if re.match(r"^[A-Z]+\.?$", txt):
                role = txt.replace(".", "")
                continue
            ids.append(f"{file}:{i}")
            metadatas.append({"role": role})
            documents.append(txt)
            i += 1
            if i % batch_size == 0:
                self.coll.upsert(ids=ids, metadatas=metadatas, documents=documents)
                ids = []
                metadatas = []
                documents = []
        if ids:
            self.coll.upsert(ids=ids, metadatas=metadatas, documents=documents)
        print(f"Batch size: {batch_size}\nUpserted: {i}")

    def peek(self, collection_name=False):
        """Show first few items of collection"""
        if collection_name:
            self.get_collection(collection_name)
        return self.coll.peek()

    def rag0(self, file=DEFAULT_DOCUMENT, collection_name=False):
        """Break a file into lines by sentence and store it in chromadb."""
        if collection_name:
            self.get_or_create_collection(collection_name)
        i = 0
        for sentence in tqdm(self.sentences(file=file)):
            self.coll.upsert(documents=[sentence], ids=[f"{file}:{i}"])
            i += 1
        print(f"Upserted {i} records.")

    # ===============

    @runtime
    def rag(self, file=DEFAULT_DOCUMENT, collection_name=False, block_size=3):
        """Break a file into lines by sentence and store it in chromadb."""
        if collection_name:
            metadata = {
                "file": file,
                "instruction": self.instruction,
                "block_size": block_size,
            }
            self.get_or_create_collection(name=collection_name, metadata=metadata)
        i = 0
        for sentence in tqdm(self.sents(file=file, block_size=block_size)):
            metadatas = [{"file": file, "block": i}]
            self.coll.upsert(
                documents=[sentence], ids=[f"{file}:{i}"], metadatas=metadatas
            )
            i += 1
        print(f"Upserted: {i}")

    def query_json(
        self,
        q=DEFAULT_QUERY,
        collection_name=False,
        n=DEFAULT_RESULTS,
        where={},
        where_document={},
    ):
        """Return json query results"""
        results = self.query(
            query_texts=[q],
            n_results=n,
            where=where,
            where_document=where_document,
        )
        out = results["documents"][0]
        return out

    def query(
        self,
        q=DEFAULT_QUERY,
        collection_name=False,
        n=DEFAULT_RESULTS,
        where={},
        where_document={},
    ):
        print(f"Query: {q}")
        
        """Return raw chroma results."""
        if collection_name:
            self.get_collection(collection_name)
        return self.coll.query(
            query_texts=[q],
            n_results=n,
            where=where,
            where_document=where_document,
        )

    def list_collections(self):
        """List collections."""
        return self.client.list_collections()

    def item(self, item_name, collection_name=False):
        """Return item from collection"""
        if collection_name:
            self.get_collection(collection_name)
        return self.coll.get(item_name)

    def get_collection(self, collection_name=DEFAULT_COLLECTION_NAME):
        """Actually get a collection."""
        self.coll = self.client.get_collection(
            collection_name, metadata={"instruction": self.instruction}
        )
        self.collection_name = collection_name

    def create_collection(self, collection_name=DEFAULT_COLLECTION_NAME):
        """Create a collection."""
        self.coll = self.client.create_collection(
            collection_name, metadata={"instruction": self.instruction}
        )
        self.collection_name = collection_name

    def get_or_create_collection(self, collection_name=DEFAULT_COLLECTION_NAME):
        """Create a collection."""
        self.coll = self.client.get_or_create_collection(
            collection_name, metadata={"instruction": self.instruction}
        )
        self.collection_name = collection_name

    def delete(self, collection_name=DEFAULT_COLLECTION_NAME):
        """Delete collection."""
        return self.client.delete_collection(collection_name)

    # Utility
    def reset(self):
        """Empties and completely resets the database.
        ⚠️ This is destructive and not reversible."""
        self.client.reset()

    def heartbeat(self):
        """Returns a nanosecond heartbeat. Useful for making sure the client remains connected."""
        return self.client.heartbeat()

    def count(self, collection_name=False):
        """Return number of records in a collection."""
        if collection_name:
            self.get_collection(collection_name)
        return self.coll.count()

    def modify(self, collection_name=False, metadata=False):
        """Rename the collection."""
        if collection_name:
            self.coll.modify(name=collection_name)
        if metadata:
            self.coll.modify(metadata=metadata)
        return {"name": ""}

    # NLP
    def space_ner(self, file=DEFAULT_DOCUMENT):
        """🙀🙀 !!WORK IN PROGRESS!! 🙀🙀
        Return with named entity information."""
        tagger: SequenceTagger = SequenceTagger.load("ner")
        sentences = self.sentences(file)
        tagger.predict(sentences)
        for sentence in sentences:
            print(sentence.to_tagged_string())

    def entities(self, text: str) -> list:
        sentences = self.splitter.split(text)
        self.link_tagger.predict(sentences)
        out = []
        for sentence in sentences:
            #print(f"{sentence}")
            spans = []

            for span in sentence.get_spans():
                #print(f"{span.start_position} : {span.end_position}")
                for label in span.labels:
                    #print(f"{span.text}\t{label.value}\t{label.score}")
                    if label.value == '<unk>':
                        val = ''
                    else:
                        val = label.value
                    spans.append({'text': span.text, 'start': span.start_position, 'end': span.end_position, 'value': val, 'score': label.score})
            out.append({'sentence': sentence.to_plain_string(), 'spans': spans})
        return out
        


if __name__ == "__main__":
    fire.Fire(Rag)
