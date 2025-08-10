import streamlit as st
import pandas as pd
from utils.db_utils import (
    get_all_orders,
    get_sales_summary,
    get_top_items,
    clear_test_data,
    export_to_csv
)
from datetime import datetime, timedelta
import plotly.express as px
from utils.email_report import send_sales_report
from config import ADMIN_PASSWORD

def password_protected():
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False
    
    if not st.session_state.admin_auth:
        password = st.text_input("Admin Password", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Incorrect password")
        return False
    return True

def render_admin_ui():
    st.title("📊 Admin Dashboard")
    
    if not password_protected():
        return
    
    # Logout button
    if st.button("Logout"):
        st.session_state.admin_auth = False
        st.rerun()
    
    # Date range selector
    col1, col2 = st.columns(2)
    today = datetime.now()
    with col1:
        start_date = st.date_input("Start Date", today - timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", today)
    
    # Data tabs
    tab1, tab2, tab3 = st.tabs(["📈 Sales Report", "🍽️ Popular Items", "🗃️ All Orders"])
    
    with tab1:
        st.subheader("Sales Summary")
        # Assuming start_date and end_date are defined somewhere in your code
        summary = get_sales_summary(start_date, end_date)
    
        # Check if the summary dictionary is empty
        if not summary:  # This checks if the summary dictionary is empty
            st.write("No sales data available for the selected date range.")
        else:
            st.write(f"Total Sales: {summary['total_sales']}")
            st.write(f"Total Orders: {summary['total_orders']}")

            
        if st.button("Email Sales Report"):
                send_sales_report(summary, start_date, end_date)
                st.success("Report sent successfully!")
        else:
            st.warning("No sales data found for selected period")
    
    with tab2:
        st.subheader("Most Popular Items")
        # Assuming start_date and end_date are defined somewhere in your code
        top_items = get_top_items(start_date, end_date)
    
        # Check if the top_items list is empty
        if not top_items:  # This checks if the list is empty
            st.write("No top items available for the selected date range.")
        else:
            for item in top_items:
                st.write(f"Item: {item[0]}, Total Sales: {item[1]}")

    
    with tab3:
        st.subheader("All Orders")
        # Assuming start_date and end_date are defined somewhere in your code
        orders = get_all_orders(start_date, end_date)
    
        # Check if the orders list is empty
        if not orders:  # This checks if the list is empty
            st.write("No orders available for the selected date range.")
        else:
            for order in orders:
                st.write(f"Order ID: {order[0]}, Items: {order[1]}, Total: {order[2]}, Created At: {order[5]}")

            
        if st.button("Export to CSV"):
            csv_path = export_to_csv(orders, "data/orders_export.csv")
            st.success(f"Exported to {csv_path}")
        else:
            st.warning("No orders found")
    
    # Admin tools
    if st.checkbox("Show Admin Tools"):
        st.warning("Danger Zone! These actions cannot be undone")
        if st.button("🔄 Reset Test Data"):
            clear_test_data()
            st.success("Test data cleared")
