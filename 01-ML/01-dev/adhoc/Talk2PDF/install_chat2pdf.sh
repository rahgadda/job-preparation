#!/bin/bash

export COMMANDLINE_ARGS="--skip-torch-cuda-test --no-half"
pip install streamlit pypdf accelerate torch faiss-cpu numpy langchain_community sentence-transformers langchain git+https://github.com/huggingface/transformers
streamlit run ./Chat2PDF.py