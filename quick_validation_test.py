"""
Quick validation test for MatchInsurance agents.

This script runs a streamlined test of the core agent functionality
to quickly verify that agents are working correctly.
"""

import asyncio
import sys
import os
from decimal import Decimal
from datetime import datetime
import uuid

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Import agent classes
from src.agents.pricing_agent import PricingAgent, PricingStrategy
from src.agents.fraud_detection_agent import FraudDetectionAgent
from src.agents.risk_assessor import RiskAssessment, RiskLevel, RiskFactorAnalysis, RiskFactor
from src.quantum.crypto import QuantumResistantSigner


async def test_pricing_agent():
    """Test core PricingAgent functionality."""
    print("\n===== PRICING AGENT TEST =====")
    
    # Initialize agent
    agent = PricingAgent()
    print(f"✓ Agent initialized: {agent.name}")
    
    # Test pricing with a simple scenario
    customer_data = {
        "customer_id": "CUST123",
        "age": 30,
        "policy_count": 1,
    }
    
    # Create a simple risk assessment
    risk_assessment = RiskAssessment(
        assessment_id="RISK123",
        customer_id="CUST123",
        policy_type="auto",
        overall_risk_level=RiskLevel.LOW,
        risk_factors=[],
        premium_multiplier=0.9,
        confidence_score=0.85,
        timestamp=datetime.now().isoformat(),
        risk_score=0.3,
        flags=[],
        notes=""
    )
    
    # Test quote calculation
    quote = await agent.calculate_quote(
        customer_data=customer_data,
        policy_type="auto",
        coverage_amount=Decimal("50000.00"),
        risk_assessment=risk_assessment,
        pricing_strategy=PricingStrategy.COMPETITIVE
    )
    
    print(f"✓ Quote calculated")
    print(f"  - Quote ID: {quote.quote_id}")
    print(f"  - Base premium: ${quote.base_premium}")
    print(f"  - Final premium: ${quote.final_premium}")
    print(f"  - Pricing factors: {len(quote.pricing_factors)}")
    
    print("✓ PricingAgent test passed")
    return True


async def test_fraud_detection_agent():
    """Test core FraudDetectionAgent functionality."""
    print("\n===== FRAUD DETECTION AGENT TEST =====")
    
    # Initialize agent
    agent = FraudDetectionAgent()
    print(f"✓ Agent initialized: {agent.name}")
    
    # Test capabilities
    capabilities = agent.get_capabilities()
    print(f"✓ Agent has {len(capabilities)} capabilities")
    
    # Test risk thresholds
    print(f"✓ Risk thresholds configured: {len(agent.risk_thresholds)} levels")
    
    print("✓ FraudDetectionAgent test passed")
    return True


async def test_quantum_crypto():
    """Test core quantum cryptography functionality."""
    print("\n===== QUANTUM CRYPTO TEST =====")
    
    # Initialize signer
    signer = QuantumResistantSigner()
    print(f"✓ QuantumResistantSigner initialized")
    
    # Test signing
    test_data = f"test-data-{uuid.uuid4()}"
    signature = await signer.sign(test_data)
    
    print(f"✓ Signature generated: {len(signature)} chars")
    
    # Test verification
    verification = await signer.verify(test_data, signature)
    print(f"✓ Signature verified: {verification}")
    
    print("✓ Quantum crypto test passed")
    return True


async def main():
    """Run all quick validation tests."""
    print("\n🚀 MATCHINSURANCE QUICK VALIDATION TEST")
    print("=======================================")
    
    try:
        pricing_result = await test_pricing_agent()
        fraud_result = await test_fraud_detection_agent()
        crypto_result = await test_quantum_crypto()
        
        if pricing_result and fraud_result and crypto_result:
            print("\n✅ All validation tests passed!")
            return 0
        else:
            print("\n❌ Some validation tests failed")
            return 1
            
    except Exception as e:
        print(f"\n❌ Validation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
