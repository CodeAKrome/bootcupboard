from segtok.segmenter import split_single
from flair.data import Sentence
import mmap
import fire
import re
import flair
import torch
from tqdm import trange, tqdm

# chroma imports
import chromadb
from chromadb.utils import embedding_functions
from flair.models import SequenceTagger
#from chromadb.config import Settings

# https://github.com/poteha/docker-nlp

# chroma config
srctxt = "artofwar.txt"
collname = "test"
dbpath = "db"
CHUNK_SIZE = 512
instruction = "Represent the manual sentence for matching"
client = chromadb.PersistentClient(path=dbpath)
#client = chromadb.Client(
#    Settings(chroma_db_impl="duckdb+parquet", persist_directory=dbpath)
#)

if torch.cuda.is_available():
    device = torch.device("cuda:0")
    device_name = "cuda"
else:
    device = torch.device("cpu")
    device_name = "cpu"

flair.device = device

ef = embedding_functions.InstructorEmbeddingFunction(
    model_name="hkunlp/instructor-xl", device=device_name, instruction=instruction
)

coll = client.get_or_create_collection(name=collname, embedding_function=ef)

class Nlp(object):
    """Natural language processing functions using flair."""

    def mmap_file(self, filepath):
        """Use memory mapping to reaad an entire file."""
        with open(filepath, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            return mm.read().decode()

    def sentences(self, file="artofwar.txt"):
        """Break a file into lines by sentence."""
        print(f"Reading: {file}")
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text)
        sents = split_single(text)
        sents = [sent for sent in sents if sent]
        sentences = [Sentence(sent, use_tokenizer=True) for sent in sents]
        for sentence in sentences:
            print(sentence.text)

    def play(self, file="artofwar.txt"):
        """Break a play into lines.
        Concattenate next line to this if this line starts with capitals."""
        print(f"Reading: {file}")
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text)
        sents = split_single(text)
        sents = [sent for sent in sents if sent]
        sentences = [Sentence(sent, use_tokenizer=True) for sent in sents]
        hold = ''
        for sentence in sentences:
            txt = sentence.text
            if re.match(r'^[A-Z\.]{3,}', txt):
                hold = txt
                continue
            if hold:
                print(f"{hold} {txt}")
                hold = ''
            else:
                print(txt)

    def playrag(self, file="artofwar.txt"):
        """Break a play into lines.
        Concattenate next line to this if this line starts with capitals."""
        print(f"Reading: {file}")
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text)
        sents = split_single(text)
        sents = [sent for sent in sents if sent]
        sentences = [Sentence(sent, use_tokenizer=True) for sent in sents]
        buf = ''
        actor = ''
        i = 0
        for sentence in tqdm(sentences):
            txt = sentence.text
            if re.match(r'^[A-Z\.]{3,}', txt):
                actor = txt
                buf = txt
                continue
            if buf:
                txt = f"{buf} {txt}"
                buf = ''
            #print(txt)
            coll.upsert(ids=[f"{file}:{i}"], metadatas=[{'player':actor}], documents=[txt])
            i += 1


    def peek(self):
        """Show first 5 items of collection"""
        return coll.peek()

    def rag(self, file="artofwar.txt"):
        """Break a file into lines by sentence and store it in chromadb."""
        print(f"Reading: {file}")
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text)
        sents = split_single(text)
        sents = [sent for sent in sents if sent]
        sentences = [Sentence(sent, use_tokenizer=True) for sent in sents]
        i = 0
        for sentence in tqdm(sentences):
            coll.upsert(documents=[sentence.text], ids=[f"{file}:{i}"])
#            coll.add(documents=[sentence.text], ids=[f"{file}:{i}"])
            i += 1

    def query(self, q="What are the seven considerations?"):
        #        print(f"Q: {query}")
        answer = coll.query(
            query_texts=[q],
            n_results=3,
        )

        #        print(answer)
        return answer

    def ner(self, file="artofwar.txt"):
        """Print jsonl with named entity information."""
        from flair.models import SequenceTagger

        tagger: SequenceTagger = SequenceTagger.load("ner")
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text).strip()
        sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
        sentences = [sentence for sentence in sentences if sentence]
        tagger.predict(sentences)
        for sentence in sentences:
            print(sentence.to_tagged_string())


if __name__ == "__main__":
    fire.Fire(Nlp)
