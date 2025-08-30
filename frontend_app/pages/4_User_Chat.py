# frontend_app/pages/4_User_Chat.py

import streamlit as st
from services import api_client

st.set_page_config(page_title="Chatbot", layout="wide")

# --- Authentication Check ---
# Ensure the user is logged in and is a regular user.
if not st.session_state.get('logged_in') or (st.session_state.get('role') != 'user' and st.session_state.get('role') != 'admin'):
    st.error("You are not authorized to view this page. Please login as a user.")
    st.stop()

st.title("Company Chatbot")
st.write("Ask any questions about your company's documents.")

# --- Chat History Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Prior Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and Processing ---
if prompt := st.chat_input("What is your question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            token = st.session_state.get('token')
            if token:
                # Call the backend API to get the chatbot's response
                response_data = api_client.query_chatbot(token, prompt)
                if response_data and 'answer' in response_data:
                    assistant_response = response_data['answer']
                    # Use st.markdown to correctly render the formatted response
                    st.markdown(assistant_response)
                else:
                    assistant_response = "Sorry, I couldn't get a response. Please try again."
                    st.error(assistant_response)
            else:
                assistant_response = "Authentication error. Please login again."
                st.error(assistant_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# --- Logout Button ---
if st.sidebar.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()