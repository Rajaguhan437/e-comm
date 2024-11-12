import streamlit as st
import json
from streamlit_option_menu import option_menu

from api.protectedAPI import make_authenticated_request, logout
from web.utils import sideBar


def display_category(category):
    """Displays a single category with an image, title, and button."""
    st.markdown(
        f"""
        <div style="
            padding: 50px;
            border-radius: 10px;
            # border: 1px solid #ddd;
            margin: 10px 0;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            height:400px;
            display: flex;
            justify-item: center;
        ">
            <img src="{category['cat_img']}" alt="{category['cat_name']} width="200" height="300" style="
                width: 100%; /* Adjust as needed */
                height: auto;
                display:block;
                margimgin-bottom: 10px;
                border-radius: 5px;
            ">
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(f"Browse {category['cat_name']}", key=f"btn_{category['cat_name']}", use_container_width=True,):
        st.session_state.current_category = category['cat_name']
        

def display_categories(categories):
    col1, col2, col3, col4 = st.columns(4, gap="large", vertical_alignment="center")
    columns = [col1, col2, col3, col4]
    
    for i, category in enumerate(categories):
        with columns[i % 4]:
            with st.container():
                display_category(category)

def sidebar_filters():
    app = sideBar("category")

    st.sidebar.markdown("### Quick Search")
    search_term = st.sidebar.text_input("Search categories...")

    st.sidebar.markdown("### Filters")
    price_range = st.sidebar.slider("Price Range ($)", 0, 1000, (0, 1000))
    sort_by = st.sidebar.selectbox("Sort By", ["Popularity", "Price: Low to High", "Price: High to Low", "Newest First"])

def app():
    st.header('Categories 🛍️')

    response = make_authenticated_request("category/read/", "get")
    categories =  json.loads(response.content.decode())
    sidebar_filters()
    display_categories(categories)


