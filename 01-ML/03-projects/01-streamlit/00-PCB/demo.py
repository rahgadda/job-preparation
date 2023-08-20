import streamlit as st
from streamlit_option_menu import option_menu

# -- Page Settings
st.set_page_config(page_title='Telangana Pollution Control Board',layout='wide', initial_sidebar_state='auto')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title("Welcome to PCB Command Center!!!")

# -- Main Menu
with st.sidebar:
    selected = option_menu("Main Menu", ["Dashboard",'Transactions','Setup'], 
        icons=['speedometer','activity', 'gear'], menu_icon="cast", default_index=1)
    selected