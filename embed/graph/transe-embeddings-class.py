import networkx as nx
import numpy as np
from pydot import graph_from_dot_file

class TransEEmbeddings:
    def __init__(self, dot_file_path, embedding_dim=50, learning_rate=0.01, epochs=100, batch_size=32):
        self.dot_file_path = dot_file_path
        self.embedding_dim = embedding_dim
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        
        self.graph = None
        self.entity_embeddings = None
        self.relation_embeddings = None
        self.entity_to_id = {}
        self.relation_to_id = {}
        
    def load_graph_from_dot(self):
        dot_graph = graph_from_dot_file(self.dot_file_path)[0]
        self.graph = nx.DiGraph()
        
        for node in dot_graph.get_nodes():
            self.graph.add_node(node.get_name())
        
        for edge in dot_graph.get_edges():
            source = edge.get_source()
            target = edge.get_destination()
            label = edge.get_label()
            if label is None:
                label = "unlabeled"
            self.graph.add_edge(source, target, relation=label)
        
    def initialize_embeddings(self):
        self.entity_to_id = {entity: i for i, entity in enumerate(self.graph.nodes())}
        self.relation_to_id = {relation: i for i, relation in enumerate(set(nx.get_edge_attributes(self.graph, 'relation').values()))}
        
        num_entities = len(self.entity_to_id)
        num_relations = len(self.relation_to_id)
        
        self.entity_embeddings = np.random.uniform(low=-6/np.sqrt(self.embedding_dim), 
                                                   high=6/np.sqrt(self.embedding_dim), 
                                                   size=(num_entities, self.embedding_dim))
        self.relation_embeddings = np.random.uniform(low=-6/np.sqrt(self.embedding_dim), 
                                                     high=6/np.sqrt(self.embedding_dim), 
                                                     size=(num_relations, self.embedding_dim))
        
    def train(self):
        for _ in range(self.epochs):
            self.train_epoch()
    
    def train_epoch(self):
        edges = list(self.graph.edges(data=True))
        np.random.shuffle(edges)
        
        for i in range(0, len(edges), self.batch_size):
            batch = edges[i:i+self.batch_size]
            self.train_batch(batch)
    
    def train_batch(self, batch):
        pos_h, pos_t, pos_r = [], [], []
        neg_h, neg_t, neg_r = [], [], []
        
        for head, tail, edge_data in batch:
            relation = edge_data['relation']
            pos_h.append(self.entity_to_id[head])
            pos_t.append(self.entity_to_id[tail])
            pos_r.append(self.relation_to_id[relation])
            
            # Generate negative sample
            neg_head = np.random.choice(list(self.entity_to_id.values()))
            neg_tail = np.random.choice(list(self.entity_to_id.values()))
            neg_h.append(neg_head)
            neg_t.append(neg_tail)
            neg_r.append(self.relation_to_id[relation])
        
        pos_h = self.entity_embeddings[pos_h]
        pos_t = self.entity_embeddings[pos_t]
        pos_r = self.relation_embeddings[pos_r]
        neg_h = self.entity_embeddings[neg_h]
        neg_t = self.entity_embeddings[neg_t]
        neg_r = self.relation_embeddings[neg_r]
        
        pos_score = np.sum(np.abs(pos_h + pos_r - pos_t), axis=1)
        neg_score = np.sum(np.abs(neg_h + neg_r - neg_t), axis=1)
        
        loss = np.sum(np.maximum(pos_score - neg_score + 1, 0))
        
        grad_pos_h = (pos_h + pos_r - pos_t) / np.maximum(np.linalg.norm(pos_h + pos_r - pos_t, axis=1, keepdims=True), 1e-8)
        grad_pos_t = -(pos_h + pos_r - pos_t) / np.maximum(np.linalg.norm(pos_h + pos_r - pos_t, axis=1, keepdims=True), 1e-8)
        grad_pos_r = grad_pos_h
        
        grad_neg_h = -(neg_h + neg_r - neg_t) / np.maximum(np.linalg.norm(neg_h + neg_r - neg_t, axis=1, keepdims=True), 1e-8)
        grad_neg_t = (neg_h + neg_r - neg_t) / np.maximum(np.linalg.norm(neg_h + neg_r - neg_t, axis=1, keepdims=True), 1e-8)
        grad_neg_r = grad_neg_h
        
        self.entity_embeddings[pos_h] -= self.learning_rate * grad_pos_h
        self.entity_embeddings[pos_t] -= self.learning_rate * grad_pos_t
        self.relation_embeddings[pos_r] -= self.learning_rate * grad_pos_r
        self.entity_embeddings[neg_h] -= self.learning_rate * grad_neg_h
        self.entity_embeddings[neg_t] -= self.learning_rate * grad_neg_t
        self.relation_embeddings[neg_r] -= self.learning_rate * grad_neg_r
        
        # Normalize embeddings
        self.entity_embeddings = self.entity_embeddings / np.maximum(np.linalg.norm(self.entity_embeddings, axis=1, keepdims=True), 1e-8)
        self.relation_embeddings = self.relation_embeddings / np.maximum(np.linalg.norm(self.relation_embeddings, axis=1, keepdims=True), 1e-8)
    
    def get_embeddings(self):
        return {
            'entities': {entity: self.entity_embeddings[self.entity_to_id[entity]] for entity in self.entity_to_id},
            'relations': {relation: self.relation_embeddings[self.relation_to_id[relation]] for relation in self.relation_to_id}
        }
    
    def encode_graph(self):
        self.load_graph_from_dot()
        self.initialize_embeddings()
        self.train()
        return self.get_embeddings()

# Example usage:
# transe = TransEEmbeddings('path_to_your_dotfile.dot')
# embeddings = transe.encode_graph()
