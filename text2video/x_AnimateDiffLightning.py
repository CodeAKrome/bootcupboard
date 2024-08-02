import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_gif, export_to_video
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
import sys

TEXT = "The first images, from ten thousand kilometres away, brought to a halt the activities of all mankind."
TEXT = "On a billion television screens, there appeared a tiny, featureless cylinder, growing rapidly second by second."
TEXT = "Its body was a cylinder so geometrically perfect that it might have been turned on a lathe - one with centres fifty kilometres apart. The two ends were quite flat, apart from some small structures at the centre of one face, and were twenty kilometres across; from a distance, when there was no sense of scale, Rama looked almost comically like an ordinary domestic boiler."
TEXT = sys.argv[1]

device = "cuda"
device = "mps"
dtype = torch.float16

step = 4  # Options: [1,2,4,8]
repo = "ByteDance/AnimateDiff-Lightning"
ckpt = f"animatediff_lightning_{step}step_diffusers.safetensors"
base = "emilianJR/epiCRealism"  # Choose to your favorite base model.

adapter = MotionAdapter().to(device, dtype)
adapter.load_state_dict(load_file(hf_hub_download(repo, ckpt), device=device))
pipe = AnimateDiffPipeline.from_pretrained(
    base, motion_adapter=adapter, torch_dtype=dtype
).to(device)
pipe.scheduler = EulerDiscreteScheduler.from_config(
    pipe.scheduler.config, timestep_spacing="trailing", beta_schedule="linear"
)

# output = pipe(prompt="A girl smiling", guidance_scale=1.0, num_inference_steps=step)
output = pipe(prompt=TEXT, guidance_scale=1.0, num_inference_steps=step)

# export_to_gif(output.frames[0], "animation.gif")
export_to_video(output.frames[0], "animation.mp4")
