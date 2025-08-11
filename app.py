import streamlit as st
from ui.main_ui import render_main_ui
from ui.admin_ui import render_admin_ui
from utils.db_utils import init_db, check_db_integrity
import time
from utils.db_utils import update_schema
update_schema()
   
def setup():
    st.set_page_config(
        page_title="Restaurant Billing System",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    init_db()
    check_db_integrity()

def main():
    setup()
    
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("", ["Customer Billing", "Admin Dashboard"])
    
    if menu == "Customer Billing":
        render_main_ui()
    elif menu == "Admin Dashboard":
        render_admin_ui()

if __name__ == '__main__':
    main()
