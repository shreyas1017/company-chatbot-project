# app/models.py

import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class StatusEnum(str, enum.Enum):
    processing = "processing"
    ready = "ready"
    error = "error"

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    users = relationship("User", back_populates="company")
    documents = relationship("Document", back_populates="company")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False) 
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")
    
    # This line adds a rule that the COMBINATION of email and company_id must be unique
    __table_args__ = (UniqueConstraint('email', 'company_id', name='_email_company_uc'),)

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.processing)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="documents")