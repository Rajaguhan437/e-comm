import streamlit as st
import asyncio

if 'page_config_set' not in st.session_state:
    st.set_page_config(page_title="E-Commerce", layout="wide")
    st.session_state.page_config_set = True

from streamlit_option_menu import option_menu
from web import about, category, sub_category, login
from web.utils import sideBar


def hide_menu_style():
    return """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stBaseButton-headerNoPadding"] {
            display: none;
        }
        </style>
    """

def show_menu_style():
    return """
        <style>
        [data-testid="stSidebar"] {
            display: block;
        }
        </style>
    """

class MultiWeb:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

async def run():

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        #st.markdown(hide_menu_style(), unsafe_allow_html=True)
        login.app()
    else:
        #st.markdown(show_menu_style(), unsafe_allow_html=True)  

        app = sideBar("main")

        if app == 'Category':
            category.app()
        elif app == 'Sub Category':
            sub_category.app()
        elif app == 'About':
            about.app()
        
asyncio.run(run())