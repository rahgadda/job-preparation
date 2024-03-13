import streamlit as st
import tempfile
import os

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

    print("Downloading TheBloke of "+mv_selected_model)
    fn_display_user_messages("Downloading TheBloke of "+mv_selected_model, "Success", mv_processing_message)

    if mv_selected_model == 'microsoft/phi-2':
        print()
    elif mv_selected_model == 'mistralai/Mistral-7B-Instruct-v0.2':
        print()

    print("Download completed")
    fn_display_user_messages("Model download completed","Info", mv_processing_message)

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