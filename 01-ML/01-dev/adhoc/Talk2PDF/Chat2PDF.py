import streamlit as st
import tempfile
import os
import requests
import time

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

# Download TheBloke Models
def fn_download_llm_models(mv_selected_model, mv_processing_message):
    """Download TheBloke Models"""

    lv_download_url = ""

    print("Downloading TheBloke of "+mv_selected_model)
    fn_display_user_messages("Downloading TheBloke of "+mv_selected_model, "Info", mv_processing_message)

    if mv_selected_model == 'microsoft/phi-2':
        lv_download_url = "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q2_K.gguf"
    elif mv_selected_model == 'mistralai/Mistral-7B-Instruct-v0.2':
        lv_download_url = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q2_K.gguf"

    if not os.path.exists("model"):
        os.makedirs("model")
    
    lv_filename = os.path.basename(lv_download_url)
    if os.path.exists("model/"+lv_filename):
        print("Model already available")
        fn_display_user_messages("Model already available","Warning", mv_processing_message)
    else:
        lv_response = requests.get(lv_download_url, stream=True)
        if lv_response.status_code == 200:
            with open("model/"+lv_filename, 'wb') as f:
                for chunk in lv_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            
            print("Download completed")
            fn_display_user_messages("Model download completed","Info", mv_processing_message)
        else:
            print(f"Model download completed {response.status_code}")
            fn_display_user_messages(f"Model download completed {response.status_code}","Error", mv_processing_message)

# Main Function
def main():
    
    # -- Streamlit Settings
    st.set_page_config(layout='wide')
    col1, col2, col3 = st.columns(3)
    col2.title("Chat with PDF")
    st.text("")

    # -- Downloading Model Files
    col1, col2, col3 = st.columns(3)
    mv_selected_model = col3.selectbox('Select Model',
                                        [
                                            'microsoft/phi-2',
                                            'mistralai/Mistral-7B-Instruct-v0.2'
                                        ]
                                      )
    st.text("")
    # -- Reading PDF File
    col1, col2, col3 = st.columns(3)
    mv_pdf_input_file = col2.file_uploader("Choose a PDF file:", type=["pdf"])

    # -- Display Processing Details
    st.text("")
    col1, col2, col3 = st.columns(3)
    mv_processing_message = col2.empty()
    st.text("")

    # -- Downloading Model Files
    fn_download_llm_models(mv_selected_model, mv_processing_message)

# Calling Main Function
if __name__ == '__main__':
    main()