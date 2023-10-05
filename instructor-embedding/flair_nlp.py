from segtok.segmenter import split_single
from flair.data import Sentence
import mmap
import fire
import re
import flair
import torch

# https://github.com/poteha/docker-nlp

if torch.cuda.is_available():
    device = torch.device('cuda:0')
#    print("CUDA")
else:
    device = torch.device('cpu')
#    print("CPU")

flair.device = device

class Nlp(object):
    """Natural language processing functions using flair."""

    def mmap_file(self, filepath):
        """Use memory mapping to reaad an entire file."""
        with open(filepath, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            return mm.read().decode()

    def sentences(self, file='artofwar.txt'):
        """Break a file into lines by sentence."""
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text)
        sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
        sentences = [sentence for sentence in sentences if sentence]
        for sentence in sentences:
            print(sentence.text)

    def ner(self, file="artofwar.txt"):
        """Print jsonl with named entity information."""
        from flair.models import SequenceTagger
        tagger: SequenceTagger = SequenceTagger.load('ner')
        text = self.mmap_file(file)
        text = re.sub(r"\s+", " ", text).strip()
        sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
        sentences = [sentence for sentence in sentences if sentence]
        tagger.predict(sentences)
        for sentence in sentences:
            print(sentence.to_tagged_string())


if __name__ == '__main__':
    fire.Fire(Nlp)
