#!env python
from diffusers import DiffusionPipeline
import torch

# https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_xl

# import torch._dynamo
# torch._dynamo.config.suppress_errors = True

# from torch.utils.benchmark import CompileMode
# from torch.fx.experimental.optimization import compile_fx, optimize_assert
# from torch.fx.experimental.optimization import compile as compile_torch
from torch._inductor import config


def grafix_device():
    """Return device to use for GPU"""
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    if torch.cuda.is_available():
        device = "cuda"
    return device


device = grafix_device()
# device = "cpu"
print(f"using {device}")

# From: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

# load both base & refiner
base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
)


# Acceleration torch.compile https://huggingface.co/docs/diffusers/main/en/tutorials/fast_diffusion
# Full list of compiler flags https://github.com/pytorch/pytorch/blob/main/torch/_inductor/config.py

# When using torch >= 2.0, you can improve the inference speed by 20-30% with torch.compile. Simple wrap the unet with torch compile before running the pipeline:
if torch.__version__ >= "2.0":
    print(f"Compiling UNets for faster inference... torch version {torch.__version__}")

    torch._inductor.config.conv_1x1_as_mm = True
    torch._inductor.config.coordinate_descent_tuning = True
    torch._inductor.config.epilogue_fusion = False
    torch._inductor.config.coordinate_descent_check_all_directions = True

    # set TorchDynamo options
    # config.conv_1x1_as_mm = True
    # config.coordinate_descent_tuning = True
    # config.epilogue_fusion = False
    # config.coordinate_descent_check_all_directions = True

    base.unet = torch.compile(base.unet, mode="max-autotune", fullgraph=True)
#    pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)

# base.unet = torch.compile(base.unet)
# refiner.unet = torch.compile(refiner.unet)


# compile the model using TorchDynamo
#   base.unet = optimize_assert(base.unet, torch._C.Conv2d)
# base.unet = torch.compile(base.unet, base.example_inputs, mode=CompileMode.PROFILE)

# base.to("cuda")
base.to(device)
refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
)

# It is also important to change the UNet and VAE’s memory layout to “channels_last” when compiling them to ensure maximum speed.
# pipe.unet.to(memory_format=torch.channels_last)
# pipe.vae.to(memory_format=torch.channels_last)
# refiner.unet.to(memory_format=torch.channels_last)
# refiner.vae.to(memory_format=torch.channels_last)


# refiner.to("cuda")
refiner.to(device)

# Define how many steps and what % of steps to be run on each experts (80/20) here
n_steps = 40
high_noise_frac = 0.8

prompt = "A majestic lion jumping from a big stone at night"


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

image.save("x_fullpipe.png")
