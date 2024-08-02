import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_video
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
import sys
import fire


""" Create video clips reading a line at a time from stdin. """


class AnimatedTextProcessor:
    def __init__(self, base_filename="video/vid", step=4, repo="ByteDance/AnimateDiff-Lightning", base="emilianJR/epiCRealism"):
        self.base_filename = base_filename
        self.counter = 0
        self.device = "cuda" if torch.cuda.is_available() else "mps"
        self.dtype = torch.float16
        self.step = step  # Options: [1,2,4,8]
        self.repo = repo
        self.ckpt = f"animatediff_lightning_{step}step_diffusers.safetensors"
        self.base = base  # Choose to your favorite base model.

        adapter = MotionAdapter().to(self.device, self.dtype)
        adapter.load_state_dict(
            load_file(hf_hub_download(self.repo, self.ckpt), device=self.device)
        )
        self.pipe = AnimateDiffPipeline.from_pretrained(
            base, motion_adapter=adapter, torch_dtype=self.dtype
        ).to(self.device)
        self.pipe.scheduler = EulerDiscreteScheduler.from_config(
            self.pipe.scheduler.config,
            timestep_spacing="trailing",
            beta_schedule="linear",
        )

    def generate_filename(self):
        filename = f"{self.base_filename}_{self.counter:06d}.mp4"
        self.counter += 1
        return filename

    def process_input(self):
        for line in sys.stdin:
            prompt = line.strip()
            output = self.pipe(prompt=prompt, guidance_scale=1.0, step=self.step)
            export_to_video(output.frames[0], self.generate_filename())


def main(base_filename="video/vid"):
    processor = AnimatedTextProcessor(base_filename)
    processor.process_input()


if __name__ == "__main__":
    fire.Fire(main)
