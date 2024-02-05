#!env python
from flair.data import Sentence
from flair.nn import Classifier
from flair.splitter import SegtokSentenceSplitter

SPACY_MODEL_NAME = "en_core_web_trf"

TEXT = """Russian forces are carrying out required operational and combat measures in the southwestern Voronezh Region as part of a counter-terror operation, Regional Governor Alexander Gusev said on Saturday.
The Russian Armed Forces are carrying out required operational and combat measures on the territory of the Voronezh Region as part of a counter-terror operation.
"I will keep informing you about the latest developments," the governor said on his Telegram channel.
A counter-terror regime was introduced in Moscow, the Moscow and Voronezh Regions earlier on Saturday.
The Telegram channel of Wagner private military company founder Yevgeny Prigozhin earlier posted several audio records with accusations against the country\u2019s military leaders.
In the wake of this, the Federal Security Service (FSB) of Russia has opened a criminal case into a call for an armed mutiny.
The FSB urged Wagner fighters not to obey Prigozhin\u2019s orders and take measures for his detention."""

SENTENCE = "Russian forces are carrying out required operational and combat measures in the southwestern Voronezh Region as part of a counter-terror operation, Regional Governor Alexander Gusev said on Saturday."

from flair.models import SequenceTagger

# load tagger
tagger4 = SequenceTagger.load("flair/ner-english-large")


# tagger4 = Classifier.load('ner-large')
# tagger18 = Classifier.load('ner-ontonotes-large')
# tagger_sent = Classifier.load('sentiment')
splitter = SegtokSentenceSplitter()
link_tagger = Classifier.load("linker")


def get_ner(text: str, splitter: SegtokSentenceSplitter, tagger) -> list:
    sentences = splitter.split(text)
    tagger.predict(sentences)
    out = []
    for sentence in sentences:
        # print(f"{sentence}")
        spans = []

        for span in sentence.get_spans():
            # print(f"{span.start_position} : {span.end_position}")
            for label in span.labels:
                # print(f"{span.text}\t{label.value}\t{label.score}")
                if label.value == "<unk>":
                    val = ""
                else:
                    val = label.value
                spans.append(
                    {
                        "text": span.text,
                        "start": span.start_position,
                        "end": span.end_position,
                        "value": val,
                        "score": label.score,
                    }
                )
        out.append({"sentence": sentence.to_plain_string(), "spans": spans})
    return out


def print_ner(text: str, splitter: SegtokSentenceSplitter, tagger) -> list:
    sentences = splitter.split(text)
    tagger.predict(sentences)

    for sentence in sentences:
        print(f"{sentence}")
        for span in sentence.get_spans():
            print(f"{span.start_position} : {span.end_position}")
            for label in span.labels:
                print(f"{span.text}\t{label.value}\t{label.score}")


def ner_link(text: str):
    sentences = splitter.split(text)
    # link_sentences = sentences
    # link_tagger.predict(link_sentences)
    link_tagger.predict(sentences)
    tagger4.predict(sentences)

    for sentence in sentences:
        print(f"{sentence}")
        # print(f"{sentence.to_dict()}")
        # print(f"{dir(sentence)}")

        # print(f"{sentence.annotation_layers['ner']}")
        # for ner in sentence.annotation_layers['ner']:
        #     print(sentence.text[ner.data_point])
        # print(ner.value)
        # print(dir(ner))

        # print(dir(sentence))
        # print(f"{sentence.get_spans()}")

        # print(sentence.get_token(1))

        for span in sentence.get_spans():
            # print(dir(span))
            # print(span)
            # print(sentence.text[span.start_position:span.end_position])
            # print(f"{span.text}\t{span.labels[0].value}")
            # print(f"dic: {span.to_dict()}")

            for label in span.labels:
                print(f"{span.text}\t{label.value}\t{label.score}")

        # for label in sentence.get_labels():
        # print(label.value) # wiki item
        # print(label.labeled_identifier) # span[] label/wiki
        # print(dir(label.labeled_identifier))

        print("\n===\n")


def ner4(text: str):
    sentences = splitter.split(text)
    tagger4.predict(sentences)
    for sentence in sentences:
        print(f"{sentence}")


def ner18(text: str):
    sentences = splitter.split(text)
    tagger18.predict(sentences)
    for sentence in sentences:
        print(f"{sentence}")


def sent(text: str):
    sentences = splitter.split(text)
    tagger_sent.predict(sentences)
    # oneshot = True
    for sentence in sentences:
        print(f"{sentence}")
        print(f"SCORE {sentence.tag} {sentence.score}")
        # if oneshot:
        #     print("\n".join(dir(sentence)))
        #     oneshot = False


# --- MAIN ---

# dump_nlp(TEXT.replace("\n", ""))
# nlp_annotate(TEXT)
# nlp_flair(SENTENCE)

# ner_link(TEXT)
out = get_ner(TEXT, splitter, link_tagger)
for rec in out:
    print(rec)

# ner4(TEXT)
# ner18(TEXT)
# sent(TEXT)

# [What do we Really Know about State of the Art NER](https://arxiv.org/ftp/arxiv/papers/2205/2205.00034.pdf)

# Library Reported Obtained Delta
# Stanza 88.8 88.71 0.01
# SpaCy 90.0 89.09 0.91
# SparkNLP 89.97 88.6 1.37

# Genre Stanza Spacy SparkNLP
# News
# (bn, mz, nw)
# 90.41 90.79 90.47
# bc 88.35 88.72 87.59
# tc 76.68 71.16 78.37
# wb 81.2 82.81 80.11
