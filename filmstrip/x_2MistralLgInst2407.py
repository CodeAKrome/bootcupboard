from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    concatenate_audioclips,
)

# from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, concatenate_audioclips


class MediaToMp4:
    def __init__(self, mp3_files, png_files):
        if len(mp3_files) != len(png_files):
            raise ValueError("The number of MP3 files and PNG images must be the same")

        self.mp3_files = mp3_files
        self.png_files = png_files

    def create_video(self, output_path="output.mp4", fps=24, transition_duration=2):
        # Create a list to hold the video clips with corresponding audio durations and transitions
        clips = []
        audio_clips = []

        # Iterate through the images and mp3 files
        for i, (png, mp3) in enumerate(zip(self.png_files, self.mp3_files)):
            audio_clip = AudioFileClip(mp3)
            image_clip = (
                ImageClip(png)
                .set_duration(audio_clip.duration - transition_duration)
                .set_fps(fps)
                .set_audio(audio_clip)
            )

            if i > 0:
                # Add a crossfadein transition to the beginning of the current clip
                image_clip = image_clip.crossfadein(transition_duration)

            clips.append(image_clip)
            audio_clips.append(audio_clip)

        # Concatenate all video clips into one video clip with transitions
        if clips:
            final_video = concatenate_videoclips(clips, method="compose")
        else:
            raise ValueError("No PNG images or MP3 files provided")

        # Concatenate all audio clips into one audio clip (optional as it's already set in the image_clip)
        final_audio = concatenate_audioclips(audio_clips)

        # Set the audio of the video clip to the combined audio clip (optional)
        final_video = final_video.set_audio(final_audio).set_duration(
            final_audio.duration
        )

        # Write the result to a file with specified fps
        final_video.write_videofile(output_path, codec="libx264", fps=fps)


if __name__ == "__main__":
    mp3_files = ["gandalf.mp3", "gandalf.mp3"]  # List of MP3 files
    png_files = ["scn_600.jpg", "scn_603.jpg"]  # List of PNG images

    if len(mp3_files) != len(png_files):
        raise ValueError("The number of MP3 files and PNG images must be the same")

    media_to_mp4 = MediaToMp4(mp3_files, png_files)
    media_to_mp4.create_video()
