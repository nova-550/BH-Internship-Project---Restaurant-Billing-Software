# File: ui/main_ui.py

import streamlit as st
from utils.calculator import calculate_total
from utils.db_utils import fetch_menu_items, insert_order
from datetime import datetime
import os
from generate_pdf import generate_pdf_receipt
from utils import receipt_generator


# Sample usage
order_items = ["2x Sugar", "1x Wheat", "3x Milk"]
total_price = 395.50
order_id = "ORD12345"

pdf_path = generate_pdf_receipt(order_items, total_price, order_id)
print(f"PDF receipt saved at: {pdf_path}")

# RECEIPT_DIR = "receipts"
# os.makedirs(RECEIPT_DIR, exist_ok=True)

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
        receipt_path = generate_receipt(order, total)

        st.success("Bill generated successfully!")
        with open(receipt_path, "rb") as f:
            st.download_button("Download Receipt", f, file_name=os.path.basename(receipt_path))

    
    mode = st.toggle("🌙 Dark Mode", value=False)

    if mode:
        st.markdown("<style>body { background-color: #121212; color: white; }</style>", unsafe_allow_html=True)



# def generate_receipt(order, total):
#     now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"receipt_{now}.txt"
#     filepath = os.path.join(RECEIPT_DIR, filename)

#     with open(filepath, "w", encoding="utf-8") as f:
#         f.write("--- Restaurant Bill Receipt ---\n")
#         for item in order:
#             f.write(f"{item['name']} x {item['quantity']} = ₹{item['price'] * item['quantity']}\n")
#         f.write(f"\nTotal: ₹{total}\n")
#         f.write("Thank you for dining with us!")
#     return filepath



RECEIPT_DIR = "receipts"

def generate_receipt(order, total):
    # Ensure receipts directory exists
    os.makedirs(RECEIPT_DIR, exist_ok=True)

    # Create timestamped receipt filename
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"receipt_{timestamp}.txt"
    filepath = os.path.join(RECEIPT_DIR, filename)

    # Writing to receipt file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("╔════════════════════════════════╗\n")
        f.write("║   🍽️  Restaurant Receipt 🍽️   ║\n")
        f.write("╚════════════════════════════════╝\n\n")
        f.write(f"Date: {now.strftime('%d %B %Y')}   Time: {now.strftime('%I:%M %p')}\n")
        f.write("────────────────────────────────\n")

        for item in order:
            name = item['name']
            qty = item['quantity']
            price = item['price']
            line_total = price * qty
            f.write(f"{name:<20} x{qty:<3} ₹{line_total:.2f}\n")

        f.write("────────────────────────────────\n")
        f.write(f"Total Bill: ₹{total:.2f}\n")
        f.write("\n🙏 Thank you for dining with us!\n")
        f.write("Visit Again 🍛🍹\n")

    return filepath


order = [
    {"name": "Paneer Butter Masala", "quantity": 2, "price": 180},
    {"name": "Butter Naan", "quantity": 4, "price": 35}
]
total = sum(item["price"] * item["quantity"] for item in order)

path = generate_receipt(order, total)
print(f"Receipt saved at: {path}")


def download_receipt():
    receipt_content = "Thank you for dining with us!\nTotal: ₹500"
    st.download_button(
        label="Download Receipt",
        data=receipt_content,
        file_name="receipt.txt",
        mime="text/plain"
    )

# Call it in main UI
download_receipt()