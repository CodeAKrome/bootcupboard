import json
import sys
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

class EmbeddingsProcessor:
    def __init__(self, model_name: str = 'nvidia/NV-Embed-v2', max_seq_length: int = 32768):
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.model.max_seq_length = max_seq_length
        self.model.tokenizer.padding_side = "right"

    def add_eos(self, input_examples: List[str]) -> List[str]:
        return [input_example + self.model.tokenizer.eos_token for input_example in input_examples]

    def count_tokens(self, texts: List[str]) -> List[int]:
        texts_with_eos = self.add_eos(texts)
        return [len(self.model.tokenizer.encode(text)) for text in texts_with_eos]

    def process_json(self, input_json: Dict[str, Any]) -> Dict[str, Any]:
        if 'text' not in input_json:
            raise KeyError("Input JSON must contain a 'text' field")

        text = input_json['text']
        if not isinstance(text, str):
            raise ValueError("The 'text' field must be a string")

        token_count = self.count_tokens([text])[0]
        
        output_json = input_json.copy()
        output_json['token_count'] = token_count
        
        return output_json

def main():
    processor = EmbeddingsProcessor()

    try:
        input_json = json.load(sys.stdin)
        output_json = processor.process_json(input_json)
        json.dump(output_json, sys.stdout, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
