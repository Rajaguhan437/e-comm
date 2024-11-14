import streamlit as st
import pandas as pd
import json
from api.protectedAPI import make_authenticated_request
from web.utils import sideBar

async def app():
    st.session_state.page = 'category'
    sideBar('category')

    st.markdown("""
    <style>
    .category-card {
        border-radius: 10px;
        padding: 20px;
        margin: 30px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
        cursor: pointer;
    }
    .category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .category-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .category-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
        color: #1a1a1a;
    }
    .category-meta {
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        font-size: 0.9rem;
        color: #666;
        margin-top: 10px;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        background: #e7f7ef;
        color: #0f5132;
        font-size: 0.8rem;
    }
    .stats-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        color: black;
    }
    div.stButton > button{
        background-color: black;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        margin-left: 25%;
        border: none;
        cursor: pointer;
        width: 50%;
    }
    div.stButton > button p{
    font-size: 20px !important; 
    font-weight: bold !important; 
    text-align: center; 
    }
    div.stButton > button:hover {
        background-color: white;
        color: green; 
        transform: scale(1.1);
    }

    </style>
    """, unsafe_allow_html=True)

    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None

    st.title("Product Categories")

    with st.container():
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            st.markdown("""
            <div class="stats-container">
                <h3>Total Categories</h3>
                <h2>8</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="stats-container">
                <h3>Active Categories</h3>
                <h2>8</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="stats-container">
                <h3>Total Products</h3>
                <h2>283</h2>
            </div>
            """, unsafe_allow_html=True)


    col1, col2, col3 = st.columns([4, 2, 1], vertical_alignment='center')
    with col1:
        search = st.text_input("Search categories...", "")
    with col2:
        sort_by = st.selectbox("Sort by", ["Name", "Date Created"])
    with col3:
        if st.button("+ Add Category", key="add_cat_btn"):
            st.session_state.page = "add_category"

    response = await make_authenticated_request("category/read/", "get")

    try:
        print(response.content)
    except Exception as e:
        print(e)
    categories = json.loads(response.content)

    # Filter categories based on search
    if search:
        categories = [c for c in categories if search.lower() in c["cat_name"].lower()]

    # Sort categories
    if sort_by == "Name":
        categories.sort(key=lambda x: x["cat_name"])
    elif sort_by == "Date Created":
        categories.sort(key=lambda x: x["created_at"], reverse=True)

    # Display categories in grid
    cols = st.columns(3)
    for idx, category in enumerate(categories):
        with cols[idx % 3]:
            # Create clickable card
            card_clicked = st.container()
            with card_clicked:
                st.markdown(f"""
                <div class="category-card">
                    <div class="category-title"><h3>{category['cat_name']}</h3></div>
                    <img src="{category['cat_img']}" class="category-image" alt="{category['cat_name']}">
                    <div class="category-meta">
                        <div class="status-badge">{'Active' if category['is_active'] else 'Inactive'}</div>
                        <p>Created: {category['created_at'].split('T')[0]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)


                if st.button("View Subcategories", key=f"cat_{category['cat_id']}", use_container_width=True):
                    st.session_state.selected_category = category['cat_id']
                    # Navigate to sub_category page
                    st.session_state.page = "Sub Category"
                    st.rerun()


    # Handle navigation to subcategory page
    if st.session_state.selected_category is not None:
        st.session_state.page = "Sub Category"
        # The sub_category.app() function will handle the display of subcategories