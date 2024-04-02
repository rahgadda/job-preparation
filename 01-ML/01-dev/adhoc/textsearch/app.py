import os
from dotenv import load_dotenv

import streamlit as st
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate

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

# Read book
def fn_read_book(mv_processing_message):
    """Read book"""

    lv_temp_file_path = os.path.join("book","completeworks.txt")

    try:
        with open(lv_temp_file_path, 'r') as lv_file:
            lv_file_content = lv_file.read()
            lv_file_content = lv_file_content.replace('\n', ' ').replace('\t', ' ')
            
            print(f"Step1: Completed reading file `completeworks.txt`")
            fn_display_user_messages("Step1: Completed reading file `completeworks.txt`","Info", mv_processing_message)

            return lv_file_content
            
    except FileNotFoundError:
        print(f"Step1: File '{lv_temp_file_path}' not found.")
        fn_display_user_messages(f"Step1: Error file '{lv_temp_file_path}' not found.","Error", mv_processing_message)

        return ""
    except IOError:
        print(f"Step1: Error reading file '{lv_temp_file_path}'.")
        fn_display_user_messages(f"Step1: Error reading file '{lv_temp_file_path}.","Error", mv_processing_message)

        return ""

# Return QA Response
def fn_generate_QnA_response(mv_user_question, mv_file_content, mv_processing_message):
    """Returns QA Response"""

    print("Step2: Generating LLM response")
    fn_display_user_messages("Step2: Generating LLM response","Info", mv_processing_message)

    lv_template =  """Instruction:
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
    lv_generation_config = {
                                "temperature": 0.0,
                                "top_p": 1,
                                "top_k": 1
                           }
    lv_safety_settings = [
                            {
                                "category": "HARM_CATEGORY_HARASSMENT",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_HATE_SPEECH",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                "threshold": "BLOCK_NONE"
                            },
                            {
                                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                "threshold": "BLOCK_NONE"
                            },
                        ]
    # lv_model = ChatGoogleGenerativeAI(
    #                                     model="gemini-pro",
    #                                     temperature=0.0, 
    #                                     top_p=1,
    #                                     top_k=1,
    #                                     safety_settings = safety_settings
    #                                  )

    lv_model = genai.GenerativeModel(
                                        model_name='gemini-pro',
                                        generation_config=lv_generation_config,
                                        safety_settings=lv_safety_settings
                                    )
    
    lv_qa_formatted_prompt = lv_qa_prompt.format(  
                                                    question=mv_user_question,
                                                    context=mv_file_content
                                                )
    try:
        # lv_llm_response = lv_model.invoke(lv_qa_formatted_prompt).content
        lv_llm_response = lv_model.generate_content(lv_qa_formatted_prompt).text
        print("Step3: LLM response generated")
        fn_display_user_messages("Step3: LLM response generated","Info", mv_processing_message)
    except Exception as error:
        lv_llm_response = f"Error processing request "+type(error).__name__
        print("Step3: Error generation LLM response")
        fn_display_user_messages("Step3: Error generation LLM response","Error", mv_processing_message)
        raise error

    return lv_llm_response

# Main Program
def main():
    # -- Streamlit Settings
    st.set_page_config("Chat With Your Textbook")
    st.header("Chat With Your Textbook 💁")
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

    # -- Setting Book Content
    mv_file_content = ""
    if "file_content" in st.session_state:
        mv_file_content = st.session_state["file_content"]
    else:
        mv_file_content = fn_read_book(mv_processing_message)
        st.session_state["file_content"] = mv_file_content

    # -- Creating Chat Details
    mv_user_question = st.chat_input("Pass your input here")

    # -- Recording Chat Input and Generating Response
    if mv_user_question:
        
        # -- Saving User Input
        st.session_state.messages.append({"role": "user", "content": mv_user_question})

        # -- Generating LLM Response
        # print("File "+mv_file_content)
        lv_response = fn_generate_QnA_response(mv_user_question, mv_file_content, mv_processing_message)

        # -- Saving LLM Response
        st.session_state.messages.append(
            {"role": "agent", "content": lv_response}
        )

        # -- Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Loading Main
if __name__ == "__main__":
    main()