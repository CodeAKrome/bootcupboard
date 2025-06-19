import flair

class EntityTagger:
    def __init__(self):
        # Load the OntoNotes-large model
        self.tagger = flair.models.SequenceTagger.load('ner-ontonotes-large')

    def tag_entities(self, text):
        """
        Tags entities in the given text with their respective opening and closing tags.

        Args:
            text (str): The input text string.

        Returns:
            str: The text with entities tagged.
        """
        # Create a Flair Sentence object from the input text
        sentence = flair.data.Sentence(text)

        # Use the OntoNotes-large model to predict entities in the sentence
        self.tagger.predict(sentence)

        # Initialize an empty list to store the tagged entities
        tagged_entities = []

        # Iterate over the entities predicted by the model
        for entity in sentence.get_spans('ner'):
            # Get the entity text and its tag
            entity_text = entity.text
            entity_tag = entity.tag

            # Append the tagged entity to the list
            tagged_entities.append((entity_text, entity_tag))

        # Initialize an empty string to store the final tagged text
        tagged_text = text

        # Iterate over the tagged entities and replace them in the original text
        for entity_text, entity_tag in tagged_entities:
            # Create the opening and closing tags for the entity
            opening_tag = f"<{entity_tag}>"
            closing_tag = f"</{entity_tag}>"

            # Replace the entity in the original text with its tagged version
            tagged_text = tagged_text.replace(entity_text, f"{opening_tag}{entity_text}{closing_tag}")

        # Return the final tagged text
        return tagged_text

# Example usage
tagger = EntityTagger()
text = "James Dean was an American actor."
print(tagger.tag_entities(text))
