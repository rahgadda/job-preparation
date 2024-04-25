import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Creating outputparser to display user input Response
callbacks = [StreamingStdOutCallbackHandler()]

# Creating instance of AI model
model_name="gpt-4"
chat = ChatOpenAI(
                    temperature=0.5, 
                    model=model_name,
                    callbacks=callbacks,
                    streaming=True
               )

# Creating a Prompt to get better response for user input
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")

# Creating outputparser to display user input Response
output_parser = StrOutputParser()

# Creating a sequential chain to connect prompt, model and output parser
# chain = prompt | chat |output_parser
chain = prompt | chat 

# Generating response
# print(chain.invoke({"topic": "ice cream"}))
chain.invoke({"topic": "ice cream"})