#!/bin/bash

pip install streamlit pypdf torch langchain_community git+https://github.com/huggingface/transformers
streamlit run ./Talk2PDF.py