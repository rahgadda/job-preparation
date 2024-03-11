import streamlit as st
import tempfile
import os
import re
from pypdf import PdfReader

st.title("Talk to your PDF")

# 0. Global variables
gv_pdf_input_file = st.file_uploader("Choose a PDF file:", type=["pdf"])
gv_temp_file_storage_dir = tempfile.mkdtemp()

if gv_pdf_input_file is not None:
    lv_temp_file_path = os.path.join(gv_temp_file_storage_dir,gv_pdf_input_file.name)

    # 1. Creating the destination file path with secure handling
    with open(lv_temp_file_path,"wb") as lv_file:
        lv_file.write(gv_pdf_input_file.getbuffer())

    # 2. Creating file upload success message
    if gv_pdf_input_file.type not in ['application/pdf', '']:  # Handle empty type as well
        st.error("Uploaded file is not a PDF. Please select a valid PDF file.")
    else:
        st.success("PDF uploaded successfully at -> " + lv_temp_file_path)

    # 3. Reading the uploaded PDF
    with open(lv_temp_file_path, 'rb') as lv_pdf_file:
        lv_pdf = PdfReader(lv_pdf_file)
        
        for lv_page_no, lv_page in enumerate(lv_pdf.pages, start=1):
            lv_text = lv_page.extract_text()

            # Merge hyphenated words
            lv_text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", lv_text)

            # Fix newlines in the middle of sentences
            lv_text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", lv_text.strip())

            # Remove multiple newlines
            lv_text = re.sub(r"\n\s*\n", "\n\n", lv_text)
            
            print('Processing Page Content - '+str(lv_page_no)+" Started")
            print(lv_text)
            print('Processing Page Content - '+str(lv_page_no)+" Ended")
