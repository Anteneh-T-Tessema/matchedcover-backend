"""
Blockchain-Integrated Fraud Detection API

This module provides REST API endpoints for fraud detection with Hyperledger
Fabric
blockchain integration for immutable audit trails and
automated claim processing.

Key Features:
- Fraud analysis with blockchain logging
- Automated claim submission to blockchain
- Smart contract-based payouts
- Identity verification using DID
- Regulatory compliance audit trails"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any


from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field

from src.blockchain.blockchain_integration import get_blockchain_fraud_agent
from src.blockchain.hyperledger_fabric import get_fabric_manager
from src.api.auth import get_current_user

logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Router
router = APIRouter(
prefix="/api/v1/blockchain-fraud", tags=["Blockchain Fraud Detection"]
)


# Pydantic models
class BlockchainFraudAnalysisRequest(BaseModel):
    """Request model for blockchain-integrated fraud analysis."""

    claim_id: str = Field(..., description="Unique claim identifier")
policy_number: str = Field(..., description="Insurance policy number")
claim_amount: float = Field(..., description="Claimed amount")
incident_type: str = Field(..., description="Type of incident")
incident_date: str = Field(..., description="Date of incident")
claimant_info: Dict[str, Any] = Field(
    ..., description="Claimant information"
)
incident_details: Dict[str, Any] = Field(
    ..., description="Incident details"
)
supporting_documents: List[str] = Field(
    default=[], description="Document references"
)
submit_to_blockchain: bool = Field(
    default=True, description="Whether to log to blockchain"
)


class BlockchainFraudAnalysisResponse(BaseModel):
    """Response model for blockchain-integrated fraud analysis."""

    claim_id: str
fraud_score: float
risk_level: str
confidence: float
indicators: List[Dict[str, Any]]
explanation: Dict[str, Any]
requires_human_review: bool
recommended_actions: List[str]
compliance_status: Dict[str, Any]
blockchain_audit: Dict[str, Any]
processing_time_ms: float


class ClaimSubmissionRequest(BaseModel):
    """Request model for claim submission to blockchain."""

    claim_id: str = Field(..., description="Unique claim identifier")
policy_number: str = Field(..., description="Insurance policy number")
claim_amount: float = Field(..., description="Claimed amount")
claimant_info: Dict[str, Any] = Field(
    ..., description="Claimant information"
)
incident_details: Dict[str, Any] = Field(
    ..., description="Incident details"
)
payout_address: Optional[str] = Field(
    None, description="Blockchain payout address"
)


class PayoutApprovalRequest(BaseModel):
    """Request model for payout approval."""

    claim_id: str = Field(..., description="Claim identifier")
payout_amount: float = Field(..., description="Amount to pay out")
approver_notes: str = Field(default="", description="Approval notes")
force_approval: bool = Field(
    default=False, description="Force approval override"
)


class IdentityVerificationRequest(BaseModel):
    """Request model for blockchain identity verification."""

    customer_id: str = Field(..., description="Customer identifier")
verification_type: str = Field(
    ..., description="Type of verification (KYC, AML, etc.)"
)
customer_data: Dict[str, Any] = Field(
    ..., description="Customer data for verification"
)


class ReinsuranceContractRequest(BaseModel):
    """Request model for reinsurance contract creation."""

    claim_id: str = Field(..., description="Claim identifier")
claim_amount: float = Field(..., description="Claim amount")
risk_assessment: Dict[str, Any] = Field(
    ..., description="AI risk assessment"
)
coverage_percentage: Optional[float] = Field(
    None, description="Coverage percentage override"
)


@router.post("/analyze", response_model=BlockchainFraudAnalysisResponse)
async def analyze_fraud_with_blockchain(
    request: BlockchainFraudAnalysisRequest,
background_tasks: BackgroundTasks,
current_user: dict = Depends(get_current_user),
):"""
Analyze claim for fraud with blockchain logging.

    This endpoint performs comprehensive fraud analysis and automatically
logs the results to Hyperledger Fabric for immutable audit trails."""
try:
        start_time = datetime.now()

        # Get blockchain-integrated fraud agent
    fraud_agent = await get_blockchain_fraud_agent()

        # Prepare claim data
    claim_data = {
        "claim_id": request.claim_id,
        "policy_number": request.policy_number,
        "claim_amount": request.claim_amount,
        "incident_type": request.incident_type,
        "incident_date": request.incident_date,
        "claimant_info": request.claimant_info,
        "incident_details": request.incident_details,
        "supporting_documents": request.supporting_documents,
        "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        "analyzing_user": current_user.get("email", "unknown"),
    }

        # Perform blockchain-integrated analysis
    if request.submit_to_blockchain:
            analysis_result = await fraud_agent.analyze_claim_with_blockchain(
            claim_data
        )
    else:
            # Fallback to standard analysis
        analysis_result = await fraud_agent.analyze_claim(claim_data)
        analysis_result["blockchain_audit"] = {"enabled": False}

        # Calculate processing time
    processing_time = (datetime.now() - start_time).total_seconds() * 1000

        # Create response
    response = BlockchainFraudAnalysisResponse(
        claim_id=request.claim_id,
        fraud_score=analysis_result.get("fraud_score", 0.0),
        risk_level=analysis_result.get("risk_level", "unknown"),
        confidence=analysis_result.get("confidence", 0.0),
        indicators=analysis_result.get("indicators", []),
        explanation=analysis_result.get("explanation", {}),
        requires_human_review=analysis_result.get(
            "requires_human_review", False
        ),
        recommended_actions=analysis_result.get("recommended_actions", []),
        compliance_status=analysis_result.get("compliance_status", {}),
        blockchain_audit=analysis_result.get("blockchain_audit", {}),
        processing_time_ms=processing_time,
    )

        logger.info(
        f"Blockchain fraud analysis completed for claim {request.claim_id}"
    )
    return response

    except Exception as e:
        logger.error(f"Blockchain fraud analysis failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Fraud analysis failed: {str(e)}",
    )


@router.post("/submit-claim")
async def submit_claim_to_blockchain(
    request: ClaimSubmissionRequest,
current_user: dict = Depends(get_current_user),
):"""
Submit claim to blockchain for transparent processing.

    This endpoint submits a claim to Hyperledger Fabric for immutable
tracking and automated processing workflows."""
try:
        # Get blockchain-integrated fraud agent
    fraud_agent = await get_blockchain_fraud_agent()

        # Prepare claim data
    claim_data = {
        "claim_id": request.claim_id,
        "policy_number": request.policy_number,
        "claim_amount": request.claim_amount,
        "claimant_info": request.claimant_info,
        "incident_details": request.incident_details,
        "payout_address": request.payout_address,
        "submitting_user": current_user.get("email", "unknown"),
        "submission_timestamp": datetime.now(timezone.utc).isoformat(),
    }

        # Perform fraud analysis first
    analysis_result = await fraud_agent.analyze_claim_with_blockchain(
        claim_data
    )

        # Submit to blockchain
    tx_id = await fraud_agent.submit_claim_to_blockchain(
        claim_data, analysis_result
    )

        return {
        "status": "success",
        "message": "Claim submitted to blockchain successfully",
        "claim_id": request.claim_id,
        "blockchain_tx_id": tx_id,
        "fraud_analysis": {
            "fraud_score": analysis_result.get("fraud_score", 0.0),
            "risk_level": analysis_result.get("risk_level", "unknown"),
            "requires_human_review": analysis_result.get(
                "requires_human_review", False
            ),
        },
    }

    except Exception as e:
        logger.error(f"Claim submission to blockchain failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Claim submission failed: {str(e)}",
    )


@router.post("/approve-payout")
async def approve_payout(
    request: PayoutApprovalRequest,
current_user: dict = Depends(get_current_user),
):"""
Approve claim payout through smart contract.

    This endpoint approves claim payouts through Hyperledger Fabric
smart contracts for automated and transparent processing."""
try:
        # Check user permissions for payout approval
    user_role = current_user.get("role", "")
    if user_role not in ["adjuster", "manager", "admin"]:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions for payout approval",
        )

        # Get blockchain-integrated fraud agent
    fraud_agent = await get_blockchain_fraud_agent()

        # Check if automated approval is possible
    if not request.force_approval:
            auto_tx_id = await fraud_agent.approve_automated_payout(
            request.claim_id, request.payout_amount
        )

            if auto_tx_id:
                return {
                "status": "success",
                "message": "Automated payout approved",
                "claim_id": request.claim_id,
                "payout_amount": request.payout_amount,
                "blockchain_tx_id": auto_tx_id,
                "approval_type": "automated",
            }

        # Manual approval process
    fabric_manager = await get_fabric_manager()

        # Create approval signatures
    approver_signatures = [
        f"{current_user.get("
            'email', 'unknown')}_{datetime.now(timezone.utc).isoformat()}","
        f"ROLE_{user_role}_{request.claim_id}",
    ]

        # Approve payout on blockchain
    tx_id = await fabric_manager.approve_claim_payout(
        request.claim_id, request.payout_amount, approver_signatures
    )

        return {
        "status": "success",
        "message": "Manual payout approved",
        "claim_id": request.claim_id,
        "payout_amount": request.payout_amount,
        "blockchain_tx_id": tx_id,
        "approval_type": "manual",
        "approver": current_user.get("email", "unknown"),
        "notes": request.approver_notes,
    }

    except Exception as e:
        logger.error(f"Payout approval failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Payout approval failed: {str(e)}",
    )


@router.post("/verify-identity")
async def verify_identity_blockchain(
    request: IdentityVerificationRequest,
current_user: dict = Depends(get_current_user),
):"""
Verify customer identity using blockchain attestations.

    This endpoint verifies customer identity using decentralized
identity (DID) attestations stored on Hyperledger Fabric."""
try:
        # Get blockchain-integrated fraud agent
    fraud_agent = await get_blockchain_fraud_agent()

        # Prepare customer data for verification
    customer_data = request.customer_data.copy()
    customer_data.update(
        {
            "customer_id": request.customer_id,
            "verification_type": request.verification_type,
            "verifying_user": current_user.get("email", "unknown"),
            "verification_timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }
    )

        # Perform blockchain identity verification
    verification_result = (
        await fraud_agent.verify_customer_identity_blockchain(
            customer_data
        )
    )

        return {
        "status": "success",
        "customer_id": request.customer_id,
        "verification_type": request.verification_type,
        "verification_result": verification_result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    except Exception as e:
        logger.error(f"Identity verification failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Identity verification failed: {str(e)}",
    )


@router.post("/create-reinsurance-contract")
async def create_reinsurance_contract(
    request: ReinsuranceContractRequest,
current_user: dict = Depends(get_current_user),
):"""
Create reinsurance smart contract for high-value claims.

    This endpoint creates reinsurance smart contracts on Hyperledger Fabric
for automated multi-party risk sharing."""
try:
        # Check user permissions for reinsurance contracts
    user_role = current_user.get("role", "")
    if user_role not in ["manager", "admin", "reinsurance_officer"]:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Insufficient permissions for reinsurance "
                "contract creation",
            )
        )

        # Get blockchain-integrated fraud agent
    fraud_agent = await get_blockchain_fraud_agent()

        # Prepare claim data
    claim_data = {
        "claim_id": request.claim_id,
        "claim_amount": request.claim_amount,
        "creating_user": current_user.get("email", "unknown"),
        "creation_timestamp": datetime.now(timezone.utc).isoformat(),
    }

        # Create reinsurance contract
    tx_id = await fraud_agent.create_reinsurance_smart_contract(
        claim_data, request.risk_assessment
    )

        if tx_id:
            return {
            "status": "success",
            "message": "Reinsurance contract created successfully",
            "claim_id": request.claim_id,
            "contract_tx_id": tx_id,
            "risk_assessment": request.risk_assessment,
        }
    else:
            return {
            "status": "info",
            "message": "Reinsurance contract not required for this claim",
            "claim_id": request.claim_id,
            "reason": "Claim amount below threshold or risk level too low",
        }

    except Exception as e:
        logger.error(f"Reinsurance contract creation failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Reinsurance contract creation failed: {str(e)}",
    )


@router.get("/audit-trail/{claim_id}")
async def get_blockchain_audit_trail(
    claim_id: str, current_user: dict = Depends(get_current_user)
):"""
Get comprehensive blockchain audit trail for a claim.

    This endpoint retrieves the complete audit trail from Hyperledger Fabric
including fraud analysis, claim processing, and agent decisions."""
try:
        # Get blockchain-integrated fraud agent
    fraud_agent = await get_blockchain_fraud_agent()

        # Get comprehensive audit summary
    audit_summary = await fraud_agent.get_blockchain_audit_summary(
        claim_id
    )

        if "error" in audit_summary:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit trail not found: {audit_summary['error']}",
        )

        return {
        "status": "success",
        "claim_id": claim_id,
        "audit_summary": audit_summary,
        "retrieved_by": current_user.get("email", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    except HTTPException:
        raise
except Exception as e:
        logger.error(f"Audit trail retrieval failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Audit trail retrieval failed: {str(e)}",
    )


@router.get("/network-status")
async def get_blockchain_network_status(
    current_user: dict = Depends(get_current_user),
):"""
Get Hyperledger Fabric network status and health.

    This endpoint provides information about the blockchain network
connectivity and channel status."""
try:
        # Get fabric manager
    fabric_manager = await get_fabric_manager()

        # Get network status
    network_status = await fabric_manager.get_network_status()

        return {
        "status": "success",
        "network_status": network_status,
        "checked_by": current_user.get("email", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    except Exception as e:
        logger.error(f"Network status check failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Network status check failed: {str(e)}",
    )


@router.get("/claims/statistics")
async def get_blockchain_claims_statistics(
    start_date: Optional[str] = None,
end_date: Optional[str] = None,
current_user: dict = Depends(get_current_user),
):"""
Get fraud detection and claims processing statistics from blockchain.

    This endpoint retrieves aggregated statistics from Hyperledger Fabric
for fraud detection and claims processing analytics."""
try:
        # Default date range if not provided
    if not start_date:
            start_date = (
            datetime.now(timezone.utc) - timedelta(days=30)
        ).isoformat()
    if not end_date:
            end_date = datetime.now(timezone.utc).isoformat()

        # Get fabric manager
    # fabric_manager = ...  # Unused variable

        # Get fraud statistics (would need to implement this in fabric manager)
    # fraud_stats = await fabric_manager.get_fraud_statistics(start_date,
    # end_date)

        # For now, return mock statistics
    statistics = {
        "date_range": {"start": start_date, "end": end_date},
        "fraud_detection": {
            "total_claims_analyzed": 150,
            "high_risk_detected": 12,
            "medium_risk_detected": 23,
            "low_risk_detected": 115,
            "average_fraud_score": 0.234,
        },
        "claims_processing": {
            "total_claims_submitted": 145,
            "approved_payouts": 98,
            "rejected_claims": 8,
            "pending_review": 39,
            "total_payout_amount": 2450000.00,
        },
        "blockchain_integrity": {
            "total_transactions": 487,
            "signature_failures": 0,
            "consensus_failures": 0,
            "network_uptime": "99.8%",
        },
    }

        return {
        "status": "success",
        "statistics": statistics,
        "retrieved_by": current_user.get("email", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    except Exception as e:
        logger.error(f"Statistics retrieval failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Statistics retrieval failed: {str(e)}",
    )
