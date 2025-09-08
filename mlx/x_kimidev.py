#!/usr/bin/env python3

from mlx_lm import load, generate

#mname = "mlx-community/Kimi-Dev-72B-8bit"
mname ="mlx-community/DeepSeek-R1-Distill-Qwen-32B-float16"
model, tokenizer = load(mname)

prompt = "hello"

if tokenizer.chat_template is not None:
    messages = [{"role": "user", "content": prompt}]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True
    )

response = generate(model, tokenizer, prompt=prompt, verbose=True)
