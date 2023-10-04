#!/usr/bin/env python3
from flair.data import Sentence
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings
import sys
import time
from flair.nn import Classifier

tagger = Classifier.load("ner")

# create a StackedEmbedding object that combines glove and forward/backward flair embeddings
stacked_embeddings = StackedEmbeddings(
    [
        WordEmbeddings("glove"),
        FlairEmbeddings("news-forward"),
        FlairEmbeddings("news-backward"),
    ]
)
tokes = 0


def stacked(sentence):
    stacked_embeddings.embed(sentence)
    return sentence


def ner(sentence):
    tagger.predict(sentence)
    return sentence


start_time = time.time()

for line in sys.stdin:
    sentence = Sentence(line)
    sentence = stacked(sentence)
    tokes += len(sentence)
    sentence = ner(sentence)
#    print(sentence)
#    for token in sentence:
#        print(token)
#        print(token.embedding)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
tps = tokes / elapsed_time
print(f"tokens: {tokes}\ntps: {tps:.2f}")
