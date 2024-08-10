from transformers import AutoProcessor, BarkModel
import torch
from scipy.io.wavfile import write as write_wav


device = "cuda" if torch.cuda.is_available() else "cpu"
device = "mps" if torch.backends.mps.is_available() and torch.backends.mps.is_built() else device
device = "cuda"
processor = AutoProcessor.from_pretrained("suno/bark-small")
model = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float16).to(device)

model.enable_cpu_offload()

model =  model.to_bettertransformer()
voice_preset = "v2/en_speaker_6"
inputs = processor("Hello, my dog is cute", voice_preset=voice_preset)
audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()
sample_rate = model.generation_config.sample_rate
write_wav("bark_generation.wav", sample_rate, audio_array)
