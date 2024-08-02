import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, afx
import fire

""" Concatnate video files with audio files to make one. """


class MediaConcatenator:
    def __init__(self, video_dir: str = "video", audio_dir: str = "audio"):
        self.video_dir = video_dir
        self.audio_dir = audio_dir
        self.final_clips = []

    def get_sorted_files(self, directory):
        return sorted(
            [
                os.path.join(directory, f)
                for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))
            ]
        )

    def load_clips(self):
        video_files = self.get_sorted_files(self.video_dir)
        audio_files = self.get_sorted_files(self.audio_dir)

        if len(video_files) != len(audio_files):
            raise ValueError(
                "The number of video files must match the number of audio files."
            )

        for video_path, audio_path in zip(video_files, audio_files):
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            # Loop the video clip for the duration of the audio clip
            looped_video_clip = afx.loop(
                video_clip, n=int(audio_clip.duration / video_clip.duration) + 1
            ).subclip(0, audio_clip.duration)
            self.final_clips.append(looped_video_clip.set_audio(audio_clip))

    def concatenate_media(self, output_file: str = "out.mp4"):
        if not self.final_clips:
            raise ValueError("No media files to write")

        final_clip = concatenate_videoclips(self.final_clips)
        final_clip.write_videofile(output_file, codec="libx264")
        print(f"Output written to {output_file}")


def main(
    video_dir: str = "video", audio_dir: str = "audio", output_file: str = "out.mp4"
):
    """Concatenates video and audio files from directories.

    Args:
      video_dir (str): The path to the directory containing video files.
      audio_dir (str): The path to the directory containing audio files.
      output_file (str): The path to the output file.
    """
    concatenator = MediaConcatenator(video_dir, audio_dir)
    concatenator.load_clips()
    concatenator.concatenate_media(output_file)


if __name__ == "__main__":
    fire.Fire(main)
