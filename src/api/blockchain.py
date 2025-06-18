"""
Blockchain API endpoints for MatchedCover Insurance Platform.

Provides REST API endpoints for blockchain operations including
smart contract interactions, policy management,
and quantum-resistant signatures."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.blockchain.smart_contracts import (
SmartPolicyContract,
PolicyTerms,
ClaimData,
ClaimStatus,
)
from src.blockchain.audit_trail import (
BlockchainAuditTrail,
AuditEventType,
AuditSeverity,
)
from src.quantum.crypto import QuantumResistantSigner

router = APIRouter(prefix="/api/v1/blockchain", tags=["Blockchain"])


# Request/Response Models
class PolicyCreationRequest(BaseModel):
    """Request model for creating a blockchain policy."""

    customer_id: str = Field(..., description="Customer identifier")
coverage_amount: Decimal = Field(..., description="Coverage amount")
premium: Decimal = Field(..., description="Premium amount")
deductible: Decimal = Field(..., description="Deductible amount")
policy_type: str = Field(..., description="Type of insurance policy")
coverage_details: Dict[str, Any] = Field(
    ..., description="Coverage details"
)
exclusions: List[str] = Field(default=[], description="Policy exclusions")
duration_months: int = Field(..., description="Policy duration in months")
customer_signature: str = Field(
    ..., description="Customer's quantum signature"
)


class ClaimSubmissionRequest(BaseModel):
    """Request model for submitting a blockchain claim."""

    policy_id: str = Field(..., description="Policy identifier")
claim_amount: Decimal = Field(..., description="Claim amount")
description: str = Field(..., description="Claim description")
evidence_files: List[str] = Field(
    default=[], description="Evidence file hashes"
)
customer_signature: str = Field(
    ..., description="Customer's quantum signature"
)


class PolicyResponse(BaseModel):
    """Response model for policy operations."""

    policy_id: str
transaction_hash: str
block_number: int
status: str
quantum_signature: str


class ClaimResponse(BaseModel):
    """Response model for claim operations."""

    claim_id: str
transaction_hash: str
block_number: int
status: str
estimated_processing_time: str


class AuditTrailRequest(BaseModel):
    """Request model for audit trail queries."""

    entity_id: Optional[str] = None
event_type: Optional[str] = None
start_date: Optional[datetime] = None
end_date: Optional[datetime] = None
compliance_tag: Optional[str] = None


class ComplianceReportRequest(BaseModel):
    """Request model for compliance reports."""

    compliance_standard: str = Field(..., description="GDPR, HIPAA, SOX, etc.")
start_date: datetime = Field(..., description="Report start date")
end_date: datetime = Field(..., description="Report end date")


# Initialize blockchain services
smart_contract = SmartPolicyContract()
audit_trail = BlockchainAuditTrail()
quantum_signer = QuantumResistantSigner()


@router.post("/policies", response_model=PolicyResponse)
async def create_policy(request: PolicyCreationRequest):"""
Create a new insurance policy on the blockchain.

    This endpoint creates a smart contract-based insurance policy with
quantum-resistant signatures for maximum security and transparency."""
try:
        # Create policy terms
    policy_terms = PolicyTerms(
        coverage_amount=request.coverage_amount,
        premium=request.premium,
        deductible=request.deductible,
        policy_type=request.policy_type,
        coverage_details=request.coverage_details,
        exclusions=request.exclusions,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow().replace(
            month=datetime.utcnow().month + request.duration_months
        ),
    )

        # Create policy on blockchain
    result = await smart_contract.create_policy(
        customer_id=request.customer_id,
        policy_terms=policy_terms,
        customer_signature=request.customer_signature,
    )

        # Log audit event
    await audit_trail.log_event(
        event_type=AuditEventType.POLICY_CREATED,
        entity_id=result["policy_id"],
        description=f"New {request.policy_type} policy created for customer"
            {request.customer_id}","
        details={
            "coverage_amount": str(request.coverage_amount),
            "premium": str(request.premium),
            "policy_type": request.policy_type,
            "blockchain_tx": result["transaction_hash"],
        },
        severity=AuditSeverity.MEDIUM,
        compliance_tags=["GDPR", "SOX"],
    )

        return PolicyResponse(
        policy_id=result["policy_id"],
        transaction_hash=result["transaction_hash"],
        block_number=result["block_number"],
        status=result["status"],
        quantum_signature=result["quantum_signature"],
    )

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Failed to create policy: {str(e)}",
    )


@router.post("/claims", response_model=ClaimResponse)
async def submit_claim(request: ClaimSubmissionRequest):"""
Submit an insurance claim to the blockchain.

    This endpoint allows customers to submit claims that are recorded
immutably on the blockchain with quantum-resistant authentication."""
try:
        # Create claim data
    claim_data = ClaimData(
        claim_id=f"CLM_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        policy_id=request.policy_id,
        claim_amount=request.claim_amount,
        description=request.description,
        evidence_hashes=request.evidence_files,
        timestamp=datetime.utcnow(),
        status=ClaimStatus.SUBMITTED,  # This would need to be imported
    )

        # Submit claim to blockchain
    result = await smart_contract.submit_claim(
        policy_id=request.policy_id,
        claim_data=claim_data,
        customer_signature=request.customer_signature,
    )

        # Log audit event
    await audit_trail.log_event(
        event_type=AuditEventType.CLAIM_SUBMITTED,
        entity_id=result["claim_id"],
        description=f"Claim submitted for policy {request.policy_id}",
        details={
            "claim_amount": str(request.claim_amount),
            "evidence_count": len(request.evidence_files),
            "blockchain_tx": result["transaction_hash"],
        },
        severity=AuditSeverity.MEDIUM,
        compliance_tags=["HIPAA", "SOX"],
    )

        return ClaimResponse(
        claim_id=result["claim_id"],
        transaction_hash=result["transaction_hash"],
        block_number=result["block_number"],
        status=result["status"],
        estimated_processing_time=result["estimated_processing_time"],
    )

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Failed to submit claim: {str(e)}",
    )


@router.get("/policies/{policy_id}")
async def get_policy(policy_id: str):"""
Retrieve policy details from the blockchain.

    Returns comprehensive policy information including blockchain
transaction details and verification status."""
try:
        policy = await smart_contract.get_policy(policy_id)
    if not policy:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )

        # Verify policy integrity
    is_valid = await smart_contract.verify_policy_integrity(policy_id)

        policy["integrity_verified"] = is_valid
    policy["quantum_secure"] = True

        return policy

    except HTTPException:
        raise
except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to retrieve policy: {str(e)}",
    )


@router.get("/policies/{policy_id}/claims")
async def get_policy_claims(policy_id: str):"""
Get all claims for a specific policy.

    Returns the complete claim history for a policy from the blockchain."""
try:
        claims = await smart_contract.get_claim_history(policy_id)
    return {
        "policy_id": policy_id,
        "total_claims": len(claims),
        "claims": claims,
    }

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to retrieve claims: {str(e)}",
    )


@router.post("/audit/events")
async def get_audit_trail(request: AuditTrailRequest):"""
Retrieve audit trail events with filtering.

    Provides access to the immutable blockchain audit trail with
various filtering options for compliance and investigation purposes."""
try:
        events = await audit_trail.get_audit_trail(
        entity_id=request.entity_id,
        event_type=(
            AuditEventType(request.event_type)
            if request.event_type
                else None
        ),
        start_date=request.start_date,
        end_date=request.end_date,
        compliance_tag=request.compliance_tag,
    )

        return {
        "total_events": len(events),
        "events": [
            {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "timestamp": event.timestamp.isoformat(),
                "entity_id": event.entity_id,
                "description": event.description,
                "severity": event.severity.value,
                "compliance_tags": event.compliance_tags,
            }
            for event in events
            ],
    }

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to retrieve audit trail: {str(e)}",
    )


@router.post("/compliance/report")
async def generate_compliance_report(request: ComplianceReportRequest):"""
Generate a compliance report for regulatory requirements.

    Creates comprehensive compliance reports for standards like
GDPR, HIPAA, SOX, etc., with blockchain verification."""
try:
        report = await audit_trail.generate_compliance_report(
        compliance_standard=request.compliance_standard,
        start_date=request.start_date,
        end_date=request.end_date,
    )

        return report

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to generate compliance report: {str(e)}",
    )


@router.get("/blockchain/integrity")
async def verify_blockchain_integrity():"""
Verify the integrity of the entire blockchain.

    Performs comprehensive verification of all blocks, signatures,
and hash chains to ensure data integrity."""
try:
        verification_result = await audit_trail.verify_blockchain_integrity()
    return verification_result

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to verify blockchain integrity: {str(e)}",
    )


@router.post("/quantum/keypair/{entity_id}")
async def generate_quantum_keypair(entity_id: str):"""
Generate a quantum-resistant key pair for an entity.

    Creates new post-quantum cryptographic keys for enhanced security."""
try:
        key_pair = quantum_signer.generate_key_pair(entity_id)

        return {
        "entity_id": entity_id,
        "algorithm": key_pair.algorithm.value,
        "public_key": key_pair.public_key.hex(),
        "created_at": key_pair.created_at.isoformat(),
        "expires_at": (
            key_pair.expires_at.isoformat()
            if key_pair.expires_at
                else None
        ),
    }

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to generate key pair: {str(e)}",
    )


@router.post("/quantum/sign")
async def quantum_sign_message(message: str, entity_id: str = "platform"):"""
Create a quantum-resistant digital signature for a message.

    Uses post-quantum cryptographic algorithms to create tamper-proof
    signatures."""
try:
        signature = await quantum_signer.sign(message, entity_id)

        return {
        "message": message,
        "entity_id": entity_id,
        "signature": signature,
        "algorithm": "quantum_resistant",
        "timestamp": datetime.utcnow().isoformat(),
    }

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to sign message: {str(e)}",
    )


@router.post("/quantum/verify")
async def quantum_verify_signature(
    message: str, signature: str, entity_id: str
):"""
Verify a quantum-resistant digital signature.

    Validates the authenticity and integrity of quantum-resistant signatures."""
try:
        is_valid = await quantum_signer.verify(message, signature, entity_id)

        return {
        "message": message,
        "entity_id": entity_id,
        "signature_valid": is_valid,
        "verified_at": datetime.utcnow().isoformat(),
    }

    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to verify signature: {str(e)}",
    )
