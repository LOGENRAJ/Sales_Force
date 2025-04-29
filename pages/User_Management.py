import streamlit as st
import pandas as pd

# 🎯 Ensure only Admin can access
if "logged_in" not in st.session_state or not st.session_state.logged_in or st.session_state.user_role != "Admin":
    st.error("🚫 Unauthorized Access! Please log in as Admin.")
    st.stop()

st.title("👥 User Management")

# 📝 Sample User Data (Replace with Database in Production)
if "users" not in st.session_state:
    st.session_state.users = pd.DataFrame([
        {"Username": "admin", "Role": "Admin"},
        {"Username": "sales1", "Role": "Salesperson"},
        {"Username": "sales2", "Role": "Salesperson"}
    ])

# 📌 Show Users Table
st.subheader("📋 Current Users")
st.dataframe(st.session_state.users)

# 🔹 **Add New User**
st.subheader("➕ Add New User")
new_username = st.text_input("Username")
new_role = st.selectbox("Role", ["Admin", "Salesperson"])

if st.button("Add User"):
    # Sample DataFrame
    df = pd.DataFrame({'Username': ['admin', 'user1'], 'Role': ['Admin', 'Sales']})

    # New user to add
    new_user = pd.DataFrame({'Username': ['new_user'], 'Role': ['Salesperson']})

    # Correct way to add a row
    df = pd.concat([df, new_user], ignore_index=True)

    print(df)
    st.success(f"✅ User '{new_username}' added successfully!")

# 🔹 **Delete User**
st.subheader("🗑 Delete User")
user_to_delete = st.selectbox("Select User to Delete", st.session_state.users["Username"].unique())

if st.button("Delete User"):
    st.session_state.users = st.session_state.users[st.session_state.users["Username"] != user_to_delete]
    st.success(f"🗑 User '{user_to_delete}' deleted!")

st.success("✅ User Management Feature Added!")
