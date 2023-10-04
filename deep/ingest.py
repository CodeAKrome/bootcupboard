from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import os

# HAL
# Heuristically programmed ALgorithmic computer.
# Generative Pre-trained Transformer 2

repo_path = 'pool'

docs = []
for dirpath, dirnames, filenames in os.walk(repo_path):
    for file in filenames:
        try: 
            loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
            docs.extend(loader.load_and_split())
        except Exception as e: 
            print(e)
            pass
        
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)

#dataset_path = 'hub://<org-id>/twitter_algorithm'
