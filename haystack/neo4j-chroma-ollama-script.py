import sys
import json
from typing import List, Dict, Any
from haystack import Pipeline
from haystack.dataclasses import Document
from neo4j_haystack import Neo4jDocumentStore
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
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

def setup_document_stores() -> tuple:
    neo4j_store = Neo4jDocumentStore(
        url="bolt://localhost:7687",
        username="neo4j",
        password="your_password",
        database="neo4j"
    )
    chroma_store = ChromaDocumentStore(
        collection_name="my_collection",
        embedding_dim=384  # Dimension for 'nomic-embed-text' model
    )
    return neo4j_store, chroma_store

def index_documents(neo4j_store: Neo4jDocumentStore, chroma_store: ChromaDocumentStore, documents: List[Document]):
    embedder = OllamaDocumentEmbedder(model="nomic-embed-text", url="http://localhost:11434")
    
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("embedder", embedder)
    indexing_pipeline.add_component("neo4j_writer", neo4j_store)
    indexing_pipeline.add_component("chroma_writer", chroma_store)
    indexing_pipeline.connect("embedder.documents", "neo4j_writer.documents")
    indexing_pipeline.connect("embedder.documents", "chroma_writer.documents")

    results = indexing_pipeline.run({"embedder": {"documents": documents}})
    
    # Link Neo4j and Chroma using unique IDs
    for neo4j_doc, chroma_doc in zip(results["neo4j_writer"]["documents"], results["chroma_writer"]["documents"]):
        neo4j_store.update_document_meta(neo4j_doc.id, {"chroma_id": chroma_doc.id})

    print(f"Indexed {len(documents)} documents.")

def setup_search_pipeline(chroma_store: ChromaDocumentStore) -> Pipeline:
    text_embedder = OllamaTextEmbedder(model="nomic-embed-text", url="http://localhost:11434")
    retriever = ChromaEmbeddingRetriever(document_store=chroma_store, top_k=5)

    search_pipeline = Pipeline()
    search_pipeline.add_component("text_embedder", text_embedder)
    search_pipeline.add_component("retriever", retriever)
    search_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

    return search_pipeline

def search(pipeline: Pipeline, query: str) -> List[Document]:
    results = pipeline.run({"text_embedder": {"text": query}})
    return results["retriever"]["documents"]

def main(keys_to_embed: List[str]):
    # Setup document stores
    neo4j_store, chroma_store = setup_document_stores()

    # Load JSONL data from stdin
    data = load_jsonl_from_stdin()

    # Create documents
    documents = create_documents(data, keys_to_embed)

    # Index documents
    index_documents(neo4j_store, chroma_store, documents)

    # Setup search pipeline
    search_pipeline = setup_search_pipeline(chroma_store)

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
            
            # Fetch additional data from Neo4j if needed
            neo4j_doc = neo4j_store.get_document_by_id(doc.meta.get("neo4j_id"))
            if neo4j_doc:
                print(f"   Additional Neo4j data: {neo4j_doc.meta}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <key1> <key2> ...")
        sys.exit(1)

    keys_to_embed = sys.argv[1:]
    main(keys_to_embed)
