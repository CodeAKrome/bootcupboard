from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import declarative_base
from tidb_vector.sqlalchemy import VectorType


import os
DB_NAME = 'news'
TABLE_NAME = 'test_table'
PASS = os.getenv("TIDB_PASS")
CONNECTION_STRING = f"mysql://2s5azfALGtC83jk.root:{PASS}@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/{DB_NAME}"

#engine = create_engine('mysql://****.root:******@gateway01.xxxxxx.shared.aws.tidbcloud.com:4000/test')
engine = create_engine(CONNECTION_STRING)


Base = declarative_base()

class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    embedding = Column(VectorType(3))

# or add hnsw index when creating table
class TestWithIndex(Base):
    __tablename__ = 'test_with_index'
    id = Column(Integer, primary_key=True)
    embedding = Column(VectorType(3), comment="hnsw(distance=l2)")

Base.metadata.create_all(engine)

test = Test(embedding=[1, 2, 3])
session.add(test)
session.commit()

