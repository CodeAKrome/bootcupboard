from transformers import FuyuProcessor, FuyuForCausalLM
from PIL import Image
import torch
import fire
from security import safe_requests

PENGUINS = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Adelie_penguins_in_the_South_Shetland_Islands.jpg/640px-Adelie_penguins_in_the_South_Shetland_Islands.jpg"
BUS = "https://huggingface.co/adept/fuyu-8b/resolve/main/bus.png"

#@profile
def main(
    image_path: str = PENGUINS,
    question: str = "Generate a coco-style caption.",
    tokens: int = 100,
    model_id="adept/fuyu-8b",
):
    # Doesn't look like it does mps for mac yet
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    #device="mps"
    
    processor = FuyuProcessor.from_pretrained(model_id)
    model = FuyuForCausalLM.from_pretrained(model_id, device_map=device)
    # prepare inputs for the model. It wants a newline at the end of the prompt.
    text_prompt = question + "\n"

    # convert() call fixes following error:
    # raise ValueError("Unable to infer channel dimension format")

    if image_path.startswith("http"):
        url = image_path
        image = Image.open(safe_requests.get(url, stream=True).raw)
    else:
        image = Image.open(image_path).convert("RGB")

    inputs = processor(text=text_prompt, images=image, return_tensors="pt").to(device)
    # autoregressively generate text
    generation_output = model.generate(**inputs, max_new_tokens=tokens)
    generation_text = processor.batch_decode(
        generation_output[:, :], skip_special_tokens=True
    )
    # generation_text = processor.batch_decode(
    #     generation_output[:, -7:], skip_special_tokens=True
    # )

    # Example raw output with bunches of speakers in front. Truncate before hex char
    # |SPEAKER||SPEAKER||NEWLINE|<s> Generate a coco-style caption.\n\x04 Three
    hex_char_index = generation_text[0].find("\x04")
    print(generation_text[0][hex_char_index + 2 :])


if __name__ == "__main__":
    fire.Fire(main)
