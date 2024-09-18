import sys
import json
from typing import List, Dict, Any
from haystack.schema import Document
from haystack.document_stores import Neo4jDocumentStore
from haystack.nodes import PreProcessor, EmbeddingRetriever
from haystack import Pipeline as HaystackPipeline
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
        index="documents",
        embedding_dim=384  # Dimension for 'nomic-embed-text' model
    )

def index_documents(document_store: Neo4jDocumentStore, documents: List[Document]):
    preprocessor = PreProcessor()
    processed_docs = preprocessor.process(documents)
    
    embedder = OllamaDocumentEmbedder(model="nomic-embed-text", url="http://localhost:11434")
    embedded_docs = embedder.embed(processed_docs)
    
    document_store.write_documents(embedded_docs)
    print(f"Indexed {len(embedded_docs)} documents.")

def setup_search_pipeline(document_store: Neo4jDocumentStore) -> HaystackPipeline:
    text_embedder = OllamaTextEmbedder(model="nomic-embed-text", url="http://localhost:11434")
    retriever = EmbeddingRetriever(document_store=document_store, top_k=5)

    pipeline = HaystackPipeline()
    pipeline.add_node(component=text_embedder, name="TextEmbedder", inputs=["Query"])
    pipeline.add_node(component=retriever, name="Retriever", inputs=["TextEmbedder"])

    return pipeline

def search(pipeline: HaystackPipeline, query: str) -> List[Document]:
    results = pipeline.run(query=query)
    return results["documents"]

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
