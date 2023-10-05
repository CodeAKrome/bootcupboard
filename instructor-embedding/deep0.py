from deeplake.core.vectorstore import VectorStore
from InstructorEmbedding import INSTRUCTOR
import os
from sentence_transformers import SentenceTransformer
import subprocess

CHUNK = 512

srctxt = "artofwar.txt"
instruction = "Represent the news sentence for matching"

dbpath = "db"
db_model = INSTRUCTOR("hkunlp/instructor-large")

hf_key = os.getenv("HUGGINGFACE_API_KEY")
hf_model_name = "sentence-transformers/all-MiniLM-L6-v2"
hf_model = SentenceTransformer(hf_model_name)


def seppuku(dbpath):
    subprocess.run(["rm", "-Rf", dbpath])


# 切腹
seppuku(dbpath)

vector_store = VectorStore(
    path=dbpath,
)


def chunking(file_path, chunk_size):
    # Split the input string into chunks by line
    current_chunk = ""
    with open(file_path, "r") as f:
        for line in f:
            line = line.replace("\n", " ")
            line = line.replace("  ", " ")
            remaining_space = chunk_size - len(current_chunk)
            if len(line) <= remaining_space:
                current_chunk += line + " "
            else:
                current_chunk = current_chunk.strip()
                current_chunk = " " * (chunk_size - len(current_chunk))
                yield current_chunk
                current_chunk = line + " "
                if len(current_chunk) > chunk_size:
                    raise ValueError(
                        "Chunk size is too small to accommodate a single line."
                    )
            # Yield the last chunk if it's not empty
    if current_chunk:
        current_chunk = current_chunk.strip()
        current_chunk = " " * (chunk_size - len(current_chunk))
        yield current_chunk


def embedding_function(texts, instruction=instruction):
    if isinstance(texts, str):
        texts = [texts]

    texts = [t.replace("\n", " ") for t in texts]
    out = []
    for text in texts:
        out.append(db_model.encode([instruction, text]))

    return out


def write(chunked_text, embedding_function):
    vector_store.add(
        text=chunked_text,
        embedding_function=embedding_function,
        embedding_data=chunked_text,
        metadata=[{"source": srctxt}] * len(chunked_text),
    )


# --== MAIN ==--


chunked_text = []
for chunk in chunking(srctxt, CHUNK):
    chunked_text.append(chunk)

# embeddings = embedding_function(chunked_text)

write(chunked_text, embedding_function)


# for chunk in chunking(srctxt, CHUNK):
#     print(f"->\t{chunk}\n{embedding_function(instruction, chunk)}\n")

query = "What are the seven considerations?"
answer = vector_store.search(
    embedding_data=query, embedding_function=embedding_function
)
print(answer)
