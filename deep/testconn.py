#from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain.embeddings.openai import

from langchain.text_splitter import CharacterTextSplitter 
from langchain.document_loaders import TextLoader 
from langchain.vectorstores import DeepLake 
import os 

from langchain.docstore.document import Document
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.document_loaders import TextLoader


from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings

# create a StackedEmbedding object that combines glove and forward/backward flair embeddings
stacked_embeddings = StackedEmbeddings([
                                        WordEmbeddings('glove'),
                                        FlairEmbeddings('news-forward'),
                                        FlairEmbeddings('news-backward'),
                                       ])
#sentence = Sentence('The grass is green .')

# just embed a sentence using the StackedEmbedding as you would with any single embedding.
#stacked_embeddings.embed(sentence)

# now check out the embedded tokens.
#for token in sentence:
#    print(token)
#    print(token.embedding)

    
fname = "shake.txt"
with open(fname) as f:
    text = f.read()

# load the document and split it into chunks
#loader = TextLoader("shake.txt")
#documents = loader.load()

# split it into chunks
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#docs = text_splitter.split_documents(documents)
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
    is_separator_regex = False,
)
docs = text_splitter.create_documents(text)
print(docs[0])

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


#text = "The pasta is really great when Joe Biden gets hit in the face with it."

# Example example below. Switch from curl to wget if using Linux 
# !curl -LO https://github.com/activeloopai/examples/raw/main/colabs/starting_data/paul_graham_essay.txt --output "paul_graham_essay.txt" 
# source_text = "paul_graham_essay.txt" 

#dataset_path = "hub://hal3x/text_embedding" 
dataset_path = "db" 

#documents = TextLoader(source_text).load() 
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) 
#docs = text_splitter.split_documents(documents) 

#doc = Document(page_content="foo", metadata={'a':'1'})
#doc1 = Document(page_content="bar1", metadata={'b':'2'})
#docs = [doc, doc1]

#db = DeepLake.from_documents(docs, dataset_path=dataset_path, embedding=stacked_embeddings)
db = DeepLake.from_documents(docs, dataset_path=dataset_path, embedding=embedding_function)

#data = db.search(query = "foo", search_type='similarity')
data = db.search(query = "Falstaff", search_type='similarity')
print(data)
