import requests
import json
import os

class LitellmProxy:
    def __init__(self, base_url="http://localhost:4000", api_key=None, model_id="gemini/gemini-1.5-pro"):
        """
        Initialize the LitellmProxy class.

        Args:
        base_url (str): The base URL of the Litellm endpoint. Defaults to "http://localhost:4000".
        api_key (str): The API key for the Litellm endpoint.
        model_id (str): The ID of the model to use for inference. Defaults to "gemini/gemini-1.5-pro".
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model_id = model_id

    def _construct_headers(self):
        """
        Construct the headers for the API request.

        Returns:
        dict: A dictionary containing the API key in the "Authorization" header.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _construct_url(self, endpoint=''):
        """
        Construct the full URL for the API request.

        Args:
        endpoint (str): The endpoint to append to the base URL.

        Returns:
        str: The full URL for the API request.
        """
        return f"{self.base_url}{endpoint}"

    def generate_text(self, prompt, max_tokens=100, temperature=0.7):
        """
        Generate text using the specified model.

        Args:
        prompt (str): The prompt to generate text from.
        max_tokens (int): The maximum number of tokens to generate. Defaults to 100.
        temperature (float): The temperature to use for generation. Defaults to 0.7.

        Returns:
        dict: A dictionary containing the generated text and other metadata.
        """

        url = self._construct_url()
        headers = self._construct_headers()
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

# Example usage:
api_key=os.environ.get('GEMINI_API_KEY')
proxy = LitellmProxy(api_key=api_key)
response = proxy.generate_text("Hello, world!")
print(response)
