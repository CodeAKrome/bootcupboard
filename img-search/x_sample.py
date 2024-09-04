import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import MySQLConnection
from tidb import TiDB
from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
print("Embeddings shape:", embeddings.shape)

# Load environment variables from .env file
load_dotenv()

def get_connection(autocommit: bool = True) -> MySQLConnection:
    db_conf = {
        "host": os.getenv("TIDB_HOST"),
        "port": int(os.getenv("TIDB_PORT")),  # Convert to int
        "user": os.getenv("TIDB_USER"),
        "password": os.getenv("TIDB_PASSWORD"),
        "database": os.getenv("TIDB_DB_NAME"),
        "autocommit": autocommit,
        "use_pure": True,
    }

    ca_path = os.getenv("CA_PATH")
    if ca_path:
        db_conf["ssl_verify_cert"] = True
        db_conf["ssl_verify_identity"] = True
        db_conf["ssl_ca"] = ca_path

    return mysql.connector.connect(**db_conf)

# -------

create_schema = """
CREATE DATABASE IF NOT EXISTS test;
USE test;
DROP TABLE IF EXISTS image;
CREATE TABLE image (
    id INT PRIMARY KEY, 
    doc TEXT,
    embedding VECTOR(384) COMMENT "hnsw(distance=cosine)"
);
"""

# Prepare insert statement and data
insert_sql = "INSERT INTO image (id, doc, embedding) VALUES (%s, %s, %s)"
insert_data = [(id, sentence, embedding.tolist()) for id, (sentence, embedding) in enumerate(zip(sentences, embeddings))]

query = "SELECT id, doc FROM image;"

with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        # Execute schema creation
        for statement in create_schema.split(';'):
            if statement.strip():
                cur.execute(statement)
        
        # Execute inserts
        cur.executemany(insert_sql, insert_data)
        
        # Execute select query
        cur.execute(query)
        print(cur.fetchall())

# -----


# for id, embedding in enumerate(embeddings):
#     sql += f"INSERT INTO image (id, doc, embedding) VALUES ({id}, '{sentences[id]}', '{embedding}');\n"


# query = "select id, doc from image;"

# with get_connection(autocommit=True) as conn:
#     with conn.cursor() as cur:
#         cur.executemany(sql)
#         cur.execute(query)
#         print(cur.fetchall())
#         # cursor.execute("INSERT INTO players (id, coins, goods) VALUES (%s, %s, %s)", player)
        