# frontend_app/services/api_client.py

import os
import requests
from dotenv import load_dotenv

# Load the backend URL from the .env file
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")

def login_user(email, password, company_id):
    """Sends login request to the backend API."""
    payload = {"email": email, "password": password, "company_id": company_id}
    try:
        response = requests.post(f"{BACKEND_URL}/auth/login", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        return None

def register_user(email, password, role, company_id):
    """Sends signup request to the backend API."""
    payload = {
        "email": email,
        "password": password,
        "role": role,
        "company_id": company_id
    }
    try:
        response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Registration failed: {e}")
        return None

def upload_document(token: str, file):
    """Sends document upload request to the backend API."""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    files = {
        "file": (file.name, file, file.type)
    }
    try:
        response = requests.post(f"{BACKEND_URL}/documents/upload", headers=headers, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Upload failed: {e}")
        return None

def query_chatbot(token: str, query: str):
    """Sends a chat query to the backend API."""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "query": query
    }
    try:
        response = requests.post(f"{BACKEND_URL}/chat/query", headers=headers, json=payload)
        response.raise_for_status()
        return response.json() # Returns {'answer': '...'}
    except requests.exceptions.RequestException as e:
        print(f"Query failed: {e}")
        return None
    
def get_companies():
    """Fetches the list of all companies from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/companies/")
        response.raise_for_status()
        return response.json() # Returns a list of company objects
    except requests.exceptions.RequestException as e:
        print(f"Failed to get companies: {e}")
        return []