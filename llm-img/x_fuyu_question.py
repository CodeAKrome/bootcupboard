from transformers import FuyuProcessor, FuyuForCausalLM
from PIL import Image
import requests
import torch

device="cuda:0" if torch.cuda.is_available() else "cpu"
#device="mps"

# load model and processor
model_id = "adept/fuyu-8b"
processor = FuyuProcessor.from_pretrained(model_id)
model = FuyuForCausalLM.from_pretrained(model_id, device_map=device)

text_prompt = "What color is the bus?\n"
url = "https://huggingface.co/adept/fuyu-8b/resolve/main/bus.png"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=text_prompt, images=image, return_tensors="pt").to(device)

generation_output = model.generate(**inputs, max_new_tokens=6)
generation_text = processor.batch_decode(generation_output[:, -6:], skip_special_tokens=True)

print(f"{text_prompt} -> {generation_text}")

assert generation_text == ["The bus is blue.\n"]


text_prompt = "What is the highest life expectancy at birth of male?\n"
url = "https://huggingface.co/adept/fuyu-8b/resolve/main/chart.png"
image = Image.open(requests.get(url, stream=True).raw)

model_inputs = processor(text=text_prompt, images=image, return_tensors="pt").to(device)

generation_output = model.generate(**model_inputs, max_new_tokens=16)
generation_text = processor.batch_decode(generation_output[:, -16:], skip_special_tokens=True)

print(f"{text_prompt} -> {generation_text}")

assert generation_text == ["The life expectancy at birth of males in 2018 is 80.7.\n"]
