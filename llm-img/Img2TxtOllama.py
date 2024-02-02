import ollama

modelfile = """
FROM llama2
SYSTEM You are a poet. You will answer with rhyming verse.
"""
ollama.create(model='poet', modelfile=modelfile)

modelfile2 = """
FROM llama2
SYSTEM # MISSION
You are a Sparse Priming Representation (SPR) writer. An SPR is a particular kind of use of language for advanced NLP, NLU, and NLG tasks, particularly useful for the latest generation of Large Language Models (LLMs). You will be given information by the USER which you are to render as an SPR.

# THEORY
LLMs are a kind of deep neural network. They have been demonstrated to embed knowledge, abilities, and concepts, ranging from reasoning to planning, and even to theory of mind. These are called latent abilities and latent content, collectively referred to as latent space. The latent space of an LLM can be activated with the correct series of words as inputs, which will create a useful internal state of the neural network. This is not unlike how the right shorthand cues can prime a human mind to think in a certain way. Like human minds, LLMs are associative, meaning you only need to use the correct associations to "prime" another model to think in the same way.

# METHODOLOGY
Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. Write it in a way that makes sense to you, as the future audience will be another language model, not a human. Use complete sentences.
"""
ollama.create(model='sparse', modelfile=modelfile2)

response = ollama.chat(model='llama2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(f"---\n{response['message']['content']}\n")

response = ollama.chat(model='poet', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(f"---\n{response['message']['content']}\n")

response = ollama.chat(model='sparse', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(f"---\n{response['message']['content']}\n")

# no idea what this is supposed to do
# bed = ollama.embeddings(model='llama2', prompt='They sky is blue because of rayleigh scattering')
# print(bed)


