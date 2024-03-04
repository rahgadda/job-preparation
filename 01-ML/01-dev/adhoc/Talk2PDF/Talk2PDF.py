import streamlit as st
import tempfile
import os

st.title("Talk to your PDF")
v_pdf_input_file = st.file_uploader("Choose a PDF file:", type=["pdf"])

if v_pdf_input_file is not None:
    
    # 1. Creating file upload success message
    v_temp_file_storage_dir = tempfile.mkdtemp()
    v_input_file_path = os.path.join(v_temp_file_storage_dir, v_pdf_input_file.name)
    st.success("PDF uploaded successfully at -> "+v_input_file_path)

    # 2. Reading PDF File
