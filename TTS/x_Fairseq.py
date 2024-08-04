import torch
from TTS.api import TTS

# TTS with on the fly voice conversion
api = TTS("tts_models/eng/fairseq/vits")
api.tts_with_vc_to_file(
    "What's all this then?",
    dataset = 'universal',
    speaker_wav="untitled.wav",
    file_path="output.wav"
)
