""" Use a multimodal model with Ollama"""
import base64
import requests
import json
import sys

TEST_IMG = 'img/Kenwood-ts-990s.png'

class OllamaImg2Txt:
    def __init__(self, model="llava", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_endpoint = f"{self.base_url}/api/generate"

    @staticmethod
    def get_base_64_img(image):
        """ Converts an image from either a local file or a URL to base64 encoding. """
        if "http" not in image:
            with open(image, "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        else:
            response = requests.get(image)
            base64_image = base64.b64encode(response.content).decode("utf-8")
        return base64_image

    def image2text(self, image, prompt="What's in this image?", temp=0, tokens=1000):
        """ Connect to Ollama API and process the image """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temp,
                "num_predict": tokens
            },
            "images": [self.get_base_64_img(image)]
        }

        response = requests.post(self.api_endpoint, json=payload, stream=True)
        
        msg = ''
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if 'response' in chunk:
                    msg += chunk['response']
                if chunk.get('done', False):
                    break

        return msg

    def change_model(self, new_model):
        """ Change the model being used """
        self.model = new_model

    def set_base_url(self, new_url):
        """ Change the base URL for the Ollama API """
        self.base_url = new_url
        self.api_endpoint = f"{self.base_url}/api/generate"

if __name__ == "__main__":
    image = TEST_IMG
    if len(sys.argv) > 1:
        image = sys.argv[1]
    # Example usage
    ollama = OllamaMultimodal()
    models = ['llava', 'bakllava', 'moondream', 'llava-phi3']
    for model in models:
        # Changing model and trying again
        ollama.change_model(model)  # Assuming you have this model available
        result = ollama.image2text(image, prompt="Describe this radio in detail")
        print(f"\n{model} result:\n{result}")
        
