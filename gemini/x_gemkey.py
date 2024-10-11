from litellm import completion
import os
import sys

model = "gemini/gemini-1.5-flash"
model = "gemini/gemini-1.5-flash-exp-0827"
model = "gemini/gemini-nano"
model = "gemini/gemini-1.5-pro"

api_key=os.environ.get('GEMINI_API_KEY')
system_file = sys.argv[1]

with open(system_file, 'r') as fh:
    system = fh.read()
system = system.replace("\n", " ")

for line in sys.stdin:
    prompt = line.strip()
    response = completion(
        model=model, 
        messages=[{"role":"system", "content": system}, {"role": "user", "content": prompt}]
    )
    print(response.choices[0].message.content)
