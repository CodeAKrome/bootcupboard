import os
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from tidb import TiDB
from ollama_img2txt import OllamaImg2Txt

PASS = os.getenv("TIDB_PASS")

class ImageDescriptionEmbedder:
    def __init__(self, tidb_password: str, database: str, ollama_model: str = "llava"):
        self.tidb = TiDB(password=tidb_password, database=database)
        self.ollama = OllamaImg2Txt(model=ollama_model)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Ensure the necessary table exists
        self._create_table()

    def _create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS image_embeddings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_path VARCHAR(255) NOT NULL,
            description TEXT,
            embedding VECTOR(384)
        )
        """
        self.tidb.execute_query(create_table_query)

        # Create vector index
        create_index_query = """
        ALTER TABLE image_embeddings
        ADD INDEX embedding_idx ON image_embeddings USING VECTOR(embedding) VECTOR_ALGORITHM('hnswlib')
        """
        self.tidb.execute_query(create_index_query)

    def describe_and_embed_images(self, image_paths: List[str]):
        for image_path in image_paths:
            # Generate description using OllamaImg2Txt
            description = self._generate_description(image_path)

            # Generate embedding
            embedding = self.embedding_model.encode(description)

            # Store in TiDB
            self._store_embedding(image_path, description, embedding)

    def _generate_description(self, image_path: str) -> str:
        prompt = "Describe this image in detail."
        description = self.ollama.image2text(image_path, prompt=prompt)
        return description.strip()

    def _store_embedding(self, image_path: str, description: str, embedding: np.ndarray):
        query = """
        INSERT INTO image_embeddings (image_path, description, embedding)
        VALUES (%s, %s, %s)
        """
        self.tidb.execute_query(query, (image_path, description, embedding.tolist()))

    def search_images(self, query: str, limit: int = 10) -> List[str]:
        # Generate embedding for the query
        query_embedding = self.embedding_model.encode(query)

        # Search for similar embeddings in TiDB using vector search
        search_query = f"""
        SELECT image_path, DISTANCE(embedding, ARRAY{query_embedding.tolist()}) AS distance
        FROM image_embeddings
        ORDER BY distance
        LIMIT {limit}
        """
        results = self.tidb.execute_query(search_query)

        # Return the matching image paths
        return [image_path for image_path, _ in results]

    def change_ollama_model(self, new_model: str):
        """ Change the Ollama model being used """
        self.ollama.change_model(new_model)

if __name__ == "__main__":
    # The TiDB class remains the same as in the previous answer
    embedder = ImageDescriptionEmbedder(tidb_password=PASS, database="test")

    # Describe and embed images
    image_paths = [
        "./img/scn_300.jpg",
        "./img/scn_337.jpg",
        "./img/scn_333.jpg",
        ]
    embedder.describe_and_embed_images(image_paths)

    # Search for images
    query = "flowers"
    matching_images = embedder.search_images(query)
    print(f"Matching images for '{query}':")
    for image_path in matching_images:
        print(image_path)

    # Change Ollama model
#    embedder.change_ollama_model("bakllava")
