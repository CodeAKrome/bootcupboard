import os
import io
import torch
import numpy as np

from PIL import Image
#from transformers import AutoProcessor, AutoModelForSeq2SeqLM


# ----
# Load model directly
from transformers import AutoProcessor, AutoModelForCausalLM

processor = AutoProcessor.from_pretrained("adept/fuyu-8b")
model = AutoModelForCausalLM.from_pretrained("adept/fuyu-8b")
# ----


#processor = AutoProcessor.from_pretrained("adept/fuyu-8b")
#model = AutoModelForSeq2SeqLM.from_pretrained("adept/fuyu-8b")

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("mps")

def image_to_prompt(image: Image, processor: AutoProcessor) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    encoding = processor(images=buffered, return_tensors="pt").data
    encoding = encoding.to(device)
    input_ids = encoding["pixel_values"].squeeze().tolist()
    return input_ids

def generate_from_prompt(input_ids: list, model: AutoModelForSeq2SeqLM):
    print("Generating image...")
    generated_image = model.generate(
        input_ids=torch.LongTensor([input_ids]).to(device), 
        max_length=1000, 
        num_beams=5
    )[0]
    output = (processor.batch_decode(generated_image, skip_special_tokens=True)[0])
    return output
    
def write_prompt_to_file(output: str):
    with open("generated_output.txt", "w") as f:
        f.write(output)
        
if __name__ == "__main__":
    image = Image.open("llm.png").convert('RGB')
    input_ids = image_to_prompt(image, processor)
    print(input_ids)
    
    # output = generate_from_prompt(input_ids, model)
    # write_prompt_to_file(output)
    
