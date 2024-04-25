# Langchain

## Overview
- The term langchain originates from the amalgamation of `language` and `chain`, symbolizing the interlinked nature of linguistic elements within an AI framework.
- It is a framework designed to simplify the creation of applications using `Large Language Models (LLMs)`. 
- LangChain libraries are available in both Python and JavaScript.

## History
- Founder `Harrison Chase` was still an engineer at `Robust Intelligence` and ChatGPT hadn’t taken over the world yet.
- In `early 2022`, while attending a company hackathon, Harrison built a chatbot that could query internal data from Notion and Slack. That work would eventually lead to Notion QA, an open-source project where users could ask questions to internal Notion databases in natural language.
- Then, as the year wore on, he attended meetups in SF where the beginnings of an AI ecosystem were building. Stable Diffusion had ignited interest in image generation, and GPT-3 was starting to show promise for real-world applications.
- At these meetups, Harrison consistently saw common, duplicative abstractions that developers had to build on top of LLMs to make them useful and that pain point became the idea for LangChain, an open-source projects to simplify these abstractions.
- The project started on `October 16th 2022` with a fairly simple PR - [“add initial prompt stuff”](https://github.com/langchain-ai/langchain/pull/1).
- The timing was perfect, `On November 30th 2022`, ChatGPT came out and brought the first spike of developers to LangChain. In December, the month after ChatGPT’s launch, LangChain tripled in traction from 584 to 1,413 stars.
- In January 2023, Harrison made things official by recruiting [Ankush Gola](https://www.linkedin.com/in/ankush-gola-77255866/), a former coworker at Robust Intelligence, and incorporated the company.
- All in all, LangChain has won the hearts and minds of most AI developers.


## Modules
- `langchain-core`:
  - Base abstractions and `LangChain Expression Language - (LCEL)`.
  - It is the foundation of many of LangChain's components, and is a declarative way to compose chains.
  - It makes it easy to build complex chains from basic components, and supports out of the box functionality such as streaming, parallelism, and logging.
  - Example of basic chain, chaining  a prompt template, model & output parser
    ```bash
    pip install -qU langchain-openai
    ```
    ```python
    import getpass
    import os

    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    # Getting OpenAI model password
    os.environ["OPENAI_API_KEY"] = getpass.getpass()

    # Creating instance of OpenAI GPT-4 model
    model = ChatOpenAI(model="gpt-4")

    # Creating outputparser to display user input Response
    output_parser = StrOutputParser()

    # Creating a Prompt to get better response for user input
    prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")

    # Creating a sequential chain to connect prompt, model and output parser
    chain = prompt | model | output_parser

    # Generating response
    chain.invoke({"topic": "ice cream"})
    ```
- `langchain-community`: Third party integrations and partner packages that only rely on langchain-core.
- `langchain`: Chains, agents, and retrieval strategies that make up an application's cognitive architecture.
- `LangGraph`: A library for building robust and stateful multi-actor applications with LLMs by modeling steps as edges and nodes in a graph.
- `LangSmith`: A developer platform that lets you debug, test, evaluate, and monitor chains built on any LLM framework and seamlessly integrates with LangChain.
- `LangServe`: A library for deploying LangChain chains as REST APIs.

    ![](https://python.langchain.com/svg/langchain_stack.svg)

## Glossary
- `Chains`: It refer to sequences of calls - whether to an LLM, a tool, or a data preprocessing step. The primary supported way to do this is with `LCEL`.
- `Prompt Templates`:  Convert raw user input to better input to the LLM.
- `Agents`: In chains, a sequence of actions is hardcoded. To overcome this, agents use LLM as reasoning engine to determine which actions to take and in which order.
- `Tools:` These are interfaces that an agent, chain, or LLM can use to interact with the world. 


## Reference
- [LangChain's origin story](https://www.basedash.com/blog/langchains-origin-story)
- [Langchain - Quickstart Guide](https://python.langchain.com/docs/get_started/quickstart/)