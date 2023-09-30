# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="TheBloke/StableBeluga-7B-GGUF")
