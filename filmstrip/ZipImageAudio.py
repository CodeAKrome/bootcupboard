#!python
# -*- coding: utf-8 -*-
from ImageAudioZip import ImageAudioZip
import os
import fire
import time


def get_media_files(image_dir=None, sound_dir=None):
    if not image_dir or not sound_dir:
        raise ValueError("Both image_dir and sound_dir must be provided")
    # sound_files = [os.path.join(sound_dir, file) for file in os.listdir(sound_dir) if file.endswith('.sound')]
    # image_files = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.png')]
    sound_files = sorted(
        [os.path.join(sound_dir, file) for file in os.listdir(sound_dir)]
    )
    image_files = sorted(
        [os.path.join(image_dir, file) for file in os.listdir(image_dir)]
    )
    t0 = time.time()
    media_to_mp4 = ImageAudioZip(sound_files, image_files)
    media_to_mp4.create_video()
    return time.time() - t0


if __name__ == "__main__":
    lap = fire.Fire(get_media_files)
    print(f"Execution time: {lap:.2f} seconds")
