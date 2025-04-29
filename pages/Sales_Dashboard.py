import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set Streamlit page configuration
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .main { background-color: #F5F5F5; }
        .stButton>button { border-radius: 10px; padding: 10px 20px; font-size: 16px; }
        .css-1d391kg { background-color: #000000 !important; }
        .stDataFrame { border-radius: 10px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in or st.session_state.user_role != "Salesperson":
    st.error("Unauthorized Access! Please log in as Salesperson.")
    st.stop()

# Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.rerun()

# 🎉 Main Dashboard
st.title("📊 Sales Dashboard")


# Logout button
st.sidebar.button("🚪 Logout", on_click=logout)

# Excel file for sales data
EXCEL_FILE = "sales_data.xlsx"

# Load sales data from Excel
def load_sales_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=["Date & Time", "Customer Name", "Product", "Units Bought", "Revenue ($)", "Customer Email"])

# Save new sale to Excel
def save_sales_data(new_sale):
    sales_data.to_csv("sales_data.csv", index=False)
    updated_data = pd.concat([sales_data, new_sale], ignore_index=True)
    updated_data.to_excel(EXCEL_FILE, index=False)

# Initialize sales data
sales_data = load_sales_data()

# 📌 Tabs for Sales History & New Sale
tab1, tab2 = st.tabs(["📋 Sales History", "📝 Add New Sale"])

# 📋 Sales History Tab
with tab1:
    st.subheader("📋 Sales Records")
    st.dataframe(sales_data.style.set_table_styles([{'selector': 'th', 'props': [('font-size', '18px')]}]))

# 📝 Add New Sale Tab (Only for Salesperson/Admin)
with tab2:
    if st.session_state.user_role == "Admin" or st.session_state.user_role == "Salesperson":
        st.subheader("📝 Add New Sale")
        with st.form("sales_form"):
            col1, col2 = st.columns(2)

            # Date & Time Auto-filled
            date_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
            col1.text_input("📅 Date & Time", date_time, disabled=True)

            # Customer Details
            customer_name = col1.text_input("👤 Customer Name")
            customer_email = col1.text_input("📧 Customer Email")

            # Product Details
            product = col2.text_input("📦 Product Name")
            units_bought = col2.number_input("🛒 Units Bought", min_value=1, step=1)
            revenue = col2.number_input("💰 Revenue ($)", min_value=1, step=100)

            submitted = st.form_submit_button("➕ Add Sale")

            if submitted:


                if customer_name and customer_email and product and units_bought and revenue:
                    new_sale = pd.DataFrame([[date_time, customer_name, product, units_bought, revenue, customer_email]],
                                            columns=["Date & Time", "Customer Name", "Product", "Units Bought", "Revenue ($)", "Customer Email"])
                    save_sales_data(new_sale)
                    st.success(f"✅ New sale added for {customer_name} - {product} ({units_bought} units) - ${revenue}")
                    st.rerun()  # Refresh the page to update sales history
                else:
                    st.error("❌ Please fill in all fields before submitting!")
    else:
        st.warning("⚠️ Only Salespersons and Admins can add new sales!")
