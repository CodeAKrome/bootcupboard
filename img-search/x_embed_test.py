import torch
from torch import Tensor
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

class SentenceEmbedder:
    def __init__(self, model_id="sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModel.from_pretrained(model_id)
        self.model.eval()
        self.max_length = 256  # Default max length for this model

    def mean_pooling(self, model_output: Tensor, attention_mask: Tensor) -> Tensor:
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def embed(self, sentences):
        # Tokenize sentences
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, 
                                       max_length=self.max_length, return_tensors='pt')
        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        # Perform pooling
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings

    def compute_similarity(self, sentences1, sentences2):
        embeddings1 = self.embed(sentences1)
        embeddings2 = self.embed(sentences2)
        # Compute cosine similarity
        similarity_scores = F.cosine_similarity(embeddings1.unsqueeze(1), embeddings2.unsqueeze(0), dim=2)
        return similarity_scores.tolist()

if __name__ == "__main__":    
    # Initialize the embedder
    embedder = SentenceEmbedder()

    # Example usage
    sentences1 = [
        "This is an example sentence",
        "Each sentence is embedded separately"
    ]

    sentences2 = [
        "This is another example",
        "Embeddings can be compared"
    ]

    # Compute embeddings
    embeddings = embedder.embed(sentences1)
    print("Embeddings shape:", embeddings.shape)

    # Compute similarity
    similarity_scores = embedder.compute_similarity(sentences1, sentences2)
    print("Similarity scores:")
    for i, s1 in enumerate(sentences1):
        for j, s2 in enumerate(sentences2):
            print(f"Similarity between '{s1}' and '{s2}': {similarity_scores[i][j]:.4f}")
            
                