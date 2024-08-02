import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video

if torch.backends.mps.is_available():
    print("MPS device HO!")
else:
    print("MPS device not found.")

device = "cpu"
device = "mps"
torch.set_default_device(device)

pipe = DiffusionPipeline.from_pretrained(
    "damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16"
)

pipe = pipe.to(device)

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

pipe.enable_model_cpu_offload()

prompt = "Spiderman is surfing"

# KEG
# pipe = pipe.to("cpu")

video_frames = pipe(prompt, num_inference_steps=25).frames
video_path = export_to_video(video_frames)
