import os
from moviepy.editor import *
from moviepy.video.fx.all import loop
import fire


class VideoAudioMerger:
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


def main(
    video_dir: str = "video", audio_dir: str = "audio", output_file: str = "out.mp4"
):
    merger = VideoAudioMerger(video_dir, audio_dir)
    merger.sort_files()
    merger.join_videos_with_audios(output_file)


if __name__ == "__main__":
    fire.Fire(main)
