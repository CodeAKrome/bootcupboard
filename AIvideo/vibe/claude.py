#!/usr/bin/env python3
"""
Sentence-to-Video Pipeline
Reads sentences from file or stdin, generates videos with SD and Kokoro TTS audio
"""

import sys
import os
import argparse
import tempfile
import subprocess
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline
from kokoro import generate as kokoro_generate
import numpy as np
from PIL import Image
import cv2

class VideoGenerator:
    def __init__(self, model_id="stabilityai/stable-diffusion-2-1", fps=24):
        """Initialize the video generation pipeline."""
        self.fps = fps
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        print(f"Loading Stable Diffusion model on {self.device}...")
        self.sd_pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "mps" else torch.float32
        )
        self.sd_pipe = self.sd_pipe.to(self.device)
        
    def generate_frames(self, prompt, num_frames=48, width=512, height=512):
        """Generate video frames for a prompt."""
        frames = []
        print(f"Generating {num_frames} frames for: '{prompt}'")
        
        # Generate interpolated prompts for smooth transitions
        for i in range(num_frames):
            # Add variation to seed for each frame
            seed = 42 + i
            generator = torch.Generator(device=self.device).manual_seed(seed)
            
            # Generate image
            with torch.no_grad():
                image = self.sd_pipe(
                    prompt,
                    num_inference_steps=20,
                    generator=generator,
                    width=width,
                    height=height
                ).images[0]
            
            frames.append(np.array(image))
            
            if (i + 1) % 10 == 0:
                print(f"  Generated {i + 1}/{num_frames} frames")
        
        return frames
    
    def generate_audio(self, text, output_path):
        """Generate audio using Kokoro TTS."""
        print(f"Generating audio for: '{text}'")
        
        # Generate audio with Kokoro
        # Note: Adjust voice and parameters as needed
        audio = kokoro_generate(text, voice="af_bella", speed=1.0)
        
        # Save audio to file
        import soundfile as sf
        sf.write(output_path, audio, 24000)
        
        # Get audio duration
        duration = len(audio) / 24000
        return duration
    
    def create_video_segment(self, sentence, output_path, temp_dir):
        """Create a single video segment from a sentence."""
        print(f"\n{'='*60}")
        print(f"Processing sentence: {sentence}")
        print(f"{'='*60}")
        
        # Generate audio first to determine duration
        audio_path = os.path.join(temp_dir, "audio.wav")
        audio_duration = self.generate_audio(sentence, audio_path)
        
        # Calculate number of frames needed
        num_frames = max(int(audio_duration * self.fps), 24)  # Minimum 24 frames
        
        # Generate video frames
        frames = self.generate_frames(sentence, num_frames=num_frames)
        
        # Create video without audio
        temp_video_path = os.path.join(temp_dir, "video_no_audio.mp4")
        height, width = frames[0].shape[:2]
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_video_path, fourcc, self.fps, (width, height))
        
        for frame in frames:
            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)
        
        out.release()
        
        # Combine video and audio using ffmpeg
        print("Combining video and audio...")
        cmd = [
            'ffmpeg', '-y',
            '-i', temp_video_path,
            '-i', audio_path,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-shortest',
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Created segment: {output_path}")
        
        return output_path

def read_sentences(input_source):
    """Read sentences from file or stdin."""
    if input_source == '-':
        print("Reading sentences from stdin (Ctrl+D to finish)...")
        sentences = [line.strip() for line in sys.stdin if line.strip()]
    else:
        with open(input_source, 'r') as f:
            sentences = [line.strip() for line in f if line.strip()]
    
    return sentences

def concatenate_videos(video_paths, output_path):
    """Concatenate multiple video files into one."""
    print(f"\nConcatenating {len(video_paths)} video segments...")
    
    # Create a temporary file list for ffmpeg
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        list_path = f.name
        for video_path in video_paths:
            f.write(f"file '{os.path.abspath(video_path)}'\n")
    
    try:
        # Use ffmpeg to concatenate
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_path,
            '-c', 'copy',
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Final video created: {output_path}")
    finally:
        os.unlink(list_path)

def main():
    parser = argparse.ArgumentParser(
        description='Generate video from sentences using Stable Diffusion and Kokoro TTS'
    )
    parser.add_argument(
        'input',
        help='Input file path or "-" for stdin'
    )
    parser.add_argument(
        '-o', '--output',
        default='output.mkv',
        help='Output video file path (default: output.mkv)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=24,
        help='Frames per second (default: 24)'
    )
    parser.add_argument(
        '--model',
        default='stabilityai/stable-diffusion-2-1',
        help='Stable Diffusion model ID'
    )
    
    args = parser.parse_args()
    
    # Read sentences
    sentences = read_sentences(args.input)
    
    if not sentences:
        print("Error: No sentences found in input")
        sys.exit(1)
    
    print(f"\nFound {len(sentences)} sentences to process")
    
    # Initialize generator
    generator = VideoGenerator(model_id=args.model, fps=args.fps)
    
    # Create temporary directory for segments
    with tempfile.TemporaryDirectory() as temp_dir:
        video_segments = []
        
        # Generate video for each sentence
        for i, sentence in enumerate(sentences, 1):
            segment_path = os.path.join(temp_dir, f"segment_{i:03d}.mp4")
            try:
                generator.create_video_segment(sentence, segment_path, temp_dir)
                video_segments.append(segment_path)
            except Exception as e:
                print(f"Error processing sentence {i}: {e}")
                continue
        
        if not video_segments:
            print("Error: No video segments were successfully created")
            sys.exit(1)
        
        # Concatenate all segments
        concatenate_videos(video_segments, args.output)
    
    print(f"\n{'='*60}")
    print(f"Pipeline complete! Output saved to: {args.output}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()