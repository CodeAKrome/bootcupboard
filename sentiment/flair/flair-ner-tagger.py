from flair.data import Sentence
from flair.models import SequenceTagger
import re

class FlairNERTagger:
    def __init__(self):
        self.tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")

    def tag_text(self, text):
        # Create a Flair Sentence object
        sentence = Sentence(text)

        # Run NER on the sentence
        self.tagger.predict(sentence)

        # Get the tagged string
        tagged_string = sentence.to_tagged_string()


        print(f"TAGGED:\n{tagged_string}\n")
        
        
        # Convert Flair's output format to XML-style tags
        output = ""
        current_entity = None
        for token in tagged_string.split():
            if token.startswith('<') and token.endswith('>'):
                if current_entity:
                    output += f"</{current_entity}>"
                current_entity = token[1:-1]
                output += f"<{current_entity}>"
            elif token == '<':
                if current_entity:
                    output += f"</{current_entity}>"
                current_entity = None
            elif token == '>':
                continue
            else:
                output += token + " "

        if current_entity:
            output += f"</{current_entity}>"

        # Clean up extra spaces
        output = re.sub(r'\s+', ' ', output).strip()

        return output

# Example usage
if __name__ == "__main__":
    tagger = FlairNERTagger()
    sample_text = "James Dean was an American actor who starred in films such as Rebel Without a Cause and East of Eden."
    tagged_text = tagger.tag_text(sample_text)
    print(tagged_text)
