#!env python3
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_default_device("cuda")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)
inputs = tokenizer('''```python
def print_prime(n):
   """
   Print all primes between 1 and n
   """''', return_tensors="pt", return_attention_mask=False)

with torch.autocast(model.device.type, dtype=torch.float16, enabled=True):
    outputs = model.generate(**inputs, max_length=200)
text = tokenizer.batch_decode(outputs)[0]
print(text)
