from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import os


class VideoGenerator:
    def __init__(self, mp3_files, png_images):
        self.mp3_files = mp3_files
        self.png_images = png_images

    def generate_video(self, output_filename="output.mp4"):
        # Load audio clips
        audio_clips = [AudioFileClip(file) for file in self.mp3_files]
        # Concatenate audio clips into a single clip
        final_audio = concatenate_videoclips(audio_clips, method="compose")

        # Create video clips from images
        image_clips = []
        for image in self.png_images:
            clip = ImageClip(image)
            # Set the duration of each clip to match the corresponding audio clip
            clip = clip.set_duration(final_audio.duration / len(self.png_images))
            image_clips.append(clip)

        # Concatenate video clips into a single clip
        final_video = concatenate_videoclips(image_clips, method="compose")

        # Set the audio of the final video to the combined audio clip
        final_video = final_video.set_audio(final_audio)

        # Write the final video to a file
        final_video.write_videofile(output_filename, fps=24)


# mp3_files = ["audio1.mp3", "audio2.mp3"]  # Replace with your actual MP3 filenames
# png_images = ["image1.png", "image2.png"]  # Replace with your actual PNG filenames
# video_generator = VideoGenerator(mp3_files, png_images)
