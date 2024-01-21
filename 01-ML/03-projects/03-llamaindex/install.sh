#!/bin/bash

# Create Virutal Python Environment
sudo pip install virtualenv
python -m venv 01_basic_shakesearch_venv
source 01_basic_shakesearch_venv/bin/activate

# Download text file
# cd docs
# wget https://raw.githubusercontent.com/rahgadda/shakesearch/master/books/completeworks.txt
# cd ..

# Moving artifacts
cp shakesearch.py 01_basic_shakesearch_venv/
cp requirements.txt 01_basic_shakesearch_venv/

# Running Code
cd 01_basic_shakesearch_venv 
pip install -r requirements.txt
streamlit run shakesearch.py

# Logout of Virutal Python Environment
cd ..
source 01_basic_shakesearch_venv/bin/deactivate