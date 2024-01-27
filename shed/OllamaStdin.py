#!env python
import ollama
import sys

# args: system prompt, instructions

modelfile = f"""
FROM llama2
SYSTEM {sys.argv[1]}
"""
text = sys.stdin.read() 
ollama.create(model='custom', modelfile=modelfile)

content = f"{sys.argv[2]}\nBase your reply on the following information:\n{text}\n"
#print(f"Mod: {modelfile}\nCON: {content}")

response = ollama.chat(model='custom', messages=[
  {
    'role': 'user',
    'content': content,
  },
])
print(f"---\n{response['message']['content']}\n")

# no idea what this is supposed to do
# bed = ollama.embeddings(model='llama2', prompt='They sky is blue because of rayleigh scattering')
# print(bed)


