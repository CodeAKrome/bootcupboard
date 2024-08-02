import sys
from flair.splitter import SegtokSentenceSplitter


# text = "There once was a girl names Alice Liddel. She saw a rabbit and she said, 'I love rabbits.' It then hopped away."
splitter = SegtokSentenceSplitter()
text = "".join(sys.stdin.read())
sentences = splitter.split(text)
for sentence in sentences:
    print(sentence.to_plain_string())
