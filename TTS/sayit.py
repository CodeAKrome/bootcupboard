import torch
from TTS.api import TTS
from time import perf_counter
import subprocess
import sys

PLAY = 'afplay'
OUTFILE = 'sayit.wav'

modl = 'tts_models/en/jenny/jenny'

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
#print(TTS().list_models())

# Init TTS
#tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
tts = TTS(modl).to(device)


#wav = tts.tts(text="Hello world!", speaker_wav="untitled.wav", language="en")

# Text to speech to a file
#tts.tts_to_file(text="Hello world!", speaker_wav="untitled.wav", language="en", file_path="output.wav")
def readstd(callback):
    data = ''
    for line in sys.stdin:
        data += line.strip()

    callback(data)

def speek(text):
    tts.tts_to_file(text=text, file_path=OUTFILE)
#    subprocess.run(PLAY, OUTFILE)


if __name__ == '__main__':
    b = perf_counter()
    if len(sys.argv) > 1:
        speek(sys.argv[1])
    else:
        readstd(speek)
    print(f"Lap: {perf_counter() - b}")
