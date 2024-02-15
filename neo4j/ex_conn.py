from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://localhost"
AUTH = ("neo4j", "inojoe")

data = [
    {"feed":"feed0", "title":"title0", "text":"article0", "tags":["tag0","tag1"]},
    {"feed":"feed1", "title":"title1", "text":"article1", "tags":["tag2","tag3"]}
    ]

gdb_driver = GraphDatabase.driver(URI, auth=AUTH)
sess = driver.session()


gdb_driver.close()

#with GraphDatabase.driver(URI, auth=AUTH) as driver:
#    driver.verify_connectivity()
