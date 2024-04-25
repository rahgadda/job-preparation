import os

from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Creating outputparser to display user input Response
callbacks = [StreamingStdOutCallbackHandler()]

# Creating instance of AI model
model_name="gemini-1.5-pro-preview-0409"
chat = ChatVertexAI(
                        temperature=0.5, 
                        model=model_name,
                        callbacks=callbacks,
                        streaming=True
                   )

# Creating a Prompt to get better response for user input
prompt = ChatPromptTemplate.from_template("tell me a long joke about {topic}")

# Creating a sequential chain to connect prompt, model and output parser
chain = prompt | chat 

# Generating response
print(chain.invoke({"topic": "ice cream"}).content)