#!/usr/bin/env python3

import chromadb
import sys
import time

dbpath = "db"

chroma_client = chromadb.PersistentClient(path=dbpath)
collection = chroma_client.create_collection(name="Colin")
start_time = time.time()
ln = 0
for line in sys.stdin:
    collection.add(documents=[line], metadatas=[{"source": "shake"}], ids=[f"id{ln}"])

    ln += 1

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

results = collection.query(query_texts=["Who is BERTRAM"], n_results=3)

print(results)
