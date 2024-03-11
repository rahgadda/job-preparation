import streamlit as st
import tempfile
import os
import re
import torch
import PyPDF2
from transformers import AutoTokenizer, AutoModelForCausalLM
import faiss
import numpy as np


# 0. Streamlit Settings
st.set_page_config(layout='wide')
col1, col2, col3 = st.columns(3)
col2.title("Talk to your PDF")
st.text("")
col1, col2, col3 = st.columns(3)
gv_selected_model=col3.selectbox('Select Model',['microsoft/phi-2'])
st.text("")
st.text("")
st.text("")
col1, col2, col3 = st.columns(3)

# 1. Global variables
gv_pdf_input_file = col2.file_uploader("Choose a PDF file:", type=["pdf"])
gv_temp_file_storage_dir = tempfile.mkdtemp()
gv_processing_message = col2.empty()
gv_vector_storage_dir = "/workspace/knowledge-base/01-ML/01-dev/adhoc/Talk2PDF/vector_store"

if torch.cuda.is_available():
    torch.set_default_device("cuda")

def fn_prompts():
    """Return prompts for Q&A and Summarization"""

    lv_retrieval_prompt = """
        URS Q: Find the answer to the following question in the document:
        """
    lv_answer_prompt = """
        ASSISTANT: Answer the question: {}
        CONTEXT: {}
        """
    lv_summary_prompt = """
        URS S: Summarize the content of the following page(s): {}
        """
    
    return lv_retrieval_prompt, lv_answer_prompt, lv_summary_prompt

def fn_read_pdf_page(lv_pdf, lv_page_no):
    """Return reads PDF specific page number and return text"""

    lv_text = lv_pdf.pages[lv_page_no].extract_text()
    # Merge hyphenated words
    lv_text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", lv_text)
    # Fix newlines in the middle of sentences
    lv_text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", lv_text.strip())
    # Remove multiple newlines
    lv_text = re.sub(r"\n\s*\n", "\n\n", lv_text)
    
    return lv_text

def fn_create_embeddings(lv_text):
    """ Return embeddings using Hugging Face Transformers"""

    lv_model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", device_map="cpu", trust_remote_code=True)
    lv_tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
    lv_inputs = lv_tokenizer(lv_text, return_tensors="pt", truncation=True)

    with torch.no_grad():
        lv_outputs = lv_model(**lv_inputs)
    
    lv_embeddings = lv_outputs.last_hidden_state.mean(dim=1).numpy()
    
    return lv_embeddings

def fn_create_faiss_index(lv_embeddings, lv_metadata):
    """Creates a FAISS index for efficient vector search, handling potential dimension mismatch."""
    
    # Dimensionality of embeddings
    lv_dim_embedding = embeddings.shape[1]
    
    lv_faiss_index = faiss.IndexFlatL2(lv_dim_embedding)
    lv_faiss_index.add_with_ids(lv_embeddings, lv_metadata)
    
    return lv_faiss_index

def fn_save_faiss_index(lv_faiss_index, lv_metadata, lv_file_name):
    """Save Faiss index and metadata to disk""" 

    lv_vectorstore_file_name = os.path.join(gv_vector_storage_dir, lv_file_name[:-4] + ".vectorstore")
    lv_metadata_file_name = os.path.join(gv_vector_storage_dir, lv_file_name[:-4] + ".metadata")

    faiss.write_index(lv_faiss_index, lv_vectorstore_file_name)
    np.save(lv_metadata_file_name, lv_metadata)

def fn_load_faiss_index(lv_file_name):
    """Load Faiss index and metadata from the disk"""

    lv_vectorstore_file_name = os.path.join(gv_vector_storage_dir, lv_file_name[:-4] + ".vectorstore")
    lv_metadata_file_name = os.path.join(gv_vector_storage_dir, lv_file_name[:-4] + ".metadata")

    lv_faiss_index = faiss.read_index(lv_vectorstore_file_name)
    lv_metadata = np.load(lv_metadata_file_name)

    return lv_faiss_index, lv_metadata

def fn_processing_pdf():
    """Reading PDF uploaded and creating vector store for RAG"""

    lv_file_name = gv_pdf_input_file.name
    lv_temp_file_path = os.path.join(gv_temp_file_storage_dir,lv_file_name)
    lv_vectorstore_file_name = os.path.join(gv_vector_storage_dir, lv_file_name[:-4] + ".vectorstore")
    lv_metadata_file_name = os.path.join(gv_vector_storage_dir, lv_file_name[:-4] + ".metadata")

    # 2. Storing file into temp folder
    with open(lv_temp_file_path,"wb") as lv_file:
        lv_file.write(gv_pdf_input_file.getbuffer())

    # 3. Creating file upload success message
    gv_processing_message.text("PDF uploaded successfully at -> " + lv_temp_file_path)

    # 4. Verifying in Faiss index already created
    if os.path.exists(lv_vectorstore_file_name) and os.path.exists(lv_metadata_file_name):
        gv_processing_message.text("Loading already created vector store")
        lv_faiss_index, lv_metadata = fn_load_faiss_index(lv_file_name) 
    else:
        gv_processing_message.text("Creating new vector store")

        # 5. Reading the uploaded PDF
        with open(lv_temp_file_path, 'rb') as lv_pdf_file:
            lv_pdf = PyPDF2.PdfReader(lv_pdf_file)
            lv_total_num_pages = len(lv_pdf.pages)
            lv_faiss_index = faiss.IndexFlatL2(768)
            lv_metadata = []

            for lv_page_no in range(lv_total_num_pages):
                gv_processing_message.text(f"Processing page {lv_page_no} out of {lv_total_num_pages}...")
                
                lv_text = fn_read_pdf_page(lv_pdf, lv_page_no)
                # lv_embeddings = fn_create_embeddings(lv_text)
                # lv_faiss_index.add_with_ids(lv_embeddings, [{"page_no":lv_page_no}])
                # lv_metadata.append(lv_page_no)

                print('Processing Page Content - '+str(lv_page_no)+" Started")
                print(lv_text)
                print('Processing Page Content - '+str(lv_page_no)+" Ended")

            # fn_save_faiss_index(lv_faiss_index, lv_metadata, lv_file_name)


if gv_pdf_input_file is not None:
    fn_processing_pdf()    
        
    # X. Clearing messages
    gv_processing_message.empty()
