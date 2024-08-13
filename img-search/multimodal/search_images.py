import streamlit as st
from PIL import Image
import os

from image_embedding_search import ImageEmbeddingSearch

# Initialize the ImageEmbeddingSearch class
image_paths = [f"path/to/images/{img}" for img in os.listdir("path/to/images")]
embedding_names = ["sentence-transformers/all-MiniLM-L6-v2", "openai/clip-vit-base-patch32"]
search_engine = ImageEmbeddingSearch(image_paths, embedding_names)

st.title("Image Search with Multiple Embeddings")

# Search input
query = st.text_input("Enter your search query")
search_button = st.button("Search")

if search_button and query:
    results = search_engine.search(query)
    
    # Display summary of results
    st.subheader("Search Results Summary")
    for embedding, images in results.items():
        st.write(f"{embedding}: {len(images)} matches")
    
    # Display results for each embedding
    for embedding, images in results.items():
        st.subheader(f"Results for {embedding}")
        cols = st.columns(5)
        for i, image_path in enumerate(images):
            with cols[i % 5]:
                img = Image.open(image_path)
                st.image(img, caption=os.path.basename(image_path), use_column_width=True)
