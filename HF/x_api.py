import requests
import os

# Set your Hugging Face API token as an environment variable
# os.environ["HF_API_TOKEN"] = "your_api_token_here"

API_TOKEN = os.environ.get("HF_API_TOKEN")
API_BASE = "https://api-inference.huggingface.co/models/"
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(f"{API_BASE}{MODEL_NAME}", headers=headers, json=payload)
    return response.json()

def chat_loop():
    print("Chat started. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        payload = {
            "inputs": f"User: {user_input}\nAssistant:",
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.95,
                "do_sample": True,
            }
        }
        
        response = query(payload)
        if isinstance(response, list) and len(response) > 0:
            print("Assistant:", response[0]['generated_text'])
        else:
            print("Error in API response:", response)

if __name__ == "__main__":
    if not API_TOKEN:
        print("Please set your Hugging Face API token as an environment variable named HF_API_TOKEN")
    else:
        chat_loop()
