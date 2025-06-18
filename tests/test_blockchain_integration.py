"""
Integration Tests for Blockchain-Enabled Fraud Detection

These tests validate the end-to-end functionality of the blockchain-integrated
insurance platform, including fraud detection, claims processing, and audit trails.

Test Categories:
1. Blockchain connectivity and configuration
2. Fraud detection with blockchain logging
3. Claims processing and smart contract integration
4. Identity verification and DID attestation
5. Reinsurance contract management
6. Audit trail queries and compliance
"""

import asyncio
import json
import pytest
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any
from unittest.mock import Mock, patch, AsyncMock

from src.blockchain.blockchain_integration import BlockchainIntegratedFraudAgent, get_blockchain_fraud_agent
from src.blockchain.hyperledger_fabric import (
    HyperledgerFabricManager,
    FraudAuditRecord,
    ClaimRecord,
    IdentityAttestation,
    AgentDecisionRecord,
    ChannelType,
    TransactionType
)
from src.api.blockchain_fraud_detection import router as blockchain_router
from src.core.config import settings


class TestBlockchainConnectivity:
    """Test blockchain connectivity and network setup."""
    
    @pytest.mark.asyncio
    async def test_fabric_manager_initialization(self):
        """Test HyperledgerFabricManager initialization."""
        fabric_manager = HyperledgerFabricManager()
        
        # Should initialize without errors
        assert fabric_manager is not None
        assert fabric_manager.connection_profile is not None
        assert fabric_manager.quantum_signer is not None
        
    @pytest.mark.asyncio
    async def test_mock_fabric_client_fallback(self):
        """Test fallback to mock client when Fabric SDK unavailable."""
        fabric_manager = HyperledgerFabricManager()
        
        # Connect using mock client
        await fabric_manager.connect()
        
        # Should use mock client
        assert fabric_manager.client is not None
        assert hasattr(fabric_manager.client, 'invoke_chaincode')
        assert hasattr(fabric_manager.client, 'query_chaincode')
        
    @pytest.mark.asyncio
    async def test_blockchain_agent_initialization(self):
        """Test blockchain-integrated fraud agent initialization."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        assert agent is not None
        assert hasattr(agent, 'fabric_manager')
        

class TestFraudDetectionBlockchain:
    """Test fraud detection with blockchain integration."""
    
    @pytest.fixture
    def sample_claim_data(self) -> Dict[str, Any]:
        """Sample claim data for testing."""
        return {
            "claim_id": str(uuid.uuid4()),
            "policy_number": "POL-2024-001",
            "claim_amount": 25000.0,
            "incident_type": "vehicle_accident",
            "incident_date": "2024-01-15",
            "claimant_info": {
                "name": "John Doe",
                "id": "ID123456789",
                "contact": "john.doe@email.com"
            },
            "incident_details": {
                "location": "Highway 101",
                "weather": "rainy",
                "description": "Vehicle collision at intersection"
            },
            "supporting_documents": ["police_report.pdf", "medical_records.pdf"]
        }
    
    @pytest.mark.asyncio
    async def test_fraud_analysis_with_blockchain_logging(
        self, sample_claim_data: Dict[str, Any]
    ):
        """Test fraud analysis with automatic blockchain logging."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        # Perform analysis with blockchain logging
        result = await agent.analyze_claim_with_blockchain(sample_claim_data)
        
        # Validate analysis result
        assert "fraud_score" in result
        assert "risk_level" in result
        assert "blockchain_info" in result
        assert isinstance(result["fraud_score"], float)
        assert 0.0 <= result["fraud_score"] <= 1.0
        
        # Validate blockchain integration
        blockchain_info = result["blockchain_info"]
        if agent.blockchain_enabled:
            assert "fraud_audit_tx_id" in blockchain_info
            assert "agent_decision_tx_id" in blockchain_info
    
    @pytest.mark.asyncio
    async def test_fraud_audit_record_creation(self):
        """Test creation and validation of fraud audit records."""
        fraud_record = FraudAuditRecord(
            claim_id="CLAIM-123",
            fraud_score=0.75,
            risk_level="high",
            agent_id="agent-001",
            timestamp=datetime.now(timezone.utc).isoformat(),
            decision_hash="hash123",
            quantum_signature="sig123",
            evidence_hash="evidence456",
            compliance_flags=["suspicious_pattern"],
            human_review_required=True
        )
        
        # Validate record structure
        assert fraud_record.claim_id == "CLAIM-123"
        assert fraud_record.fraud_score == 0.75
        assert fraud_record.risk_level == "high"
        assert fraud_record.human_review_required is True
        
        # Test serialization
        record_dict = fraud_record.to_dict()
        assert isinstance(record_dict, dict)
        assert "claim_id" in record_dict
        assert "fraud_score" in record_dict
    
    @pytest.mark.asyncio
    async def test_batch_fraud_analysis(self):
        """Test batch processing of claims with blockchain logging."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        # Create multiple claims
        claims = []
        for i in range(3):
            claim = {
                "claim_id": f"CLAIM-{i:03d}",
                "policy_number": f"POL-2024-{i:03d}",
                "claim_amount": 10000.0 + i * 5000,
                "incident_type": "auto_accident",
                "incident_date": "2024-01-15",
                "claimant_info": {"name": f"Claimant {i}"},
                "incident_details": {"description": f"Incident {i}"}
            }
            claims.append(claim)
        
        # Process batch
        results = []
        for claim in claims:
            result = await agent.analyze_claim_with_blockchain(claim)
            results.append(result)
        
        # Validate batch results
        assert len(results) == 3
        for result in results:
            assert "fraud_score" in result
            assert "blockchain_info" in result


class TestClaimsProcessingChaincode:
    """Test claims processing smart contract functionality."""
    
    @pytest.mark.asyncio
    async def test_claim_submission_to_blockchain(self):
        """Test submitting a claim to blockchain for processing."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        claim_record = ClaimRecord(
            claim_id="CLAIM-SUBMIT-001",
            policy_id="POL-2024-001",
            claim_amount=15000.0,
            status="submitted",
            ai_assessment={
                "fraud_score": 0.25,
                "risk_factors": ["low_impact"],
                "recommendation": "approve"
            },
            approval_conditions=["verify_documents"],
            payout_address=None,
            timestamp=datetime.now(timezone.utc).isoformat(),
            approver_signatures=[]
        )
        
        # Submit to blockchain
        if agent.fabric_manager:
            analysis_result = {"fraud_score": 0.25, "recommendation": "approve"}
            tx_id = await agent.submit_claim_to_blockchain(claim_record.to_dict(), analysis_result)
            assert tx_id is not None
    
    @pytest.mark.asyncio
    async def test_automated_payout_approval(self):
        """Test automated payout approval for low-risk claims."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        # Low-risk claim for automated approval
        claim_id = "CLAIM-AUTO-001"
        payout_amount = 5000.0
        confidence_threshold = 0.9
        
        # Process automated payout using the actual method
        if agent.fabric_manager:
            result = await agent.approve_automated_payout(
                claim_id, payout_amount, confidence_threshold
            )
            assert result is not None


class TestIdentityVerification:
    """Test decentralized identity verification."""
    
    @pytest.mark.asyncio
    async def test_identity_attestation_creation(self):
        """Test creation of identity attestation records."""
        identity_record = IdentityAttestation(
            user_id="DID:example:123456789abcdef",
            verification_type="KYC_VERIFIED",
            attestation_hash="attestation_hash_123",
            verifier_agent_id="agent-001",
            timestamp=datetime.now(timezone.utc).isoformat(),
            validity_period=365,  # days
            revocation_status=False,
            zero_knowledge_proof="zkp_proof_123"
        )
        
        assert identity_record.user_id.startswith("DID:")
        assert identity_record.verification_type == "KYC_VERIFIED"
        assert identity_record.revocation_status is False
    
    @pytest.mark.asyncio
    async def test_identity_verification_workflow(self):
        """Test complete identity verification workflow."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        identity_data = {
            "user_id": "DID:example:test123",
            "verification_documents": ["passport.pdf", "utility_bill.pdf"],
            "biometric_data": "encrypted_fingerprint_hash",
            "kyc_provider": "verified_identity_corp"
        }
        
        # Verify identity using the customer verification method
        if agent.fabric_manager:
            result = await agent.verify_customer_identity_blockchain(identity_data)
            assert result is not None


class TestReinsuranceContracts:
    """Test reinsurance contract management on blockchain."""
    
    @pytest.mark.asyncio
    async def test_reinsurance_contract_creation(self):
        """Test creating reinsurance contracts on blockchain."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        contract_data = {
            "contract_id": "REINS-2024-001",
            "primary_insurer": "MatchedCover Insurance",
            "reinsurer": "Global Reinsurance Corp",
            "coverage_amount": 1000000.0,
            "risk_categories": ["auto", "property"],
            "effective_date": "2024-01-01",
            "expiry_date": "2024-12-31",
            "premium_percentage": 0.15
        }
        
        # Create reinsurance contract
        if agent.fabric_manager:
            result = await agent.create_reinsurance_contract(contract_data)
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_risk_sharing_calculation(self):
        """Test risk sharing calculations for reinsurance."""
        agent = BlockchainIntegratedFraudAgent()
        await agent.initialize()
        
        claim_data = {
            "claim_amount": 75000.0,
            "policy_type": "auto",
            "reinsurance_threshold": 50000.0,
            "reinsurance_percentage": 0.80
        }
        
        # Calculate risk sharing
        risk_share = await agent.calculate_reinsurance_share(claim_data)
        assert risk_share is not None
        assert "primary_liability" in risk_share
        assert "reinsurer_liability" in risk_share


class TestAuditTrailQueries:
    """Test audit trail queries and compliance reporting."""
    
    @pytest.mark.asyncio
    async def test_fraud_audit_trail_query(self):
        """Test querying fraud audit trails."""
        fabric_manager = HyperledgerFabricManager()
        await fabric_manager.connect()
        
        # Query audit trail for specific claim
        claim_id = "CLAIM-AUDIT-001"
        
        # This would query the blockchain for audit records
        audit_trail = await fabric_manager.query_fraud_audit_trail(claim_id)
        
        # Mock fabric manager should return empty list or mock data
        assert audit_trail is not None
        assert isinstance(audit_trail, list)
    
    @pytest.mark.asyncio
    async def test_compliance_report_generation(self):
        """Test generation of compliance reports from blockchain data."""
        fabric_manager = HyperledgerFabricManager()
        await fabric_manager.connect()
        
        # Generate compliance report for date range
        report_params = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "include_fraud_stats": True,
            "include_claim_processing": True,
            "regulatory_framework": "GDPR"
        }
        
        compliance_report = await fabric_manager.generate_compliance_report(report_params)
        assert compliance_report is not None
    
    @pytest.mark.asyncio
    async def test_agent_decision_governance(self):
        """Test agent decision governance and explainability."""
        agent_decision = AgentDecisionRecord(
            decision_id=str(uuid.uuid4()),
            agent_id="fraud-agent-001",
            claim_id="CLAIM-GOV-001",
            decision_type="fraud_assessment",
            decision_outcome="approve_with_conditions",
            confidence_score=0.87,
            reasoning_trace=[
                "Low fraud indicators detected",
                "Supporting documents verified",
                "Pattern analysis shows normal behavior"
            ],
            model_version="v2.1.0",
            timestamp=datetime.now(timezone.utc).isoformat(),
            human_review_triggered=False
        )
        
        assert agent_decision.decision_id is not None
        assert agent_decision.confidence_score > 0.8
        assert len(agent_decision.reasoning_trace) > 0


class TestAPIEndpoints:
    """Test blockchain-enabled API endpoints."""
    
    @pytest.mark.asyncio
    async def test_blockchain_fraud_analysis_endpoint(self):
        """Test blockchain fraud analysis API endpoint."""
        # This would test the actual FastAPI endpoints
        # For now, we'll test the core functionality
        
        request_data = {
            "claim_id": "API-TEST-001",
            "policy_number": "POL-2024-API",
            "claim_amount": 20000.0,
            "incident_type": "auto_accident",
            "incident_date": "2024-01-15",
            "claimant_info": {"name": "Test Claimant"},
            "incident_details": {"description": "Test incident"},
            "submit_to_blockchain": True
        }
        
        # The endpoint would process this data through the blockchain agent
        agent = await get_blockchain_fraud_agent()
        result = await agent.analyze_claim_with_blockchain(request_data)
        
        assert result is not None
        assert "fraud_score" in result
    
    @pytest.mark.asyncio
    async def test_network_status_endpoint(self):
        """Test blockchain network status endpoint."""
        fabric_manager = HyperledgerFabricManager()
        await fabric_manager.connect()
        
        network_status = await fabric_manager.get_network_status()
        
        assert network_status is not None
        assert "status" in network_status
        assert "peers" in network_status


class TestQuantumResistance:
    """Test quantum-resistant cryptographic features."""
    
    @pytest.mark.asyncio
    async def test_quantum_signature_verification(self):
        """Test quantum-resistant digital signatures."""
        fabric_manager = HyperledgerFabricManager()
        
        # Test data for signing
        test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
        data_string = json.dumps(test_data, sort_keys=True)
        
        # Generate quantum-resistant signature
        if fabric_manager.quantum_signer:
            # This would use the quantum signer if available
            # For now, we test the interface
            assert hasattr(fabric_manager.quantum_signer, 'generate_keypair')
    
    @pytest.mark.asyncio
    async def test_post_quantum_cryptography_integration(self):
        """Test post-quantum cryptography integration in blockchain."""
        # Test that quantum-resistant algorithms are properly configured
        assert settings.QUANTUM_ALGORITHM == "dilithium3"
        assert settings.ENABLE_QUANTUM_RESISTANCE is True
        assert settings.QUANTUM_KEY_ROTATION_DAYS == 90


class TestErrorHandling:
    """Test error handling and resilience."""
    
    @pytest.mark.asyncio
    async def test_blockchain_network_unavailable(self):
        """Test behavior when blockchain network is unavailable."""
        agent = BlockchainIntegratedFraudAgent()
        
        # Simulate network unavailable
        with patch.object(agent, 'blockchain_enabled', False):
            await agent.initialize()
            
            claim_data = {"claim_id": "ERROR-TEST-001"}
            result = await agent.analyze_claim_with_blockchain(claim_data)
            
            # Should still return analysis without blockchain
            assert result is not None
            assert "fraud_score" in result
    
    @pytest.mark.asyncio
    async def test_chaincode_invocation_failure(self):
        """Test handling of chaincode invocation failures."""
        fabric_manager = HyperledgerFabricManager()
        await fabric_manager.connect()
        
        # Simulate chaincode failure
        fraud_record = FraudAuditRecord(
            claim_id="FAIL-TEST-001",
            fraud_score=0.5,
            risk_level="medium",
            agent_id="test-agent",
            timestamp=datetime.now().isoformat(),
            decision_hash="test-hash",
            quantum_signature="test-sig",
            evidence_hash="test-evidence",
            compliance_flags=[],
            human_review_required=False
        )
        
        # Should handle errors gracefully
        try:
            result = await fabric_manager.log_fraud_detection(fraud_record)
            # Mock implementation should return a result
            assert result is not None
        except Exception as e:
            # Should not raise unhandled exceptions
            assert False, f"Unhandled exception: {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
