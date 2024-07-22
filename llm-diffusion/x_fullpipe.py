#!env python
from diffusers import DiffusionPipeline
import torch
from tqdm import trange

# https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_xl
# From: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
REFINER = "stabilityai/stable-diffusion-xl-refiner-1.0"
IMGFILE = "x_fullpipe.png"
prompt = "A majestic lion jumping from a big stone at night"

prompt = "sign that says W3FNK"


def run_pipeline(prompt, model_name, refiner_name, n_steps=40, high_noise_frac=0.8):
    """Define how many steps and what % of steps to be run on each experts (80/20) here"""
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    if torch.cuda.is_available():
        device = "cuda"

    print(f"using {device}")

    # load both base & refiner
    base = DiffusionPipeline.from_pretrained(
        model_name, torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    )

    base.to(device)
    refiner = DiffusionPipeline.from_pretrained(
        refiner_name,
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    )

    refiner.to(device)

    # run both experts
    image = base(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_end=high_noise_frac,
        output_type="latent",
    ).images
    image = refiner(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_start=high_noise_frac,
        image=image,
    ).images[0]
    return image


# image = run_pipeline(prompt, model_name=MODEL, refiner_name=REFINER, n_steps=50, high_noise_frac=0.7)
# image.save(IMGFILE)

for steps in trange(30, 71):
    for i in trange(6, 9):
        frac = i / 10
        image = run_pipeline(
            prompt,
            model_name=MODEL,
            refiner_name=REFINER,
            n_steps=steps,
            high_noise_frac=frac,
        )
        img = f"fullseq_{steps}_{frac}.png"
        print(img)
        image.save(img)
