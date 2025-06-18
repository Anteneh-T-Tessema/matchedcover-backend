""""
User and authentication models for MatchedCover.

This module defines the database models for users, authentication,
and role-based access control.
""""

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
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from src.core.database import Base


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
AGENT = "agent"
CUSTOMER = "customer"
UNDERWRITER = "underwriter"
CLAIMS_ADJUSTER = "claims_adjuster"
COMPLIANCE_OFFICER = "compliance_officer"


class UserStatus(str, Enum):
    """User status enumeration."""

    ACTIVE = "active"
INACTIVE = "inactive"
SUSPENDED = "suspended"
PENDING_VERIFICATION = "pending_verification"


class User(Base):
    """User model for authentication and basic information."""

    __tablename__ = "users"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)
email = Column(String(255), unique=True, index=True, nullable=False)
username = Column(String(100), unique=True, index=True, nullable=True)
hashed_password = Column(String(255), nullable=False)

    # Profile information
first_name = Column(String(100), nullable=True)
last_name = Column(String(100), nullable=True)
phone_number = Column(String(20), nullable=True)

    # Role and permissions
role = Column(String(50), default=UserRole.CUSTOMER, nullable=False)
status = Column(
    String(50), default=UserStatus.PENDING_VERIFICATION, nullable=False
)
is_verified = Column(Boolean, default=False, nullable=False)
is_active = Column(Boolean, default=True, nullable=False)

    # Metadata
metadata_json = Column(JSONB, nullable=True)
preferences = Column(JSONB, nullable=True)

    # Timestamps
created_at = Column(DateTime(timezone=True), server_default=func.now())
updated_at = Column(DateTime(timezone=True), onupdate=func.now())
last_login = Column(DateTime(timezone=True), nullable=True)
email_verified_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
customer_profile = relationship(
    "Customer", back_populates="user", uselist=False
)
audit_logs = relationship("AuditLog", back_populates="user")

    @property
def full_name(self) -> Optional[str]:
        """Get user's full name."""
    if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
    return None

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class UserSession(Base):
    """User session model for tracking active sessions."""

    __tablename__ = "user_sessions"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)
user_id = Column(
    UUID(as_uuid=True),
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)
session_token = Column(
    String(255), unique=True, nullable=False, index=True
)
refresh_token = Column(String(255), unique=True, nullable=True, index=True)

    # Session metadata
ip_address = Column(String(45), nullable=True)  # IPv6 compatible
user_agent = Column(Text, nullable=True)
device_fingerprint = Column(String(255), nullable=True)
location = Column(JSONB, nullable=True)

    # Session control
is_active = Column(Boolean, default=True, nullable=False)
expires_at = Column(DateTime(timezone=True), nullable=False)

    # Timestamps
created_at = Column(DateTime(timezone=True), server_default=func.now())
last_activity = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
user = relationship("User")

    def __repr__(self) -> str:
        return f"<UserSession(id={self.id}, user_id={self.user_id})>"


class Permission(Base):
    """Permission model for fine-grained access control."""

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
name = Column(String(100), unique=True, nullable=False, index=True)
description = Column(Text, nullable=True)
# e.g., "policies", "claims"
resource = Column(String(100), nullable=False)
# e.g., "read", "write", "delete"
action = Column(String(50), nullable=False)

    # Timestamps
created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Permission("
        name={self.name},
        resource={self.resource},
        action={self.action}
    )>""


class RolePermission(Base):
    """Many-to-many relationship between roles and permissions."""

    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
role = Column(String(50), nullable=False, index=True)
permission_id = Column(
    Integer,
    ForeignKey("permissions.id", ondelete="CASCADE"),
    nullable=False,
)

    # Timestamps
created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
permission = relationship("Permission")

    def __repr__(self) -> str:
        return f"<RolePermission("
        role={self.role},
        permission_id={self.permission_id}
    )>""


class AuditLog(Base):
    """Audit log model for tracking user actions."""

    __tablename__ = "audit_logs"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)
user_id = Column(
    UUID(as_uuid=True),
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True,
    index=True,
)

    # Action details
action = Column(String(100), nullable=False, index=True)
resource_type = Column(String(50), nullable=False, index=True)
resource_id = Column(String(255), nullable=True, index=True)

    # Request details
ip_address = Column(String(45), nullable=True)
user_agent = Column(Text, nullable=True)
request_id = Column(String(255), nullable=True, index=True)

    # Additional context
details = Column(JSONB, nullable=True)
success = Column(Boolean, nullable=False, default=True)
error_message = Column(Text, nullable=True)

    # Timestamps
created_at = Column(
    DateTime(timezone=True), server_default=func.now(), index=True
)

    # Relationships
user = relationship("User", back_populates="audit_logs")

    def __repr__(self) -> str:
        return f"<AuditLog("
        id={self.id},
        action={self.action},
        user_id={self.user_id}
    )>""
