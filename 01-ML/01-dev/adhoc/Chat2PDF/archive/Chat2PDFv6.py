import streamlit as st
import os
import requests
import re

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS

from langchain.prompts.prompt import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA

# Upload pdf file into 'pdf-data' folder if it does not exist
def fn_upload_pdf(mv_pdf_input_file, mv_processing_message):
    """Upload pdf file into 'pdf-data' folder if it does not exist"""

    lv_file_name = mv_pdf_input_file.name

    if not os.path.exists("pdf-data"):
        os.makedirs("pdf-data")
    
    lv_temp_file_path = os.path.join("pdf-data",lv_file_name)
    
    if os.path.exists(lv_temp_file_path):
        print("File already available")
        fn_display_user_messages("File already available","Warning", mv_processing_message)
    else:
        with open(lv_temp_file_path,"wb") as lv_file:
            lv_file.write(mv_pdf_input_file.getbuffer())
    
        print("Step1: PDF uploaded successfully at -> " + lv_temp_file_path)
        fn_display_user_messages("Step1: PDF uploaded successfully at -> " + lv_temp_file_path, "Info", mv_processing_message)

# Create Vector DB of uploaded PDF
def fn_create_vector_db(mv_pdf_input_file, mv_processing_message):
    """Create Vector DB of uploaded PDF"""

    lv_file_name = mv_pdf_input_file.name[:-4] + ".vectorstore"

    if not os.path.exists(os.path.join("vectordb","fiaas")):
        os.makedirs(os.path.join("vectordb","fiaas"))
    
    lv_temp_file_path = os.path.join(os.path.join("vectordb","fiaas"),lv_file_name)
    lv_embeddings = HuggingFaceEmbeddings(
                                            model_name="sentence-transformers/all-mpnet-base-v2",
                                            model_kwargs={'device': 'cpu'}
                                        )
    
    if os.path.exists(lv_temp_file_path):
        print("VectorDB already available for uploaded file")
        fn_display_user_messages("VectorDB already available for uploaded file","Warning", mv_processing_message)

        lv_vector_store = FAISS.load_local(lv_temp_file_path, lv_embeddings,allow_dangerous_deserialization=True)
        return lv_vector_store
    else:
        lv_temp_pdf_file_path = os.path.join("pdf-data",mv_pdf_input_file.name)
        
        # -- Loading PDF Data
        lv_pdf_loader = PyPDFLoader(lv_temp_pdf_file_path)
        lv_pdf_content = lv_pdf_loader.load()
        print("Step2: PDF content extracted")
        fn_display_user_messages("Step2: PDF content extracted", "Info", mv_processing_message)

        # -- Chunking PDF Data
        lv_text_splitter = CharacterTextSplitter(
                                                    separator="\n",
                                                    chunk_size=300,
                                                    chunk_overlap=30,
                                                    length_function=len
                                                )
        lv_pdf_chunk_documents = lv_text_splitter.split_documents(lv_pdf_content)
        print("Step3: PDF content chucked and document object created")
        fn_display_user_messages("Step3: PDF content chucked and document object created", "Info", mv_processing_message)

        # -- Creating FIASS Vector Store
        lv_vector_store = FAISS.from_documents(lv_pdf_chunk_documents, lv_embeddings)
        print("Step4: Vector store created")
        fn_display_user_messages("Step4: Vector store created", "Info", mv_processing_message)
        lv_vector_store.save_local(lv_temp_file_path)

        return lv_vector_store

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
    elif mv_selected_model == 'google/gemma-2b':
        lv_download_url = "https://huggingface.co/MaziyarPanahi/gemma-2b-it-GGUF/resolve/main/gemma-2b-it.Q2_K.gguf"
    elif mv_selected_model == 'mistralai/Mistral-7B-Instruct-v0.2':
        lv_download_url = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q2_K.gguf"

    if not os.path.exists("model"):
        os.makedirs("model")
    
    lv_filename = os.path.basename(lv_download_url)
    lv_temp_file_path = os.path.join("model",lv_filename)

    if os.path.exists(lv_temp_file_path):
        print("Model already available")
        fn_display_user_messages("Model already available","Warning", mv_processing_message)
    else:
        lv_response = requests.get(lv_download_url, stream=True)
        if lv_response.status_code == 200:
            with open(lv_temp_file_path, 'wb') as f:
                for chunk in lv_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            
            print("Download completed")
            fn_display_user_messages("Model download completed","Info", mv_processing_message)
        else:
            print(f"Model download completed {response.status_code}")
            fn_display_user_messages(f"Model download completed {response.status_code}","Error", mv_processing_message)

# Function return QA Response using Vector Store
def fn_generate_QnA_response(mv_selected_model, mv_user_question, lv_vector_store, mv_processing_message):
    """Returns QA Response using Vector Store"""

    lv_model_path = ""
    lv_model_type = ""
    lv_template   = """Instruction:
                    You are an AI assistant for answering questions about the provided context.
                    You are given the following extracted parts of a long document and a question. Provide a detailed answer.
                    If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
                    =======
                    {context}
                    =======
                    Question: {question}
                    Output:\n"""
    lv_qa_prompt = PromptTemplate(
                                template=lv_template,
                                input_variables=["question", "context"]
                              )

    if mv_selected_model == 'microsoft/phi-2':
        lv_model_path = "model/phi-2.Q2_K.gguf"
        lv_model_type = "pi"
    elif mv_selected_model == 'google/gemma-2b':
        lv_model_path = "model/gemma-2b-it.Q2_K.gguf"
        lv_model_type = "gemma"
    elif mv_selected_model == 'mistralai/Mistral-7B-Instruct-v0.2':
        lv_model_path = "model/mistral-7b-instruct-v0.2.Q2_K.gguf"
        lv_model_type = "mistral"
    
    
    print("Step4: Generating LLM response")
    fn_display_user_messages("Step4: Generating LLM response","Info", mv_processing_message)

    lv_model = LlamaCpp(
                            model_path=lv_model_path,
                            temperature=0.00,
                            max_tokens=2048,
                            top_p=1,
                            verbose=False
                       )
    lv_retriever = lv_vector_store.as_retriever(search_kwargs={'k': 2})
    
    # lv_qa_chain = RetrievalQA.from_chain_type(  llm=lv_model,
    #                                             chain_type='stuff',
    #                                             retriever=lv_retriever,
    #                                             return_source_documents=True,
    #                                             chain_type_kwargs={'prompt': lv_qa_prompt}
    #                                           )

    # lv_response = lv_qa_chain({"query": mv_user_question})

    lv1=lv_retriever(mv_user_question)
    print(lv1)
    lv2=lv_qa_prompt.format(  question=mv_user_question,
                                context=lv_retriever(mv_user_question)
                           )
    print(lv2)
    print(lv_model(lv2))

    print("Step5: LLM response generated")
    fn_display_user_messages("Step5: LLM response generated","Info", mv_processing_message)

    return "hello"

# Main Function
def main():
    
    # -- Streamlit Settings
    st.set_page_config(layout='wide')
    col1, col2, col3 = st.columns(3)
    col2.title("Chat with PDF")
    st.text("")

    # -- Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -- Display Supported Models
    col1, col2, col3 = st.columns(3)
    mv_selected_model = col3.selectbox('Select Model',
                                        [
                                            'microsoft/phi-2',
                                            'google/gemma-2b',
                                            'mistralai/Mistral-7B-Instruct-v0.2'
                                        ]
                                      )
    
    # -- Display Supported Vector Stores
    col1, col2, col3 = st.columns(3)
    mv_selected_vector_db = col3.selectbox('Select Vector DB', ['FAISS'])
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

    # -- Processing PDF
    if (mv_pdf_input_file is not None):

        # -- Upload PDF
        fn_upload_pdf(mv_pdf_input_file, mv_processing_message)

        # -- Create Vector Index
        lv_vector_store = fn_create_vector_db(mv_pdf_input_file, mv_processing_message)

        # -- Perform RAG
        col1, col2, col3 = st.columns(3)
        st.text("")
        lv_chat_history = col2.chat_message
        st.text("")

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

        # -- Validate Data

        # -- Get Web Response

# Calling Main Function
if __name__ == '__main__':
    main()