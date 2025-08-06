import streamlit as st
from utils.calculator import calculate_total
from utils.db_utils import fetch_menu_items, insert_order
from datetime import datetime
import os
from generate_pdf import generate_pdf_receipt

RECEIPT_DIR = "receipts"
os.makedirs(RECEIPT_DIR, exist_ok=True)

def render_main_ui():
    st.title("🍽️ Restaurant Billing System")
    menu_items = fetch_menu_items()

    if not menu_items:
        st.warning("No menu items found. Please seed the database.")
        return

    order = []
    for item in menu_items:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{item['name']}** - ₹{item['price']}")
        with col2:
            qty = st.number_input(f"Quantity for {item['name']}", min_value=0, step=1, key=item['id'])
            if qty > 0:
                order.append({"id": item['id'], "name": item['name'], "price": item['price'], "quantity": qty})

    if st.button("✅ Generate Bill"):
        if not order:
            st.error("Please select at least one item.")
            return

        total = calculate_total(order)
        insert_order(order, total)
        receipt_path = generate_pdf_receipt(order, total)

        st.success("Bill generated successfully!")
        with open(receipt_path, "rb") as f:
            st.download_button("Download Receipt", f, file_name=os.path.basename(receipt_path))
