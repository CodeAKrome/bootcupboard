from sentence_transformers import SentenceTransformer

sentences = ["Paris est une capitale de la France", "Paris is a capital of France"]


model = SentenceTransformer('Lajavaness/bilingual-embedding-large', trust_remote_code=True)

sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]

# 2. Calculate embeddings by calling model.encode()
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# 3. Calculate the embedding similarities
similarities = model.similarity(embeddings, embeddings)
print(similarities)

print(embeddings)

