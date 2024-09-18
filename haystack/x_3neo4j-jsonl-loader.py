import sys
import json
from typing import List, Dict, Any
from haystack import Pipeline, Document
from haystack.components.preprocessors import TextPreprocessor
from haystack.document_stores import Neo4jDocumentStore
from haystack.components.retrievers import EmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder, OllamaTextEmbedder

def load_jsonl_from_stdin() -> List[Dict[str, Any]]:
    return [json.loads(line) for line in sys.stdin]

def create_documents(data: List[Dict[str, Any]], keys_to_embed: List[str]) -> List[Document]:
    documents = []
    for item in data:
        content = " ".join(str(item.get(key, "")) for key in keys_to_embed)
        doc = Document(content=content, meta=item)
        documents.append(doc)
    return documents

def setup_document_store() -> Neo4jDocumentStore:
    return Neo4jDocumentStore(
        url="bolt://localhost:7687",
        username="neo4j",
        password="your_password",
        database="neo4j",
        embedding_dim=384  # Dimension for 'nomic-embed-text' model
    )

def index_documents(document_store: Neo4jDocumentStore, documents: List[Document]):
    preprocessor = TextPreprocessor()
    embedder = OllamaDocumentEmbedder(model="nomic-embed-text", url="http://localhost:11434")
    
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("preprocessor", preprocessor)
    indexing_pipeline.add_component("embedder", embedder)
    indexing_pipeline.add_component("document_store", document_store)
    indexing_pipeline.connect("preprocessor", "embedder")
    indexing_pipeline.connect("embedder", "document_store")

    indexing_pipeline.run({"preprocessor": {"documents": documents}})

    print(f"Indexed {len(documents)} documents.")

def setup_search_pipeline(document_store: Neo4jDocumentStore) -> Pipeline:
    text_embedder = OllamaTextEmbedder(model="nomic-embed-text", url="http://localhost:11434")
    retriever = EmbeddingRetriever(document_store=document_store, top_k=5)

    search_pipeline = Pipeline()
    search_pipeline.add_component("text_embedder", text_embedder)
    search_pipeline.add_component("retriever", retriever)
    search_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

    return search_pipeline

def search(pipeline: Pipeline, query: str) -> List[Document]:
    results = pipeline.run({"text_embedder": {"text": query}})
    return results["retriever"]["documents"]

def main(keys_to_embed: List[str]):
    # Setup document store
    document_store = setup_document_store()

    # Load JSONL data from stdin
    data = load_jsonl_from_stdin()

    # Create documents
    documents = create_documents(data, keys_to_embed)

    # Index documents
    index_documents(document_store, documents)

    # Setup search pipeline
    search_pipeline = setup_search_pipeline(document_store)

    # Interactive search loop
    while True:
        query = input("Enter your search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        results = search(search_pipeline, query)
        print(f"\nTop {len(results)} results:")
        for i, doc in enumerate(results, 1):
            print(f"{i}. Content: {doc.content[:100]}...")
            print(f"   Score: {doc.score:.4f}")
            print(f"   Metadata: {doc.meta}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <key1> <key2> ...")
        sys.exit(1)

    keys_to_embed = sys.argv[1:]
    main(keys_to_embed)
