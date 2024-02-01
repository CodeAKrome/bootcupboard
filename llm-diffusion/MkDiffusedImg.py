from diffusers import DiffusionPipeline
import torch
import fire

def text2image(prompt:str, outfile:str="diffused_image.png", model:str="runwayml/stable-diffusion-v1-5"):
    if torch.backends.mps.is_available():
        device_name = "mps"
    else:
        if torch.cuda.is_available():
            device_name = "cuda:0"
        else:
            device_name = "cpu"

    pipe = DiffusionPipeline.from_pretrained(model)
    pipe = pipe.to(device_name)

    # Recommended if your computer has < 64 GB of RAM
    #pipe.enable_attention_slicing()

    image = pipe(prompt).images[0]
    image.save(outfile)

if __name__ == "__main__":
    fire.Fire(text2image)