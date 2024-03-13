#!/bin/bash

pip install streamlit pypdf bitsandbytes loralib accelerate torch faiss-cpu numpy langchain_community sentence-transformers langchain git+https://github.com/huggingface/transformers
streamlit run ./Chat2PDF.py