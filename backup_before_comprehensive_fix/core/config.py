""""
Core configuration settings for MatchedCover Insurance Platform.

This module handles all application configuration using Pydantic Settings
for type safety and validation.
""""

import os
from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(
    env_file=".env", env_ignore_empty=True, extra="ignore"
)

    # Application settings
APP_NAME: str = Field(default="MatchedCover")
VERSION: str = Field(default="1.0.0")
DEBUG: bool = Field(default=False)
HOST: str = Field(default="0.0.0.0")
PORT: int = Field(default=8000)
LOG_LEVEL: str = Field(default="INFO")

    # Security settings
SECRET_KEY: str = Field(
    default="your-secret-key-change-in-production",
    description="Secret key for JWT token generation",
)
ALGORITHM: str = Field(default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    # Database settings
DATABASE_URL: str = Field(
    default="postgresql://mc_user:mc_password@localhost:5432/matchedcover"
)
DATABASE_ECHO: bool = Field(default=False)

    # Redis settings
REDIS_URL: str = Field(default="redis://localhost:6379")
REDIS_DB: int = Field(default=0)

    # MongoDB settings
MONGODB_URL: str = Field(default="mongodb://localhost:27017/matchedcover")

    # Vector database settings
CHROMADB_HOST: str = Field(default="localhost")
CHROMADB_PORT: int = Field(default=8001)
QDRANT_URL: str = Field(default="http://localhost:6333")

    # AI API Keys
OPENAI_API_KEY: Optional[str] = Field(default=None)
ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
GOOGLE_API_KEY: Optional[str] = Field(default=None)

    # Blockchain settings
ETHEREUM_RPC_URL: Optional[str] = Field(default=None)
PRIVATE_KEY: Optional[str] = Field(default=None)
CONTRACT_ADDRESS: Optional[str] = Field(default=None)

    # External APIs
WEATHER_API_KEY: Optional[str] = Field(default=None)
GEOLOCATION_API_KEY: Optional[str] = Field(default=None)

    # File upload settings
UPLOAD_DIRECTORY: str = Field(default="./uploads")
MAX_FILE_SIZE: int = Field(default=10485760)  # 10MB

    # Fraud detection settings
FRAUD_DETECTION_THRESHOLD: float = Field(default=0.7)
ANOMALY_DETECTION_SENSITIVITY: float = Field(default=0.8)

    # Rate limiting
RATE_LIMIT_PER_MINUTE: int = Field(default=100)
RATE_LIMIT_BURST: int = Field(default=20)

    # CORS settings
ALLOWED_HOSTS: List[str] = Field(
    default=["localhost", "127.0.0.1", "0.0.0.0"]
)

    # Email settings
SMTP_HOST: Optional[str] = Field(default=None)
SMTP_PORT: int = Field(default=587)
SMTP_USERNAME: Optional[str] = Field(default=None)
SMTP_PASSWORD: Optional[str] = Field(default=None)

    # Webhook URLs
SLACK_WEBHOOK_URL: Optional[str] = Field(default=None)
DISCORD_WEBHOOK_URL: Optional[str] = Field(default=None)

    # Monitoring
PROMETHEUS_PORT: int = Field(default=9090)
GRAFANA_PORT: int = Field(default=3001)

    # Blockchain Configuration
BLOCKCHAIN_NETWORK: str = Field(default="testnet")
ETHEREUM_MAINNET_URL: str = Field(
    default="https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
)
ETHEREUM_TESTNET_URL: str = Field(
    default="https://goerli.infura.io/v3/YOUR_PROJECT_ID"
)
POLYGON_RPC_URL: str = Field(default="https://polygon-rpc.com")
SMART_CONTRACT_ADDRESS: str = Field(
    default="0x1234567890abcdef1234567890abcdef12345678"
)

    # Quantum Resistance Configuration
QUANTUM_ALGORITHM: str = Field(default="dilithium3")
QUANTUM_KEY_ROTATION_DAYS: int = Field(default=90)

    # Audit Trail Configuration
AUDIT_BLOCK_SIZE: int = Field(default=100)
AUTO_SETTLEMENT_THRESHOLD: float = Field(default=0.85)  # 85% AI confidence

    # Advanced Security
ENABLE_QUANTUM_RESISTANCE: bool = Field(default=True)
ENABLE_BLOCKCHAIN_AUDIT: bool = Field(default=True)
ENABLE_ZERO_KNOWLEDGE_PROOFS: bool = Field(default=False)

    # Hyperledger Fabric Configuration
FABRIC_ORG_NAME: str = Field(default="InsuranceOrg")
FABRIC_USER_NAME: str = Field(default="User1")
FABRIC_ORDERER_URL: str = Field(default="grpcs://localhost:7050")
FABRIC_PEER_URL: str = Field(default="grpcs://localhost:7051")
FABRIC_CA_URL: str = Field(default="https://localhost:7054")
FABRIC_TLS_CERT: str = Field(default="")  # TLS certificate PEM
FABRIC_USER_CERT: str = Field(default="")  # User certificate PEM
FABRIC_USER_KEY: str = Field(default="")  # User private key PEM
FABRIC_CHANNEL_NAME: str = Field(default="insurance-channel")
FABRIC_CHAINCODE_NAME: str = Field(default="insurance-chaincode")

    @property
def database_url_sync(self) -> str:
        """Get synchronous database URL for SQLAlchemy."""
    db_url = str(self.DATABASE_URL)
    if db_url.startswith("sqlite"):
            return db_url
    return db_url.replace("postgresql://", "postgresql+psycopg2://")

    @property
def database_url_async(self) -> str:
        """Get asynchronous database URL for SQLAlchemy."""
    db_url = str(self.DATABASE_URL)
    if db_url.startswith("sqlite"):
            return db_url.replace("sqlite://", "sqlite+aiosqlite://")
    return db_url.replace("postgresql://", "postgresql+asyncpg://")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
return Settings()


# Global settings instance
settings = get_settings()


# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
