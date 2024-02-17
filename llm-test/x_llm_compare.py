import transformers
import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline

model_names = [
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
]

bnb_config = BitsAndBytesConfig(
    load_in_4bits=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_type=torch.bfloat16,
)

models =   [
    AutoModelForCausalLM.from_pretrained(
        model_names[0],
        device_map='auto',
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
#         attn_implementation="flash_attention_2",
        cache_dir="./.cache",
        )
]

tokenizers = [
    AutoTokenizer.from_pretrained(model_names[0], cache_dir="./.cache", use_fast=True )
]

if hasattr(tokenizers[0], 'chat_template') and tokenizers[0].chat_template:
    print(f"Using chat template: {tokenizers[0].chat_template}")
else:
    print("NONE!!")

def generate(model, tokenizer, user_prompt):
    messages = [
        {"role": "user", "content": f"{user_prompt.strip()}"},
    ]
    
    # tokenize True?
    prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    inputs = tokenizer([prompt], return_tensors="pt").to("mps")
    shape = inputs.input_ids.shape
    print(f"Length of input is {shape[1]}")
    result = model.generate(**inputs, max_new_tokens=500, eos_token_id=tokenizer.eos_token_id)
    result_str = tokenizer.decode(result[0], skip_special_tokens=True)
    return result_str

prompt = 'List the planets in our solar system. Respond only with the list of planets.'
result = generate(models[0], tokenizers[0], prompt)
print(result)
