import streamlit as st
import tempfile
import os
import re
import torch
import PyPDF2
from threading import Thread

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts.prompt import PromptTemplate
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.utils import DistanceStrategy
from langchain.vectorstores.base import VectorStoreRetriever

# Function that returns prompt for Q&A
def fn_prompts(lv_pdf_context, lv_question):
    """Return prompts for Q&A"""

    lv_template = """Instruction:
    You are an AI assistant for answering questions about the provided context.
    You are given the following extracted parts of a long document and a question. Provide a detailed answer.
    If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
    =======
    {lv_pdf_context}
    =======
    Question: {lv_question}
    Output:\n"""

    lv_qa_prompt = PromptTemplate(
                                    template=template,
                                    input_variables=["lv_question", "lv_pdf_context"]
                                 )
    
    return lv_qa_prompt

# Function return PDF text content
def fn_read_pdf(lv_temp_file_path, mv_processing_message):
    """Return text of all PDF pages"""

    lv_pdf_context = ""
    with open(lv_temp_file_path, 'rb') as lv_pdf_file:
        lv_pdf = PyPDF2.PdfReader(lv_pdf_file)
        lv_total_num_pages = len(lv_pdf.pages)
        
        for lv_page_no in range(lv_total_num_pages):
            mv_processing_message.text(f"Processing page {lv_page_no} out of {lv_total_num_pages}...")
            lv_text = lv_pdf.pages[lv_page_no].extract_text()
            # Merge hyphenated words
            lv_text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", lv_text)
            # Fix newlines in the middle of sentences
            lv_text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", lv_text.strip())
            # Remove multiple newlines
            lv_text = re.sub(r"\n\s*\n", "\n\n", lv_text)

            lv_pdf_context += lv_text
    
#     return lv_pdf_context



# Main Function
def main():
    
    # -- Streamlit Settings
    st.set_page_config(layout='wide')
    
    col1, col2, col3 = st.columns(3)
    col2.title("Talk to your PDF")
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
    
    if mv_pdf_input_file is not None:
        mv_file_name = mv_pdf_input_file.name
        mv_vectorstore_file_name = os.path.join(mv_vector_storage_dir, mv_file_name[:-4] + ".vectorstore")
        mv_metadata_file_name = os.path.join(mv_vector_storage_dir, mv_file_name[:-4] + ".metadata")

        lv_temp_file_path = os.path.join(mv_temp_file_storage_dir,mv_file_name)
        with open(lv_temp_file_path,"wb") as lv_file:
            lv_file.write(mv_pdf_input_file.getbuffer())
        mv_processing_message.text("PDF uploaded successfully at -> " + lv_temp_file_path)

        # -- Extracting PDF Text
        lv_pdf_context = fn_read_pdf(lv_temp_file_path, mv_processing_message)
        print("=============Extracted Page Details===========")
        print(lv_pdf_context)
        print("=============End of Page Details==============")
    


# Calling Main Function
if __name__ == '__main__':
    main()