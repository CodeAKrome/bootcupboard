from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/tinyroberta-squad2"

# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name, device="mps")
QA_input = {
    'question': 'Why is model conversion important?',
    'context': 'The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.'
}
res = nlp(QA_input)
print(res)
# b) Load model & tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
