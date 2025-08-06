import streamlit as st
from ui.main_ui import render_main_ui
from ui.admin_ui import render_admin_ui
from utils.db_utils import init_db

st.set_page_config(page_title="Restaurant Billing System")

# Initialize DB
def initialize():
    init_db()

# Run the UI
def main():
    initialize()
    menu = st.sidebar.radio("Navigate", ["Main", "Admin"])
    if menu == "Main":
        render_main_ui()
    elif menu == "Admin":
        render_admin_ui()

if __name__ == '__main__':
    main()
