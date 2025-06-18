"""
Core configuration settings for MatchedCover Insurance Platform.

This module handles all application configuration using Pydantic Settings
for type safety and validation.
"""

import os
from functools import lru_cache
from typing import Dict, Any


class Settings:
    """Application settings with validation."""

    def __init__(self):
        # Application settings
        self.APP_NAME = "MatchedCover"
        self.VERSION = "1.0.0"
        self.DEBUG = False
        self.HOST = "0.0.0.0"
        self.PORT = 8000
        self.LOG_LEVEL = "INFO"

        # Security settings
        self.SECRET_KEY = "your-secret-key-change-in-production"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

        # Database settings
        self.DATABASE_URL = "postgresql://mc_user:mc_password@localhost:5432/matchedcover"
        self.DATABASE_ECHO = False

        # Redis settings
        self.REDIS_URL = "redis://localhost:6379"
        self.REDIS_DB = 0

        # MongoDB settings
        self.MONGODB_URL = "mongodb://localhost:27017/matchedcover"
        
        # API settings
        self.API_PREFIX = "/api/v1"
        self.DOCS_URL = "/docs"
        self.OPENAPI_URL = "/openapi.json"
        
        # Pricing settings
        self.DEFAULT_PRICING_STRATEGY = "competitive"
        self.MIN_PREMIUM_AMOUNT = 50.0
        self.DEFAULT_COMMISSION_RATE = 0.10
        
        # Risk settings
        self.DEFAULT_RISK_THRESHOLD = 0.7
        self.HIGH_RISK_THRESHOLD = 0.85


@lru_cache()
def get_settings() -> Settings:
    """
    Create and return a cached Settings instance.
    
    Returns:
        Settings object with application configuration
    """
    return Settings()
