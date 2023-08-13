#!/bin/bash

sudo apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
pip install -y opencv-python pandas numpy streamlit

streamlit run text.py