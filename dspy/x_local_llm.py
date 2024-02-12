#!env python
import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import BootstrapFewShot, BootstrapFewShotWithRandomSearch, BootstrapFinetune
from icecream import ic

MODEL = 'llama2:13b'
TEXT_URL = 'http://20.102.90.50:2017/wiki17_abstracts'
TEXT = 'textsample0.txt'

lm = dspy.OllamaLocal(model=MODEL)
#colbertv2 = dspy.ColBERTv2(url=TEXT_URL)
colbertv2 = dspy.ColBERTv2(url=TEXT)
dspy.settings.configure(rm=colbertv2, lm=lm)

train = [
    ('Where was combat taking place?', 'southwestern Voronezh Region'),
    ('Where did the governor make an announcement?', 'Telegram'),
    ('What did Yevgeny Prigozhin say?', 'accusations'),
    ('What case was opened?', 'criminal case'),
    ('Why was a case opened?', 'mutiny'),
]

train = [dspy.Example(question=question, answer=answer).with_inputs('question') for question, answer in train]

dev = [
    ('Who founded Wagner?', 'Yevgeny Prigozhin'),
    ('Who urged fighers not to obay?', 'FSB'),
    ('What should be done with Yevgeny Prigozhin?', 'detention'),
    ('What was introduced in Moscow?', 'counter-terror regime'),
    ('What was announced Saturday?', 'counter-terror'),
]

dev = [dspy.Example(question=question, answer=answer).with_inputs('question') for question, answer in dev]

# predict = dspy.Predict('question -> answer')
# predict(question='What was announced Saturday?')
#print(f"->{out}")

class CoT(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought('question -> answer')
        
    def forward(self, question):
        return self.generate_answer(question=question)
    
metric_EM = dspy.evaluate.answer_exact_match
teleprompter = BootstrapFewShot(metric=metric_EM, max_bootstrapped_demos=2)
cot_compiled = teleprompter.compile(CoT(), trainset=train)
out = cot_compiled("What Telegram channels were used?")
print(f"->{out}")

#ic(cot_compiled("What Telegram channels were used?"))
