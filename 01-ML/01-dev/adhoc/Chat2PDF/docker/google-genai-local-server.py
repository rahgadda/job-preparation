import os

from flask import Flask, request, jsonify

import google.generativeai as genai
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain_community.document_loaders import TextLoader

app = Flask(__name__)

@app.route('/', methods=['GET'])
def api():

    # Loading Google Gemini API Key from Environment Variables
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Getting the input string from the request
    input_string = request.args.get('query')

    if input_string:
        # Variables
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
        
        lv_model = genai.GenerativeModel('gemini-pro')

        lv_file_name = "oracle-banking-common-core-user-guide-pages-5.txt"
        lv_temp_file_path = os.path.join(os.path.join("vectordb","txt"),lv_file_name)
        lv_text_loader = TextLoader(lv_temp_file_path)
        lv_pdf_formatted_content = lv_text_loader.load()
        lv_text_data = ""    
        for lv_page in lv_pdf_formatted_content:
            lv_text_data = lv_text_data + lv_page.page_content

        lv_qa_formatted_prompt = lv_qa_prompt.format(  
                                                        question=input_string,
                                                        context=lv_text_data
                                                    )

        lv_llm_response = lv_model.generate_content(lv_qa_formatted_prompt).text

        # Returning the output as JSON response
        return jsonify({'response': lv_llm_response}), 200, {'Content-Type': 'application/json'}
    else:
        # Return "Search at /generate_output" message in HTML format
        return "<h1>Add Query Parameter</h1>", 200, {'Content-Type': 'text/html'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)