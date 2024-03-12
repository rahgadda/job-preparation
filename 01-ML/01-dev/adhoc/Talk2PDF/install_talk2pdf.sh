#!/bin/bash

pip install streamlit PyPDF2 accelerate torch faiss-cpu numpy langchain_community git+https://github.com/huggingface/transformers
streamlit run ./Talk2PDF.py