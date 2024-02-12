#!env python
from ragatouille import RAGPretrainedModel
from ragatouille.utils import get_wikipedia_page

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
my_documents = [get_wikipedia_page("Hayao_Miyazaki"), get_wikipedia_page("Studio_Ghibli")]
index_path = RAG.index(index_name="my_index", collection=my_documents)



# query = "ColBERT my dear ColBERT, who is the fairest document of them all?"
# RAG = RAGPretrainedModel.from_index(index_path)
# results = RAG.search(query)
# print(f"->{results}")
