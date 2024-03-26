import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Loading Google Gemini API Key from Environment Variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Main Program
def main():
    st.set_page_config("Chat With Your Product User Manual")
    st.header("Chat With Your Product User Manual💁")


# Loading Main
if __name__ == "__main__":
    main()