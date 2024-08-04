import torch
from TTS.api import TTS

# https://docs.coqui.ai/en/latest/inference.html

SAMPLE = "This is a black and white photograph capturing a moment of familial joy. The main subjects are a man, a woman, and two children, all standing on a grassy lawn in front of a house.  The man is positioned to the left of the frame, kneeling down with his arms lovingly wrapped around the two children. His posture suggests he's sharing a tender moment with them. Standing next to him is the woman, who has her arm affectionately draped over one of the children. Her stance indicates she's part of this intimate family gathering. The house behind them features a garage door and a window, providing context to their location. The lawn they're standing on appears well-maintained, adding to the serene ambiance of the scene. Please note that as this is a black and white image, specific colors cannot be determined. However, the varying shades of gray add depth and contrast to the photograph."

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
#device = torch.device(device)
#device = "mps"
# List available 🐸TTS models
#print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
#wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
# Text to speech to a file
#tts.tts_to_file(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
tts.tts_to_file(text=SAMPLE, speaker_wav="gandalf.wav", language="en", file_path="outgandalf.wav")
