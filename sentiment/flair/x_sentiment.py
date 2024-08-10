from flair.data import Sentence
from flair.nn import Classifier
from icecream import ic

TEXT = "Barack Obama is the president of the United States."
NER_TAGGER = "flair/ner-english-large"
NER_TAGGER = "ner-ontonotes-large"


# make a sentence
# sentence = Sentence('I love Berlin and New York.')
sentence = Sentence(TEXT)

# load the sentiment tagger
sentiment_tagger = Classifier.load("sentiment")
ner_tagger = Classifier.load(NER_TAGGER)

# run sentiment analysis over sentence
sentiment_tagger.predict(sentence)
ner_tagger.predict(sentence)

# print the sentence with all annotations
# ic(sentence)
ic(f"{sentence.tag} {sentence.score}")


# print predicted NER spans
print("The following NER tags are found:")
# iterate over entities and print
for entity in sentence.get_spans("ner"):
    print(entity)
