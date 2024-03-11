#!/bin/bash

pip install streamlit PyPDF2 accelerate torch faiss-cpu numpy git+https://github.com/huggingface/transformers
streamlit run ./Talk2PDF.py