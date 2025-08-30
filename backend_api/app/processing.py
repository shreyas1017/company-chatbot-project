# app/processing.py

import os
import cohere
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)
db_client = chromadb.PersistentClient(path="chroma_db")
collection = db_client.get_or_create_collection(name="company_documents")

# The function now accepts 'filename'
def process_and_store_document(file_path: str, filename: str, company_id: int, document_id: int):
    """
    Reads a document, chunks it, creates embeddings, and stores them in ChromaDB.
    """
    print(f"Starting processing for document_id: {document_id}, filename: {filename}")

    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            print(f"No text extracted from document_id: {document_id}")
            return

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        print(f"Document split into {len(chunks)} chunks.")

        response = co.embed(
            texts=chunks, model="embed-english-v3.0", input_type="search_document"
        )
        embeddings = response.embeddings
        print("Embeddings created successfully.")

        ids = [f"{document_id}_{i}" for i in range(len(chunks))]
        # We now add a unique 'chunk_id' to the metadata for each chunk
        metadatas = [{
            "company_id": company_id,
            "document_id": document_id,
            "filename": filename,
            "chunk_id": f"{document_id}_{i}", # This is the new unique ID
            "text_chunk": chunk
        } for i, chunk in enumerate(chunks)] # Use enumerate to get the index 'i'

        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
        print(f"Embeddings stored in ChromaDB for document_id: {document_id}")

    except Exception as e:
        print(f"An error occurred during processing for document_id {document_id}: {e}")
    finally:
        os.remove(file_path)
        print(f"Removed temporary file: {file_path}")