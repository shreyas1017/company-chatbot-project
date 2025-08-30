# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas, security

def get_user_by_email_and_company(db: Session, email: str, company_id: int):
    """Fetches a user from the database by their email and company ID."""
    return db.query(models.User).filter(
        models.User.email == email,
        models.User.company_id == company_id
    ).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Creates a new user in the database."""
    # Hash the password before storing it
    hashed_password = security.hash_password(user.password)
    
    # Create a new User model instance
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        company_id=user.company_id
    )
    
    # Add to the session and commit to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user