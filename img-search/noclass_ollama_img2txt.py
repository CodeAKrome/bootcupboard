""" Use a multimodal model with Ollama"""
import base64
import requests
import json

TESTIMG = 'img/Kenwood-ts-990s.png'

def get_base_64_img(image):
    """ Converts an image from either a local file or a URL to base64 encoding. """

    if "http" not in image:
        base64_image = base64.b64encode(open(image, "rb").read()).decode("utf-8")
    else:
        response = requests.get(image)
        base64_image = base64.b64encode(response.content).decode("utf-8")
    return base64_image

def image2text(
    image: str = TESTIMG,
    prompt: str = "What's in this image?",
    temp: float = 0,
    tokens: int = 1000,
    model: str = "llava"  # Default model, can be changed
):
    """ Connect to Ollama API """
    ollama_url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temp,
            "num_predict": tokens
        },
        "images": [get_base_64_img(image)]
    }

    response = requests.post(ollama_url, json=payload, stream=True)
    
    msg = ''
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            if 'response' in chunk:
                msg += chunk['response']
            if chunk.get('done', False):
                break

    return msg

if __name__ == "__main__":
    # Example usage
    result = image2text()
    print(result)
