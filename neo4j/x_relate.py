from neo4j import GraphDatabase
import json
import sys


class Neo4jUpdater:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = "news"
        # with self.driver.session() as session:
        #     session.execute_write(self._create_database, database_name="news")

    def close(self):
        self.driver.close()

    def update_database(self, line):
        with self.driver.session() as session:
            session.execute_write(self._process_line, line)

    @staticmethod
    def _process_line(tx, line):
        parts = line.strip().split("->")
        if len(parts) != 3:
            print(f"Invalid input format: {line}")
            return

        node1, relationship, node2 = [part.strip() for part in parts]

        node1_name, node1_props = Neo4jUpdater._parse_node(node1)
        relationship_name, relationship_props = Neo4jUpdater._parse_node(relationship)
        node2_name, node2_props = Neo4jUpdater._parse_node(node2)

        query = (
            f"CREATE ({node1_name}:widget {node1_props}) "
            f"CREATE ({node2_name}:widget {node2_props}) "
            f"CREATE ({node1_name})-[:{relationship_name} {relationship_props}]->({node2_name})"
        )
        tx.run(query)

    @staticmethod
    def _parse_node(node_string):
        name, props_str = node_string.split(":", 1)
        name = name.strip('"')
        props = json.loads(props_str)
        props_str = json.dumps(props)
        return name, props_str

    @staticmethod
    def _create_database(tx, database_name: str):
        tx.run(f"CREATE DATABASE {database_name}")

    @staticmethod
    def _use_database(tx, database_name: str):
        tx.run(f"USE {database_name}")
        
        

if __name__ == "__main__":
    uri = "bolt://localhost:7687"  # Replace with your Neo4j URI
    user = "neo4j"  # Replace with your username
    password = "N0Baldric!"  # Replace with your password

    updater = Neo4jUpdater(uri, user, password)

    for line in sys.stdin:
        if line.strip():
            updater.update_database(line)

    updater.close()
