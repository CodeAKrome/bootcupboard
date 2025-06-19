import sys
import json
import torch
from TTS.api import TTS
from time import perf_counter

modl = 'tts_models/en/jenny/jenny'
# Get device
#device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cuda" if torch.cuda.is_available() else "mps"
tts = TTS(modl).to(device)

def say(text: str, file: str):
    tts.tts_to_file(text=text, file_path=file)

def process_jsonl():
    for line in sys.stdin:
        try:
            # Parse JSONL line
            data = json.loads(line.strip())
            if 'id' not in data or 'text' not in data:
                print(f"Skipping invalid JSONL line: missing id or text field")
                continue
            
            id_str = str(data['id'])
            text = data['text']
            output_filename = f"{id_str}.mp3"
            
            # Convert text to speech and save as MP3
            say(text, output_filename)
            print(f"Successfully converted text to {output_filename}")
            
        except json.JSONDecodeError:
            print(f"Error: Invalid JSONL format in line: {line.strip()}")
        except Exception as e:
            print(f"Error processing id {data.get('id', 'unknown')}: {str(e)}")

if __name__ == "__main__":
    process_jsonl()