#!/usr/bin/env python3
from flair.data import Sentence
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings

# create a StackedEmbedding object that combines glove and forward/backward flair embeddings
stacked_embeddings = StackedEmbeddings(
    [
        WordEmbeddings("glove"),
        FlairEmbeddings("news-forward"),
        FlairEmbeddings("news-backward"),
    ]
)
sentence = Sentence("The grass is green .")

# just embed a sentence using the StackedEmbedding as you would with any single embedding.
stacked_embeddings.embed(sentence)

# now check out the embedded tokens.
for token in sentence:
    print(token)
    print(token.embedding)
