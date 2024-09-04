import pymysql
from tidb_vector.integrations import TiDBVectorClient
import os

DB_NAME = 'news'
TABLE_NAME = 'test_table'
PASS = os.getenv("TIDB_PASS")

CONNECTION_STRING = f"mysql://2s5azfALGtC83jk.root:{PASS}@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/{DB_NAME}"

# tidb_vs = TiDBVectorClient(
#     # the table which will store the vector data
#     table_name=TABLE_NAME,
#     # tidb connection string
#     connection_string=CONNECTION_STRING,
#     # the dimension of the vector, in this example, we use the ada model, which has 1536 dimensions
#     vector_dimension=1536,
#     # if recreate the table if it already exists
#     drop_existing_table=True,
# )

tidb_vs = TiDBVectorClient(
    table_name=TABLE_NAME,
    connection_string=CONNECTION_STRING,
    vector_dimension=1536,
    drop_existing_table=True,
)

# ids = [
#     "f8e7dee2-63b6-42f1-8b60-2d46710c1971",
#     "8dde1fbc-2522-4ca2-aedf-5dcb2966d1c6",
#     "e4991349-d00b-485c-a481-f61695f2b5ae",
# ]

# documents = ["foo", "bar", "baz"]

# embeddings = [
#     text_to_embedding("foo"),
#     text_to_embedding("bar"),
#     text_to_embedding("baz"),
# ]

# metadatas = [
#     {"page": 1, "category": "P1"},
#     {"page": 2, "category": "P1"},
#     {"page": 3, "category": "P2"},
# ]

# tidb_vs.insert(
#     ids=ids,
#     texts=documents,
#     embeddings=embeddings,
#     metadatas=metadatas,
# )

#tidb_vs.query(text_to_embedding("foo"), k=3)

# query with filter
#tidb_vs.query(text_to_embedding("foo"), k=3, filter={"category": "P1"})


#tidb_vs.delete(["f8e7dee2-63b6-42f1-8b60-2d46710c1971"])

# delete with filter
#tidb_vs.delete(["f8e7dee2-63b6-42f1-8b60-2d46710c1971"], filter={"category": "P1"})
