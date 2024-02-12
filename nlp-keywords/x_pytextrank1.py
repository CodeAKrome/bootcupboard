import spacy
import pytextrank
import sys
import fire

def main():
    text = sys.stdin.read()
    nlp = spacy.load("en_core_web_sm")
    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    doc = nlp(text)
    for phrase in doc._.phrases:
        print(phrase.text)
        print(phrase.rank, phrase.count)
        print(phrase.chunks)


# --- MAIN ---

if __name__ == "__main__":
    fire.Fire(main)
    
