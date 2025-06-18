"""
API router definitions for MatchedCover Insurance Platform.

This module defines all the API routers that are imported by the main
application."""

from .auth import router as auth_router
from .customers import router as customers_router
from .policies import router as policies_router
from .claims import router as claims_router
from .agents import router as agents_router
from .analytics import router as analytics_router
from .blockchain import router as blockchain_router
from .enhanced_fraud_detection import router as enhanced_fraud_router

__all__ = [
"auth_router",
"customers_router",
"policies_router",
"claims_router",
"agents_router",
"analytics_router",
"blockchain_router",
"enhanced_fraud_router",
]
