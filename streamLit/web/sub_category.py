import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
#st.set_page_config(page_title="Eyewear Catalog", layout="wide")

def app():
    # Custom CSS for styling
    st.markdown("""
    <style>
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1rem;
        padding: 1rem;
    }
    .status-badge {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-bottom: 8px;
    }
    .available {
        background-color: #e7f7ef;
        color: #0f5132;
    }
    .disabled {
        background-color: #fff3cd;
        color: #856404;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("Eyewear Product Catalog")

    # Initialize product data
    products = [
        {
            "name": "Round Selfy Black Frame",
            "lens": "White Lens",
            "price": 25.00,
            "date": "12.09.20",
            "status": "Available",
            "image": "https://placeholder.com/300x200",  # Using placeholder as we can't host real images
        },
        {
            "name": "Cat Eye Brown Frame",
            "lens": "White Lens",
            "price": 25.00,
            "date": "12.09.20",
            "status": "Available",
            "image": "https://placeholder.com/300x200",
        },
        {
            "name": "Square Gold Frame",
            "lens": "White Lens",
            "price": 25.00,
            "date": "12.09.20",
            "status": "Disabled",
            "image": "https://placeholder.com/300x200",
        },
        {
            "name": "Vintage Round Frame",
            "lens": "White Lens",
            "price": 25.00,
            "date": "12.09.20",
            "status": "Available",
            "image": "https://placeholder.com/300x200",
        },
        {
            "name": "Modern Yellow Frame",
            "lens": "White Lens",
            "price": 25.00,
            "date": "12.09.20",
            "status": "Available",
            "image": "https://placeholder.com/300x200",
        },
        {
            "name": "Classic Black Frame",
            "lens": "White Lens",
            "price": 25.00,
            "date": "12.09.20",
            "status": "Disabled",
            "image": "https://placeholder.com/300x200",
        },
        {
            "name": "Oval Black Frame",
            "lens": "White Lens",
            "price": 25.00,
            "date": "12.09.20",
            "status": "Available",
            "image": "https://placeholder.com/300x200",
        },
        {
            "name": "Half-Rim Gold Frame",
            "lens": "White Lens",
            "price": 25.00,
            "date": "12.09.20",
            "status": "Available",
            "image": "https://placeholder.com/300x200",
        }
    ]

    # Filter controls
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search = st.text_input("Search products...", "")

    with col2:
        status_filter = st.selectbox(
            "Status",
            ["All", "Available", "Disabled"],
        )

    with col3:
        sort_by = st.selectbox(
            "Sort by",
            ["Name", "Price", "Date"]
        )

    # Filter and sort products
    filtered_products = [p for p in products if search.lower() in p["name"].lower()]
    if status_filter != "All":
        filtered_products = [p for p in filtered_products if p["status"] == status_filter]

    if sort_by == "Name":
        filtered_products.sort(key=lambda x: x["name"])
    elif sort_by == "Price":
        filtered_products.sort(key=lambda x: x["price"])
    elif sort_by == "Date":
        filtered_products.sort(key=lambda x: x["date"])

    # Display products in a grid
    cols = st.columns(4)
    for idx, product in enumerate(filtered_products):
        with cols[idx % 4]:
            st.image(product["image"], use_container_width=True)
            status_class = "available" if product["status"] == "Available" else "disabled"
            st.markdown(f'<div class="status-badge {status_class}">{product["status"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**{product['name']}**")
            st.markdown(f"{product['lens']}")
            st.markdown(f"${product['price']:.2f}")
            st.markdown(f"Added: {product['date']}")

    # Display total count
    st.sidebar.markdown(f"Total Products: {len(filtered_products)}")