import ollama
import requests
import base64
import fire

PENGUINS = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Adelie_penguins_in_the_South_Shetland_Islands.jpg/640px-Adelie_penguins_in_the_South_Shetland_Islands.jpg"
BUS = "https://huggingface.co/adept/fuyu-8b/resolve/main/bus.png"

modelfile = """
FROM llama2
SYSTEM You are a poet. You will answer with rhyming verse.
"""
ollama.create(model="poet", modelfile=modelfile)

modelfile = """
FROM llava:34b
SYSTEM You are a poet. You will answer with rhyming verse.
"""
ollama.create(model="imgpoet", modelfile=modelfile)

model = "llama2"
model = "llava:34b"
model = "imgpoet"

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
        response = requests.get(image)
        return base64.b64encode(response.content).decode("utf-8")
    # Local File: Read the binary content of the file, encode it in base64, and decode as UTF-8
    return base64.b64encode(open(image, "rb").read()).decode("utf-8")


response = ollama.chat(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "What is in this picture?",
            "stream": False,
            "images": [get_base_64_img(PENGUINS)],
        },
    ],
)
print(f"---\n{response['message']['content']}\n")

# response = ollama.chat(model='poet', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(f"---\n{response['message']['content']}\n")
