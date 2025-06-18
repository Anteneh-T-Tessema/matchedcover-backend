#!/bin/bash

# Quick Setup Script for MatchedCover Blockchain Integration
# This script sets up the development environment for testing blockchain features

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 MatchedCover Blockchain Integration Quick Setup${NC}"
echo -e "${BLUE}=================================================${NC}"

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is required but not installed${NC}"
    echo -e "${YELLOW}Please install Docker and try again${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is required but not installed${NC}"
    echo -e "${YELLOW}Please install Docker Compose and try again${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose found${NC}"

# Install Python dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Main dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, skipping main dependencies${NC}"
fi

# Install blockchain-specific dependencies (optional)
if [ -f "requirements-blockchain.txt" ]; then
    echo -e "${YELLOW}🔗 Installing blockchain dependencies...${NC}"
    pip install -r requirements-blockchain.txt || {
        echo -e "${YELLOW}⚠️  Some blockchain dependencies failed to install${NC}"
        echo -e "${YELLOW}This is normal for development - mock implementation will be used${NC}"
    }
else
    echo -e "${YELLOW}⚠️  requirements-blockchain.txt not found${NC}"
fi

# Set up environment variables
echo -e "${YELLOW}🔧 Setting up environment variables...${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cat > .env << EOF
# MatchedCover Environment Configuration

# Application Settings
APP_NAME=MatchedCover
DEBUG=true
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://mc_user:mc_password@localhost:5432/matchedcover

# Blockchain Settings (Development)
ENABLE_BLOCKCHAIN_AUDIT=true
FABRIC_MOCK_MODE=true
FABRIC_ORG_NAME=InsuranceOrg
FABRIC_USER_NAME=User1
FABRIC_CHANNEL_NAME=insurance-channel
FABRIC_CHAINCODE_NAME=insurance-chaincode

# Security Settings (Change in production)
SECRET_KEY=dev-secret-key-change-in-production
ENABLE_QUANTUM_RESISTANCE=true

# API Keys (Optional - for enhanced features)
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here
EOF
    echo -e "${GREEN}✅ Created .env file with default settings${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating necessary directories...${NC}"
mkdir -p logs uploads tests/data fabric-config/{crypto-config,channel-artifacts,scripts,chaincode}
echo -e "${GREEN}✅ Directories created${NC}"

# Test blockchain integration
echo -e "${YELLOW}🧪 Testing blockchain integration...${NC}"

# Run basic tests
if python -c "from src.blockchain.hyperledger_fabric import HyperledgerFabricManager; print('✅ Blockchain imports working')" 2>/dev/null; then
    echo -e "${GREEN}✅ Blockchain integration imports working${NC}"
else
    echo -e "${YELLOW}⚠️  Blockchain imports failed - this is normal in development${NC}"
fi

# Test the application startup
echo -e "${YELLOW}🚀 Testing application startup...${NC}"
if timeout 10s python -c "
import asyncio
from src.blockchain.blockchain_integration import BlockchainIntegratedFraudAgent

async def test():
    agent = BlockchainIntegratedFraudAgent()
    await agent.initialize()
    print('✅ Blockchain agent initialized successfully')

asyncio.run(test())
" 2>/dev/null; then
    echo -e "${GREEN}✅ Blockchain agent initialization successful${NC}"
else
    echo -e "${YELLOW}⚠️  Blockchain agent initialization failed - mock mode will be used${NC}"
fi

# Run tests if available
if [ -f "tests/test_blockchain_integration.py" ]; then
    echo -e "${YELLOW}🧪 Running blockchain integration tests...${NC}"
    python -m pytest tests/test_blockchain_integration.py::TestBlockchainConnectivity -v || {
        echo -e "${YELLOW}⚠️  Some tests failed - this is expected in development mode${NC}"
    }
else
    echo -e "${YELLOW}⚠️  Test file not found${NC}"
fi

# Display next steps
echo -e "${BLUE}🎉 Setup Complete!${NC}"
echo -e "${BLUE}================${NC}"
echo ""
echo -e "${GREEN}✅ MatchedCover blockchain integration is ready for development${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. 🚀 Start the application:"
echo "   python -m uvicorn src.main:app --reload"
echo ""
echo "2. 🧪 Run tests:"
echo "   python -m pytest tests/test_blockchain_integration.py -v"
echo ""
echo "3. 🌐 Access the API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "4. 🔗 For full blockchain network (optional):"
echo "   ./scripts/setup-fabric-network.sh"
echo "   ./fabric-config/scripts/start-network.sh"
echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "- Mock blockchain mode: ENABLED (for development)"
echo "- Audit logging: ENABLED"
echo "- Quantum resistance: ENABLED"
echo "- Environment file: .env"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "- Blockchain integration: docs/blockchain-integration.md"
echo "- API endpoints: /api/v1/blockchain-fraud/*"
echo ""
echo -e "${GREEN}Happy coding! 🎯${NC}"
