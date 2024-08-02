""" Use a multimodeal model with an Lm Studio server"""
from openai import OpenAI
import base64
from security import safe_requests

TESTIMG = 'Kenwood-ts-990s.png'

def get_base_64_img(image):
    """ Converts an image from either a local file or a URL to base64 encoding. """

    if "http" not in image:
        base64_image = base64.b64encode(open(image, "rb").read()).decode("utf-8")
    else:
        response = safe_requests.get(image)
        base64_image = base64.b64encode(response.content).decode("utf-8")
    return base64_image

def image2text(
    image: str = TESTIMG,
    prompt: str = "What's in this image?",
    temp: float = 0,
    tokens: int = 1000,
):
    """ Connect to Lm Studio api_key and model are faux """
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
    completion = client.chat.completions.create(
        model="argument-ignored",
        temperature=temp,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{get_base_64_img(image)}"
                        },
                    },
                ],
            }
        ],
        max_tokens=tokens,
        stream=True,
    )

    msg = ''
    for chunk in completion:
        if chunk.choices[0].delta.content:
            msg += chunk.choices[0].delta.content
    return msg
