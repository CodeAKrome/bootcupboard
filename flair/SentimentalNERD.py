#from flair.data import Sentence
from flair.nn import Classifier
from flair.splitter import SegtokSentenceSplitter
from NewsSentiment import TargetSentimentClassifier
import sys
from json import dumps

"""Document Level Features for Named Entity Recognition and Target-Dependant Sentiment Analysis"""

# CITATIONS
# Flair
#
# @misc{schweter2020flert,
#     title={FLERT: Document-Level Features for Named Entity Recognition},
#     author={Stefan Schweter and Alan Akbik},
#     year={2020},
#     eprint={2011.06993},
#     archivePrefix={arXiv},
#     primaryClass={cs.CL}
# }
#
# @inproceedings{akbik2019flair,
#   title={{FLAIR}: An easy-to-use framework for state-of-the-art {NLP}},
#   author={Akbik, Alan and Bergmann, Tanja and Blythe, Duncan and Rasul, Kashif and Schweter, Stefan and Vollgraf, Roland},
#   booktitle={{NAACL} 2019, 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics (Demonstrations)},
#   pages={54--59},
#   year={2019}
# }
#
# https://huggingface.co/flair/ner-english-large
# https://github.com/flairNLP/flair
#
# NewsSentiment (NewsMTSC)
#
# @InProceedings{Hamborg2021b,
#   author    = {Hamborg, Felix and Donnay, Karsten},
#   title     = {NewsMTSC: (Multi-)Target-dependent Sentiment Classification in News Articles},
#   booktitle = {Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2021)},
#   year      = {2021},
#   month     = {Apr.},
#   location  = {Virtual Event},
# }
#
# https://pypi.org/project/NewsSentiment/
# https://aclanthology.org/2021.eacl-main.142.pdf
# https://huggingface.co/fhamborg/roberta-targeted-sentiment-classification-newsarticles

# ontonotes large has many additional entities.
# NER_TAGGER = "ner-ontonotes-large"
# the flair model is a document level one which takes into account the whole document.
NER_TAGGER = "flair/ner-english-large"


def nerd_tsc(text: str) -> list:
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

out = nerd_tsc(sys.stdin.read())
for rec in out:
    print(dumps(rec, indent=True))
