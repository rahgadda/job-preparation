import streamlit as st
import tempfile
import os
from pdfminer.high_level import extract_pages

st.title("Talk to your PDF")
gv_pdf_input_file = st.file_uploader("Choose a PDF file:", type=["pdf"])

if v_pdf_input_file is not None:
    
    # 1. Creating file upload success message
    gv_temp_file_storage_dir = tempfile.mkdtemp()
    gv_input_file_path = os.path.join(gv_temp_file_storage_dir, gv_pdf_input_file.name)
    st.success("PDF uploaded successfully at -> "+gv_input_file_path)

    # 2. Reading PDF File
    with open(gv_input_file_path, 'rb') as lv_pdf_file:
        lv_pages = extract_pages(lv_pdf_file)