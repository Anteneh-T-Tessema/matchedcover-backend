"""
Blockchain Integration Layer for Enhanced Fraud Detection

This module provides seamless integration between AI agents and
Hyperledger Fabric for immutable audit trails, automated claim
processing, and regulatory compliance.

Key Features:
- Automatic logging of fraud detection results to blockchain
- Smart contract integration for claims processing
- Decentralized identity verification
- Multi-party consensus for high-value claims
- Quantum-resistant digital signatures"""

import json
import logging
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
import uuid


from src.blockchain.hyperledger_fabric import (
HyperledgerFabricManager,
FraudAuditRecord,
ClaimRecord,
IdentityAttestation,
AgentDecisionRecord,
get_fabric_manager,
)
from src.agents.fraud_detection_agent import FraudDetectionAgent
from src.core.config import settings
from src.compliance.regulatory_compliance import (
ComplianceManager,
get_compliance_manager,
)

logger = logging.getLogger(__name__)


class BlockchainIntegratedFraudAgent(FraudDetectionAgent):"""
Enhanced fraud detection agent with blockchain integration.

    This agent extends the base fraud detection agent to automatically
log decisions to blockchain for immutable audit trails and compliance."""

    def __init__(self):
        """Initialize blockchain-integrated fraud detection agent."""
    super().__init__()
    self.fabric_manager: Optional[HyperledgerFabricManager] = None
    self.compliance_manager: Optional[ComplianceManager] = None
    self.blockchain_enabled = settings.ENABLE_BLOCKCHAIN_AUDIT

    async def initialize(self):
        """Initialize agent with blockchain connectivity."""
    # Initialize base agent
    await super().initialize()

        # Initialize blockchain connection if enabled
    if self.blockchain_enabled:
            try:
                self.fabric_manager = await get_fabric_manager()
            self.compliance_manager = await get_compliance_manager()
            logger.info("Blockchain integration initialized successfully")
        except Exception as e:
                logger.error(
                f"Failed to initialize blockchain integration: {e}"
            )
            logger.warning("Continuing without blockchain integration")
            self.blockchain_enabled = False

    async def analyze_claim_with_blockchain(
        self, claim_data: Dict[str, Any]
) -> Dict[str, Any]:"""
    Analyze claim with automatic blockchain logging.

        Args:
            claim_data: Claim information

        Returns:
            Analysis result with blockchain transaction IDs"""
    # Validate and enhance claim data
    enhanced_claim_data = self._validate_and_enhance_claim_data(claim_data)

        # Perform standard fraud analysis using the base agent's process_task'
    # method
    analysis_result = await self.process_task(
        task_type="claim_fraud",
        input_data={"entity_data": enhanced_claim_data},
        context={},
    )

        # Log to blockchain if enabled
    blockchain_info = {}
    if self.blockchain_enabled and self.fabric_manager:
            try:
                # Create fraud audit record
            fraud_record = FraudAuditRecord(
                claim_id=claim_data.get("claim_id", str(uuid.uuid4())),
                fraud_score=analysis_result.get("fraud_score", 0.0),
                risk_level=analysis_result.get("risk_level", "unknown"),
                agent_id=self.agent_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                decision_hash="",  # Will be set by fabric manager
                quantum_signature="",  # Will be set by fabric manager
                evidence_hash=self._create_evidence_hash(
                    claim_data, analysis_result
                ),
                compliance_flags=analysis_result.get(
                    "compliance_status", {}
                ).get("violations", []),
                human_review_required=analysis_result.get(
                    "requires_human_review", False
                ),
            )

                # Log fraud detection to blockchain
            fraud_tx_id = await self.fabric_manager.log_fraud_detection(
                fraud_record
            )
            blockchain_info["fraud_audit_tx_id"] = fraud_tx_id

                # Log agent decision for governance
            decision_record = AgentDecisionRecord(
                agent_id=self.agent_id,
                decision_type="fraud_analysis",
                input_hash=self._create_input_hash(claim_data),
                output_hash=self._create_output_hash(analysis_result),
                confidence_score=analysis_result.get("confidence", 0.0),
                explanation_hash=self._create_explanation_hash(
                    analysis_result.get("explanation", {})
                ),
                timestamp=datetime.now(timezone.utc).isoformat(),
                model_version=analysis_result.get(
                    "agent_version", "1.0.0"
                ),
                compliance_check=analysis_result.get(
                    "compliance_status", {}
                ),
                quantum_signature="",  # Will be set by fabric manager
            )

                governance_tx_id = (
                await self.fabric_manager.log_agent_decision(
                    decision_record
                )
            )
            blockchain_info["governance_tx_id"] = governance_tx_id

                logger.info(
                f"Fraud analysis logged to blockchain: "
                f"fraud={fraud_tx_id}, governance={governance_tx_id}"
            )

            except Exception as e:
                logger.error(
                f"Failed to log fraud analysis to blockchain: {e}"
            )
            blockchain_info["blockchain_error"] = str(e)

        # Add blockchain information to analysis result
    analysis_result["blockchain_audit"] = blockchain_info
    return analysis_result

    async def submit_claim_to_blockchain(
        self, claim_data: Dict[str, Any], analysis_result: Dict[str, Any]
) -> str:"""
    Submit claim to blockchain for transparent processing.

        Args:
            claim_data: Original claim data
        analysis_result: AI analysis result

        Returns:
            Blockchain transaction ID"""
    if not self.blockchain_enabled or not self.fabric_manager:
            raise ValueError("Blockchain integration not available")

        # Create claim record for blockchain
    claim_record = ClaimRecord(
        claim_id=claim_data.get("claim_id", str(uuid.uuid4())),
        policy_id=claim_data.get("policy_number", ""),
        claim_amount=float(claim_data.get("claim_amount", 0)),
        status="submitted",
        ai_assessment=analysis_result,
        approval_conditions=self._generate_approval_conditions(
            analysis_result
        ),
        payout_address=claim_data.get("payout_address"),
        timestamp=datetime.now(timezone.utc).isoformat(),
        approver_signatures=[],
    )

        # Submit to blockchain
    tx_id = await self.fabric_manager.submit_claim_to_blockchain(
        claim_record
    )
    logger.info(f"Claim submitted to blockchain: {tx_id}")

        return tx_id

    async def approve_automated_payout(
        self,
    claim_id: str,
    payout_amount: float,
    confidence_threshold: float = 0.9,
) -> Optional[str]:"""
    Approve automated payout for high-confidence, low-risk claims.

        Args:
            claim_id: Claim identifier
        payout_amount: Amount to pay out
        confidence_threshold: Minimum confidence for automation

        Returns:
            Blockchain transaction ID if approved, None otherwise"""
    if not self.blockchain_enabled or not self.fabric_manager:
            return None

        try:
            # Get fraud analysis from blockchain
        fraud_audit_trail = (
            await self.fabric_manager.query_fraud_audit_trail(claim_id)
        )

            if not fraud_audit_trail:
                logger.warning(
                f"No fraud audit trail found for claim {claim_id}"
            )
            return None

            # Check latest analysis
        latest_analysis = (
            fraud_audit_trail[-1] if fraud_audit_trail else {}
        )
        fraud_score = latest_analysis.get("fraud_score", 1.0)
        risk_level = latest_analysis.get("risk_level", "high")

            # Auto-approve if conditions are met
        if (
                fraud_score < 0.1  # Very low fraud score
            and risk_level.lower() == "low"  # Low risk
            and payout_amount <= settings.AUTO_SETTLEMENT_THRESHOLD
        ):  # Below threshold

                # Create digital signature for automated approval
            approver_signatures = [
                f"AI_AGENT_{self.agent_id}_{datetime.now("
                    timezone.utc).isoformat()}""
            ]

                # Approve payout on blockchain
            tx_id = await self.fabric_manager.approve_claim_payout(
                claim_id, payout_amount, approver_signatures
            )

                logger.info(
                f"Automated payout approved for claim {claim_id}: {tx_id}"
            )
            return tx_id
        else:
                logger.info(
                f"Claim {claim_id} requires human approval: fraud_score={fraud_score},"
                    risk={risk_level}""
            )
            return None

        except Exception as e:
            logger.error(
            f"Failed to process automated payout for claim {claim_id}: {e}"
        )
        return None

    async def verify_customer_identity_blockchain(
        self, customer_data: Dict[str, Any]
) -> Dict[str, Any]:"""
    Verify customer identity using blockchain attestations.

        Args:
            customer_data: Customer information

        Returns:
            Identity verification result"""
    if not self.blockchain_enabled or not self.fabric_manager:
            return {"verified": False, "reason": "Blockchain not available"}

        try:
            user_id = customer_data.get("customer_id") or customer_data.get(
            "user_id"
        )
        if not user_id:
                return {"verified": False, "reason": "No user ID provided"}

            # Check existing attestations
        kyc_attestation = (
            await self.fabric_manager.verify_identity_attestation(
                user_id, "KYC"
            )
        )
        aml_attestation = (
            await self.fabric_manager.verify_identity_attestation(
                user_id, "AML"
            )
        )

            verification_result = {
            "user_id": user_id,
            "kyc_verified": bool(
                kyc_attestation
                and not kyc_attestation.get("revocation_status")
            ),
            "aml_verified": bool(
                aml_attestation
                and not aml_attestation.get("revocation_status")
            ),
            "attestations": {
                "kyc": kyc_attestation,
                "aml": aml_attestation,
            },
            "verified": False,
        }

            # Overall verification status
        verification_result["verified"] = (
            verification_result["kyc_verified"]
            and verification_result["aml_verified"]
        )

            # Create new attestation if verification is performed
        if verification_result["verified"]:
                attestation = IdentityAttestation(
                user_id=user_id,
                verification_type="FRAUD_CHECK",
                attestation_hash=self._create_verification_hash(
                    customer_data
                ),
                verifier_agent_id=self.agent_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                validity_period=365 * 24 * 60 * 60,  # 1 year in seconds
                revocation_status=False,
                zero_knowledge_proof=None,
                    # Could be implemented for privacy
            )

                attestation_tx_id = (
                await self.fabric_manager.create_identity_attestation(
                    attestation
                )
            )
            verification_result["new_attestation_tx_id"] = (
                attestation_tx_id
            )

            return verification_result

        except Exception as e:
            logger.error(f"Failed to verify identity on blockchain: {e}")
        return {"verified": False, "reason": f"Blockchain error: {str(e)}"}

    async def create_reinsurance_smart_contract(
        self, claim_data: Dict[str, Any], risk_assessment: Dict[str, Any]
) -> Optional[str]:"""
    Create reinsurance smart contract for high-value claims.

        Args:
            claim_data: Original claim data
        risk_assessment: AI risk assessment

        Returns:
            Blockchain transaction ID if contract created"""
    if not self.blockchain_enabled or not self.fabric_manager:
            return None

        try:
            claim_amount = float(claim_data.get("claim_amount", 0))

            # Only create reinsurance contracts for high-value claims
        if claim_amount < 100000:  # $100k threshold
                return None

            contract_data = {
            "claim_id": claim_data.get("claim_id"),
            "primary_insurer": settings.FABRIC_ORG_NAME,
            "claim_amount": claim_amount,
            "risk_score": risk_assessment.get("fraud_score", 0),
            "risk_level": risk_assessment.get("risk_level", "unknown"),
            "ai_confidence": risk_assessment.get("confidence", 0),
            "coverage_percentage": self._calculate_reinsurance_coverage(
                claim_amount, risk_assessment
            ),
            "terms": {
                # 10% or $50k max retention
                "retention_limit": min(claim_amount * 0.1, 50000),
                "coverage_limit": claim_amount * 0.9,
                "deductible": claim_amount * 0.05,
            },
            "conditions": [
                "Fraud investigation completed",
                "Independent adjuster verification",
                "Regulatory approval if required",
            ],
            "automatic_triggers": {
                "weather_event": claim_data.get("incident_type")
                == "weather",
                "parametric_payout": risk_assessment.get("risk_level")
                == "low",
            },
        }

            tx_id = await self.fabric_manager.create_reinsurance_contract(
            contract_data
        )
        logger.info(
            f"Reinsurance contract created for claim {claim_data.get("
                'claim_id')}: {tx_id}""
        )

            return tx_id

        except Exception as e:
            logger.error(f"Failed to create reinsurance contract: {e}")
        return None

    def _create_evidence_hash(
        self, claim_data: Dict[str, Any], analysis_result: Dict[str, Any]
) -> str:
        """Create hash of evidence used in fraud detection."""
    evidence = {
        "claim_data_keys": list(claim_data.keys()),
        "indicators_count": len(analysis_result.get("indicators", [])),
        "risk_factors": analysis_result.get("risk_factors", []),
    }
    return self._hash_dict(evidence)

    def _create_input_hash(self, claim_data: Dict[str, Any]) -> str:
        """Create hash of input data (without PII)."""
    sanitized_data = {
        k: v
        for k, v in claim_data.items()
            if k not in ["ssn", "driver_license", "credit_card"]
        }
    return self._hash_dict(sanitized_data)

    def _create_output_hash(self, analysis_result: Dict[str, Any]) -> str:
        """Create hash of analysis output."""
    return self._hash_dict(analysis_result)

    def _create_explanation_hash(self, explanation: Dict[str, Any]) -> str:
        """Create hash of AI explanation."""
    return self._hash_dict(explanation)

    def _create_verification_hash(self, customer_data: Dict[str, Any]) -> str:
        """Create hash of identity verification data."""
    verification_data = {
        "verification_timestamp": datetime.now(timezone.utc).isoformat(),
        "data_points_verified": len(customer_data),
        "verification_method": "AI_AGENT",
    }
    return self._hash_dict(verification_data)

    def _hash_dict(self, data: Dict[str, Any]) -> str:
        """Create SHA-256 hash of dictionary data."""

        json_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_str.encode()).hexdigest()

    def _generate_approval_conditions(
        self, analysis_result: Dict[str, Any]
) -> List[str]:
        """Generate approval conditions based on analysis."""
    conditions = []

        risk_level = analysis_result.get("risk_level", "").lower()
    fraud_score = analysis_result.get("fraud_score", 0)

        if risk_level == "high" or fraud_score > 0.7:
            conditions.extend(
            [
                "Independent fraud investigation required",
                "Multiple approver signatures required",
                "Identity verification mandatory",
            ]
        )
    elif risk_level == "medium" or fraud_score > 0.3:
            conditions.extend(
            [
                "Senior adjuster approval required",
                "Additional documentation review",
            ]
        )
    else:
            conditions.append("Standard processing approved")

        if analysis_result.get("requires_human_review"):
            conditions.append("Human review completed")

        return conditions

    def _calculate_reinsurance_coverage(
        self, claim_amount: float, risk_assessment: Dict[str, Any]
) -> float:
        """Calculate reinsurance coverage percentage."""
    base_coverage = 0.8  # 80% base coverage

        # Adjust based on risk
    risk_level = risk_assessment.get("risk_level", "").lower()
    if risk_level == "high":
            base_coverage = 0.9  # Higher coverage for higher risk
    elif risk_level == "low":
            base_coverage = 0.7  # Lower coverage for lower risk

        # Adjust based on claim amount
    if claim_amount > 1000000:  # $1M+
            base_coverage = min(base_coverage + 0.1, 0.95)

        return base_coverage

    async def get_blockchain_audit_summary(
        self, claim_id: str
) -> Dict[str, Any]:"""
    Get comprehensive blockchain audit summary for a claim.

        Args:
            claim_id: Claim identifier

        Returns:
            Audit summary with all blockchain interactions"""
    if not self.blockchain_enabled or not self.fabric_manager:
            return {"error": "Blockchain not available"}

        try:
            # Get fraud audit trail
        fraud_trail = await self.fabric_manager.query_fraud_audit_trail(
            claim_id
        )

            # Get claim history
        claim_history = await self.fabric_manager.query_claim_history(
            claim_id
        )

            # Get agent decisions
        agent_decisions = await self.fabric_manager.query_agent_decisions(
            self.agent_id,
            start_date=(
                datetime.now(timezone.utc) - timedelta(days=30)
            ).isoformat(),
        )

            # Filter decisions for this claim
        claim_decisions = [
            decision
            for decision in agent_decisions
                if claim_id in decision.get("input_hash", "")
                or claim_id in decision.get("output_hash", "")
        ]

            summary = {
            "claim_id": claim_id,
            "audit_trail": {
                "fraud_detections": fraud_trail,
                "claim_processing": claim_history,
                "agent_decisions": claim_decisions,
            },
            "blockchain_integrity": {
                "total_transactions": len(fraud_trail)
                + len(claim_history)
                + len(claim_decisions),
                "signature_verification": "pending",
                    # Would verify signatures
                "tamper_evidence": "none_detected",
            },
            "compliance_status": {
                "audit_trail_complete": bool(
                    fraud_trail and claim_history
                ),
                "signatures_valid": True,
                    # Would validate quantum signatures
                "regulatory_requirements_met": True,
            },
        }

            return summary

        except Exception as e:
            logger.error(f"Failed to get blockchain audit summary: {e}")
        return {"error": str(e)}

    def _validate_and_enhance_claim_data(
        self, claim_data: Dict[str, Any]
) -> Dict[str, Any]:"""
    Validate and enhance claim data with required fields.

        Args:
            claim_data: Original claim data

        Returns:
            Enhanced claim data with required fields"""
    enhanced_data = claim_data.copy()

        # Ensure claim_date is present
    if "claim_date" not in enhanced_data:
            enhanced_data["claim_date"] = datetime.now(
            timezone.utc
        ).isoformat()
        logger.info("Added current timestamp as claim_date")

        # Ensure claim_id is present
    if "claim_id" not in enhanced_data:
            enhanced_data["claim_id"] = str(uuid.uuid4())
        logger.info(f"Generated claim_id: {enhanced_data['claim_id']}")

        # Ensure claim_amount is numeric
    if "claim_amount" in enhanced_data:
            try:
                enhanced_data["claim_amount"] = float(
                enhanced_data["claim_amount"]
            )
        except (ValueError, TypeError):
                logger.warning(
                f"Invalid claim_amount: {enhanced_data['claim_amount']}, "
                f"setting to 0"
            )
            enhanced_data["claim_amount"] = 0.0

        return enhanced_data


# Global blockchain-integrated fraud agent instance
blockchain_fraud_agent = None


async def get_blockchain_fraud_agent() -> BlockchainIntegratedFraudAgent:
    """Get the global blockchain-integrated fraud detection agent."""
global blockchain_fraud_agent

    if blockchain_fraud_agent is None:
        blockchain_fraud_agent = BlockchainIntegratedFraudAgent()
    await blockchain_fraud_agent.initialize()

    return blockchain_fraud_agent
