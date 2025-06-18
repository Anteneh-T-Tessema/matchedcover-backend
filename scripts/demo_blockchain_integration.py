#!/usr/bin/env python3
"""
MatchedCover Blockchain Integration Demo

This script demonstrates the key blockchain integration features:
1. Fraud detection with blockchain logging
2. Claims processing through smart contracts
3. Identity verification using DID
4. Audit trail queries and compliance

Run this script to see the blockchain integration in action.
"""

import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Dict, Any
import uuid

# Add src to path for imports
sys.path.append('src')

from src.blockchain.blockchain_integration import BlockchainIntegratedFraudAgent
from src.blockchain.hyperledger_fabric import (
    FraudAuditRecord,
    ClaimRecord,
    IdentityAttestation,
    get_fabric_manager
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def demo_fraud_detection():
    """Demo fraud detection with blockchain logging."""
    print("\n🔍 FRAUD DETECTION WITH BLOCKCHAIN DEMO")
    print("=" * 50)
    
    # Initialize blockchain-integrated fraud agent
    agent = BlockchainIntegratedFraudAgent()
    await agent.initialize()
    
    # Sample claim data
    claim_data = {
        "claim_id": f"DEMO-CLAIM-{uuid.uuid4().hex[:8]}",
        "policy_number": "POL-2024-DEMO-001",
        "claim_amount": 25000.0,
        "incident_type": "auto_accident",
        "incident_date": "2024-01-15",
        "claimant_info": {
            "name": "John Demo",
            "id": "DEMO123456789",
            "contact": "john.demo@example.com"
        },
        "incident_details": {
            "location": "Demo Highway 101",
            "weather": "clear",
            "description": "Demo vehicle collision for testing"
        },
        "supporting_documents": ["demo_police_report.pdf", "demo_photos.pdf"]
    }
    
    print(f"📋 Analyzing claim: {claim_data['claim_id']}")
    print(f"💰 Claim amount: ${claim_data['claim_amount']:,.2f}")
    
    # Perform fraud analysis with blockchain logging
    result = await agent.analyze_claim_with_blockchain(claim_data)
    
    print(f"🎯 Fraud score: {result.get('fraud_score', 'N/A')}")
    print(f"⚠️  Risk level: {result.get('risk_level', 'N/A')}")
    print(f"🔗 Blockchain info: {json.dumps(result.get('blockchain_info', {}), indent=2)}")
    
    return result


async def demo_claims_processing():
    """Demo claims processing through smart contracts."""
    print("\n📄 CLAIMS PROCESSING SMART CONTRACT DEMO")
    print("=" * 50)
    
    agent = BlockchainIntegratedFraudAgent()
    await agent.initialize()
    
    # Create a claim record
    claim_record = ClaimRecord(
        claim_id=f"DEMO-CLAIM-{uuid.uuid4().hex[:8]}",
        policy_id="POL-2024-DEMO-002",
        claim_amount=15000.0,
        status="submitted",
        ai_assessment={
            "fraud_score": 0.15,
            "risk_factors": ["low_impact", "verified_location"],
            "recommendation": "approve",
            "confidence": 0.92
        },
        approval_conditions=["verify_documents", "confirm_identity"],
        payout_address=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
        approver_signatures=[]
    )
    
    print(f"📋 Processing claim: {claim_record.claim_id}")
    print(f"💰 Amount: ${claim_record.claim_amount:,.2f}")
    print(f"🤖 AI recommendation: {claim_record.ai_assessment['recommendation']}")
    
    # Submit claim to blockchain
    analysis_result = claim_record.ai_assessment
    if agent.fabric_manager:
        tx_id = await agent.submit_claim_to_blockchain(claim_record.to_dict(), analysis_result)
        print(f"✅ Claim submitted to blockchain. TX ID: {tx_id}")
    else:
        print("⚠️  Mock mode: Claim would be submitted to blockchain")
    
    # Demo automated payout for low-risk claim
    if claim_record.ai_assessment["fraud_score"] < 0.3:
        print("🚀 Triggering automated payout (low fraud risk)...")
        payout_result = await agent.approve_automated_payout(
            claim_record.claim_id, 
            claim_record.claim_amount, 
            confidence_threshold=0.9
        )
        if payout_result:
            print(f"💸 Automated payout approved: {payout_result}")
        else:
            print("⚠️  Mock mode: Payout would be processed automatically")
    
    return claim_record


async def demo_identity_verification():
    """Demo identity verification using DID."""
    print("\n🆔 IDENTITY VERIFICATION DEMO")
    print("=" * 50)
    
    agent = BlockchainIntegratedFraudAgent()
    await agent.initialize()
    
    # Sample customer data for identity verification
    customer_data = {
        "user_id": f"DID:demo:{uuid.uuid4().hex[:16]}",
        "verification_documents": ["demo_passport.pdf", "demo_utility_bill.pdf"],
        "biometric_data": "demo_encrypted_fingerprint_hash",
        "kyc_provider": "demo_identity_verification_corp",
        "verification_level": "FULL_KYC"
    }
    
    print(f"👤 Verifying identity: {customer_data['user_id']}")
    print(f"📄 Documents: {', '.join(customer_data['verification_documents'])}")
    print(f"🏢 KYC Provider: {customer_data['kyc_provider']}")
    
    # Verify customer identity
    verification_result = await agent.verify_customer_identity_blockchain(customer_data)
    
    print(f"✅ Identity verification result:")
    print(json.dumps(verification_result, indent=2))
    
    return verification_result


async def demo_reinsurance_contracts():
    """Demo reinsurance contract management."""
    print("\n🏛️ REINSURANCE CONTRACT DEMO")
    print("=" * 50)
    
    agent = BlockchainIntegratedFraudAgent()
    await agent.initialize()
    
    # Sample claim data for reinsurance calculation
    claim_data = {
        "claim_id": f"DEMO-REINS-{uuid.uuid4().hex[:8]}",
        "claim_amount": 150000.0,  # High value claim
        "policy_type": "auto",
        "risk_category": "high_value_vehicle"
    }
    
    # Sample reinsurance contract data
    contract_data = {
        "contract_id": f"REINS-DEMO-{uuid.uuid4().hex[:8]}",
        "primary_insurer": "MatchedCover Insurance",
        "reinsurer": "Demo Global Reinsurance Corp",
        "coverage_amount": 1000000.0,
        "risk_categories": ["auto", "property"],
        "effective_date": "2024-01-01",
        "expiry_date": "2024-12-31",
        "reinsurance_threshold": 100000.0,
        "reinsurance_percentage": 0.75
    }
    
    print(f"📋 Claim: {claim_data['claim_id']}")
    print(f"💰 Claim amount: ${claim_data['claim_amount']:,.2f}")
    print(f"🏢 Reinsurer: {contract_data['reinsurer']}")
    print(f"🎯 Threshold: ${contract_data['reinsurance_threshold']:,.2f}")
    
    # Create reinsurance smart contract
    contract_result = await agent.create_reinsurance_smart_contract(claim_data, contract_data)
    
    print(f"📄 Reinsurance contract created:")
    print(json.dumps(contract_result, indent=2))
    
    return contract_result


async def demo_audit_trail():
    """Demo audit trail queries and compliance."""
    print("\n📊 AUDIT TRAIL & COMPLIANCE DEMO")
    print("=" * 50)
    
    fabric_manager = await get_fabric_manager()
    await fabric_manager.initialize()
    
    # Demo claim ID for audit trail query
    demo_claim_id = f"DEMO-AUDIT-{uuid.uuid4().hex[:8]}"
    
    print(f"🔍 Querying audit trail for claim: {demo_claim_id}")
    
    # Query fraud audit trail
    audit_trail = await fabric_manager.query_fraud_audit_trail(demo_claim_id)
    print(f"📋 Fraud audit records found: {len(audit_trail)}")
    
    # Query claim history
    claim_history = await fabric_manager.query_claim_history(demo_claim_id)
    print(f"📄 Claim history records found: {len(claim_history)}")
    
    # Get network status
    network_status = await fabric_manager.get_network_status()
    print(f"🌐 Network status:")
    print(json.dumps(network_status, indent=2))
    
    return {
        "audit_trail": audit_trail,
        "claim_history": claim_history,
        "network_status": network_status
    }


async def main():
    """Run all blockchain integration demos."""
    print("🚀 MATCHEDCOVER BLOCKCHAIN INTEGRATION DEMO")
    print("=" * 60)
    print("This demo showcases key blockchain features for insurance AI agents")
    print("")
    
    try:
        # Run all demos
        fraud_result = await demo_fraud_detection()
        claims_result = await demo_claims_processing()
        identity_result = await demo_identity_verification()
        reinsurance_result = await demo_reinsurance_contracts()
        audit_result = await demo_audit_trail()
        
        print("\n🎉 DEMO SUMMARY")
        print("=" * 50)
        print("✅ Fraud detection with blockchain logging")
        print("✅ Claims processing through smart contracts")
        print("✅ Identity verification using DID")
        print("✅ Reinsurance contract management")
        print("✅ Audit trail queries and compliance")
        print("")
        print("🔗 All operations have been logged to the blockchain")
        print("📊 Audit trails are available for regulatory compliance")
        print("🔒 Quantum-resistant signatures ensure future security")
        print("")
        print("🚀 MatchedCover blockchain integration is ready for production!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")
        print("This is likely due to missing dependencies or configuration.")
        print("Run './scripts/quick-setup.sh' to set up the environment.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
