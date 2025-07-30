import streamlit as st
import sqlite3
import pandas as pd
import os

# Connect to DB
def connect_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'restaurant.db')
    db_path = os.path.abspath(db_path)
    return sqlite3.connect(db_path)

# Fetch menu from DB
def fetch_menu():
    conn = connect_db()
    query = "SELECT item_id, name, category, price FROM menu"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Streamlit UI
def main():
    st.set_page_config(page_title="Restaurant Billing System", layout="wide")
    st.title("🍽️ Restaurant Billing System")
    st.markdown("##### Welcome, please select an order mode to begin")

    # Order Mode Selector
    order_mode = st.radio("Choose Order Mode:", ["Dine-in", "Takeaway"], horizontal=True)

    st.divider()

    # Display Menu
    st.subheader("📋 Available Menu Items")

    menu_df = fetch_menu()

    if menu_df.empty:
        st.warning("⚠️ No menu items found. Please upload a menu file.")
    else:
        grouped = menu_df.groupby("category")
        for category, items in grouped:
            st.markdown(f"#### 🍴 {category}")
            st.dataframe(items[['name', 'price']], use_container_width=True)

if __name__ == "__main__":
    main()
