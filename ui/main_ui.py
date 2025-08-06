import streamlit as st
from utils.db_utils import insert_order
from utils.calculator import calculate_total, apply_discount
from utils.pdf_generator import generate_pdf_receipt
from utils.notify import send_notification
import time
from config import RECEIPT_DIR

def render_main_ui():
    st.title("🍽️ Restaurant Billing System")
    st.markdown("---")
    
    # Sample menu - replace with dynamic loading from DB
    menu_items = [
        {"id": 1, "name": "Paneer Butter Masala", "price": 180},
        {"id": 2, "name": "Chicken Biryani", "price": 220},
        {"id": 3, "name": "Butter Naan", "price": 40},
        {"id": 4, "name": "Veg Pulao", "price": 150},
        {"id": 5, "name": "Cold Drink", "price": 30}, 
    ]

    order_type = st.radio("Order Type:", ["Dine-in", "Takeaway"], horizontal=True)
    
    # Order selection UI
    order = []
    for item in menu_items:
        cols = st.columns([5, 2, 3])
        with cols[0]:
            st.write(f"**{item['name']}**")
        with cols[1]:
            qty = st.number_input("Qty", key=f"qty_{item['id']}_{item['name']}", min_value=0, max_value=20, value=0)  # Unique key
        with cols[2]:
            st.write(f"₹{item['price']:.2f}")
        
        if qty > 0:
            order.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "quantity": qty
            })

    if not order:
        st.info("Please select items to place an order")
        return

    # Order summary
    with st.expander("📝 Order Summary", expanded=True):
        st.subheader("Your Order")
        for item in order:
            st.write(f"{item['name']} x {item['quantity']} - ₹{item['price'] * item['quantity']:.2f}")
        
        subtotal = calculate_total(order)
        discount = st.number_input("Discount (%)", min_value=0, max_value=100, value=0)
        total = apply_discount(subtotal, discount)
        
        st.markdown("---")
        st.metric("Total Amount", f"₹{total:.2f}")
        
        customer_notes = st.text_area("Special Instructions:")

        if st.button("💳 Process Payment", key="process_payment"):
            try:
                with st.spinner("Processing your order..."):
                    # Insert order and get ID
                    order_id = insert_order(order, total, order_type, customer_notes)
                    
                    # Generate receipt
                    receipt_path = generate_pdf_receipt(order, total, discount)
                    
                    # Send notification (replace with your email)
                    send_notification(
                        subject="New Order Received",
                        body=f"Order #{order_id} has been placed successfully.",
                        to_email="admin@example.com"
                    )
                    
                    st.success(f"Order #{order_id} processed successfully!")
                    st.balloons()
                    
                    # Download receipt
                    with open(receipt_path, "rb") as f:
                        st.download_button(
                            "📄 Download Receipt",
                            f,
                            file_name=f"receipt_{order_id}.pdf"
                        )
                    
                    time.sleep(2)
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error processing order: {str(e)}")
