#!env python
from diffusers import StableDiffusionXLPipeline
import torch

# https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_2

MODEL = "stabilityai/stable-diffusion-2-base"
MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

prompt = "A majestic lion jumping from a big stone at night"
prompt = "Ham radio operator in front of a radio displaying the word W3FNK"

torch._inductor.config.conv_1x1_as_mm = True
torch._inductor.config.coordinate_descent_tuning = True
torch._inductor.config.epilogue_fusion = False
torch._inductor.config.coordinate_descent_check_all_directions = True


def grafix_device():
    """Return device to use for GPU"""
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    if torch.cuda.is_available():
        device = "cuda"
    return device


device = grafix_device()
print(f"using {device}")


pipe = StableDiffusionXLPipeline.from_pretrained(MODEL).to(device)

# It is also important to change the UNet and VAE’s memory layout to “channels_last” when compiling them to ensure maximum speed.
pipe.unet.to(memory_format=torch.channels_last)
pipe.vae.to(memory_format=torch.channels_last)

# not supported mps bfloat16
# Run the attention ops without SDPA.
# pipe.unet.set_default_attn_processor()
# pipe.vae.set_default_attn_processor()


# Compile the UNet and VAE.
# pipe.unet = torch.compile(pipe.unet, mode="max-autotune", fullgraph=True)
# pipe.vae.decode = torch.compile(pipe.vae.decode, mode="max-autotune", fullgraph=True)
# pipe.unet = torch.compile(pipe.unet)
# pipe.vae.decode = torch.compile(pipe.vae.decode)

# prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"

# First call to `pipe` is slow, subsequent ones are faster.
image = pipe(prompt, num_inference_steps=30).images[0]

# prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
# image = pipe(prompt, num_inference_steps=30).images[0]


# image = base(prompt, num_inference_steps=25).images[0]
image.save("x_compile.png")
