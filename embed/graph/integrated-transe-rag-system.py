import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForCausalLM

class IntegratedTransERAG:
    def __init__(self, dot_file_path, model_name="gpt2", embedding_dim=50, learning_rate=0.01, epochs=100, batch_size=32):
        self.transe = TransEEmbeddings(dot_file_path, embedding_dim, learning_rate, epochs, batch_size)
        self.embeddings = self.transe.encode_graph()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def find_similar_entities(self, query_embedding, top_k=5):
        entity_embeddings = np.array(list(self.embeddings['entities'].values()))
        similarities = cosine_similarity([query_embedding], entity_embeddings)[0]
        
        top_indices = similarities.argsort()[-top_k:][::-1]
        entities = list(self.embeddings['entities'].keys())
        return [entities[i] for i in top_indices]

    def get_entity_relations(self, entity):
        relations = []
        for head, tail, edge_data in self.transe.graph.edges(data=True):
            if head == entity:
                relations.append((edge_data['relation'], tail))
            elif tail == entity:
                relations.append((edge_data['relation'], head))
        return relations

    def generate_response(self, query, max_length=100):
        # Convert query to TransE embedding space
        query_embedding = self.query_to_transe_embedding(query)
        
        # Find similar entities
        similar_entities = self.find_similar_entities(query_embedding)
        
        # Get relations for these entities
        context = []
        for entity in similar_entities:
            relations = self.get_entity_relations(entity)
            for relation, related_entity in relations:
                context.append(f"{entity} {relation} {related_entity}")
        
        # Prepare input for language model
        context_text = " ".join(context)
        input_text = f"Context: {context_text}\n\nQuery: {query}\n\nResponse:"
        
        # Generate response
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)
        
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def query_to_transe_embedding(self, query):
        # This is a simplified method to map a query to the TransE embedding space
        # In a real-world scenario, you'd want a more sophisticated approach
        query_words = query.lower().split()
        query_embedding = np.zeros(self.transe.embedding_dim)
        count = 0
        for word in query_words:
            if word in self.transe.entity_to_id:
                query_embedding += self.embeddings['entities'][word]
                count += 1
            elif word in self.transe.relation_to_id:
                query_embedding += self.embeddings['relations'][word]
                count += 1
        return query_embedding / max(count, 1)  # Avoid division by zero

# Example usage:
# rag = IntegratedTransERAG('path_to_your_dotfile.dot')
# query = "Tell me about the relationship between A and B"
# response = rag.generate_response(query)
# print(response)
