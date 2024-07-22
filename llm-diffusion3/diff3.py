import torch
from diffusers import StableDiffusion3Pipeline

"""Generate images using Stable Diffusion 3"""

DEFAULT_PROMPT = "a photo of an astronaut riding a horse on mars"
DEFAULT_FILENAME = "astronaut.png"

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch.float16
)


def grafix_device():
    """Return device to use for GPU"""
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    if torch.cuda.is_available():
        device = "cuda"
    return device


pipe = pipe.to(grafix_device())


def generate_image(
    prompt: str = DEFAULT_PROMPT,
    negative_prompt: str = "",
    num_inference_steps: int = 28,
    guidance_scale: float = 7.0,
    filename: str = DEFAULT_FILENAME,
):
    """Prompt -> image using Stable Diffusion 3.
    If filename is provided, return save results, otherwise return image"""
    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
    ).images[0]

    if filename:
        return image.save(filename)
    return image
