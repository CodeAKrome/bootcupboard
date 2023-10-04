import chromadb
from chromadb.utils import embedding_functions

srctxt = 'artofwar.txt'
collname = 'test'
dbpath = 'db'
CHUNK_SIZE = 512
instruction = 'Represent the manual sentence for matching'

client = chromadb.PersistentClient(path=dbpath)
#ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-xl", device="cuda", instruction=instruction)
ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-xl", instruction=instruction)

try:
    client.delete_collection(collname)
except ValueError as ve:
    print("Db doesn't exist to kill; Creating.")
    coll = client.create_collection(name=collname, embedding_function=ef)
except Exception as e:
    print(f"Type: {type(e)}\tCreate: {collname}")
    coll = client.create_collection(name=collname, embedding_function=ef)


def chunking(file_path, chunk_size):
    # Split the input string into chunks by line
    current_chunk = ''
    with open(file_path, 'r') as f:
        for line in f:
            line = line.replace('\n', ' ')
            line = line.replace('  ', ' ')
            remaining_space = chunk_size - len(current_chunk)
            if len(line) <= remaining_space:
                current_chunk += line + ' '
            else:
                yield current_chunk.strip()
                current_chunk = line + ' '
                if len(current_chunk) > chunk_size:
                    raise ValueError("Chunk size is too small to accommodate a single line.")
            # Yield the last chunk if it's not empty
    if current_chunk:
        yield current_chunk.strip()

chunked_text = []
for chunk in chunking(srctxt, CHUNK_SIZE):
    chunked_text.append(chunk)
ids = coll.add(documents=chunked_text, ids=[f"id{i}" for i in range(len(chunked_text))])
query = "What are the seven considerations?"
answer = coll.query(
    query_texts=[query],
    n_results=3,
)

print(answer)
