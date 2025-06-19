import torch
from sentence_transformers import SentenceTransformer

class EmbeddingsProcessor:
    def __init__(self, model_name='nvidia/NV-Embed-v2', max_seq_length=32768):
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.model.max_seq_length = max_seq_length
        self.model.tokenizer.padding_side = "right"
        
        self.task_name_to_instruct = {
            "example": "Given a question, retrieve passages that answer the question",
        }
        self.query_prefix = "Instruct: " + self.task_name_to_instruct["example"] + "\nQuery: "

    def add_eos(self, input_examples):
        return [input_example + self.model.tokenizer.eos_token for input_example in input_examples]

    def encode(self, texts, batch_size=2, is_query=False):
        texts_with_eos = self.add_eos(texts)
        prompt = self.query_prefix if is_query else None
        embeddings = self.model.encode(
            texts_with_eos, 
            batch_size=batch_size, 
            prompt=prompt, 
            normalize_embeddings=True
        )
        return embeddings

    def calculate_similarity(self, queries, passages, batch_size=2):
        query_embeddings = self.encode(queries, batch_size, is_query=True)
        passage_embeddings = self.encode(passages, batch_size)
        scores = (query_embeddings @ passage_embeddings.T) * 100
        return scores.tolist()

    def count_tokens(self, texts, is_query=False):
        if is_query:
            texts = [self.query_prefix + text for text in texts]
        texts_with_eos = self.add_eos(texts)
        token_counts = [len(self.model.tokenizer.encode(text)) for text in texts_with_eos]
        return token_counts

    def process(self, queries, passages, batch_size=2):
        similarity_scores = self.calculate_similarity(queries, passages, batch_size)
        query_token_counts = self.count_tokens(queries, is_query=True)
        passage_token_counts = self.count_tokens(passages)
        
        return {
            "similarity_scores": similarity_scores,
            "query_token_counts": query_token_counts,
            "passage_token_counts": passage_token_counts
        }

# Example usage
if __name__ == "__main__":
    processor = EmbeddingsProcessor()
    
    queries = [
        'are judo throws allowed in wrestling?', 
        'how to become a radiology technician in michigan?'
    ]
    passages = [
        "Since you're reading this, you are probably someone from a judo background or someone who is just wondering how judo techniques can be applied under wrestling rules. So without further ado, let's get to the question. Are Judo throws allowed in wrestling? Yes, judo throws are allowed in freestyle and folkstyle wrestling. You only need to be careful to follow the slam rules when executing judo throws. In wrestling, a slam is lifting and returning an opponent to the mat with unnecessary force.",
        "Below are the basic steps to becoming a radiologic technologist in Michigan:Earn a high school diploma. As with most careers in health care, a high school education is the first step to finding entry-level employment. Taking classes in math and science, such as anatomy, biology, chemistry, physiology, and physics, can help prepare students for their college studies and future careers.Earn an associate degree. Entry-level radiologic positions typically require at least an Associate of Applied Science. Before enrolling in one of these degree programs, students should make sure it has been properly accredited by the Joint Review Committee on Education in Radiologic Technology (JRCERT).Get licensed or certified in the state of Michigan."
    ]
    
    results = processor.process(queries, passages)
    print("Similarity Scores:", results["similarity_scores"])
    print("Query Token Counts:", results["query_token_counts"])
    print("Passage Token Counts:", results["passage_token_counts"])
