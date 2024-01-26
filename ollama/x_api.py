import ollama

modelfile = """
FROM llama2
SYSTEM You are a poet. You will answer with rhyming verse.
"""
ollama.create(model='poet', modelfile=modelfile)

response = ollama.chat(model='llama2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])

response = ollama.chat(model='poet', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])


