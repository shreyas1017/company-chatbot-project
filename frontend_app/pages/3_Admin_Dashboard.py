# frontend_app/pages/3_Admin_Dashboard.py

import streamlit as st
from services import api_client

st.set_page_config(page_title="Admin Dashboard", layout="wide")

# --- Authentication Check ---
# Ensure the user is logged in and is an admin.
if not st.session_state.get('logged_in') or st.session_state.get('role') != 'admin':
    st.error("You are not authorized to view this page. Please login as an admin.")
    st.stop() # Stop script execution

st.title("Admin Dashboard")
st.write(f"Welcome, Admin!")

# --- Document Upload Section ---
st.subheader("Upload a New Document")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if st.button("Upload Document"):
    if uploaded_file:
        # Get the token from the session state
        token = st.session_state.get('token')
        if token:
            with st.spinner("Uploading and processing document..."):
                # Call the API client to upload the document
                response = api_client.upload_document(token, uploaded_file)
                if response:
                    st.success(f"Successfully uploaded '{uploaded_file.name}'!")
                    st.write(response)
                else:
                    st.error("Upload failed. Please check the backend logs for details.")
        else:
            st.error("Authentication token not found. Please login again.")
    else:
        st.warning("Please choose a file to upload.")

# --- Logout Button ---
if st.sidebar.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()