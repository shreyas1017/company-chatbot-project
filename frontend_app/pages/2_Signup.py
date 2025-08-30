# frontend_app/pages/2_Signup.py

import streamlit as st
from services import api_client

# Set the page title
st.set_page_config(page_title="Signup", layout="centered")

st.markdown("<h2 style='text-align:center;'>Create an Account</h2>", unsafe_allow_html=True)

# --- Signup Form ---
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
role = st.selectbox("Register as", ["admin", "user"]) # Matches backend roles

# Fetch company list from the API
companies = api_client.get_companies()
if companies:
    # Create a mapping of company names to their IDs
    company_options = {comp['name']: comp['id'] for comp in companies}
    selected_company_name = st.selectbox("Select your company", options=company_options.keys())
    company_id = company_options[selected_company_name]
else:
    st.error("Could not load company list from the server.")
    company_id = None # Prevent signup if no companies are loaded


if st.button("Signup"):
    if not (email and password and confirm_password and company_id):
        st.error("Please fill all fields.")
    elif password != confirm_password:
        st.error("Passwords do not match.")
    else:
        # Call the API client to attempt registration
        response_data = api_client.register_user(email, password, role, company_id)
        
        if response_data:
            st.success("User registered successfully! Please proceed to login.")
            st.switch_page("pages/1_Login.py")
        else:
            # The api_client will print the detailed error to the console
            st.error("Registration failed. The email may already be registered or the company ID may not exist.")