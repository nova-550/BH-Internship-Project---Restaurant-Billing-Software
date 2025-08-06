import streamlit as st
import pandas as pd
from db.database import get_all_bills  # Corrected import

def render_admin_ui():
    st.title("🍽️ Admin Portal")
    st.subheader("📜 Full Billing Records")
    
    records = get_all_bills()
    if records:
        df = pd.DataFrame(records, columns=["ID", "Items", "Total", "Timestamp"])
        st.write(df)
        st.download_button("Download Sales CSV", df.to_csv(index=False), "sales_report.csv")
    else:
        st.warning("No billing records found.")
