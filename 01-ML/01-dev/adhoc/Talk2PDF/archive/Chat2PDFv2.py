import streamlit as st
import tempfile
import os
import re
import torch
from threading import Thread

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores.faiss import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain

# Function return langchain document object of PDF pages
def fn_read_pdf(lv_temp_file_path, mv_processing_message):
    """Returns langchain document object of PDF pages"""

    lv_pdf_loader = PyPDFLoader(lv_temp_file_path)
    lv_pdf_content = lv_pdf_loader.load()
    mv_processing_message.text("Step2: PDF content extracted")

    return lv_pdf_content

# Function return FAISS Vector store
def fn_create_faiss_vector_store(lv_pdf_content, mv_processing_message):
    """Returns FAISS vector store index of PDF Content"""

    lv_embeddings = HuggingFaceEmbeddings(
                                            model_name="sentence-transformers/msmarco-distilbert-base-v4",
                                            model_kwargs={'device': 'cpu'},
                                            encode_kwargs={'normalize_embeddings': False}
                                         )
    lv_vector_store = FAISS.from_documents(lv_pdf_content, lv_embeddings)
    mv_processing_message.text("Step3: Vector store created")

    return lv_vector_store

# Function return QA Response using Vector Store
def fn_generate_QnA_response(mv_selected_model, mv_processing_message):
    """Returns QA Response using Vector Store"""
    mv_processing_message.text("Step4: Generating LLM response")

    lv_tokenizer = AutoTokenizer.from_pretrained(mv_selected_model, trust_remote_code=True)
    lv_model = AutoModelForCausalLM.from_pretrained(mv_selected_model, torch_dtype="auto", device_map="cpu", trust_remote_code=True)

    mv_processing_message.text("Step5: LLM response generated")
    st.session_state.initial_load = 'Y'


# Main Function
def main():
    
    # -- Streamlit Settings
    if 'initial_load' not in st.session_state:
        st.session_state.initial_load = 'Y'

    print("Session Value: - "+st.session_state.initial_load)
    st.set_page_config(layout='wide')

    col1, col2, col3 = st.columns(3)
    col2.title("Chat with your PDF")
    st.text("")
    
    col1, col2, col3 = st.columns(3)
    mv_selected_model=col3.selectbox('Select Model',['microsoft/phi-2'])
    st.text("")
    st.text("")
    st.text("")
    col1, col2, col3 = st.columns(3)

    # -- Reading PDF File
    mv_pdf_input_file = col2.file_uploader("Choose a PDF file:", type=["pdf"])
    mv_temp_file_storage_dir = tempfile.mkdtemp()
    mv_processing_message = col2.empty()
    mv_vector_storage_dir = "/workspace/knowledge-base/01-ML/01-dev/adhoc/Talk2PDF/vector_store"
    
    if (mv_pdf_input_file is not None) and (st.session_state.initial_load == 'Y'):
        print("Session Value: - "+st.session_state.initial_load)
        mv_file_name = mv_pdf_input_file.name
        mv_vectorstore_file_name = os.path.join(mv_vector_storage_dir, mv_file_name[:-4] + ".vectorstore")
        mv_metadata_file_name = os.path.join(mv_vector_storage_dir, mv_file_name[:-4] + ".metadata")

        lv_temp_file_path = os.path.join(mv_temp_file_storage_dir,mv_file_name)
        with open(lv_temp_file_path,"wb") as lv_file:
            lv_file.write(mv_pdf_input_file.getbuffer())
        mv_processing_message.text("Step1: PDF uploaded successfully at -> " + lv_temp_file_path)

        # -- Extracting PDF Text
        lv_pdf_content = fn_read_pdf(lv_temp_file_path, mv_processing_message)

        # -- Creating FAISS Vector Store
        lv_vector_store = fn_create_faiss_vector_store(lv_pdf_content, mv_processing_message)

        # -- Taking input question
        col1, col2, col3 = st.columns(3)
        st.text("")
        col2.text_area(label='Query')
        st.text("")
        if col2.button(label="Submit"):
            fn_generate_QnA_response(mv_selected_model, mv_processing_message)
        
        # -- Avoid re-creating vector store 
        st.session_state.initial_load = 'N'

# Calling Main Function
if __name__ == '__main__':
    main()