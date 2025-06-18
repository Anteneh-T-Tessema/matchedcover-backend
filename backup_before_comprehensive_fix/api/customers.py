""""
Customer API endpoints for MatchedCover Insurance Platform.

This module handles customer management operations.
""""

from typing import Dict, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.api.auth import get_current_user

router = APIRouter()


class CustomerResponse(BaseModel):
    """Customer response schema."""

    id: str
customer_number: str
first_name: str
last_name: str
email: str
phone: Optional[str]
status: str
risk_category: str
customer_since: str


@router.get("/")
async def list_customers(
    page: int = 1,
limit: int = 50,
current_user: Dict = Depends(get_current_user),
):
    """Get list of customers."""
# Mock response
customers = [
    {
        "id": "cust-123",
        "customer_number": "C123456",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@email.com",
        "phone": "+1234567890",
        "status": "active",
        "risk_category": "medium",
        "customer_since": "2024-01-01T00:00:00Z",
    }
]

    return {
    "customers": customers,
    "total": len(customers),
    "page": page,
    "limit": limit,
}


@router.get("/{customer_id}")
async def get_customer(
    customer_id: str, current_user: Dict = Depends(get_current_user)
):
    """Get customer details."""
# Mock response
return {
    "id": customer_id,
    "customer_number": "C123456",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "phone": "+1234567890",
    "status": "active",
    "risk_category": "medium",
    "customer_since": "2024-01-01T00:00:00Z",
    "policies": 2,
    "claims": 1,
    "total_premium": 2500.00,
}
