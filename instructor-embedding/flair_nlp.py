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

# https://github.com/poteha/docker-nlp
# python flair_nlp.py query --q="Falstaff" --where='{"role":"PAGE."}' --where_document='{"$contains":"disguise"}'


DEFAULT_CHUNK_SIZE = 512
DEFAULT_DOCUMENT = 'artofwar.txt'
DEFAULT_QUERY = 'What are the seven considerations?'
DEFAULT_INSTRUCTION = 'Represent the sentences for retrieval'
DEFAULT_COLLECTION_NAME = 'default'
DEFAULT_DB_PATH = 'db/default'
DEFAULT_MODEL_NAME = 'hkunlp/instructor-xl'
DEFAULT_RESULTS = 3

if torch.cuda.is_available():
    flair.device = torch.device('cuda:0')
    device_name = 'cuda'
else:
    flair.device = torch.device('cpu')
    device_name = 'cpu'

class Search(object):
    """Vector similarity search with chromadb and NER using flair."""

    def __init__(
        self,
        collection_name=DEFAULT_COLLECTION_NAME,
        instruction=DEFAULT_INSTRUCTION,
        database_path=DEFAULT_DB_PATH,
        model_name=DEFAULT_MODEL_NAME,
        device_name=device_name,
        chunk_size=DEFAULT_CHUNK_SIZE,
    ):
        self.instruction = instruction
        self.collection_name = collection_name
        self.database_path = database_path
        self.model_name = model_name
        self.device_name = device_name
        self.client = chromadb.PersistentClient(path=self.database_path)
        self.embedding_function = embedding_functions.InstructorEmbeddingFunction(
            model_name=self.model_name, device=self.device_name, instruction=self.instruction
        )
        self.coll = self.client.get_or_create_collection(
            name=self.collection_name, embedding_function=self.embedding_function
        )

    def mmap_file(self, filepath):
        """Use memory mapping to MAINLINE an entire file."""
        with open(filepath, 'r+b') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            return mm.read().decode()

    def sentences(self, file=DEFAULT_DOCUMENT):
        """Break a file into lines by sentence."""
        print(f"Reading: {file}")
        text = self.mmap_file(file)
        text = re.sub(r'\s+', ' ', text)
        sents = split_single(text)
        sents = [sent for sent in sents if sent]
        sentences = [Sentence(sent, use_tokenizer=True) for sent in sents]
        for sent in sentences:
            yield sent.text

    def play(self, file=DEFAULT_DOCUMENT):
        """Break a play into lines.
        Concattenate next line to this if this line starts with capitals."""
        buf = ''
        for sentence in self.sentences(file):
            txt = sentence
            if re.match(r'^\w+\.$', txt):
                buf = txt
                continue
            if buf:
                txt = f"{buf} {txt}"
                buf = ''
            yield txt

    def psentences(self, file=DEFAULT_DOCUMENT):
        for sentence in self.sentences(file):
            print(sentence)

    def pplay(self, file=DEFAULT_DOCUMENT):
        for sentence in self.play(file):
            print(sentence)

    def playrag(self, file=DEFAULT_DOCUMENT, collection_name=False):
        """Break a play into lines.
        Concattenate next line to this if this line starts with capitals."""
        if collection_name:
            self.get(collection_name)
        buf = ''
        role = ''
        i = 0
        for sentence in tqdm(self.sentences(file)):
            txt = sentence
            if re.match(r'^\w+\.$', txt):
                role = txt
                buf = txt
                continue
            if buf:
                txt = f"{buf} {txt}"
                buf = ''
            self.coll.upsert(
                ids=[f"{file}:{i}"], metadatas=[{'role': role}], documents=[txt]
            )
            i += 1
        print(f"Upserted {i} records.")


    def peek(self):
        """Show first few items of collection"""
        return self.coll.peek()

    def rag(self, file=DEFAULT_DOCUMENT, collection_name=False):
        """Break a file into lines by sentence and store it in chromadb."""
        if collection_name:
            self.get(collection_name)
        i = 0
        for sentence in tqdm(self.sentences(file=file)):
            self.coll.upsert(documents=[sentence], ids=[f"{file}:{i}"])
            i += 1
        print(f"Upserted {i} records.")

    def query(self, q=DEFAULT_QUERY, n=DEFAULT_RESULTS, where={}, where_document={}):
        return self.coll.query(
            query_texts=[q],
            n_results=n,
            where=where,
            where_document=where_document,
        )

    def list(self):
        return self.client.list_collections()

    def get(self, collection_name=DEFAULT_COLLECTION_NAME):
        """Actually get_or_create()"""
        self.coll = self.client.get_or_create_collection(collection_name)
        self.collection_name = collection_name

    def delete(self, collection_name=DEFAULT_COLLECTION_NAME):
        return self.client.delete_collection(collection_name)

    # Utility
    def reset(self):
        self.client.reset()

    def heartbeat(self):
        return self.client.heartbeat()

    def count(self):
        return self.coll.count()

    # NLP
    def ner(self, file=DEFAULT_DOCUMENT):
        """!!WORK IN PROGRESS!! Return with named entity information."""
        from flair.models import SequenceTagger
        tagger: SequenceTagger = SequenceTagger.load('ner')
        text = self.mmap_file(file)
        text = re.sub(r'\s+', ' ', text).strip()
        sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
        sentences = [sentence for sentence in sentences if sentence]
        tagger.predict(sentences)
        for sentence in sentences:
            print(sentence.to_tagged_string())


if __name__ == "__main__":
    fire.Fire(Search)
