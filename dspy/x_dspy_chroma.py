from dspy.retrieve import ChromadbRM
import os
#import openai
# from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb.utils.embedding_functions import InstructorEmbeddingFunction

# embedding_function = OpenAIEmbeddingFunction(
#     api_key=os.environ.get('OPENAI_API_KEY'),
#     model_name="text-embedding-ada-002"
# )

embedding_function = InstructorEmbeddingFunction(
    model_name="hkunlp/instructor-xl",
)

retriever_model = ChromadbRM(
    'kolin',
    'db',
    embedding_function=embedding_function,
    k=5
)

results = retriever_model("Explore the significance of quantum computing", k=5)

for result in results:
    print("Document:", result.long_text, "\n")
