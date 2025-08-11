import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from utils.db_utils import (
    init_db,
    get_all_orders,
    get_sales_summary,
    export_to_csv,
    clear_test_data
)
from utils.email_report import send_sales_report
from config import ADMIN_PASSWORD
import os

DB_PATH = os.path.join("db", "restaurant.db")

def password_protected():
    """Password protection for admin dashboard"""
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False
    
    if not st.session_state.admin_auth:
        st.title("Admin Login")
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Incorrect password")
        return False
    return True

def render_admin_ui():
    """Main admin dashboard with enhanced reporting"""
    if not password_protected():
        return
    
    st.title("📊 Restaurant Admin Dashboard")
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.admin_auth = False
        st.rerun()
    
    # Date range selector
    st.sidebar.header("Filters")
    today = datetime.now().date()
    default_start = today - timedelta(days=7)
    
    start_date = st.sidebar.date_input("Start Date", default_start)
    end_date = st.sidebar.date_input("End Date", today)
    
    if start_date > end_date:
        st.sidebar.error("End date must be after start date")
        return
    
    # Quick filter buttons
    st.sidebar.subheader("Quick Filters")
    cols = st.sidebar.columns(2)
    with cols[0]:
        if st.button("Today"):
            start_date = today
            end_date = today
    with cols[1]:
        if st.button("This Week"):
            start_date = today - timedelta(days=today.weekday())
            end_date = today
    
    # Main dashboard tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🍽️ Orders", "⚙️ Admin Tools"])
    
    with tab1:
        # Sales Summary
        summary = get_sales_summary(start_date, end_date)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"₹{summary['total_sales']:.2f}")
        col2.metric("Total Orders", summary['total_orders'])
        col3.metric("Avg. Order", f"₹{summary['avg_order']:.2f}")
        
        # Sales Trends Chart
        st.subheader("Sales Trends")
        try:
            conn = sqlite3.connect(DB_PATH)
            trend_data = pd.read_sql(f"""
                SELECT date(created_at) as day, 
                       SUM(total) as sales,
                       COUNT(*) as orders
                FROM orders
                WHERE date(created_at) BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY day
                ORDER BY day
            """, conn)
            
            if not trend_data.empty:
                fig = px.line(trend_data, x='day', y='sales', 
                             title="Daily Sales Trend",
                             labels={'day': 'Date', 'sales': 'Total Sales'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No sales data for selected period")
        except Exception as e:
            st.error(f"Error loading trends: {str(e)}")
        
        # Email report section
        if st.button("📩 Generate Sales Report"):
            try:
                send_sales_report(summary, start_date, end_date)
                st.success("Sales report emailed successfully!")
            except Exception as e:
                st.error(f"Failed to send report: {str(e)}")
    
    with tab2:
        # Order listing
        st.subheader("Recent Orders")
        orders = get_all_orders(start_date, end_date)
        
        if not orders:
            st.info("No orders found for selected period")
        else:
            # Convert to DataFrame for better display
            df = pd.DataFrame(orders, columns=[
                "ID", "Items", "Total", "Type", "Notes", "Created At", "Status"
            ])
            st.dataframe(df)
            
            # Export button
            if st.button("Export to CSV"):
                try:
                    export_to_csv(orders, "orders_export.csv")
                    st.success("Orders exported to orders_export.csv")
                except Exception as e:
                    st.error(f"Export failed: {str(e)}")
    
    with tab3:
        st.warning("Administrative Actions")
        
        # Database management
        if st.checkbox("Show Database Tools"):
            if st.button("🔄 Initialize/Reset Database"):
                init_db()
                st.success("Database initialized/reset")
            
            if st.button("🧹 Clear Test Data"):
                clear_test_data()
                st.success("Test data cleared")
            
            if st.button("📊 Refresh Statistics"):
                st.rerun()
