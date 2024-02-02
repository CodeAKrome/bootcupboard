import hf_olmo
from transformers import pipeline
olmo_pipe = pipeline("text-generation", model="allenai/OLMo-7B")
print(olmo_pipe("Language modeling is "))
