"""
Database configuration and initialization for MatchedCover.

This module handles database connections, table creation, and provides
both sync and async database sessions."""

import logging
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import (
AsyncSession,
async_sessionmaker,
create_async_engine,
)
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from src.core.config import settings

logger = logging.getLogger(__name__)

# Create declarative base for ORM models
Base = declarative_base()

# Metadata for table creation
metadata = MetaData()

# Create sync engine
sync_engine = create_engine(
settings.database_url_sync,
echo=settings.DATABASE_ECHO,
pool_pre_ping=True,
pool_recycle=300,
)

# Create async engine
async_engine = create_async_engine(
settings.database_url_async,
echo=settings.DATABASE_ECHO,
pool_pre_ping=True,
pool_recycle=300,
)

# Create session factories
SyncSessionLocal = sessionmaker(
autocommit=False, autoflush=False, bind=sync_engine
)

AsyncSessionLocal = async_sessionmaker(
async_engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db() -> None:
    """Initialize database tables."""
try:
        # Import all models to ensure they are registered with SQLAlchemy
    from src.models import (  # noqa: F401
        user_models,
        customer_models,
        policy_models,
        claim_models,
        agent_models,
    )

        # Create all tables
    async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Database tables created successfully")

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    raise


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
async with AsyncSessionLocal() as session:
        try:
            yield session
    except Exception:
            await session.rollback()
        raise
    finally:
            await session.close()


def get_sync_session() -> Generator[Session, None, None]:
    """Get sync database session."""
session = SyncSessionLocal()
try:
        yield session
except Exception:
        session.rollback()
    raise
finally:
        session.close()


async def check_db_connection() -> bool:
    """Check if database connection is working."""
try:
        async with async_engine.begin() as conn:
            await conn.execute("SELECT 1")
    return True
except Exception as e:
        logger.error(f"Database connection failed: {e}")
    return False
