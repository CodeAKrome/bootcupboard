import chromadb
from chromadb.utils import embedding_functions
import os
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from sentence_transformers import SentenceTransformer
import sys

class ImageEmbeddingSearch:
    def __init__(self, image_paths):
        self.client = chromadb.Client()
        self.image_paths = image_paths

        # Initialize CLIP model for image description
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # Initialize Sentence Transformer for text search
        self.text_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Create ChromaDB collection
        self.collection = self.client.create_collection(
            name="image_search",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')
        )

        # Process and add images to the collection
        self._process_images()

    def _process_images(self):
        for image_path in self.image_paths:
            image_features = self.get_image_description(image_path)
            # Add to collection
            self.collection.add(
                documents=[image_features],
                metadatas=[{"path": image_path, "description": image_features}],
                ids=[image_path]
            )

    def search(self, query, n_results=10):
        search_results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return [
            {
                "path": result['metadata']['path'],
                "description": result['metadata']['description']
            }
            for result in search_results['metadatas'][0]
        ]

    def get_image_description(self, image_path):
        image = Image.open(image_path)
        inputs = self.clip_processor(images=image, return_tensors="pt", padding=True)
        image_features = self.clip_model.get_image_features(**inputs)
        return image_features

if __name__ == "__main__":
    images = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            images.append(line)
    img = ImageEmbeddingSearch(images)
    query = input("Enter your query: ")
    results = img.search(query)
    for result in results:
        print(result['path'], ":", result['description'])
        