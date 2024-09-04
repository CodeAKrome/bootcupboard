from neo4j import GraphDatabase
import networkx as nx

class Neo4jMinimumSpanningSet:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_minimum_spanning_set(self, node_names, relationship_types=None):
        with self.driver.session() as session:
            return session.execute_read(self._calculate_minimum_spanning_set, node_names, relationship_types)

    def _calculate_minimum_spanning_set(self, tx, node_names, relationship_types):
        # Query to get all relationships between the given nodes
        query = """
        MATCH (n1)-[r]-(n2)
        WHERE n1.name IN $node_names AND n2.name IN $node_names
        """
        
        if relationship_types:
            query += "AND type(r) IN $relationship_types "
        
        query += """
        RETURN n1.name AS source, n2.name AS target, type(r) AS type, 
               properties(r) AS properties
        """
        
        result = tx.run(query, node_names=node_names, relationship_types=relationship_types)

        # Create a NetworkX graph from the query results
        G = nx.Graph()
        for record in result:
            source = record['source']
            target = record['target']
            weight = record['properties'].get('weight', 1)  # Default weight to 1 if not specified
            G.add_edge(source, target, weight=weight, type=record['type'])

        # Calculate the minimum spanning tree
        mst = nx.minimum_spanning_tree(G)

        # Convert the minimum spanning tree back to a list of relationships
        min_spanning_set = []
        for edge in mst.edges(data=True):
            min_spanning_set.append({
                'source': edge[0],
                'target': edge[1],
                'weight': edge[2]['weight'],
                'type': G[edge[0]][edge[1]]['type']
            })

        return min_spanning_set

if __name__ == "__main__":
    uri = "bolt://localhost:7687"  # Replace with your Neo4j URI
    user = "neo4j"  # Replace with your username
    password = "password"  # Replace with your password

    calculator = Neo4jMinimumSpanningSet(uri, user, password)
    
    # Example usage
    node_names = ["A", "B", "C", "D", "E"]  # Replace with your node names
    relationship_types = ["CONNECTS_TO", "LINKS_WITH"]  # Replace with your relationship types
    
    min_spanning_set = calculator.get_minimum_spanning_set(node_names, relationship_types)
    
    print("Minimum Spanning Set:")
    for relation in min_spanning_set:
        print(f"{relation['source']} -{relation['type']}-> {relation['target']} (weight: {relation['weight']})")

    calculator.close()
