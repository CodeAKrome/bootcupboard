import curses
import chromadb
import sys

"""Dump it all"""

try: 
    client = chromadb.PersistentClient(path=sys.argv[1])
except Exception as e:
    print("Error:", e)
    sys.exit(1)
    
colls = client.list_collections()
print("Num Collections: ", len(colls))
collections = [c.name for c in colls]
for collection in collections:
    print("Collection: ", collection)
    cc_handle = client.get_collection(collection)
    data = cc_handle.get()
    n = len(data["ids"])
    if n > 0:
        print("Num Records: ", n)
        ids = data["ids"]
        docs = data["documents"]
        meta = data["metadatas"]
        for i, d, m in zip(ids, docs, meta):
            print(f"id {i}\ndoc {d}\nmeta {m}")
