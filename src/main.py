"""
MatchedCover - Main Application Entry Point

This module initializes and runs the main FastAPI application that orchestrates
all AI agents and handles API requests for the insurance platform."""

import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from src.api import (
auth_router,
claims_router,
customers_router,
policies_router,
agents_router,
analytics_router,
enhanced_fraud_router,
)
from src.core.config import settings
from src.core.database import init_db
from src.core.logging_config import setup_logging
from src.core.redis_client import init_redis
from src.agents.orchestrator import AgentOrchestrator
from src.services.monitoring import MetricsService


# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan management."""
logger.info("Starting MatchedCover...")

    try:
        # Initialize database
    await init_db()
    logger.info("Database initialized successfully")

        # Initialize Redis
    await init_redis()
    logger.info("Redis initialized successfully")

        # Initialize agent orchestrator
    app.state.orchestrator = AgentOrchestrator()
    await app.state.orchestrator.initialize()
    logger.info("Agent orchestrator initialized successfully")

        # Initialize monitoring
    app.state.metrics = MetricsService()
    logger.info("Monitoring services initialized successfully")

        logger.info("🚀 MatchedCover started successfully!")

        yield

    except Exception as e:
        logger.error(f"Failed to start application: {e}")
    sys.exit(1)

    finally:
        # Cleanup
    logger.info("Shutting down MatchedCover...")
    if hasattr(app.state, "orchestrator"):
            await app.state.orchestrator.shutdown()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
title="MatchedCover",
description="A fully AI agent-based insurance system",
version="1.0.0",
docs_url="/docs",
redoc_url="/redoc",
lifespan=lifespan,
)

# Add middleware
app.add_middleware(
CORSMiddleware,
allow_origins=settings.ALLOWED_HOSTS,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
return JSONResponse(
    status_code=exc.status_code,
    content={"message": exc.detail, "status_code": exc.status_code},
)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
logger.error(f"Unhandled exception: {exc}", exc_info=True)
return JSONResponse(
    status_code=500,
    content={"message": "Internal server error", "status_code": 500},
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
return {"status": "healthy", "service": "MatchedCover", "version": "1.0.0"}


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
return {
    "message": "Welcome to MatchedCover",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "health_url": "/health",
}


# Include API routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(
customers_router, prefix="/api/v1/customers", tags=["Customers"]
)
app.include_router(
policies_router, prefix="/api/v1/policies", tags=["Policies"]
)
app.include_router(claims_router, prefix="/api/v1/claims", tags=["Claims"])
app.include_router(agents_router, prefix="/api/v1/agents", tags=["AI Agents"])
app.include_router(
analytics_router, prefix="/api/v1/analytics", tags=["Analytics"]
)
app.include_router(
enhanced_fraud_router,
prefix="/api/v1/fraud-detection",
tags=["Enhanced Fraud Detection"],
)


if __name__ == "__main__":
    # Run the application
uvicorn.run(
    "src.main:app",
    host=settings.HOST,
    port=settings.PORT,
    reload=settings.DEBUG,
    log_level=settings.LOG_LEVEL.lower(),
    access_log=True,
)
