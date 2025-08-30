# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Database URL ---
# This is the connection string for your PostgreSQL database.
DATABASE_URL = "postgresql://postgres:sp12091017@localhost/chatbot_db"


# --- SQLAlchemy Engine ---
# The engine is the central point of communication with the database.
engine = create_engine(DATABASE_URL)


# --- Database Session ---
# A session is the primary interface for executing database queries.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Declarative Base ---
# Our ORM models will inherit from this class to be registered with SQLAlchemy.
Base = declarative_base()