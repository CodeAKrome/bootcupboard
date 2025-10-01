#!/usr/bin/env python3
"""
Continuous, local speech-to-text on macOS with OpenAI Whisper.
author: you
"""

import os
import tempfile
import wave
import threading
import queue
import argparse
import numpy as np
import sounddevice as sd
import whisper

# ---------- CONFIGURATION ----------
MODEL_NAME = "base"          # tiny/base/small/medium/large
MODEL_NAME = "turbo"          # tiny/base/small/medium/large
LANGUAGE = None              # None = auto-detect, or e.g. "en"
BLOCK_DURATION = 3           # seconds per chunk
SAMPLE_RATE = 16_000         # Whisper expects 16 kHz mono
# -----------------------------------

def int2float(sound: np.ndarray) -> np.ndarray:
    """Convert int16 audio to float32 in [-1, 1]."""
    abs_max = np.abs(sound).max()
    sound = sound.astype('float32')
    if abs_max > 0:
        sound *= 1 / 32768
    sound = sound.squeeze()
    return sound

class StreamTranscriber:
    def __init__(self, model_name: str, language: str | None):
        self.model = whisper.load_model(model_name)
        self.language = language
        self.q = queue.Queue()
        self.running = True

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def process(self):
        """Run in worker thread: pull audio blocks and transcribe."""
        while self.running:
            audio_int16 = self.q.get()
            audio_float = int2float(audio_int16)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name
                with wave.open(tmp_path, "wb") as wav:
                    wav.setnchannels(1)
                    wav.setsampwidth(2)
                    wav.setframerate(SAMPLE_RATE)
                    wav.writeframes(audio_int16)

            result = self.model.transcribe(
                tmp_path,
                language=self.language,
                fp16=False,               # Apple-Silicon safe
                verbose=False
            )
            text = result["text"].strip()
            if text:                      # ignore empty returns
                print(">>>", text)
            os.remove(tmp_path)

    def start(self):
        """Start audio stream + worker."""
        self.thread = threading.Thread(target=self.process, daemon=True)
        self.thread.start()

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            callback=self.callback,
            blocksize=int(SAMPLE_RATE * BLOCK_DURATION),
        ):
            print("🎙  Listening…  (Ctrl-C to stop)\n")
            try:
                while True:
                    sd.sleep(1_000)
            except KeyboardInterrupt:
                print("\nStopping…")
                self.running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live Whisper on macOS")
    parser.add_argument("-m", "--model", default=MODEL_NAME,
                        help="Whisper model: tiny/base/small/medium/large")
    parser.add_argument("-l", "--lang", default=LANGUAGE,
                        help="Language code like 'en', or omit for auto")
    args = parser.parse_args()

    st = StreamTranscriber(args.model, args.lang)
    st.start()
