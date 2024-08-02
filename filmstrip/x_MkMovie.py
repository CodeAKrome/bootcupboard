import cv2
from moviepy.editor import *


class MovieCreator:
    def __init__(self, mp3_files, png_images):
        self.mp3_files = mp3_files
        self.png_images = png_images

    def create_movie(self, output_file="output.mp4"):
        # Create a list to store the image clips
        image_clips = []
        audio_clips = []

        # Load audio clips
        #        audio_clips = [AudioFileClip(file) for file in self.mp3_files]

        # Loop through each PNG image and MP3 audio file
        for img, mp3 in zip(self.png_images, self.mp3_files):
            # Get the duration of the MP3 audio file
            audio_clip = AudioFileClip(mp3)

            audio_clips.append(audio_clip)

            duration = audio_clip.duration

            # Create an ImageClip object with the same duration as the MP3 audio file
            clip = ImageClip(img).set_duration(duration)

            # Add a fade-in transition to the clip
            # clip = clip.fl_image(self.fade_in)
            clip = clip.crossfadein(2)

            image_clips.append(clip)

        # Concatenate audio clips into a single clip
        final_audio = concatenate_audioclips(audio_clips)

        # Create a CompositeVideoClip by concatenating all the image clips
        video_clip = concatenate_videoclips(image_clips, method="compose")

        # Add the audio to the video
        video_clip = video_clip.set_audio(final_audio)

        # Write the final video to a file
        video_clip.write_videofile(output_file, fps=24)

    def fade_in(self, frame, t):
        # Simple fade-in function that fades in the image over 1 second
        if t < 1:
            return frame * t
        else:
            return frame


# Example usage:
mp3_files = ["gandalf.mp3", "gandalf.mp3"]
png_images = ["scn_600.jpg", "scn_603.jpg"]

movie_creator = MovieCreator(mp3_files, png_images)
movie_creator.create_movie("my_movie.mp4")
