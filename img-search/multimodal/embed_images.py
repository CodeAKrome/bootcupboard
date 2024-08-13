import chromadb
from chromadb.utils import embedding_functions
import os
import sys

class ImageEmbeddingSearch:
    def __init__(self, image_paths, embedding_names):
        self.client = chromadb.Client()
        self.embedding_names = embedding_names
        self.collections = {}

        for embedding_name in embedding_names:
            embedding_function = embedding_functions.HuggingFaceEmbeddingFunction(
                api_key="your_huggingface_api_key",
                model_name=embedding_name
            )
            self.collections[embedding_name] = self.client.create_collection(
                name=embedding_name,
                embedding_function=embedding_function
            )

        for image_path in image_paths:
            for embedding_name in embedding_names:
                self.collections[embedding_name].add(
                    documents=[os.path.basename(image_path)],
                    metadatas=[{"path": image_path}],
                    ids=[image_path]
                )

    def search(self, query, n_results=10):
        results = {}
        for embedding_name, collection in self.collections.items():
            search_results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            results[embedding_name] = [
                result['metadata']['path'] 
                for result in search_results['metadatas'][0]
            ]
        return results

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        