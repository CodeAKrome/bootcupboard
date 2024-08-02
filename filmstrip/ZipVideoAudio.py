#!python
from VideoAudioZip import VideoAudioZip
import fire


def main(
    video_dir: str = "video", audio_dir: str = "audio", output_file: str = "out.mp4"
):
    merger = VideoAudioZip(video_dir, audio_dir)
    merger.sort_files()
    merger.join_videos_with_audios(output_file)


if __name__ == "__main__":
    fire.Fire(main)
