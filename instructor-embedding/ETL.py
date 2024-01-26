"""Extract data from files then Translate and Load it into a chroma database"""
import sys
import os
from ruamel.yaml import YAML
from segtok.segmenter import split_single
import mmap
import re
from flair.models import SequenceTagger
from flair.data import Sentence
import flair
from litellm import token_counter, get_max_tokens
import chromadb
from chromadb.utils import embedding_functions
import torch
import icecream as ic

# pip install ruamel.yaml ruamel.yaml.cmd litellm
# to get a complete list, call litellm.model_list

# describe how the embedding is to be used
DEFAULT_INSTRUCTION = "Represent the sentences for retrieval"
DEFAULT_MAX_SIZE = 128
DEFAULT_DATABASE_FILE = "db/chroma/default"
DEFAULT_CONFIG_FILE = "etl.yaml"
DEFAULT_CONFIG_NAME = "default"
DEFAULT_MODEL_NAME = "hkunlp/instructor-xl"
DEFAULT_SEQUENCE_TAGGER = "flair/ner-english"
DEFAULT_TOKEN_MODEL = "gpt-4"
DEFAULT_COLLECTION_NAME = "default"
DEFAULT_LOG_FILE = "etl.log"

# --=={ BEGIN Utility Functions }==--

def debug_function(debug_flags):
    """Print function name, inputs and outputs if the function name is in the debug_flags list"""
    def decorator(function):
        def wrapper(*args, **kwargs):
            if function.__name__ in debug_flags:
                print(f"\nInput to function {function.__name__}: {args}\n")
                result = function(*args, **kwargs)
                print(f"\nOutput of function {function.__name__}: {result}\n")
                return result
            else:
                return function(*args, **kwargs)
        return wrapper
    return decorator

def trace(message:str, traces:list, output="stdout", file=None):
    """Print program run trace information selectably to stdout, stderr or file"""
    caller = inspect.stack()[1].frame
    ic(f"Called from {caller.f_code.co_name}")
    ic(f"my one {caller}")

# --=={ END Utility Functions }==--

trace("Initialized ETL class", [])
exit()

if torch.cuda.is_available():
    flair.device = torch.device("cuda:0")
    DEVICE_NAME = "cuda"
else:
    flair.device = torch.device("cpu")
    DEVICE_NAME = "cpu"

class ETL:
    def __init__(
        self,
        config_file=DEFAULT_CONFIG_FILE,
        config_name=DEFAULT_CONFIG_NAME,
        device_name=DEVICE_NAME,
    ):
        # unsafe allows read/write
        self.yaml = YAML(typ="unsafe")
        self.config_file = config_file
        self.config_name = config_name
        if os.path.exists(config_file):
            self.config_index = self.yaml.load(open(self.config_file, "r"))
        else:
            self.config_index = {self.config_name:self.default_config()}
            self.save_config()
        self.config = self.config_index[self.config_name]
        self.device_name = device_name
        self.embedding_function = embedding_functions.InstructorEmbeddingFunction(
            model_name=self.config["model_name"],
            device=self.device_name,
            instruction=self.config["instruction"],
        )
        # chroma creates database if it doesn't exist
        self.client = chromadb.PersistentClient(path=self.config["database_file"])
        try:
            self.get_collection(self.config["collection"])
            print(f"Loading {self.config['collection']} <= {self.config['database_file']}")
        except Exception as e:
            # it doesn't exist, create it and initialize
            self.create_collection(self.config["collection"])
            print(f"Creating {self.config['collection']} => {self.config['database_file']}")
        self.tagger = SequenceTagger.load(self.config["sequence_tagger"])

    def default_config(self):
        return {
            "max_size": DEFAULT_MAX_SIZE,
            "instruction": DEFAULT_INSTRUCTION,
            "collection": DEFAULT_COLLECTION_NAME,
            "database_file": DEFAULT_DATABASE_FILE,
            "model_name": DEFAULT_MODEL_NAME,
            "sequence_tagger": DEFAULT_SEQUENCE_TAGGER,
            "token_model": DEFAULT_TOKEN_MODEL,
            "log_file": DEFAULT_LOG_FILE,
            "debug_flags": [],
        }

    def list_collections(self):
        """List collections in current database.
        For some reason you MUST use dot notation to access field values"""
        collections = self.client.list_collections()
        out = {}
        for collection in collections:
            out[collection.name] = collection.metadata
        return out

    def get_collection(self, collection_name=DEFAULT_COLLECTION_NAME):
        """Actually get a collection."""
        self.coll = self.client.get_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
        )
        self.collection_name = collection_name

    def create_collection(self, collection_name=DEFAULT_COLLECTION_NAME):
        """Create a collection."""
        self.coll = self.client.create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={
                "max_size": self.config["max_size"],
                "instruction": self.config["instruction"],
                "model_name": self.config["model_name"],
                "sequence_tagger": self.config["sequence_tagger"],
                "token_model": self.config["token_model"],
            },
        )
        self.collection_name = collection_name

    def save_config(self):
        print(f"Saving config: {self.config_file}")
        self.yaml.dump(self.config_index, open(self.config_file, "w"))

    def debug(self, flags=[]):
        if flags:
            self.debug_flags = flags
        return self.debug_flags

    def log(self, log_entry="", log_file=False):
        if log_file:
            self.log_file_handle = open(log_file, "a")
        print(log_entry, self.log_file_handle)

    def chunk_file(self, filename, max_size=False):
        N = self.config["max_size"]
        if max_size:
            N = max_size
        with open(filename, "r") as infile:
            lines = []
            for line in infile:
                line = line.strip()
                if len(lines) < N - 1:
                    lines.append(line)
                else:
                    lines.append(line)
                    res = lines
                    lines = []
                yield res
            else:
                if len(lines) != 0:
                    yield lines

    def sentences(self, file):
        text = open(file, "r").read()
        text = re.sub(r"\s+", " ", text)
        text = text.replace("\n", "").strip()
        sentences = [sent for sent in split_single(text) if sent]
        return [Sentence(sent, use_tokenizer=True) for sent in sentences]

#    @debug_function(["collate"])
    def collate(self, sentences, max_size, token_model):
        """Counting tokens like should"""
        print(f"model {token_model} max {get_max_tokens(token_model)['max_tokens']} @ {max_size} tokens per paragraph")
        sentences = self.sentences(file)
        paragraph = []
        current_len = 0
        for sentence in sentences:
            l = token_counter(model=token_model, messages=[{"user": "role", "content": sentence.text}])

#            print(f"len: {l} {sentence.text}")

            if l > max_size:
                print(f"Sentence length {l} > {max_size}: DROPPING! {sentence.text}")
                continue
            if current_len + l >= max_size:
                para = paragraph
                para_len = current_len
                paragraph = []
                current_len = 0

 #               print(f"Y1: {para_len} {para}")

                yield para_len, para
            paragraph.append(sentence)
            current_len += l
        if paragraph:

 #           print(f"Y2: {para}")

            yield current_len, paragraph

    def ner(self, sentences):
        self.tagger.predict(sentences)
        out = []
        for sentence in sentences:
            out.append(
                [
                    f"{entity.text}/{entity.tag}"
                    for entity in sentence.get_spans("ner")
                ]
            )
        return out

    def extract_text(self, file, max_size=False, token_model=False):
        """Extract text and entities from text file using flair."""
        size = self.config["max_size"]
        if max_size:
            size = max_size
        token_model_name = self.config["token_model"]
        if token_model:
            token_model_name = token_model

        print(f"COLL: {size} {token_model_name}")

        paragraphs = self.collate(self.sentences(file), max_size=size, token_model=token_model_name)
        paragraph_n = 0
        for tokens, paragraph in paragraphs:
            entity_paragraph = self.ner(paragraph)
            meta = {"file":file,"paragraph":paragraph_n,"tokens":tokens}
            for entity_sentence in entity_paragraph:

#                print(f"DD: {entity_sentence}")

                for entity in entity_sentence:
                    if entity:

#                        print(f"EE: {entity}")

                        meta[entity] = True
            paragraph_text = " ".join([sentence.text for sentence in paragraph])

#            print(f"TXT {paragraph_text}\nMETA {meta}")

            paragraph_n += 1
            self.coll.upsert(ids=[f"{file}:{paragraph_n}"], metadatas=[meta], documents=[paragraph_text])
        print(f"Paragraph {paragraph_n} @ {size}")

    def count(self, collection_name=False):
        if collection_name:
            self.get_collection(collection_name)
        return self.coll.count()

    def peek(self):
        return self.coll.peek()

    def dump(self):
        print(f"collection: {self.collection_name}\n")
        records = self.coll.get()
        paragraphs = records["documents"]
        metadatas = records["metadatas"]
        for paragraph, meta in zip(paragraphs, metadatas):
            print(f"{meta}\n{paragraph}\n")


# --=={ FOO! }==--
file = "docs/merry.txt"
file = "docs/sm_merry.txt"
etl = ETL()
etl.extract_text(file)
#print(etl.count())
etl.dump()
print(etl.list_collections())

#pie.debug(["sentences"])
# print(pie.sentences(file))

# pie.ner(file)
#print(pie.peek())



# pie.sentences()
# pie.write_default_config()

# yaml = YAML(typ="unsafe")
# yaml.register_class(ETL)
# yaml.dump([ETL()], sys.stdout)
