import fire
import moviepy.editor as mp
import os
import glob


def join_video_audio(
    video_dir: str = "video",
    audio_dir: str = "audio",
    output_filename: str = "output.mp4",
):
    # Get the video and audio files
    video_files = glob.glob(os.path.join(video_dir, "*.mp4"))
    audio_files = glob.glob(os.path.join(audio_dir, "*.mp3"))

    # Sort the files by their names
    video_files.sort(key=os.path.basename)
    audio_files.sort(key=os.path.basename)

    # Check that the number of video and audio files match
    if len(video_files) != len(audio_files):
        print("Error: Number of video files does not match number of audio files")
        return

    # Initialize the video editor
    editor = mp.VideoEditor()

    # Iterate through the files and join them together
    for video_file, audio_file in zip(video_files, audio_files):
        # Load the video and audio clips
        video_clip = mp.VideoFileClip(video_file)
        audio_clip = mp.AudioFileClip(audio_file)

        # Get the duration of the audio clip
        audio_duration = audio_clip.duration

        # Resize the video clip to match the audio duration
        video_clip = video_clip.subclip(0, audio_duration)

        # Concatenate the video and audio clips
        editor.append(video_clip, offset=0)
        editor.append(audio_clip, offset=0)

    # Write the combined video file
    editor.write_videofile(output_filename, codec="libx264")


if __name__ == "__main__":
    fire.Fire(join_video_audio)
