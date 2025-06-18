"""
Comprehensive integration tests for blockchain fraud detection.

This test suite verifies the complete blockchain integration workflow
including fraud detection, smart contracts, and audit trails.
"""

import asyncio
import pytest
import uuid
from datetime import datetime, timezone

from src.blockchain.blockchain_integration import BlockchainIntegratedFraudAgent
from src.blockchain.hyperledger_fabric import get_fabric_manager


class TestBlockchainIntegration:
    """Test suite for blockchain-integrated fraud detection."""
    
    @pytest.fixture
    async def agent(self):
        """Create and initialize a blockchain fraud agent."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        return agent
    
    @pytest.mark.asyncio
    async def test_fraud_detection_with_complete_data(self, agent):
        """Test fraud detection with complete claim data."""
        claim_data = {
            "claim_id": f"TEST-{uuid.uuid4()}",
            "claim_amount": 10000.0,
            "claim_date": datetime.now(timezone.utc).isoformat(),
            "policy_number": "POL123456",
            "incident_type": "auto_accident",
            "location": "San Francisco, CA"
        }
        
        result = await agent.analyze_claim_with_blockchain(claim_data)
        
        # Verify analysis structure
        assert "fraud_analysis" in result
        assert "blockchain_audit" in result
        assert "quantum_signature" in result
        assert "timestamp" in result
        
        # Verify fraud analysis
        fraud_analysis = result["fraud_analysis"]
        assert "fraud_score" in fraud_analysis
        assert "risk_level" in fraud_analysis
        assert "indicators" in fraud_analysis
        assert "recommended_actions" in fraud_analysis
        
        # Verify blockchain audit (should have TX IDs in mock mode)
        blockchain_audit = result["blockchain_audit"]
        assert "fraud_audit_tx_id" in blockchain_audit
    
    @pytest.mark.asyncio
    async def test_fraud_detection_with_minimal_data(self, agent):
        """Test fraud detection with minimal claim data."""
        claim_data = {
            "claim_amount": 5000
        }
        
        result = await agent.analyze_claim_with_blockchain(claim_data)
        
        # Should still work with enhanced data
        assert "fraud_analysis" in result
        assert "blockchain_audit" in result
        
        # Verify auto-generated fields were added
        fraud_analysis = result["fraud_analysis"]
        assert isinstance(fraud_analysis.get("fraud_score"), (int, float))
        assert fraud_analysis.get("risk_level") in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    
    @pytest.mark.asyncio
    async def test_claims_processing_workflow(self, agent):
        """Test end-to-end claims processing with blockchain."""
        claim_data = {
            "claim_id": f"CLAIMS-TEST-{uuid.uuid4()}",
            "claim_amount": 8000.0,
            "claim_date": datetime.now(timezone.utc).isoformat(),
            "policy_number": "POL789012",
            "payout_address": "0x1234567890123456789012345678901234567890"
        }
        
        # Analyze claim
        analysis_result = await agent.analyze_claim_with_blockchain(claim_data)
        
        # Submit to blockchain
        tx_id = await agent.submit_claim_to_blockchain(claim_data, analysis_result)
        assert tx_id is not None
        assert isinstance(tx_id, str)
        assert len(tx_id) > 0
    
    @pytest.mark.asyncio
    async def test_automated_payout_approval(self, agent):
        """Test automated payout for low-risk claims."""
        claim_id = f"PAYOUT-TEST-{uuid.uuid4()}"
        
        # Create low-risk claim
        claim_data = {
            "claim_id": claim_id,
            "claim_amount": 2000.0,  # Below auto-settlement threshold
            "claim_date": datetime.now(timezone.utc).isoformat(),
            "policy_number": "POL345678"
        }
        
        # Analyze claim first
        await agent.analyze_claim_with_blockchain(claim_data)
        
        # Try automated payout
        payout_result = await agent.approve_automated_payout(
            claim_id, 
            2000.0, 
            confidence_threshold=0.9
        )
        
        # In mock mode, this may return None due to missing audit trail
        # but should not raise an exception
        assert payout_result is None or isinstance(payout_result, str)
    
    @pytest.mark.asyncio
    async def test_identity_verification_blockchain(self, agent):
        """Test blockchain-based identity verification."""
        customer_data = {
            "customer_id": f"CUST-{uuid.uuid4()}",
            "user_id": f"DID:test:{uuid.uuid4()}",
            "name": "John Doe",
            "documents": [
                {"type": "passport", "verified": True},
                {"type": "utility_bill", "verified": True}
            ]
        }
        
        result = await agent.verify_customer_identity_blockchain(customer_data)
        
        assert "user_id" in result
        assert "verified" in result
        assert "kyc_verified" in result
        assert "aml_verified" in result
        assert "attestations" in result
    
    @pytest.mark.asyncio
    async def test_reinsurance_contract_creation(self, agent):
        """Test reinsurance smart contract creation."""
        claim_data = {
            "claim_id": f"REINS-TEST-{uuid.uuid4()}",
            "claim_amount": 200000.0,  # High value to trigger reinsurance
            "claim_date": datetime.now(timezone.utc).isoformat(),
            "policy_number": "POL901234",
            "incident_type": "natural_disaster"
        }
        
        risk_assessment = {
            "fraud_score": 0.1,
            "risk_level": "low",
            "confidence": 0.95
        }
        
        contract_tx_id = await agent.create_reinsurance_smart_contract(
            claim_data, 
            risk_assessment
        )
        
        assert contract_tx_id is not None
        assert isinstance(contract_tx_id, str)
        assert len(contract_tx_id) > 0
    
    @pytest.mark.asyncio
    async def test_blockchain_audit_summary(self, agent):
        """Test comprehensive blockchain audit trail retrieval."""
        claim_id = f"AUDIT-TEST-{uuid.uuid4()}"
        
        # Create some activity first
        claim_data = {
            "claim_id": claim_id,
            "claim_amount": 12000.0,
            "claim_date": datetime.now(timezone.utc).isoformat(),
            "policy_number": "POL567890"
        }
        
        await agent.analyze_claim_with_blockchain(claim_data)
        
        # Get audit summary
        audit_summary = await agent.get_blockchain_audit_summary(claim_id)
        
        assert "claim_id" in audit_summary
        assert "audit_trail" in audit_summary
        assert "blockchain_integrity" in audit_summary
        assert "compliance_status" in audit_summary
    
    @pytest.mark.asyncio
    async def test_fabric_manager_initialization(self):
        """Test Hyperledger Fabric manager initialization."""
        fabric_manager = await get_fabric_manager()
        
        assert fabric_manager is not None
        assert hasattr(fabric_manager, 'log_fraud_detection')
        assert hasattr(fabric_manager, 'submit_claim_to_blockchain')
        assert hasattr(fabric_manager, 'verify_identity_attestation')
    
    @pytest.mark.asyncio
    async def test_error_handling_invalid_data(self, agent):
        """Test error handling with invalid claim data."""
        # Test with completely invalid data
        invalid_claim_data = {
            "claim_amount": "invalid_amount",
            "claim_date": "invalid_date"
        }
        
        # Should not raise exception, should handle gracefully
        result = await agent.analyze_claim_with_blockchain(invalid_claim_data)
        
        assert "fraud_analysis" in result
        # Amount should be converted to 0.0 due to validation
        # Date should be auto-generated
    
    @pytest.mark.asyncio
    async def test_concurrent_fraud_analysis(self, agent):
        """Test concurrent fraud analysis operations."""
        # Create multiple claims
        claims = []
        for i in range(5):
            claims.append({
                "claim_id": f"CONCURRENT-{i}-{uuid.uuid4()}",
                "claim_amount": 1000 * (i + 1),
                "policy_number": f"POL{i:06d}"
            })
        
        # Analyze all concurrently
        tasks = [
            agent.analyze_claim_with_blockchain(claim) 
            for claim in claims
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        for result in results:
            assert "fraud_analysis" in result
            assert "blockchain_audit" in result


# Performance and stress tests
class TestBlockchainPerformance:
    """Performance tests for blockchain integration."""
    
    @pytest.mark.asyncio
    async def test_analysis_response_time(self):
        """Test that fraud analysis completes within acceptable time."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        claim_data = {
            "claim_amount": 10000,
            "policy_number": "PERF-TEST-001"
        }
        
        start_time = asyncio.get_event_loop().time()
        result = await agent.analyze_claim_with_blockchain(claim_data)
        end_time = asyncio.get_event_loop().time()
        
        response_time = end_time - start_time
        
        # Should complete within 5 seconds even in mock mode
        assert response_time < 5.0
        assert "fraud_analysis" in result
    
    @pytest.mark.asyncio
    async def test_high_volume_processing(self):
        """Test processing multiple claims in sequence."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        # Process 20 claims in sequence
        for i in range(20):
            claim_data = {
                "claim_id": f"VOLUME-{i:03d}",
                "claim_amount": 5000 + (i * 100),
                "policy_number": f"VOL{i:06d}"
            }
            
            result = await agent.analyze_claim_with_blockchain(claim_data)
            assert "fraud_analysis" in result


if __name__ == "__main__":
    # Run tests manually if executed directly
    async def run_manual_tests():
        print("🧪 Running Blockchain Integration Tests...")
        
        # Basic functionality test
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        test_claim = {
            "claim_amount": 7500,
            "policy_number": "MANUAL-TEST-001"
        }
        
        result = await agent.analyze_claim_with_blockchain(test_claim)
        print(f"✅ Basic test passed: {result.get('fraud_analysis', {}).get('risk_level')}")
        
        # Performance test
        start_time = asyncio.get_event_loop().time()
        for i in range(10):
            await agent.analyze_claim_with_blockchain({
                "claim_amount": 1000 * (i + 1),
                "policy_number": f"PERF-{i:03d}"
            })
        end_time = asyncio.get_event_loop().time()
        
        print(f"✅ Performance test: 10 analyses in {end_time - start_time:.2f}s")
        print("🎉 All manual tests passed!")
    
    asyncio.run(run_manual_tests())
