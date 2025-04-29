import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page

# Fake database of users (In a real app, use a proper database)
USER_CREDENTIALS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "sales1": {"password": "sales123", "role": "Salesperson"},
}

# Set up session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

# Apply Custom Styling
st.markdown("""
    <style>
        /* Background Fix */
        .stApp {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
            font-family: Times New Roman', Times, serif;
            padding-top: 50px;
        }

        /* Centered Login Box */
        .login-container {
            background-color: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            margin: auto;
            text-align: center;
            animation: fadeIn 1.5s ease-in-out;
        }

        /* Login Title */
        .login-title {
            font-size: 5px;
            font-family: Times New Roman', Times, serif;        
            color: #2c5364;
            text-align: center;
            margin-bottom: 10px;
        }

        /* Input Field Styling */
        .stTextInput>div>div>input {
            border: 2px solid #2c5364 !important;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            text-align:left;
        }

        /* Custom Login Button */
        .login-button {
            background: linear-gradient(to right, #007BFF, #0056b3);
            color: white;
            font-size: 18px;
            padding: 12px;
            border-radius: 6px;
            border: none;
            width: 100%;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }

        .login-button:hover {
            background: linear-gradient(to right,#ffffff, #003c7c);
            transform: scale(1.05);
        }

        /* Footer Text */
        .footer {
            font-size: 14px;
            text-align: center;
            margin-top: 20px;
            color: light gray;
        }

        /* Animation */
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
    </style>
    """, unsafe_allow_html=True)

# Load and display the Salesforce logo (Ensure the correct file path)
logo_path = "assets/sales_force_logo.png"  # Make sure this is the correct path

# Centering the image
col1, col2, col3 = st.columns([3, 2, 3])
with col2:
    st.image(logo_path, width=150)

st.markdown(
    "<h4 style='text-align: center; font-size: 20px; margin-top: 5px;'>🚀 Sales Management Dashboard 🚀</h4>",
    unsafe_allow_html=True
)

# text input boxes
username = st.text_input("👤 Username", key="username") 
password = st.text_input("🔑 Password", type="password", key="password")

# Login Button
if st.button("🚀 Login", help="Click to log in", key="login_button", use_container_width=False):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.user_role = USER_CREDENTIALS[username]["role"]

        with st.spinner("🔄 Logging in..."):
            time.sleep(1.5)  # Adding delay for better UX

        st.success(f"✅ Welcome, {username}!")

        # Redirect user based on role
        if st.session_state.user_role == "Admin":
            switch_page("Admin_Dashboard")
        else:
            switch_page("Sales_Dashboard")

    else:
        st.error("❌ Invalid username or password. Please try again.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<p class='footer'>© 2025 Sales Force | All Rights Reserved</p>", unsafe_allow_html=True)
