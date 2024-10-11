import fire
from transformers import AutoProcessor, AutoModelForPreTraining
import torch
from PIL import Image
import requests
from io import BytesIO

class LlamaTextImageCompletion:
    def __init__(self, model_name="meta-llama/Llama-3.2-90B-Vision-Instruct"):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForPreTraining.from_pretrained(model_name)
        self.device = torch.device("mps" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def load_image(self, image_path):
        if image_path.startswith('http'):
            response = requests.get(image_path)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(image_path)
        return image

    def generate_completion(self, prompt, image=None, max_length=100, temperature=0.7, top_p=0.9):
        if image:
            image = self.load_image(image)
            inputs = self.processor(text=prompt, images=image, return_tensors="pt")
            for key in inputs:
                inputs[key] = inputs[key].to(self.device)
        else:
            inputs = self.processor(text=prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True
            )
        
        generated_text = self.processor.decode(outputs[0], skip_special_tokens=True)
        return generated_text

    def __call__(self, prompt, image=None, **kwargs):
        return self.generate_completion(prompt, image, **kwargs)

def cli(prompt, image=None, max_length=100, temperature=0.7, top_p=0.9):
    """
    Generate text completion using Llama 3.2 90B Vision Instruct model.

    :param prompt: Text prompt for completion
    :param image: (Optional) Path to an image file or URL
    :param max_length: Maximum length of the generated text
    :param temperature: Temperature for text generation
    :param top_p: Top-p value for nucleus sampling
    :return: Generated text completion
    """
    completer = LlamaTextImageCompletion()
    result = completer(prompt, image, max_length=max_length, temperature=temperature, top_p=top_p)
    print(result)

if __name__ == "__main__":
    fire.Fire(cli)
