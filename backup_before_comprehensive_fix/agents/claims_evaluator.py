""""
Claims Evaluator Agent for MatchedCover Insurance Platform.

This agent processes and evaluates insurance claims using AI, computer vision,
and fraud detection to determine claim validity and settlement amounts.
""""

import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal


import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN


from src.agents.base_agent import BaseAgent
from src.core.config import get_settings
from src.quantum.crypto import QuantumResistantSigner
from src.blockchain.audit_trail import (
BlockchainAuditTrail,
AuditEventType,
AuditSeverity,
)

logger = logging.getLogger(__name__)
settings = get_settings()

# Optional computer vision dependency - currently not used
# try:
#     import cv2
#     CV2_AVAILABLE = True
# except ImportError:
#     CV2_AVAILABLE = False
#     logger.warning("OpenCV (cv2) not available"
. Image processing features disabled.")"

CV2_AVAILABLE = False


class ClaimStatus(Enum):
    """Claim processing status."""

    SUBMITTED = "submitted"
UNDER_REVIEW = "under_review"
REQUIRES_INVESTIGATION = "requires_investigation"
APPROVED = "approved"
PARTIALLY_APPROVED = "partially_approved"
REJECTED = "rejected"
PAID = "paid"
CLOSED = "closed"


class ClaimType(Enum):
    """Types of insurance claims."""

    AUTO_ACCIDENT = "auto_accident"
AUTO_THEFT = "auto_theft"
HOME_DAMAGE = "home_damage"
HOME_THEFT = "home_theft"
HEALTH_MEDICAL = "health_medical"
LIFE_DEATH = "life_death"
BUSINESS_LIABILITY = "business_liability"
TRAVEL_EMERGENCY = "travel_emergency"


class EvidenceType(Enum):
    """Types of claim evidence."""

    PHOTO = "photo"
VIDEO = "video"
DOCUMENT = "document"
MEDICAL_RECORD = "medical_record"
POLICE_REPORT = "police_report"
WITNESS_STATEMENT = "witness_statement"
EXPERT_REPORT = "expert_report"


@dataclass
class ClaimEvidence:
    """Individual piece of claim evidence."""

    evidence_id: str
evidence_type: EvidenceType
content_hash: str
analysis_result: Dict[str, Any]
authenticity_score: float  # 0.0 to 1.0
relevance_score: float  # 0.0 to 1.0
timestamp: datetime


@dataclass
class ClaimEvaluation:
    """Complete claim evaluation result."""

    claim_id: str
policy_id: str
claim_type: ClaimType
submitted_amount: Decimal
evaluated_amount: Decimal
approved_amount: Decimal
claim_status: ClaimStatus
fraud_risk_score: float  # 0.0 to 1.0
authenticity_score: float  # 0.0 to 1.0
evidence_analysis: List[ClaimEvidence]
evaluation_reasoning: List[str]
required_actions: List[str]
evaluation_confidence: float
processing_time_minutes: int
evaluator_agent_id: str
evaluation_timestamp: datetime
quantum_signature: str


class ClaimsEvaluatorAgent(BaseAgent):
    """"
AI agent for automated claims evaluation and processing.

    Uses computer vision, natural language processing, and machine learning
to assess claim validity, detect fraud, and determine settlement amounts.
""""

    def __init__(self):
        super().__init__(
        name="ClaimsEvaluator", agent_type="claims_evaluation"
    )
    self.quantum_signer = QuantumResistantSigner()
    self.audit_trail = BlockchainAuditTrail()
    self.ml_models = {}
    self.vision_models = {}
    self._initialize_evaluation_models()

    def _initialize_evaluation_models(self):
        """Initialize machine learning models for claim evaluation."""
    try:
            # Fraud detection model
        self.ml_models["fraud_detector"] = IsolationForest(
            contamination=0.1, random_state=42
        )

            # Claim amount validator
        self.ml_models["amount_validator"] = IsolationForest(
            contamination=0.05, random_state=42
        )

            # Damage assessment clustering
        self.ml_models["damage_classifier"] = DBSCAN(
            eps=0.5, min_samples=5
        )

            # In production, load pre-trained models
        # self._load_pretrained_models()

            logger.info("Claims evaluation models initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize evaluation models: {str(e)}")
        raise

    async def evaluate_claim(
        self,
    claim_data: Dict[str, Any],
    policy_data: Dict[str, Any],
    evidence_files: List[Dict[str, Any]],
) -> ClaimEvaluation:
        """"
    Perform comprehensive claim evaluation.

        Args:
            claim_data: Claim information and details
        policy_data: Related policy information
        evidence_files: Supporting evidence files

        Returns:
            Complete claim evaluation with recommendations
    """"
    try:
            start_time = datetime.utcnow()
        logger.info(
            f"Starting evaluation for claim {claim_data.get('claim_id')}"
        )

            # Log claim submission
        await self.audit_trail.log_event(
            event_type=AuditEventType.CLAIM_SUBMITTED,
            entity_id=claim_data.get("claim_id"),
            description=f"Claim evaluation started for amount ${claim_data"
                .get('amount')}","
            details=claim_data,
            severity=AuditSeverity.MEDIUM,
        )

            # Analyze evidence
        evidence_analysis = await self._analyze_evidence(evidence_files)

            # Perform fraud detection
        fraud_score = await self._detect_fraud(
            claim_data, policy_data, evidence_analysis
        )

            # Validate claim amount
        amount_validation = await self._validate_claim_amount(
            claim_data, policy_data, evidence_analysis
        )

            # Assess claim authenticity
        authenticity_score = await self._assess_authenticity(
            evidence_analysis
        )

            # Determine claim status and approved amount
        evaluation_result = await self._make_evaluation_decision(
            claim_data,
            policy_data,
            fraud_score,
            amount_validation,
            authenticity_score,
        )

            # Calculate processing time
        processing_time = (
            datetime.utcnow() - start_time
        ).total_seconds() / 60

            # Create evaluation result
        claim_evaluation = ClaimEvaluation(
            claim_id=claim_data.get("claim_id"),
            policy_id=claim_data.get("policy_id"),
            claim_type=ClaimType(
                claim_data.get("claim_type", "auto_accident")
            ),
            submitted_amount=Decimal(str(claim_data.get("amount", 0))),
            evaluated_amount=amount_validation["evaluated_amount"],
            approved_amount=evaluation_result["approved_amount"],
            claim_status=evaluation_result["status"],
            fraud_risk_score=fraud_score,
            authenticity_score=authenticity_score,
            evidence_analysis=evidence_analysis,
            evaluation_reasoning=evaluation_result["reasoning"],
            required_actions=evaluation_result["required_actions"],
            evaluation_confidence=evaluation_result["confidence"],
            processing_time_minutes=int(processing_time),
            evaluator_agent_id=self.agent_id,
            evaluation_timestamp=datetime.utcnow(),
            quantum_signature="",
        )

            # Add quantum signature
        evaluation_data = json.dumps(
            {
                "claim_id": claim_evaluation.claim_id,
                "approved_amount": str(claim_evaluation.approved_amount),
                "status": claim_evaluation.claim_status.value,
                "timestamp": claim_evaluation
                    .evaluation_timestamp.isoformat(),
            }
        )
        claim_evaluation.quantum_signature = (
            await self.quantum_signer.sign(evaluation_data)
        )

            # Log evaluation completion
        await self.audit_trail.log_event(
            event_type=AuditEventType.CLAIM_PROCESSED,
            entity_id=claim_evaluation.claim_id,
            description=f"Claim evaluation completed:"
                {evaluation_result['status'].value}","
            details={
                "approved_amount": str(claim_evaluation.approved_amount),
                "fraud_score": fraud_score,
                "processing_time_minutes": int(processing_time),
            },
            severity=AuditSeverity.MEDIUM,
        )

            logger.info(
            f"Claim evaluation completed: {evaluation_result['status']"
                .value}""
        )
        return claim_evaluation

        except Exception as e:
            logger.error(f"Claim evaluation failed: {str(e)}")
        raise

    async def _analyze_evidence(
        self, evidence_files: List[Dict[str, Any]]
) -> List[ClaimEvidence]:
        """Analyze all evidence files submitted with the claim."""
    evidence_analysis = []

        for evidence_file in evidence_files:
            try:
                evidence_type = EvidenceType(
                evidence_file.get("type", "document")
            )

                if evidence_type in [EvidenceType.PHOTO, EvidenceType.VIDEO]:
                    analysis = await self._analyze_visual_evidence(
                    evidence_file
                )
            elif evidence_type == EvidenceType.DOCUMENT:
                    analysis = await self._analyze_document_evidence(
                    evidence_file
                )
            elif evidence_type == EvidenceType.MEDICAL_RECORD:
                    analysis = await self._analyze_medical_evidence(
                    evidence_file
                )
            else:
                    analysis = await self._analyze_general_evidence(
                    evidence_file
                )

                evidence = ClaimEvidence(
                evidence_id=evidence_file.get("evidence_id", ""),
                evidence_type=evidence_type,
                content_hash=evidence_file.get("content_hash", ""),
                analysis_result=analysis,
                authenticity_score=analysis.get("authenticity_score", 0.8),
                relevance_score=analysis.get("relevance_score", 0.7),
                timestamp=datetime.utcnow(),
            )

                evidence_analysis.append(evidence)

            except Exception as e:
                logger.error(
                f"Evidence analysis failed for {evidence_file.get("
                    'evidence_id')}: {str(e)}""
            )
            continue

        return evidence_analysis

    async def _analyze_visual_evidence(
        self, evidence_file: Dict[str, Any]
) -> Dict[str, Any]:
        """Analyze photos and videos using computer vision."""
    try:
            # In production, use actual computer vision models
        # For now, provide mock analysis

            analysis = {
            "damage_detected": True,
            "damage_severity": np.random.uniform(0.3, 0.9),
            "damage_type": "collision_damage",
            "estimated_repair_cost": np.random.uniform(1000, 15000),
            "authenticity_indicators": {
                "metadata_consistent": True,
                "no_digital_manipulation": True,
                "lighting_consistent": True,
                "perspective_reasonable": True,
            },
            "objects_detected": ["vehicle", "damage", "street"],
            "authenticity_score": np.random.uniform(0.7, 0.95),
            "relevance_score": np.random.uniform(0.8, 0.95),
            "quality_score": np.random.uniform(0.6, 0.9),
        }

            # Simulate damage assessment
        if analysis["damage_severity"] > 0.7:
                analysis["damage_category"] = "severe"
        elif analysis["damage_severity"] > 0.4:
                analysis["damage_category"] = "moderate"
        else:
                analysis["damage_category"] = "minor"

            return analysis

        except Exception as e:
            logger.error(f"Visual evidence analysis failed: {str(e)}")
        return {
            "authenticity_score": 0.5,
            "relevance_score": 0.5,
            "analysis_error": str(e),
        }

    async def _analyze_document_evidence(
        self, evidence_file: Dict[str, Any]
) -> Dict[str, Any]:
        """Analyze document evidence using NLP and OCR."""
    try:
            # Mock document analysis
        analysis = {
            "document_type": "police_report",
            "key_information_extracted": {
                "incident_date": "2024-01-15",
                "incident_time": "14:30",
                "location": "Main St & 1st Ave",
                "parties_involved": 2,
                "fault_determination": "other_party",
            },
            "document_authenticity": {
                "official_format": True,
                "proper_signatures": True,
                "consistent_information": True,
                "valid_case_number": True,
            },
            "information_consistency": 0.9,
            "authenticity_score": 0.95,
            "relevance_score": 0.9,
        }

            return analysis

        except Exception as e:
            logger.error(f"Document evidence analysis failed: {str(e)}")
        return {
            "authenticity_score": 0.5,
            "relevance_score": 0.5,
            "analysis_error": str(e),
        }

    async def _analyze_medical_evidence(
        self, evidence_file: Dict[str, Any]
) -> Dict[str, Any]:
        """Analyze medical records and reports."""
    try:
            # Mock medical record analysis
        analysis = {
            "medical_findings": {
                "injury_type": "soft_tissue_injury",
                "injury_severity": "moderate",
                "treatment_required": True,
                "recovery_time_weeks": 6,
                "work_restrictions": True,
            },
            "provider_verification": {
                "licensed_provider": True,
                "valid_medical_license": True,
                "proper_documentation": True,
            },
            "treatment_consistency": {
                "appropriate_for_injury": True,
                "standard_care_protocol": True,
                "reasonable_costs": True,
            },
            "estimated_medical_costs": np.random.uniform(2000, 10000),
            "authenticity_score": 0.9,
            "relevance_score": 0.95,
        }

            return analysis

        except Exception as e:
            logger.error(f"Medical evidence analysis failed: {str(e)}")
        return {
            "authenticity_score": 0.5,
            "relevance_score": 0.5,
            "analysis_error": str(e),
        }

    async def _analyze_general_evidence(
        self, evidence_file: Dict[str, Any]
) -> Dict[str, Any]:
        """Analyze general evidence files."""
    return {
        "authenticity_score": 0.7,
        "relevance_score": 0.6,
        "analysis_type": "general",
    }

    async def _detect_fraud(
        self,
    claim_data: Dict[str, Any],
    policy_data: Dict[str, Any],
    evidence_analysis: List[ClaimEvidence],
) -> float:
        """Detect potential fraud indicators."""
    try:
            fraud_indicators = []

            # Timing-based indicators
        claim_date = datetime.fromisoformat(
            claim_data.get("incident_date", "2024-01-01")
        )
        policy_start = datetime.fromisoformat(
            policy_data.get("start_date", "2024-01-01")
        )
        days_since_policy_start = (claim_date - policy_start).days

            if days_since_policy_start < 30:
                fraud_indicators.append(("early_claim", 0.3))

            # Amount-based indicators
        claim_amount = float(claim_data.get("amount", 0))
        coverage_amount = float(policy_data.get("coverage_amount", 100000))
        amount_ratio = claim_amount / coverage_amount

            if amount_ratio > 0.8:
                fraud_indicators.append(("high_amount_ratio", 0.4))

            # Evidence quality indicators
        avg_authenticity = np.mean(
            [e.authenticity_score for e in evidence_analysis]
        )
        if avg_authenticity < 0.6:
                fraud_indicators.append(("low_evidence_quality", 0.5))

            # Historical claim pattern
        customer_claims = claim_data.get("customer_claim_history", [])
        if len(customer_claims) > 3:
                fraud_indicators.append(("frequent_claimant", 0.3))

            # Calculate overall fraud score
        if fraud_indicators:
                fraud_score = min(
                1.0, sum(weight for _, weight in fraud_indicators) / 2
            )
        else:
                fraud_score = 0.1  # Base fraud risk

            return fraud_score

        except Exception as e:
            logger.error(f"Fraud detection failed: {str(e)}")
        return 0.5

    async def _validate_claim_amount(
        self,
    claim_data: Dict[str, Any],
    policy_data: Dict[str, Any],
    evidence_analysis: List[ClaimEvidence],
) -> Dict[str, Any]:
        """Validate and estimate appropriate claim amount."""
    try:
            submitted_amount = Decimal(str(claim_data.get("amount", 0)))
        claim_type = claim_data.get("claim_type", "auto_accident")

            # Extract damage estimates from evidence
        damage_estimates = []
        for evidence in evidence_analysis:
                if "estimated_repair_cost" in evidence.analysis_result:
                    damage_estimates.append(
                    evidence.analysis_result["estimated_repair_cost"]
                )
            elif "estimated_medical_costs" in evidence.analysis_result:
                    damage_estimates.append(
                    evidence.analysis_result["estimated_medical_costs"]
                )

            if damage_estimates:
                ai_estimated_amount = Decimal(str(np.mean(damage_estimates)))
        else:
                # Use industry averages as fallback
            industry_averages = {
                "auto_accident": 8000,
                "home_damage": 12000,
                "health_medical": 5000,
                "business_liability": 15000,
            }
            ai_estimated_amount = Decimal(
                str(industry_averages.get(claim_type, 5000))
            )

            # Compare submitted vs estimated
        amount_variance = abs(
            submitted_amount - ai_estimated_amount
        ) / max(submitted_amount, ai_estimated_amount)

            # Determine evaluated amount
        if amount_variance < 0.2:  # Within 20%
                evaluated_amount = submitted_amount
            validation_confidence = 0.9
        elif amount_variance < 0.5:  # Within 50%
                evaluated_amount = (submitted_amount + ai_estimated_amount) / 2
            validation_confidence = 0.7
        else:  # Large variance
                evaluated_amount = ai_estimated_amount
            validation_confidence = 0.5

            return {
            "submitted_amount": submitted_amount,
            "ai_estimated_amount": ai_estimated_amount,
            "evaluated_amount": evaluated_amount,
            "amount_variance": float(amount_variance),
            "validation_confidence": validation_confidence,
            "damage_estimates": damage_estimates,
        }

        except Exception as e:
            logger.error(f"Amount validation failed: {str(e)}")
        return {
            "evaluated_amount": Decimal(str(claim_data.get("amount", 0))),
            "validation_confidence": 0.5,
        }

    async def _assess_authenticity(
        self, evidence_analysis: List[ClaimEvidence]
) -> float:
        """Assess overall authenticity of claim evidence."""
    try:
            if not evidence_analysis:
                return 0.5

            authenticity_scores = [
            e.authenticity_score for e in evidence_analysis
        ]
        relevance_scores = [e.relevance_score for e in evidence_analysis]

            # Weighted average with relevance as weight
        total_weight = sum(relevance_scores)
        if total_weight > 0:
                weighted_authenticity = (
                sum(
                    auth * rel
                    for auth, rel in zip(
                            authenticity_scores, relevance_scores
                    )
                )
                / total_weight
            )
        else:
                weighted_authenticity = np.mean(authenticity_scores)

            return min(0.99, max(0.01, weighted_authenticity))

        except Exception as e:
            logger.error(f"Authenticity assessment failed: {str(e)}")
        return 0.5

    async def _make_evaluation_decision(
        self,
    claim_data: Dict[str, Any],
    policy_data: Dict[str, Any],
    fraud_score: float,
    amount_validation: Dict[str, Any],
    authenticity_score: float,
) -> Dict[str, Any]:
        """Make final evaluation decision based on all factors."""
    try:
            evaluated_amount = amount_validation["evaluated_amount"]
        policy_limit = Decimal(
            str(policy_data.get("coverage_amount", 100000))
        )
        deductible = Decimal(str(policy_data.get("deductible", 500)))

            reasoning = []
        required_actions = []

            # Determine status based on fraud and authenticity scores
        if fraud_score > 0.7:
                status = ClaimStatus.REQUIRES_INVESTIGATION
            approved_amount = Decimal("0")
            reasoning.append(
                f"High fraud risk detected (score: {fraud_score:.2f})"
            )
            required_actions.append("Detailed investigation required")
            confidence = 0.9

            elif authenticity_score < 0.4:
                status = ClaimStatus.REQUIRES_INVESTIGATION
            approved_amount = Decimal("0")
            reasoning.append(
                f"Low evidence authenticity ("
                    score: {authenticity_score:.2f})""
            )
            required_actions.append("Additional evidence required")
            confidence = 0.85

            elif fraud_score > 0.5 or authenticity_score < 0.6:
                status = ClaimStatus.UNDER_REVIEW
            approved_amount = min(
                evaluated_amount * Decimal("0.8"),
                policy_limit - deductible,
            )
            reasoning.append("Moderate risk factors require manual review")
            required_actions.append("Senior adjuster review required")
            confidence = 0.7

            else:
                # Calculate final approved amount
            if evaluated_amount <= policy_limit:
                    approved_amount = max(
                    Decimal("0"), evaluated_amount - deductible
                )
                if approved_amount == evaluated_amount - deductible:
                        status = ClaimStatus.APPROVED
                    reasoning.append("Claim meets all approval criteria")
                else:
                        status = ClaimStatus.PARTIALLY_APPROVED
                    reasoning.append("Claim approved within policy limits")
            else:
                    approved_amount = max(
                    Decimal("0"), policy_limit - deductible
                )
                status = ClaimStatus.PARTIALLY_APPROVED
                reasoning.append("Claim amount exceeds policy limit")

                confidence = 0.9

            # Add specific reasoning
        if amount_validation.get("amount_variance", 0) > 0.3:
                reasoning.append(
                "Significant variance between submitted and "
                    estimated amounts""
            )

            if authenticity_score > 0.8:
                reasoning.append("High-quality evidence supports claim")

            return {
            "status": status,
            "approved_amount": approved_amount,
            "reasoning": reasoning,
            "required_actions": required_actions,
            "confidence": confidence,
        }

        except Exception as e:
            logger.error(f"Evaluation decision failed: {str(e)}")
        return {
            "status": ClaimStatus.UNDER_REVIEW,
            "approved_amount": Decimal("0"),
            "reasoning": ["Error in evaluation process"],
            "required_actions": ["Manual review required"],
            "confidence": 0.3,
        }

    async def process_auto_settlement(
        self, claim_evaluation: ClaimEvaluation
) -> Dict[str, Any]:
        """Process automatic settlement for eligible claims."""
    try:
            # Check eligibility for auto-settlement
        if (
                claim_evaluation.claim_status == ClaimStatus.APPROVED
            and claim_evaluation.fraud_risk_score < 0.3
            and claim_evaluation.evaluation_confidence > 0.85
            and claim_evaluation.approved_amount < Decimal("10000")
        ):

                # Process automatic settlement
            settlement_result = {
                "auto_settlement": True,
                "settlement_amount": claim_evaluation.approved_amount,
                "settlement_method": "direct_deposit",
                "estimated_payment_days": 2,
                "settlement_reference": f"AUTO_{claim_evaluation"
                    .claim_id}_{datetime.utcnow().strftime('%Y%m%d')}","
            }

                # Log auto-settlement
            await self.audit_trail.log_event(
                event_type=AuditEventType.CLAIM_PAID,
                entity_id=claim_evaluation.claim_id,
                description=f"Automatic settlement processed:"
                    ${claim_evaluation.approved_amount}","
                details=settlement_result,
                severity=AuditSeverity.MEDIUM,
            )

                return settlement_result
        else:
                return {
                "auto_settlement": False,
                "reason": "Does not meet auto-settlement criteria",
                "requires_manual_processing": True,
            }

        except Exception as e:
            logger.error(f"Auto-settlement processing failed: {str(e)}")
        return {"auto_settlement": False, "error": str(e)}

    async def generate_claim_report(
        self, claim_evaluation: ClaimEvaluation
) -> Dict[str, Any]:
        """Generate comprehensive claim evaluation report."""
    try:
            report = {
            "claim_summary": {
                "claim_id": claim_evaluation.claim_id,
                "policy_id": claim_evaluation.policy_id,
                "claim_type": claim_evaluation.claim_type.value,
                "submitted_amount": str(claim_evaluation.submitted_amount),
                "approved_amount": str(claim_evaluation.approved_amount),
                "status": claim_evaluation.claim_status.value,
            },
            "evaluation_metrics": {
                "fraud_risk_score": claim_evaluation.fraud_risk_score,
                "authenticity_score": claim_evaluation.authenticity_score,
                "evaluation_confidence": claim_evaluation
                    .evaluation_confidence,
                "processing_time_minutes": claim_evaluation
                    .processing_time_minutes,
            },
            "evidence_summary": {
                "total_evidence_pieces": len(
                    claim_evaluation.evidence_analysis
                ),
                "evidence_types": list(
                    set(
                        e.evidence_type.value
                        for e in claim_evaluation.evidence_analysis
                        )
                ),
                "average_authenticity": np.mean(
                    [
                        e.authenticity_score
                        for e in claim_evaluation.evidence_analysis
                        ]
                ),
                "average_relevance": np.mean(
                    [
                        e.relevance_score
                        for e in claim_evaluation.evidence_analysis
                        ]
                ),
            },
            "decision_reasoning": claim_evaluation.evaluation_reasoning,
            "required_actions": claim_evaluation.required_actions,
            "blockchain_verification": {
                "quantum_signature": claim_evaluation.quantum_signature,
                "evaluation_timestamp": claim_evaluation
                    .evaluation_timestamp.isoformat(),
                "evaluator_agent": claim_evaluation.evaluator_agent_id,
            },
        }

            return report

        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
        return {"error": str(e), "claim_id": claim_evaluation.claim_id}
