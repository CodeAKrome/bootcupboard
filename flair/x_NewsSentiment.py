from flair.data import Sentence
from flair.nn import Classifier
from flair.splitter import SegtokSentenceSplitter

# from flair.models import SequenceTagger
from NewsSentiment import TargetSentimentClassifier
import sys
from json import dumps

# Constants

TEXT = """Russian forces are carrying out required operational and combat measures in the southwestern Voronezh Region as part of a counter-terror operation, Regional Governor Alexander Gusev said on Saturday.
The Russian Armed Forces are carrying out required operational and combat measures on the territory of the Voronezh Region as part of a counter-terror operation.
"I will keep informing you about the latest developments," the governor said on his Telegram channel.
A counter-terror regime was introduced in Moscow, the Moscow and Voronezh Regions earlier on Saturday.
The Telegram channel of Wagner private military company founder Yevgeny Prigozhin earlier posted several audio records with accusations against the country\u2019s military leaders.
In the wake of this, the Federal Security Service (FSB) of Russia has opened a criminal case into a call for an armed mutiny.
The FSB urged Wagner fighters not to obey Prigozhin\u2019s orders and take measures for his detention."""

SENTENCE = "Russian forces are carrying out required operational and combat measures in the southwestern Voronezh Region as part of a counter-terror operation, Regional Governor Alexander Gusev said on Saturday."

# init

NER_TAGGER = "ner-ontonotes-large"


def get_ner(text: str) -> list:
    sentiment_tagger = Classifier.load("sentiment")
    ner_tagger = Classifier.load(NER_TAGGER)
    splitter = SegtokSentenceSplitter()
    tsc = TargetSentimentClassifier()
    sentences = splitter.split(text)
    sentiment_tagger.predict(sentences)
    ner_tagger.predict(sentences)

    out = []
    for sentence in sentences:
        spans = []
        sent = sentence.to_plain_string()
        for span in sentence.get_spans("ner"):
            l = sent[: span.start_position]
            m = sent[span.start_position : span.end_position]
            r = sent[span.end_position :]
            sentiment = tsc.infer_from_text(l, m, r)
            for label in span.labels:
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
                        "score": f"{label.score:.2f}",
                        "sentiment": sentiment[0]["class_label"],
                        "probability": f"{sentiment[0]['class_prob']:.2f}",
                    }
                )
        out.append(
            {
                "sentence": sent,
                "tag": sentence.tag.lower(),
                "score": f"{sentence.score:.2f}",
                "spans": spans,
            }
        )
    return out


# --- MAIN ---

out = get_ner(sys.stdin.read())
for rec in out:
    print(dumps(rec, indent=True))


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
