#!env python
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import torch

# https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_2

MODEL = "stabilityai/stable-diffusion-2-base"
prompt = "A majestic lion jumping from a big stone at night"
prompt = "Ham radio operator in front of a radio displaying the word W3FNK"
prompt = "funky W3FNK"


def run_pipeline(prompt, model_name=MODEL, n_steps=40):
    """Define how many steps"""
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    if torch.cuda.is_available():
        device = "cuda"

    print(f"using {device}")

    base = DiffusionPipeline.from_pretrained(
        MODEL, torch_dtype=torch.float16, variant="fp16"
    )

    base.scheduler = DPMSolverMultistepScheduler.from_config(base.scheduler.config)
    base = base.to(device)
    n_steps = 40
    return base(prompt, num_inference_steps=25).images[0]


run_pipeline(prompt).save("x_sd2.png")
