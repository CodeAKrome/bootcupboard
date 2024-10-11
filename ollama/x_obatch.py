import ollama
import sys
from dotenv import load_dotenv
from json import dumps

"""Read from stdin, take filename of system prompt and model list on argv"""

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py [models]")
        sys.exit(1)
    
    system_file = sys.argv[1]
    models = sys.argv[2:]
    with open(system_file, 'r') as fh:
        system = fh.read()
    system = system.replace("\n", " ")
    # print(f"sys: {system}")

    for model in models:
        model_file=f"\nFROM {model}\nSYSTEM {system}\n"
        # print(f"Model file: {model_file}")
        ollama.create(model=model, modelfile=model_file)

    for line in sys.stdin:
        prompt = line.strip()
        for model in models:
            response = ollama.generate(model=model, prompt=prompt)
            print(response['response'])

if __name__ == "__main__":
    main()