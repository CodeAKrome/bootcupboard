import streamlit as st
from PIL import Image
import os

from image_embedding_search import ImageEmbeddingSearch

# Initialize the ImageEmbeddingSearch class
image_paths = [f"path/to/images/{img}" for img in os.listdir("path/to/images")]
search_engine = ImageEmbeddingSearch(image_paths)

st.title("Image Search with CLIP Descriptions")

# Search input
query = st.text_input("Enter your search query")
search_button = st.button("Search")

if search_button and query:
    results = search_engine.search(query)
    
    # Display results
    st.subheader(f"Search Results: {len(results)} matches")
    
    cols = st.columns(3)
    for i, result in enumerate(results):
        with cols[i % 3]:
            img = Image.open(result['path'])
            st.image(img, caption=os.path.basename(result['path']), use_column_width=True)
            st.write(result['description'])

    # Option to get a new description for any image
    st.subheader("Get New Image Description")
    selected_image = st.selectbox("Select an image", [os.path.basename(r['path']) for r in results])
    if st.button("Generate New Description"):
        selected_path = next(r['path'] for r in results if os.path.basename(r['path']) == selected_image)
        new_description = search_engine.get_image_description(selected_path)
        st.write(f"New description: {new_description}")
