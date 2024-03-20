#!/bin/bash

pip install streamlit requests pypdf faiss-cpu llama-cpp-python sentence-transformers torch langchain langchain_community
streamlit run ./Chat2PDF.py