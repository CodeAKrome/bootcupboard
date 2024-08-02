import ollama
import base64
import fire
from security import safe_requests

PENGUINS = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Adelie_penguins_in_the_South_Shetland_Islands.jpg/640px-Adelie_penguins_in_the_South_Shetland_Islands.jpg"
BUS = "https://huggingface.co/adept/fuyu-8b/resolve/main/bus.png"


modelfile = """
FROM llava:34b
SYSTEM You are a poet. You will answer with rhyming verse.
"""
ollama.create(model="poetbg", modelfile=modelfile)

modelfile = """
FROM llava:34b
SYSTEM You are a pirate. You will answer with answer with pirate slang.
"""
ollama.create(model="piratebg", modelfile=modelfile)

modelfile = """
FROM llava
SYSTEM You are a poet. You will answer with rhyming verse.
"""
ollama.create(model="poet", modelfile=modelfile)

modelfile = """
FROM llava
SYSTEM You are a pirate. You will answer with answer with pirate slang.
"""
ollama.create(model="pirate", modelfile=modelfile)


# define the get_base_64_img function (this function is called in the completion)
def get_base_64_img(image):
    """
    Converts an image from either a local file or a URL to base64 encoding.

    Parameters:
    - image (str): The image source, which can be a local file path or a URL.

    Returns:
    str: Base64-encoded representation of the image.
    """

    # Check if the image is a local file or a URL
    if "http" in image:
        # File on the Web: Fetch the image content from the URL, encode it in base64, and decode as UTF-8
        response = safe_requests.get(image)
        return base64.b64encode(response.content).decode("utf-8")
    # Local File: Read the binary content of the file, encode it in base64, and decode as UTF-8
    return base64.b64encode(open(image, "rb").read()).decode("utf-8")


def main(image: str = BUS, prompt: str = "What's in this image?", model: str = "llava"):
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "stream": False,
                "images": [get_base_64_img(image)],
            },
        ],
    )
    print(response["message"]["content"][1:])


if __name__ == "__main__":
    fire.Fire(main)
