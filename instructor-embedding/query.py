# chroma imports
import chromadb
import torch
from chromadb.utils import embedding_functions
import fire

# chroma config
collname = "test"
dbpath = "db"
instruction = "Represent the manual sentence for matching"
client = chromadb.PersistentClient(path=dbpath)

if torch.cuda.is_available():
    device = torch.device("cuda:0")
    device_name = "cuda"
else:
    device = torch.device("cpu")
    device_name = "cpu"

ef = embedding_functions.InstructorEmbeddingFunction(
    model_name="hkunlp/instructor-xl", device=device_name, instruction=instruction
)

coll = client.get_or_create_collection(name=collname, embedding_function=ef)


class No(object):
    def peek(self):
        """Show first 5 items of collection"""
        return coll.peek()

    def ask(self, q="What are the seven considerations?", n=3):
        #        print(f"Q: {query}")
        answers = coll.query(
            query_texts=[q],
            n_results=n,
        )

        docs = "\n".join(answers["documents"][0])
        print(f"Docs: {docs}")
        return answers


if __name__ == "__main__":
    fire.Fire(No)
