from transformers import AutoModelForCausalLM, CodeGenTokenizerFast as Tokenizer
from PIL import Image
import fire
import requests

def main(image_path:str, question:str="what is in this image?", model_id:str="vikhyatk/moondream1"):
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    tokenizer = Tokenizer.from_pretrained(model_id)

#    image = Image.open(image_path)

    if image_path.startswith("http"):
        url = image_path
        image = Image.open(requests.get(url, stream=True).raw)
    else:
        image = Image.open(image_path)


    enc_image = model.encode_image(image)
    print(model.answer_question(enc_image, question, tokenizer))

if __name__ == "__main__":
    fire.Fire(main)