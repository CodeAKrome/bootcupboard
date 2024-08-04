#!python
import torch
from TTS.api import TTS
import sys

""" Coqui.ai """
""" https://pypi.org/project/TTS/ """

class TextToSpeechProcessor:
    def __init__(self, base_filename: str="audio/tts"):
        self.base_filename = base_filename
        self.counter = 0
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/en/jenny/jenny").to(self.device)
    
    def generate_filename(self):
        filename = f"{self.base_filename}_{self.counter:06d}.wav"
        self.counter += 1
        return filename
    
    def process_input(self):
        for line in sys.stdin:
            sentence = line.strip()
            self.tts.tts_to_file(text=sentence, file_path=self.generate_filename())

tts = TextToSpeechProcessor()
tts.process_input()
