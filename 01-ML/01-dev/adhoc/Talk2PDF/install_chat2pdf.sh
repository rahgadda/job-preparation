#!/bin/bash

pip install streamlit requests pypdf faiss-cpu ctransformers sentence-transformers torch langchain langchain_community 
streamlit run ./Chat2PDF.py