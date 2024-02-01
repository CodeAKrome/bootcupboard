from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("mps")

# Recommended if your computer has < 64 GB of RAM
# pipe.enable_attention_slicing()

# prompt = "a photo of an astronaut riding a horse on mars"
# prompt = "a photo of a ham radio operator in front of a large complicated radio communicating with a martian on mars showing the radio waves moving between the two planets"

prompt = "person operating a complicated shortwave radio with radio waves moving through the air"

image = pipe(prompt).images[0]
# image
image = pipe(prompt).images[0]
image.save("test.png")
