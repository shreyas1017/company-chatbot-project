# frontend_app/app.py

import streamlit as st

st.set_page_config(page_title="Welcome", layout="centered")

# --- Authentication Check ---
# If the user is already logged in, redirect them to their respective dashboard.
if st.session_state.get('logged_in'):
    if st.session_state.get('role') == 'admin':
        st.switch_page("pages/3_Admin_Dashboard.py")
    elif st.session_state.get('role') == 'user':
        st.switch_page("pages/4_User_Chat.py")

# --- UI for non-logged-in users ---
st.title("Welcome to the Company Chatbot Portal")
st.write("Please log in or sign up to continue.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login", use_container_width=True):
        st.switch_page("pages/1_Login.py")

with col2:
    if st.button("Signup", use_container_width=True):
        st.switch_page("pages/2_Signup.py")