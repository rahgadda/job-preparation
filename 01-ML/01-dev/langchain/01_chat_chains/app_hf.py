import os

from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Getting HuggingFace Token
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

# Creating outputparser to display user input Response
callbacks = [StreamingStdOutCallbackHandler()]

# Creating instance of AI model
# -- "microsoft/Phi-3-mini-4k-instruct", "mistralai/Mistral-7B-Instruct-v0.2"
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
model = HuggingFaceEndpoint(
                                repo_id=repo_id, 
                                temperature=0.5, 
                                huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
                                callbacks=callbacks,
                                streaming=True
                           )

# Creating a Prompt to get better response for user input
prompt = ChatPromptTemplate.from_template("tell me a long joke about {topic}")


# Creating a sequential chain to connect prompt, model and output parser
chain = prompt | model 

# Generating response
chain.invoke({"topic": "ice cream"})