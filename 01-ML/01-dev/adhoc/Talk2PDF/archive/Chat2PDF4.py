import streamlit as st
import tempfile
import os
import re
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from langchain_community.document_loaders import PyPDFLoader
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

# Function return langchain document object of PDF pages
def fn_read_pdf(lv_temp_file_path, mv_processing_message):
    """Returns langchain document object of PDF pages"""

    lv_pdf_loader = PyPDFLoader(lv_temp_file_path)
    lv_pdf_content = lv_pdf_loader.load()
    print("Step2: PDF content extracted")
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
    print("Step3: Vector store created")
    mv_processing_message.text("Step3: Vector store created")

    return lv_vector_store

# Function return QA Response using Vector Store
def fn_generate_QnA_response(mv_selected_model, mv_user_question, lv_vector_store, mv_processing_message):
    """Returns QA Response using Vector Store"""

    lv_chat_history = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    else:
        lv_chat_history = st.session_state.chat_history
    
    print("Step4: Generating LLM response")
    mv_processing_message.text("Step4: Generating LLM response")

    lv_tokenizer = AutoTokenizer.from_pretrained(
                                                        mv_selected_model,
                                                        model_max_length=2048,
                                                        trust_remote_code=True
                                                )
    lv_model = AutoModelForCausalLM.from_pretrained(
                                                        mv_selected_model,  
                                                        device_map="cpu", 
                                                        trust_remote_code=True
                                                   )

    lv_ms_phi2_pipeline = pipeline(
                                        "text-generation", tokenizer=lv_tokenizer, model=lv_model,
                                        pad_token_id=lv_tokenizer.eos_token_id, eos_token_id=lv_tokenizer.eos_token_id,
                                        torch_dtype=torch.float32, repetition_penalty=1.2,
                                        device_map="cpu", max_new_tokens=2048, return_full_text=True
                                  )

    lv_hf_phi2_pipeline = HuggingFacePipeline(pipeline=lv_ms_phi2_pipeline)
    lv_chain = ConversationalRetrievalChain.from_llm(lv_hf_phi2_pipeline, lv_vector_store.as_retriever(), return_source_documents=True)
    lv_response = lv_chain({"question": mv_user_question, 'chat_history': lv_chat_history})
    
    lv_chat_history += [(mv_user_question, lv_response["answer"])]
    st.session_state.chat_history = lv_chat_history

    print("Step5: LLM response generated")
    mv_processing_message.text("Step5: LLM response generated")

    return lv_response['answer']


# Main Function
def main():
    
    # -- Streamlit Settings
    st.set_page_config(layout='wide')
    
    # -- Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
    
    if 'mv_temp_file_storage_dir' not in st.session_state:
        mv_temp_file_storage_dir = tempfile.mkdtemp()
        st.session_state.mv_temp_file_storage_dir = mv_temp_file_storage_dir
    else:
        mv_temp_file_storage_dir = st.session_state.mv_temp_file_storage_dir

    mv_processing_message = col2.empty()
    st.text("")
    st.text("")
    st.text("")

    mv_vector_storage_dir = "/workspace/knowledge-base/01-ML/01-dev/adhoc/Talk2PDF/vector_store"
    
    if (mv_pdf_input_file is not None):
        mv_file_name = mv_pdf_input_file.name
        # mv_vectorstore_file_name = os.path.join(mv_vector_storage_dir, mv_file_name[:-4] + ".vectorstore")
        # mv_metadata_file_name = os.path.join(mv_vector_storage_dir, mv_file_name[:-4] + ".metadata")
        
        if 'lv_vector_store' not in st.session_state:
            # -- Storing Uploaded PDF locally
            lv_temp_file_path = os.path.join(mv_temp_file_storage_dir,mv_file_name)
            with open(lv_temp_file_path,"wb") as lv_file:
                lv_file.write(mv_pdf_input_file.getbuffer())
            print("Step1: PDF uploaded successfully at -> " + lv_temp_file_path)    
            mv_processing_message.text("Step1: PDF uploaded successfully at -> " + lv_temp_file_path)
        
            # -- Extracting PDF Text
            lv_pdf_content = fn_read_pdf(lv_temp_file_path, mv_processing_message)

            # -- Creating FAISS Vector Store
            lv_vector_store = fn_create_faiss_vector_store(lv_pdf_content, mv_processing_message)
            st.session_state.lv_vector_store = lv_vector_store
        else:
            lv_vector_store = st.session_state.lv_vector_store

        # -- Taking input question and generate answer
        col1, col2, col3 = st.columns(3)
        lv_chat_history = col2.chat_message

        if mv_user_question := col2.chat_input("Chat on PDF Data"):
           # -- Add user message to chat history
           st.session_state.messages.append({"role": "user", "content": mv_user_question})

           # -- Generating LLM response
           lv_response = fn_generate_QnA_response(mv_selected_model, mv_user_question, lv_vector_store, mv_processing_message)

           # -- Adding assistant response to chat history
           st.session_state.messages.append({"role": "assistant", "content": lv_response})
        
        # -- Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with lv_chat_history(message["role"]):
                st.markdown(message["content"])


# Calling Main Function
if __name__ == '__main__':
    main()