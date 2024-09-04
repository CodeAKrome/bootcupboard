#from tidb import TiDB
from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]
import numpy as np

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
#model.tokenizer.clean_up_tokenization_spaces = True
model._first_module().tokenizer.clean_up_tokenization_spaces = True
embeddings = model.encode(sentences)
#print("Embeddings shape:", embeddings.shape)
# 384 vector
#print(embeddings)

#tdb = TiDB()
sql = """
CREATE DATABASE IF NOT EXISTS test;
USE test;
DROP TABLE IF EXISTS image;
CREATE TABLE image (
    id INT PRIMARY KEY, 
    doc TEXT,
    embedding VECTOR(384) COMMENT "hnsw(distance=cosine)"
);
"""
for id, embedding in enumerate(embeddings):
    formatted_embedding = np.array2string(embedding, separator=',', formatter={'float_kind':lambda x: "%f" % x})
    # formatted_embedding = np.array2string(embedding, separator=',', formatter={'float_kind':lambda x: "%.8f" % x})
    # formatted_embedding = np.array2string(embedding, separator=',', precision=8, suppress_small=False)
    formatted_embedding = formatted_embedding.replace('\n', '')  # Remove newlines for a single-line SQL insert
     
    sql += f"INSERT INTO image (id, doc, embedding) VALUES ({id}, '{sentences[id]}', '{formatted_embedding}');\n"
print(sql)
#res = tdb.query_execute(sql)
#print(f"REZ: {res} use: {tdb.use()} conn: {tdb.get_connection}")

# sql = f"SELECT id, doc, Vec_Cosine_distance(embedding, {embeddings[1]}) AS distance FROM image ORDER BY distance LIMIT 1;"
# result = tdb.query(sql)
# print("Result:", result)
