import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
target_url = "https://6006-rahgadda-knowledgebase-t3jcysjtsmd.ws-us110.gitpod.io/"
response = requests.get( target_url)
components.iframe(target_url,height=800, width=1500)