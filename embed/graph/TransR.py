import networkx as nx
import torch
from torch_geometric.data import Data
from torch_geometric.nn import TransR
from torch_geometric.utils import negative_sampling
from torch.nn import MarginRankingLoss
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader

class RAGDataset(Dataset):
    def __init__(self, graph, node2id, relation2id):
        self.graph = graph
        self.node2id = node2id
        self.relation2id = relation2id
        self.triples = []
        for u, v, data in graph.edges(data=True):
            self.triples.append((node2id[u], relation2id[data['label']], node2id[v]))

    def __len__(self):
        return len(self.triples)

    def __getitem__(self, idx):
        head, relation, tail = self.triples[idx]
        return torch.tensor(head), torch.tensor(relation), torch.tensor(tail)

class RAGRetrieval:
    def __init__(self, dot_file, embedding_dim=100, relation_dim=100):
        self.dot_file = dot_file
        self.embedding_dim = embedding_dim
        self.relation_dim = relation_dim
        self.graph = nx.DiGraph()
        self.node2id = {}
        self.relation2id = {}
        self.num_entities = 0
        self.num_relations = 0
        self.load_graph()
        self.model = TransR(self.num_entities, self.num_relations, self.embedding_dim, self.relation_dim)
        self.dataset = RAGDataset(self.graph, self.node2id, self.relation2id)
        self.dataloader = DataLoader(self.dataset, batch_size=32, shuffle=True)

    def load_graph(self):
        with open(self.dot_file, 'r') as f:
            for line in f:
                if line.startswith('node'):
                    node_id = int(line.split()[1])
                    self.node2id[f'node{node_id}'] = node_id
                    self.num_entities += 1
                elif line.startswith('edge'):
                    edge_info = line.split()
                    head = f'node{int(edge_info[1])}'
                    tail = f'node{int(edge_info[3])}'
                    relation = edge_info[5].strip('"')
                    if relation not in self.relation2id:
                        self.relation2id[relation] = self.num_relations
                        self.num_relations += 1
                    self.graph.add_edge(head, tail, label=relation)

    def train(self, epochs=100):
        optimizer = Adam(self.model.parameters(), lr=0.001)
        loss_fn = MarginRankingLoss(margin=1.0)
        for epoch in range(epochs):
            for batch in self.dataloader:
                head, relation, tail = batch
                negative_head, negative_relation, negative_tail = negative_sampling(head, relation, tail, self.num_entities, self.num_relations)
                optimizer.zero_grad()
                positive_score = self.model(head, relation, tail)
                negative_score = self.model(negative_head, negative_relation, negative_tail)
                loss = loss_fn(positive_score, negative_score, torch.ones_like(positive_score))
                loss += 0.01 * self.model.regularization_loss()
                loss.backward()
                optimizer.step()
            print(f'Epoch {epoch+1}, Loss: {loss.item()}')

    def retrieve(self, query_node, query_relation):
        query_node_id = self.node2id[query_node]
        query_relation_id = self.relation2id[query_relation]
        scores = []
        for node in self.graph.nodes():
            node_id = self.node2id[node]
            score = self.model(torch.tensor(query_node_id), torch.tensor(query_relation_id), torch.tensor(node_id))
            scores.append((node, score.item()))
        scores.sort(key=lambda x: x[1])
        return scores

# Example usage
rag_retrieval = RAGRetrieval('example.dot')
rag_retrieval.train()
query_node = 'node1'
query_relation = 'relation1'
scores = rag_retrieval.retrieve(query_node, query_relation)
print(scores)
