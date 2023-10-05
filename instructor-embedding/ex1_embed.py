from InstructorEmbedding import INSTRUCTOR

model = INSTRUCTOR("hkunlp/instructor-large")
# prepare texts with instructions
text_instruction_pairs = [
    {
        "instruction": "Represent the Science title:",
        "text": "3D ActionSLAM: wearable person tracking in multi-floor environments",
    },
    {
        "instruction": "Represent the Medicine sentence for retrieving a duplicate sentence:",
        "text": "Recent studies have suggested that statins, an established drug group in the prevention of cardiovascular mortality, could delay or prevent breast cancer recurrence but the effect on disease-specific mortality remains unclear.",
    },
]

# postprocess
texts_with_instructions = []
for pair in text_instruction_pairs:
    texts_with_instructions.append([pair["instruction"], pair["text"]])

# calculate embeddings
customized_embeddings = model.encode(texts_with_instructions)

for pair, embedding in zip(text_instruction_pairs, customized_embeddings):
    print("Instruction: ", pair["instruction"])
    print("text: ", pair["text"])
    print("Embedding: ", embedding)
    print("")
