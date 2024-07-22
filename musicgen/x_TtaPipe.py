from transformers import pipeline
import scipy

TXT = "This image captures a serene moment in a forest clearing. At the center of the frame, a couple stands under a small wooden gazebo with a pointed roof. The man, positioned to the left, and the woman, on his right, are both dressed in dark clothing that contrasts with their surroundings.  The gazebo they stand under is quaint and rustic, its brown color blending harmoniously with the surrounding trees. The forest around them is dense with tall trees, their leaves forming a natural canopy overhead. Fallen leaves are scattered on the ground, adding to the sense of tranquility. The couple's faces are lit up with smiles as they look directly at the camera, their joy palpable even in this still image. Their relative positions and the gazebo create a focal point in the center of the image, drawing the viewer's eye immediately to them. Overall, this image paints a picture of a peaceful moment shared between two people amidst nature's beauty."

synthesiser = pipeline("text-to-audio", "facebook/musicgen-large")
#music = synthesiser("lo-fi music with a soothing melody", forward_params={"do_sample": True})
music = synthesiser(TXT, forward_params={"do_sample": True})
scipy.io.wavfile.write("musicgen_out.wav", rate=music["sampling_rate"], data=music["audio"])
