import streamlit as st
from streamlit_option_menu import option_menu

def initialLoad(page_title, title_details):
    st.set_page_config(page_title=page_title,layout='wide', initial_sidebar_state='auto')
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.title(title_details)

def menu(menueList, iconList):
    with st.sidebar:
        selected = option_menu(
                                menu_title=None,
                                options=menueList,
                                icons=iconList, 
                                menu_icon="cast", 
                                default_index=0
                              )
    
    return selected
