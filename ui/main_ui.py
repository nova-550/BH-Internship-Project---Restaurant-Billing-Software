import streamlit as st
from utils.db_utils import insert_order, init_db
from utils.calculator import calculate_total, apply_discount
from utils.pdf_generator import generate_pdf_receipt
from utils.notify import send_notification
import time
import sqlite3
from config import RECEIPT_DIR
import os

DB_PATH = os.path.join("db", "restaurant.db")

def render_main_ui():
    """Main order processing interface with enhanced error handling"""
    # Initialize database
    init_db()
    
    st.title("🍽️ Restaurant Billing System")
    st.markdown("---")
    
    # Sample menu - in a real app this would come from a database
    menu_items = [
        {"id": 1, "name": "Paneer Butter Masala", "price": 180},
        {"id": 2, "name": "Chicken Biryani", "price": 220},
        {"id": 3, "name": "Butter Naan", "price": 40},
        {"id": 4, "name": "Veg Pulao", "price": 150},
        {"id": 5, "name": "Cold Drink", "price": 30}, 
    ]

    # Order type selection
    order_type = st.radio("Order Type:", ["Dine-in", "Takeaway"], horizontal=True, key="order_type")
    
    # Order selection UI
    st.subheader("Menu")
    order = []
    for item in menu_items:
        cols = st.columns([4, 2, 2])
        with cols[0]:
            st.write(f"**{item['name']}**")
        with cols[1]:
            qty = st.number_input(
                "Qty", 
                min_value=0, 
                max_value=20, 
                value=0,
                key=f"qty_{item['id']}"
            )
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

    # Order summary section
    with st.expander("📝 Order Summary", expanded=True):
        st.subheader("Your Order")
        for item in order:
            st.write(f"{item['name']} x {item['quantity']} - ₹{item['price'] * item['quantity']:.2f}")
        
        subtotal = calculate_total(order)
        discount = st.number_input("Discount (%)", min_value=0, max_value=100, value=0, key="discount")
        total = apply_discount(subtotal, discount)
        
        st.markdown("---")
        st.metric("Total Amount", f"₹{total:.2f}")
        
        customer_notes = st.text_area("Special Instructions:", key="customer_notes")

        if st.button("💳 Process Payment", key="process_payment"):
            try:
                with st.spinner("Processing your order..."):
                    # Store order with detailed item breakdown
                    order_id = insert_order(order, total, order_type, customer_notes)
                    time.sleep(0.5)
                    
                    # Enhanced verification
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM orders WHERE id = ?", (order_id,))
                    count = cursor.fetchone()[0]
                    conn.close()

                    if count == 0:
                        raise Exception(f"Critical: Order {order_id} missing from database!")
                    
                    # Generate PDF receipt
                    receipt_path = os.path.join("receipts", f"receipt_{order_id}.pdf")
                    generate_pdf_receipt(order, total, order_id)
                    
                    # Send notification
                    send_notification(
                        subject=f"New Order #{order_id}",
                        body=f"New {order_type} order for ₹{total:.2f}",
                        to_email="admin@example.com"
                    )
                    
                    # Show success message
                    st.success(f"Order #{order_id} processed successfully!")
                    st.balloons()
                    
                    # Offer receipt download
                    with open(receipt_path, "rb") as f:
                        st.download_button(
                            "📄 Download Receipt",
                            f,
                            file_name=f"receipt_{order_id}.pdf"
                        )
                    
                    # Reset form after delay
                    time.sleep(3)
                    st.rerun()
                    
            except sqlite3.Error as e:
                st.error(f"Database error: {str(e)}")
                st.error("Please try again or contact support")
            except Exception as e:
                st.error(f"Order failed: {str(e)}")
                st.error("Our team has been notified of this issue")

# Initialize and run the app
if __name__ == "__main__":
    render_main_ui()
