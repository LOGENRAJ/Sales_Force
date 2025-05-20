import streamlit as st
import pandas as pd
import bcrypt
import time
import os
from streamlit_extras.switch_page_button import switch_page

# --- Load User Data ---
user_file = "users.csv"

if not os.path.exists(user_file):
    st.error("🚫 User database not found.")
    st.stop()

users_df = pd.read_csv(user_file)

# --- Set Up Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# --- UI Styling (Same as before) ---
st.markdown("""<style>
/* Your existing styling here */
</style>""", unsafe_allow_html=True)

# Logo and Title
logo_path = "assets/sales_force_logo.png"
col1, col2, col3 = st.columns([3, 2, 3])
with col2:
    st.image(logo_path, width=150)

st.markdown(
    "<h4 style='text-align: center; font-size: 20px; margin-top: 5px;'>🚀 WEB-BASED SALES MANAGEMENT SYSTEM 🚀</h4>",
    unsafe_allow_html=True
)

# --- Login Inputs ---
username = st.text_input("👤 Username")
password = st.text_input("🔑 Password", type="password")

# --- Login Logic ---
if st.button("🚀 Login", help="Click to log in", use_container_width=False):
    if username in users_df["Username"].values:
        user_record = users_df[users_df["Username"] == username].iloc[0]
        stored_hashed_pw = user_record["Password"]

        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_pw.encode('utf-8')):
            st.session_state.logged_in = True
            st.session_state.user_role = user_record["Role"]
            st.session_state.username = username

            with st.spinner("🔄 Logging in..."):
                time.sleep(1.5)

            st.success(f"✅ Welcome, {username}!")

            # Redirect based on role
            if st.session_state.user_role == "Admin":
                switch_page("Admin_Dashboard")
            else:
                switch_page("Sales_Dashboard")
        else:
            st.error("❌ Incorrect password. Please try again.")
    else:
        st.error("❌ Username not found.")

# --- Footer ---
st.markdown("<p class='footer'>© 2025 Sales Force | All Rights Reserved</p>", unsafe_allow_html=True)
