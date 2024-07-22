from diffusers import DiffusionPipeline
import torch
from tqdm import trange
import sys
import time

# https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_xl
# From: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
REFINER = "stabilityai/stable-diffusion-xl-refiner-1.0"
IMGFILE = "x_fullpipe.png"
prompt = "A majestic lion jumping from a big stone at night"


def timer():
    start_time = False
    last_call_time = None

    def elapsed_and_lap_time(name=''):
        nonlocal start_time, last_call_time
        if not start_time:  # initial call to start the timer
            start_time = time.time()
            print(f"Timer {name} started.")
        else:
            current_time = time.time()
            elapsed_time = current_time - start_time
            lap_time = current_time - last_call_time if last_call_time else 0
            print(f"{name} took {lap_time:.3f} seconds, total time elapsed: {elapsed_time:.3f}")
            last_call_time = current_time
    
    return elapsed_and_lap_time

rol = timer()


if len(sys.argv) > 1:
    path = sys.argv[1]
    prompt = sys.argv[2]


def run_pipeline(
    prompt,
    path,
    model_name,
    refiner_name,
    b_steps,
    e_steps,
    step,
    b_noise_frac,
    e_noise_frac,
    guidance,
):
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

    romp = prompt
    for i in trange(b_noise_frac, e_noise_frac):
        for guidance_scale in guidance:
            for steps in trange(b_steps, e_steps, step):
                frac = i / 10
                # run both experts
                image = base(
                    prompt=romp,
                    guidance_scale=guidance_scale,
                    num_inference_steps=steps,
                    denoising_end=frac,
                    output_type="latent",
                ).images
                image = refiner(
                    prompt=romp,
                    guidance_scale=guidance_scale,
                    num_inference_steps=steps,
                    denoising_start=frac,
                    image=image,
                ).images[0]
                img = f"{path}seq step {steps} guide {guidance_scale} frak {frac}.png"
                print(img)
                rol(img)
                image.save(img)


run_pipeline(
    prompt,
    path,
    model_name=MODEL,
    refiner_name=REFINER,
    b_steps=150,
    e_steps=180,
    step=5,
    b_noise_frac=6,
    e_noise_frac=9,
    guidance=[9, 9.5],
)

# image.save(IMGFILE)

# for steps in trange(30, 71):
#     for i in trange(6,9):
#         frac = i / 10
#         image = run_pipeline(prompt, model_name=MODEL, refiner_name=REFINER, n_steps=steps, high_noise_frac=frac)
#         img = f"fullseq_{steps}_{frac}.png"
#         print(img)
#         image.save(img)


# https://huggingface.co/blog/annotated-diffusion
# https://huggingface.co/blog/stable_diffusion#writing-your-own-inference-pipeline
# guidance_scale is a way to increase the adherence to the conditional signal that guides the generation (text, in this case) as well as overall sample quality. It is also known as classifier-free guidance, which in simple terms forces the generation to better match the prompt potentially at the cost of image quality or diversity. Values between 7 and 8.5 are usually good choices for Stable Diffusion. By default the pipeline uses a guidance_scale of 7.5.
# If you use a very large value the images might look good, but will be less diverse. You can learn about the technical details of this parameter in this section of the post.
