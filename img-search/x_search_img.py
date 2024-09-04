import chromadb
from chromadb.utils import embedding_functions
from PIL import Image
import sys
from ollama_img2txt import OllamaImg2Txt

class SearchImg:
    def __init__(self, image_paths):
        self.client = chromadb.Client()
        self.image_paths = image_paths

        # Create ChromaDB collection
        self.collection = self.client.create_collection(
            name="image_search",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name='llava-hf/llava-v1.6-mistral-7b-hf')
        )

        # Process and add images to the collection
        self._process_images()

    def _process_images(self):
        for image_path in self.image_paths:
            image_features = self.get_image_description(image_path)
            # Add to collection
            self.collection.add(
                documents=[image_features],
                metadatas=[{"path": image_path}],
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
        return OllamaImg2Txt(image_path)
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
    img = SearchImg(images)
    query = input("Enter your query: ")
    results = img.search(query)
    for result in results:
        print(result['path'], ":", result['description'])
        