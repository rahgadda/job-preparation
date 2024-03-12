#!/bin/bash

pip install streamlit PyPDF2 accelerate torch faiss-cpu numpy langchain_community langchain git+https://github.com/huggingface/transformers
streamlit run ./Chat2PDF.py