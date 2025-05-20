import streamlit as st
import pandas as pd
import os
import bcrypt

# 🔐 Add this block immediately after imports
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🚫 Please log in to access this page.")
    st.stop()

if st.session_state.user_role != "Admin":
    st.error("🚫 Access denied. Admins only.")
    st.stop()

# --- File Setup ---
user_file = "users.csv"

# Load existing users
if os.path.exists(user_file):
    users_df = pd.read_csv(user_file)
else:
    users_df = pd.DataFrame(columns=["Username", "Password", "Role"])

st.set_page_config(page_title="User Management", layout="centered")
st.title("👥 User Management")

# --- Section: Add New User ---
st.subheader("➕ Add New User")

with st.form("add_user_form", clear_on_submit=True):
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_role = st.selectbox("Role", ["Salesperson", "Admin"])
    submitted = st.form_submit_button("Add User")

    if submitted:
        if not new_username or not new_password:
            st.error("⚠️ Username and password cannot be empty.")
        elif len(new_password) < 5:
            st.warning("🔐 Password must be at least 5 characters long.")
        elif new_username in users_df["Username"].values:
            st.warning("⚠️ Username already exists. Please choose a different name.")
        else:
            # --- Hash the password using bcrypt ---
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            new_user = pd.DataFrame({
                "Username": [new_username],
                "Password": [hashed_password],
                "Role": [new_role]
            })
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv(user_file, index=False)
            st.success(f"✅ User '{new_username}' added successfully!")

# --- Section: User List (Hide hashed passwords for security) ---
st.subheader("📋 Current Users")
if users_df.empty:
    st.info("No users found.")
else:
    st.dataframe(users_df.drop(columns=["Password"]).sort_values(by="Role").reset_index(drop=True), use_container_width=True)

# --- Section: Delete User ---
st.subheader("❌ Delete User")
delete_username = st.selectbox("Select user to delete", users_df["Username"].unique() if not users_df.empty else [])

if st.button("Delete Selected User"):
    if delete_username:
        users_df = users_df[users_df["Username"] != delete_username]
        users_df.to_csv(user_file, index=False)
        st.success(f"🗑️ User '{delete_username}' deleted successfully!")
        st.experimental_rerun()
    else:
        st.warning("⚠️ No user selected to delete.")
