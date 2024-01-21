import streamlit as st
from sentence_transformers import SentenceTransformer, util
from llama_index import VectorStoreIndex, SimpleDirectoryReader

# Load BERT model and create vectorizer
model_name = "bert-base-nli-mean-tokens"
model = SentenceTransformer(model_name)
vectorizer = model.encode

# Load documents and create index
docs_path = "docs"  # Adjust this path if needed
reader = SimpleDirectoryReader(input_dir=docs_path, required_exts=[".txt"])
documents = reader.load_data()
document_embeddings = [vectorizer(doc.text) for doc in documents]
index = VectorStoreIndex(documents=documents, document_embeddings=document_embeddings)

# Streamlit app layout
st.title("Semantic and Similarity Search with BERT")
query = st.text_input("Enter your search query:")

if query:
    # Semantic search (approximated)
    most_similar_doc = index.similarity_search(query)[0]
    st.subheader("Semantic Search Results")
    st.write(most_similar_doc.text)

    # Similarity search
    similar_documents = index.similarity_search(query, k=5)  # Show top 5 results
    st.subheader("Similarity Search Results")
    for doc in similar_documents:
        st.write(f"- {doc.id}: {doc.text[:50]}...")
