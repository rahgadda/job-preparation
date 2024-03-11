import streamlit as st
import tempfile
import os
import re
import torch
from pypdf import PdfReader
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.vectorstores import FAISS


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
if torch.cuda.is_available():
    torch.set_default_device("cuda")
gv_model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
gv_tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
gv_vector_storage_dir = "/workspace/knowledge-base/01-ML/01-dev/adhoc/Talk2PDF/vector_store"

def fn_prompts():
    
    retrieval_prompt = """
        URS Q: Find the answer to the following question in the document:
        """
    answer_prompt = """
        ASSISTANT: Answer the question: {}
        CONTEXT: {}
        """
    summary_prompt = """
        URS S: Summarize the content of the following page(s): {}
        """
    
    return retrieval_prompt, answer_prompt, summary_prompt

def fn_create_pi2_embeddings(lv_text):
    document_input = gv_tokenizer(lv_text, return_tensors="pt", max_length=512, truncation=True)

def fn_create_vector_db(lv_file_name):
    lv_vector_store_location = os.path.join(gv_vector_storage_dir,lv_file_name)
    
    if os.path.isfile(path):
       gv_processing_message.text(f"Vector store created for file {lv_file_name}")
       return false
    else:
       gv_processing_message.text(f"Creating vector store created for file {lv_file_name}")
    
    return true

def processing_pdf():
    lv_temp_file_path = os.path.join(gv_temp_file_storage_dir,gv_pdf_input_file.name)

    # 2. Creating the destination file path with secure handling
    with open(lv_temp_file_path,"wb") as lv_file:
        lv_file.write(gv_pdf_input_file.getbuffer())

    # 3. Creating file upload success message
    gv_processing_message.text("PDF uploaded successfully at -> " + lv_temp_file_path)

    # 4. Reading the uploaded PDF

    # 4. Reading the uploaded PDF
    with open(lv_temp_file_path, 'rb') as lv_pdf_file:
        lv_pdf = PdfReader(lv_pdf_file)
        lv_total_num_pages = len(lv_pdf.pages)
        
        for lv_page_no, lv_page in enumerate(lv_pdf.pages, start=1):
            gv_processing_message.text(f"Processing page {lv_page_no} out of {lv_total_num_pages}...")
            lv_text = lv_page.extract_text()

            # Merge hyphenated words
            lv_text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", lv_text)
            # Fix newlines in the middle of sentences
            lv_text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", lv_text.strip())
            # Remove multiple newlines
            lv_text = re.sub(r"\n\s*\n", "\n\n", lv_text)
            
            # print('Processing Page Content - '+str(lv_page_no)+" Started")
            # print(lv_text)
            # print('Processing Page Content - '+str(lv_page_no)+" Ended")



if gv_pdf_input_file is not None:
    processing_pdf()    
        

    # X. Clearing messages
    gv_processing_message.empty()
