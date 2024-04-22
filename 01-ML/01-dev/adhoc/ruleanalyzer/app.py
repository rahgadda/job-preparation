import os
from dotenv import load_dotenv

import streamlit as st
import phoenix as px
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import phoenix as px
from phoenix.trace.langchain import LangChainInstrumentor

# Starting Arize Phoenix
session = px.launch_app()
LangChainInstrumentor().instrument()
# session.url

# Loading Google Gemini API Key from Environment Variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
lv_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest",
                                  temperature=1, 
                                  top_p=0.95
                                 )

# Main Program
def main():
    
    # -- Streamlit Settings
    st.set_page_config("Rule Analyzer")
    st.header("Rule Analyzer 💁")
    st.text("")
    st.text("")
    st.text("")

# Loading Main
if __name__ == "__main__":
    main()