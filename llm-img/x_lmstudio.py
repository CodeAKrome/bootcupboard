from openai import OpenAI
import base64
import requests

# Initialize OpenAI client with a custom local server and a placeholder API key (not needed for local server)
# Note: The API key is not required for a local server, as indicated by "not-needed"
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# Set up the image URLs

# URL of an image hosted on the web
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Adelie_penguins_in_the_South_Shetland_Islands.jpg/640px-Adelie_penguins_in_the_South_Shetland_Islands.jpg"

# Local file path of an image
image_local = "llm.png"


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
    if "http" not in image:
        # Local File: Read the binary content of the file, encode it in base64, and decode as UTF-8
        base64_image = base64.b64encode(open(image, "rb").read()).decode("utf-8")
    else:
        # File on the Web: Fetch the image content from the URL, encode it in base64, and decode as UTF-8
        response = requests.get(image, timeout=60)
        base64_image = base64.b64encode(response.content).decode("utf-8")

    # Return the base64-encoded image
    return base64_image


# Create completion request (replace the variable image_local with your image)

completion = client.chat.completions.create(
    model="local-model",  # not used
    temperature=0,  # set the temperature
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        # replace the image_local with the variable to your image
                        "url": f"data:image/jpeg;base64,{get_base_64_img(image_local)}"
                    },
                },
            ],
        }
    ],
    max_tokens=1000,
    stream=True,
)

for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
