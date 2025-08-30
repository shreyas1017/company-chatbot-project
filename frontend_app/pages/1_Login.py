# frontend_app/pages/1_Login.py

import streamlit as st
from services import api_client
import jwt

st.set_page_config(page_title="Login", layout="centered")
st.markdown("<h2 style='text-align:center;'>Login</h2>", unsafe_allow_html=True)

# --- Step 1: Select Company ---
companies = api_client.get_companies()
if companies:
    company_options = {comp['name']: comp['id'] for comp in companies}
    selected_company_name = st.selectbox("Select your company", options=company_options.keys())
    selected_company_id = company_options[selected_company_name]

    # --- Step 2: Enter Credentials ---
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password and selected_company_id:
            response_data = api_client.login_user(email, password, selected_company_id)

            if response_data:
                token = response_data.get('access_token')
                st.session_state['logged_in'] = True
                st.session_state['token'] = token

                user_info = jwt.decode(token, options={"verify_signature": False})
                st.session_state['role'] = user_info.get('role')

                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials for the selected company.")
        else:
            st.warning("Please enter all details.")
else:
    st.error("Could not load company list. Please ensure the backend is running.")

# --- Post-Login Logic ---
if st.session_state.get('logged_in'):
    st.write("You are logged in.")
    if st.session_state.get('role') == 'admin':
        st.switch_page("pages/3_Admin_Dashboard.py")
    else:
        st.switch_page("pages/4_User_Chat.py")