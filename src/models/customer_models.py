"""
Customer models for MatchedCover.

This module defines the database models for customer information,
profiles, and related data."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
Column,
Integer,
String,
DateTime,
Boolean,
Text,
ForeignKey,
Float,
Date,
Numeric,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from src.core.database import Base


class CustomerStatus(str, Enum):
    """Customer status enumeration."""

    ACTIVE = "active"
INACTIVE = "inactive"
SUSPENDED = "suspended"
DECEASED = "deceased"


class CustomerType(str, Enum):
    """Customer type enumeration."""

    INDIVIDUAL = "individual"
BUSINESS = "business"
FAMILY = "family"


class RiskCategory(str, Enum):
    """Risk category enumeration."""

    LOW = "low"
MEDIUM = "medium"
HIGH = "high"
VERY_HIGH = "very_high"


class Customer(Base):
    """Customer model containing detailed customer information."""

    __tablename__ = "customers"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)
user_id = Column(
    UUID(as_uuid=True),
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    unique=True,
    index=True,
)
customer_number = Column(
    String(50), unique=True, nullable=False, index=True
)

    # Personal information
title = Column(String(10), nullable=True)  # Mr., Mrs., Dr., etc.
first_name = Column(String(100), nullable=False)
middle_name = Column(String(100), nullable=True)
last_name = Column(String(100), nullable=False)
maiden_name = Column(String(100), nullable=True)

    # Demographics
date_of_birth = Column(Date, nullable=True)
gender = Column(String(20), nullable=True)
nationality = Column(String(100), nullable=True)
marital_status = Column(String(50), nullable=True)
occupation = Column(String(200), nullable=True)
education_level = Column(String(100), nullable=True)

    # Contact information
primary_email = Column(String(255), nullable=False, index=True)
secondary_email = Column(String(255), nullable=True)
primary_phone = Column(String(20), nullable=True)
secondary_phone = Column(String(20), nullable=True)
preferred_contact_method = Column(
    String(50), default="email", nullable=False
)

    # Address information
addresses = Column(JSONB, nullable=True)  # Array of address objects

    # Business information (for business customers)
business_name = Column(String(255), nullable=True)
business_type = Column(String(100), nullable=True)
tax_id = Column(String(50), nullable=True)
industry = Column(String(100), nullable=True)
annual_revenue = Column(Numeric(15, 2), nullable=True)
employee_count = Column(Integer, nullable=True)

    # Customer classification
customer_type = Column(
    String(50), default=CustomerType.INDIVIDUAL, nullable=False
)
status = Column(String(50), default=CustomerStatus.ACTIVE, nullable=False)
risk_category = Column(
    String(50), default=RiskCategory.MEDIUM, nullable=False
)

    # Financial information
credit_score = Column(Integer, nullable=True)
annual_income = Column(Numeric(15, 2), nullable=True)
net_worth = Column(Numeric(15, 2), nullable=True)

    # Preferences and settings
communication_preferences = Column(JSONB, nullable=True)
document_preferences = Column(JSONB, nullable=True)
privacy_settings = Column(JSONB, nullable=True)

    # AI and analytics data
behavioral_data = Column(JSONB, nullable=True)
preferences_learned = Column(JSONB, nullable=True)
risk_factors = Column(JSONB, nullable=True)

    # Timestamps
customer_since = Column(DateTime(timezone=True), server_default=func.now())
created_at = Column(DateTime(timezone=True), server_default=func.now())
updated_at = Column(DateTime(timezone=True), onupdate=func.now())
last_activity = Column(DateTime(timezone=True), nullable=True)

    # Relationships
user = relationship("User", back_populates="customer_profile")
policies = relationship("Policy", back_populates="customer")
claims = relationship("Claim", back_populates="customer")
documents = relationship("CustomerDocument", back_populates="customer")
interactions = relationship(
    "CustomerInteraction", back_populates="customer"
)

    @property
def full_name(self) -> str:
        """Get customer's full name."""
    parts = [self.title, self.first_name, self.middle_name, self.last_name]
    return " ".join(filter(None, parts))

    @property
def age(self) -> Optional[int]:
        """Calculate customer's age from date of birth."""
    if self.date_of_birth:
            today = datetime.now().date()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
    return None

    def __repr__(self) -> str:
        return f"<Customer("
        id={self.id},
        name={self.full_name},
        number={self.customer_number}
    )>""


class CustomerDocument(Base):
    """Customer document model for storing uploaded documents."""

    __tablename__ = "customer_documents"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)
customer_id = Column(
    UUID(as_uuid=True),
    ForeignKey("customers.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)

    # Document information
document_type = Column(String(100), nullable=False, index=True)
document_name = Column(String(255), nullable=False)
file_path = Column(String(500), nullable=False)
file_size = Column(Integer, nullable=False)
mime_type = Column(String(100), nullable=False)

    # Document metadata
description = Column(Text, nullable=True)
tags = Column(JSONB, nullable=True)
extracted_data = Column(JSONB, nullable=True)  # OCR/AI extracted data

    # Status and validation
is_verified = Column(Boolean, default=False, nullable=False)
verification_status = Column(String(50), default="pending", nullable=False)
verified_by = Column(String(255), nullable=True)
verification_notes = Column(Text, nullable=True)

    # Security
is_encrypted = Column(Boolean, default=True, nullable=False)
access_level = Column(String(50), default="private", nullable=False)

    # Timestamps
uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
verified_at = Column(DateTime(timezone=True), nullable=True)
expires_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
customer = relationship("Customer", back_populates="documents")

    def __repr__(self) -> str:
        return f"<CustomerDocument("
        id={self.id},
        type={self.document_type},
        name={self.document_name}
    )>""


class CustomerInteraction(Base):
    """Customer interaction model for tracking all customer touchpoints."""

    __tablename__ = "customer_interactions"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)
customer_id = Column(
    UUID(as_uuid=True),
    ForeignKey("customers.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)

    # Interaction details
interaction_type = Column(String(100), nullable=False, index=True)
# web, mobile, phone, email, chat
channel = Column(String(50), nullable=False)
direction = Column(String(20), nullable=False)  # inbound, outbound

    # Content
subject = Column(String(255), nullable=True)
summary = Column(Text, nullable=True)
content = Column(Text, nullable=True)

    # AI analysis
sentiment_score = Column(Float, nullable=True)
intent = Column(String(100), nullable=True)
resolution_status = Column(String(50), default="pending", nullable=False)

    # Agent information
handled_by_agent = Column(String(100), nullable=True)  # AI agent name
escalated_to_human = Column(Boolean, default=False, nullable=False)
human_agent_id = Column(String(255), nullable=True)

    # Metadata
metadata_json = Column(JSONB, nullable=True)
attachments = Column(JSONB, nullable=True)

    # Timestamps
started_at = Column(DateTime(timezone=True), server_default=func.now())
ended_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
customer = relationship("Customer", back_populates="interactions")

    def __repr__(self) -> str:
        return f"<CustomerInteraction("
        id={self.id},
        type={self.interaction_type},
        customer_id={self.customer_id}
    )>""
