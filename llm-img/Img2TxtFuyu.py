from transformers import FuyuProcessor, FuyuForCausalLM
from PIL import Image
import requests
import torch
import fire


def main(image_path, question: str = "what is in the image?", model_id="adept/fuyu-8b"):
    # Doesn't look like it does mps for mac yet
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # load model and processor
    processor = FuyuProcessor.from_pretrained(model_id)
    model = FuyuForCausalLM.from_pretrained(model_id, device_map=device)
    # prepare inputs for the model
    text_prompt = "Generate a coco-style caption.\n"

    # convert() call fixes following error:
    # raise ValueError("Unable to infer channel dimension format")

    if image_path.startswith("http"):
        url = image_path
        image = Image.open(requests.get(url, stream=True).raw)
    else:
        image = Image.open(image_path).convert("RGB")

    inputs = processor(text=text_prompt, images=image, return_tensors="pt").to(device)
    # autoregressively generate text
    generation_output = model.generate(**inputs, max_new_tokens=7)
    generation_text = processor.batch_decode(
        generation_output[:, -7:], skip_special_tokens=True
    )
    print(generation_text[0])


if __name__ == "__main__":
    fire.Fire(main)
