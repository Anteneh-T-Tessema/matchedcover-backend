""""
Logging configuration for MatchedCover.

This module sets up structured logging with JSON format for better
monitoring and debugging capabilities.
""""

import logging
import logging.config
import sys
from typing import Any, Dict

import structlog

from src.core.config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""

    # Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="ISO"),
        (
            structlog.dev.ConsoleRenderer()
            if settings.DEBUG
                else structlog.processors.JSONRenderer()
        ),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        logging.getLevelName(settings.LOG_LEVEL)
    ),
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

    # Configure standard logging
logging_config: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
        "console": {
            "format": "%(asctime)s - "
                %(name)s - %(levelname)s - %(message)s""
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console" if settings.DEBUG else "json",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "logs/matchedcover.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

    # Create logs directory
import os

    os.makedirs("logs", exist_ok=True)

    # Apply logging configuration
logging.config.dictConfig(logging_config)

    # Set up structured logger
logger = structlog.get_logger()
logger.info(
    "Logging configured",
    log_level=settings.LOG_LEVEL,
    debug_mode=settings.DEBUG,
)
