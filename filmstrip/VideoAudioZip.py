import os
# from moviepy import (
#     VideoFileClip,
#     AudioFileClip,
#     CompositeVideoClip,
#     concatenate_videoclips,
# )
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
#from moviepy.video.fx.loop import loop
from moviepy.video.fx.all import loop
import fire

""" write a python class that takes video and audio directories, sorts the files, then joins them together and writes them to an mp4 file making each video file duration the same as its corresponding audio file by looping it using the fire module """


class VideoAudioZip:
    def __init__(self, video_dir, audio_dir):
        self.video_dir = video_dir
        self.audio_dir = audio_dir

    def sort_files(self):
        self.video_files = sorted(os.listdir(self.video_dir))
        self.audio_files = sorted(os.listdir(self.audio_dir))

    def join_videos_with_audios(self, output_file: str = "out.mp4"):
        clips = []
        for video, audio in zip(self.video_files, self.audio_files):
            video_path = os.path.join(self.video_dir, video)
            audio_path = os.path.join(self.audio_dir, audio)

            # Load the video clip and get its duration
            video_clip = VideoFileClip(video_path)
            video_duration = video_clip.duration

            # Load the audio clip and get its duration
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration

            # Loop the video if it's shorter than the audio
            if video_duration < audio_duration:
                # final_video = CompositeVideoClip([video_clip]) * (audio_duration / video_duration)
                final_video = loop(video_clip, duration=audio_duration)
            else:
                final_video = video_clip

            # Ensure the video and audio have the same duration
            # final_audio = AudioFileClip(audio_path).set_duration(video_duration)
            final_audio = audio_clip

            # Combine the video with the audio
            final_clip = CompositeVideoClip([final_video])
            final_clip = final_clip.set_audio(final_audio)
            clips.append(final_clip)

        concatenate_videoclips(clips).write_videofile(output_file, codec="libx264")
