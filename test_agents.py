"""
Test script for pricing_agent.py and fraud_detection_agent.py

This script tests basic instantiation and method access for our agent classes.
"""

import asyncio
import sys
from decimal import Decimal

# Add the current directory to the Python path
sys.path.insert(0, '.')

# Import our agent classes
from src.agents.pricing_agent import PricingAgent, PricingStrategy
from src.agents.fraud_detection_agent import FraudDetectionAgent

async def test_pricing_agent():
    """Test basic PricingAgent functionality."""
    print("Testing PricingAgent...")
    
    # Create an instance
    agent = PricingAgent()
    
    # Test method access (don't need to fully execute)
    print(f"Agent name: {agent.name}")
    print(f"Agent type: {agent.agent_type}")
    
    # Test enum access
    print(f"Available pricing strategies: {[strategy.value for strategy in PricingStrategy]}")
    
    print("PricingAgent tests completed successfully!")
    
async def test_fraud_detection_agent():
    """Test basic FraudDetectionAgent functionality."""
    print("\nTesting FraudDetectionAgent...")
    
    # Create an instance
    agent = FraudDetectionAgent()
    
    # Test method access
    print(f"Agent name: {agent.name}")
    print(f"Agent type: {agent.agent_type}")
    
    # Test capabilities method
    print(f"Capabilities: {agent.get_capabilities()}")
    
    print("FraudDetectionAgent tests completed successfully!")

async def main():
    """Run all tests."""
    print("Starting agent tests...\n")
    
    await test_pricing_agent()
    await test_fraud_detection_agent()
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
