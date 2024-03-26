import os
import re
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

# Loading Google Gemini API Key from Environment Variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Display user Error, Warning or Success Message
def fn_display_user_messages(lv_text, lv_type, mv_processing_message):
    """Display user Info, Error, Warning or Success Message"""
    
    if lv_type == "Success":
        with mv_processing_message.container(): 
            st.success(lv_text)
    elif lv_type == "Error":
        with mv_processing_message.container(): 
            st.error(lv_text)
    elif lv_type == "Warning":
        with mv_processing_message.container(): 
            st.warning(lv_text)
    else:
        with mv_processing_message.container(): 
            st.info(lv_text)

# Upload pdf file into 'pdf-data' folder if it does not exist
def fn_upload_pdf(mv_pdf_input_file, mv_processing_message):
    """Upload pdf file into 'pdf-data' folder if it does not exist"""

    lv_file_name = mv_pdf_input_file.name

    if not os.path.exists("pdf-data"):
        os.makedirs("pdf-data")
    
    lv_temp_file_path = os.path.join("pdf-data",lv_file_name)
    
    if os.path.exists(lv_temp_file_path):
        print("Step1: File already available")
        fn_display_user_messages("Step1: File already available","Warning", mv_processing_message)
    else:
        with open(lv_temp_file_path,"wb") as lv_file:
            lv_file.write(mv_pdf_input_file.getbuffer())
    
        print("Step1: PDF uploaded successfully at -> " + lv_temp_file_path)
        fn_display_user_messages("Step1: PDF uploaded successfully at -> " + lv_temp_file_path, "Info", mv_processing_message)

# Extract uploaded pdf data
def fn_extract_pdf_data(mv_pdf_input_file, mv_processing_message):
    """Extract uploaded pdf data"""

    lv_temp_pdf_file_path = os.path.join("pdf-data",mv_pdf_input_file.name)

    # -- Loading PDF Data
    lv_pdf_loader = PyPDFLoader(lv_temp_pdf_file_path)
    lv_pdf_content = lv_pdf_loader.load()

    # -- Define patterns with flexibility
    pattern1 = r"(\w+)-\n(\w+)"  # Match hyphenated words separated by a line break
    pattern2 = r"(?<!\n\s)\n(?!\s\n)"  # Match line breaks not surrounded by whitespace
    pattern3 = r"\n\s*\n"  # Match multiple line breaks with optional whitespace

    lv_pdf_formatted_content = []
    
    for lv_page in lv_pdf_content:
        # -- Apply substitutions with flexibility
        lv_pdf_page_content = re.sub(pattern1, r"\1\2", lv_page.page_content)
        lv_pdf_page_content = re.sub(pattern2, " ", lv_pdf_page_content.strip())
        lv_pdf_page_content = re.sub(pattern3, " ", lv_pdf_page_content)
        lv_pdf_page_content = re.sub("\n", " ", lv_pdf_page_content)

        lv_pdf_formatted_content.append(
                                            Document( page_content= lv_pdf_page_content,
                                                    metadata= lv_page.metadata
                                                )
                                       )
    
        # print("Page Details of "+str(lv_page.metadata)+" is - "+lv_pdf_page_content)

    print("Step2: PDF content extracted")
    fn_display_user_messages("Step2: PDF content extracted", "Info", mv_processing_message)

# Main Program
def main():
    # -- Streamlit Settings
    st.set_page_config("Chat With Your Product User Manual")
    st.header("Chat With Your Product User Manual💁")
    st.text("")
    st.text("")
    st.text("")

    # -- Display Processing Details
    mv_processing_message = st.empty()
    st.text("")
    st.text("")

    # -- Setting Chat History
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # -- Creating App Display
    lv_prompt = st.chat_input("Pass your input here")

    # -- Recording Chat Input and Generating Response
    if lv_prompt:
        # -- Saving User Input
        st.session_state.messages.append({"role": "user", "content": lv_prompt})

        # -- Generating LLM Response
        lv_response = "Hello"

        # -- Saving LLM Response
        st.session_state.messages.append(
            {"role": "model", "content": lv_response}
        )

        # -- Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # -- Read User Manuals for Q&A
    with st.sidebar:
        mv_pdf_input_file = st.file_uploader("Choose a UM PDF file:", type=["pdf"])
        st.text("")
        st.text("")
        
        # -- Process Uploaded User Manual PDF
        col1, col2, col3 = st.columns(3)
        if col1.button("Submit"):
            if mv_pdf_input_file is not None:
                fn_upload_pdf(mv_pdf_input_file, mv_processing_message)
                fn_extract_pdf_data(mv_pdf_input_file, mv_processing_message)
            else:
                fn_display_user_messages("Upload PDF file before clicking on Submit", "Error", mv_processing_message)

        # -- Clear Chat History
        if col2.button("Reset"):
            st.session_state["messages"] = []

# Loading Main
if __name__ == "__main__":
    main()