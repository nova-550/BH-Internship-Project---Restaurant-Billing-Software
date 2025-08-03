# File: app.py

import streamlit as st
from ui.main_ui import render_main_ui
from utils.db_utils import init_db

st.set_page_config(page_title="Restaurant Billing System")
# st.set_page_config(page_title="Restaurant Billing System", layout="wide")

# Initialize DB
def initialize():
    init_db()

# Run the UI
def main():
    initialize()
    render_main_ui()

if __name__ == '__main__':
    main()