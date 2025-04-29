import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# --- Access Control ---
if "logged_in" not in st.session_state or not st.session_state.logged_in or st.session_state.user_role != "Admin":
    st.error("Unauthorized Access! Please log in as Admin.")
    st.stop()

# --- Setup CSV File ---
file_path = "sales_data.csv"

# Load and validate sales data
if os.path.exists(file_path):
    sales_data = pd.read_csv(file_path)
    required_columns = ["Date & Time", "Customer Name", "Product", "Units Bought", "Revenue ($)", "Customer Email"]
    for col in required_columns:
        if col not in sales_data.columns:
            sales_data[col] = None
else:
    sales_data = pd.DataFrame(columns=["Date & Time", "Customer Name", "Product", "Units Bought", "Revenue ($)", "Customer Email"])

# Convert numeric and datetime columns
sales_data["Revenue ($)"] = pd.to_numeric(sales_data["Revenue ($)"], errors="coerce").fillna(0)
sales_data["Units Bought"] = pd.to_numeric(sales_data["Units Bought"], errors="coerce").fillna(0)
sales_data["Date & Time"] = pd.to_datetime(sales_data["Date & Time"], errors="coerce")

# --- Page Configuration ---
st.set_page_config(page_title="Admin Dashboard", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .metric-container { display: flex; justify-content: space-between; gap: 20px; margin-bottom: 20px; }
    .kpi-card { padding: 15px; border-radius: 10px; color: white; font-size: 18px; text-align: center; flex-grow: 1; }
    .green { background-color: #28a745; }
    .blue { background-color: #007bff; }
    .red { background-color: #dc3545; }
    .yellow { background-color: #ffc107; color: black; }
    .sales-history { margin-top: 20px; font-size: 18px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center;'>📊 Welcome to Admin Dashboard</h1>", unsafe_allow_html=True)

# --- KPI Metrics ---
total_sales = sales_data["Revenue ($)"].sum()
transactions = len(sales_data)
best_customer = (
    sales_data.groupby("Customer Name")["Revenue ($)"].sum().idxmax()
    if not sales_data.empty and sales_data["Revenue ($)"].sum() > 0
    else "N/A"
)
total_units_sold = sales_data["Units Bought"].sum()

# --- Display KPI Cards ---
st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='kpi-card green'>💰 Total Revenue:<br><b>RM {total_sales:.2f}</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi-card blue'>📦 Transactions:<br><b>{transactions}</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi-card red'>👤 Top Customer:<br><b>{best_customer}</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi-card yellow'>🛒 Units Sold:<br><b>{int(total_units_sold)}</b></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Sales History Table ---
st.markdown("<div class='sales-history'>📜 Sales History</div>", unsafe_allow_html=True)
st.dataframe(sales_data)

# --- Sales Charts ---
st.markdown("<h2>📊 Sales Insights</h2>", unsafe_allow_html=True)

# Total Revenue by Customer Name
if not sales_data.empty:
    st.markdown("### 👤 Total Revenue by Customer")
    customer_revenue = sales_data.groupby("Customer Name")["Revenue ($)"].sum().reset_index()
    fig = px.bar(customer_revenue, x="Revenue ($)", y="Customer Name", orientation="h",
                 color="Revenue ($)", color_continuous_scale="Viridis", title="Revenue by Customer")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig)

# Total Units Sold by Product
if not sales_data.empty:
    st.markdown("### 📦 Total Units Sold per Product")
    product_units = sales_data.groupby("Product")["Units Bought"].sum().reset_index()
    fig = px.bar(product_units, x="Units Bought", y="Product", orientation="h",
                 color="Units Bought", color_continuous_scale="Magma", title="Units Sold by Product")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig)

# Revenue Trend Over Time
if not sales_data.empty:
    st.markdown("### 📈 Revenue Trend Over Time")
    sales_trend = sales_data.groupby(sales_data["Date & Time"].dt.date)["Revenue ($)"].sum().reset_index()
    sales_trend.columns = ["Date", "Revenue ($)"]
    fig = px.line(sales_trend, x="Date", y="Revenue ($)", markers=True, title="Revenue Over Time")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig)
