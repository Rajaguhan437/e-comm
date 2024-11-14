import streamlit as st
from streamlit_option_menu import option_menu

def sideBar(key):
    with st.sidebar:
        print("___")
        app = option_menu(
            menu_title='QuickCart',
            options=['Category', 'Sub Category', 'About'],
            icons=['shop', 'bag-heart-fill', 'info-square'],
            menu_icon='fast-forward',
            default_index=1,
            key=key
        )
        print("+++")
    return app