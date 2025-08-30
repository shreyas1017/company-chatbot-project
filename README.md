# Company Document Chatbot

This project is a secure, multi-tenant RAG (Retrieval-Augmented Generation) application. It allows companies to upload their internal documents and enables their users to ask questions and receive context-aware, cited answers from an AI chatbot.

## ✨ Key Features

* **Secure Multi-Tenancy**: Data for each company is completely isolated.
* **Role-Based Access Control**:
    * **Admins**: Can upload and manage company documents.
    * **Users**: Can interact with the chatbot to query their company's documents.
* **AI-Powered RAG Pipeline**: Uses Cohere's state-of-the-art models for accurate document embedding and response generation.
* **Source Citation**: The chatbot cites the specific documents used to generate an answer, ensuring verifiability.
* **Decoupled Architecture**: A robust FastAPI backend API serves a modern Streamlit frontend.

---
## 🛠️ Technology Stack

* **Backend**: Python, FastAPI, Uvicorn
* **Databases**:
    * **PostgreSQL**: For storing user, company, and document metadata.
    * **ChromaDB**: For vector storage and semantic search.
* **AI**: Cohere API (Embed & Chat models)
* **Frontend**: Streamlit
* **Authentication**: JWT (JSON Web Tokens) with Passlib for password hashing.
* **Libraries**: SQLAlchemy, Pydantic, Requests

---
## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* PostgreSQL
* A Cohere API Key

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR GITHUB USERNAME]/[YOUR REPOSITORY NAME].git
    cd [YOUR REPOSITORY NAME]
    ```

2.  **Backend Setup:**
    * Navigate to the backend directory: `cd backend_api`
    * Create and activate a virtual environment:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * Install dependencies: `pip install -r requirements.txt`
    * Create a `.env` file and add your `DATABASE_URL` and `COHERE_API_KEY`.
    * Run the server: `uvicorn app.main:app --reload`

3.  **Frontend Setup:**
    * Open a new terminal and navigate to the frontend directory: `cd frontend_app`
    * Create and activate a virtual environment:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * Install dependencies: `pip install -r requirements.txt`
    * Create a `.env` file and add `BACKEND_URL="http://127.0.0.1:8000"`.
    * Run the application: `streamlit run app.py`
