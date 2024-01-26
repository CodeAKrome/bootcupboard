import spacy

# Load the spaCy English model
spacy_model_name = 'en_core_web_sm'
if not spacy.util.is_package(spacy_model_name):
    spacy.cli.download(spacy_model_name)
nlp = spacy.load(spacy_model_name)

# Define a sample text
text = "The quick brown foxes are jumping over the lazy dogs."

# Process the text using spaCy
doc = nlp(text)

# Extract lemmatized tokens
lemmatized_tokens = [token.lemma_ for token in doc]

# Join the lemmatized tokens into a sentence
lemmatized_text = ' '.join(lemmatized_tokens)

# Print the original and lemmatized text
print("Original Text:", text)
print("Lemmatized Text:", lemmatized_text)
