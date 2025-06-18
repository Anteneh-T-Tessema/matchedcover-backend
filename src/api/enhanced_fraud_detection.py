"""
Enhanced Fraud Detection API Router for MatchedCover.

Provides enterprise-grade fraud detection endpoints with compliance,
explainability, and human-in-the-loop capabilities."""

from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator
import logging
import uuid

from src.agents.enhanced_fraud_detection_agent import (
EnhancedFraudDetectionAgent,
AccessContext,
FraudRiskLevel,
DecisionStatus,
)

logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Router
router = APIRouter(
prefix="/api/v1/fraud-detection", tags=["Enhanced Fraud Detection"]
)

# Global agent instance
fraud_agent = None


# Pydantic models for API


class FraudAnalysisRequest(BaseModel):
    """Request model for fraud analysis."""

    entity_data: Dict[str, Any] = Field(
    ..., description="Data to analyze for fraud"
)
analysis_type: str = Field(
    default="general",
    description="Type of fraud analysis",
    pattern=(
        r"^(claim_fraud|application_fraud|identity_fraud|"
        r"premium_fraud|behavioral_analysis|general)$"
    ),
)
require_explanation: bool = Field(
    default=True, description="Whether to generate AI explanation"
)
user_context: Dict[str, str] = Field(
    default_factory=dict, description="User context information"
)

    @field_validator("entity_data")
@classmethod
def validate_entity_data(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        if not v:
            raise ValueError("Entity data cannot be empty")
    return v


class HumanReviewDecisionRequest(BaseModel):
    """Request model for human review decisions."""

    review_request_id: str = Field(..., description="ID of the review request")
decision: str = Field(
    ...,
    description="Review decision",
    pattern=r"^(approve|reject|escalate|request_more_info)$",
)
notes: str = Field(..., description="Reviewer notes", min_length=10)
override_fraud_score: Optional[float] = Field(
    None, description="Override fraud score if applicable", ge=0.0, le=1.0
)


class ModelPerformanceRequest(BaseModel):
    """Request model for model performance evaluation."""

    model_id: str = Field(..., description="Model identifier")
date_range: Optional[Dict[str, str]] = Field(
    None, description="Date range for performance evaluation"
)
include_drift_analysis: bool = Field(
    default=True, description="Include model drift analysis"
)


class ComplianceReportRequest(BaseModel):
    """Request model for compliance reports."""

    report_type: str = Field(
    ...,
    description="Type of compliance report",
    pattern=r"^(glba|fcra|naic|full_compliance|audit_trail)$",
)
date_range: Dict[str, str] = Field(
    ..., description="Date range for report"
)
include_sensitive_data: bool = Field(
    default=False, description="Include sensitive data in report"
)


# Response models


class FraudAnalysisResponse(BaseModel):
    """Response model for fraud analysis."""

    fraud_score: float = Field(..., description="Fraud score (0.0 to 1.0)")
risk_level: str = Field(..., description="Risk level classification")
decision_status: str = Field(..., description="Decision status")
indicators: List[Dict[str, Any]] = Field(
    ..., description="Fraud indicators"
)
explanation: Optional[Dict[str, Any]] = Field(
    None, description="AI explanation"
)
compliance_metadata: Dict[str, Any] = Field(
    ..., description="Compliance information"
)
human_review_required: bool = Field(
    ..., description="Whether human review is required"
)
recommended_actions: List[str] = Field(
    ..., description="Recommended actions"
)
audit_id: str = Field(..., description="Audit trail identifier")
processing_time_ms: float = Field(
    ..., description="Processing time in milliseconds"
)
quantum_signature: str = Field(
    ..., description="Quantum-resistant signature"
)


class HumanReviewResponse(BaseModel):
    """Response model for human review operations."""

    review_request_id: str
status: str
assigned_reviewer: Optional[str] = None
priority: str
deadline: Optional[datetime] = None
fraud_score: float
risk_level: str
created_at: datetime


class ModelPerformanceResponse(BaseModel):
    """Response model for model performance."""

    model_performance: Dict[str, Any]
decision_metrics: Dict[str, int]
compliance_status: str
recommendations: List[str]
report_timestamp: datetime


class ComplianceReportResponse(BaseModel):
    """Response model for compliance reports."""

    report_id: str
report_type: str
compliance_status: str
violations: List[Dict[str, Any]]
recommendations: List[str]
generated_at: datetime


# Dependency functions


async def get_fraud_agent() -> EnhancedFraudDetectionAgent:
    """Get the fraud detection agent instance."""
global fraud_agent
if fraud_agent is None:
        fraud_agent = EnhancedFraudDetectionAgent()
    await fraud_agent.initialize()
return fraud_agent


async def get_access_context(
    request: Request,
credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AccessContext:
    """Extract access context from request."""
# In production, validate JWT token and extract user information
# For now, simulate user context

    return AccessContext(
    user_id=request.headers.get("X-User-ID", "anonymous"),
    user_role=request.headers.get("X-User-Role", "analyst"),
    permissions=request.headers.get(
        "X-Permissions", "fraud_detection"
    ).split(","),
    access_level=request.headers.get("X-Access-Level", "basic"),
    department=request.headers.get("X-Department", "fraud_prevention"),
    request_id=str(uuid.uuid4()),
    session_id=request.headers.get("X-Session-ID", str(uuid.uuid4())),
)


# API Endpoints


@router.post("/analyze", response_model=FraudAnalysisResponse)
async def analyze_fraud(
    request: FraudAnalysisRequest,
access_context: AccessContext = Depends(get_access_context),
agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
):"""
Perform comprehensive fraud analysis with compliance and explainability.

    This endpoint provides enterprise-grade fraud detection with:
    - Regulatory compliance (GLBA, FCRA)
- Explainable AI results
- Human-in-the-loop workflows
- Audit logging
- Data privacy protection"""
try:
        start_time = datetime.now(timezone.utc)

        # Perform fraud analysis
    result = await agent.analyze_fraud_with_compliance(
        entity_data=request.entity_data,
        access_context=access_context,
        analysis_type=request.analysis_type,
        require_explanation=request.require_explanation,
    )

        processing_time = (
        datetime.now(timezone.utc) - start_time
    ).total_seconds() * 1000

        # Determine decision status
    fraud_score = result["fraud_analysis"]["fraud_score"]
    human_review = result.get("human_review") is not None

        if fraud_score >= 0.9:
            decision_status = DecisionStatus.BLOCKED.value
    elif human_review:
            decision_status = DecisionStatus.HUMAN_REVIEW_REQUIRED.value
    else:
            decision_status = DecisionStatus.AUTO_APPROVED.value

        return FraudAnalysisResponse(
        fraud_score=fraud_score,
        risk_level=result["fraud_analysis"]["risk_level"],
        decision_status=decision_status,
        indicators=result["fraud_analysis"]["indicators"],
        explanation=result.get("explanation"),
        compliance_metadata=result["compliance"],
        human_review_required=human_review,
        recommended_actions=result["fraud_analysis"].get(
            "recommended_actions", []
        ),
        audit_id=result["audit_id"],
        processing_time_ms=processing_time,
        quantum_signature=result["quantum_signature"],
    )

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
        logger.error(f"Fraud analysis failed: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/reviews/pending", response_model=List[HumanReviewResponse])
async def get_pending_reviews(
    access_context: AccessContext = Depends(get_access_context),
agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
priority: Optional[str] = None,
limit: int = 50,
):
    """Get pending human review requests."""
try:
        # Validate permissions
    if "fraud_review" not in access_context.permissions:
            raise HTTPException(
            status_code=403,
            detail="Insufficient permissions for review access",
        )

        pending_reviews = []
    for review_id, review_request in agent.pending_reviews.items():
            if priority and review_request.priority != priority:
                continue

            pending_reviews.append(
            HumanReviewResponse(
                review_request_id=review_id,
                status="pending",
                assigned_reviewer=review_request.assigned_reviewer,
                priority=review_request.priority,
                deadline=review_request.review_deadline,
                fraud_score=review_request.fraud_score,
                risk_level=review_request.risk_level,
                # Would be actual creation time
                created_at=datetime.now(timezone.utc),
            )
        )

            if len(pending_reviews) >= limit:
                break

        return pending_reviews

    except Exception as e:
        logger.error(f"Failed to get pending reviews: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/reviews/{review_id}/decision")
async def submit_review_decision(
    review_id: str,
decision_request: HumanReviewDecisionRequest,
access_context: AccessContext = Depends(get_access_context),
agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
):
    """Submit a human review decision."""
try:
        # Validate permissions
    if "fraud_review" not in access_context.permissions:
            raise HTTPException(
            status_code=403,
            detail="Insufficient permissions for review decisions",
        )

        result = await agent.submit_human_review_decision(
        review_request_id=review_id,
        reviewer_id=access_context.user_id,
        decision=decision_request.decision,
        notes=decision_request.notes,
        override_fraud_score=decision_request.override_fraud_score,
    )

        return {
        "status": "success",
        "message": "Review decision submitted successfully",
        "result": result,
    }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
except Exception as e:
        logger.error(f"Failed to submit review decision: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/models/performance", response_model=ModelPerformanceResponse)
async def get_model_performance(
    request: ModelPerformanceRequest = Depends(),
access_context: AccessContext = Depends(get_access_context),
agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
):
    """Get comprehensive model performance report."""
try:
        # Validate permissions
    if "model_monitoring" not in access_context.permissions:
            raise HTTPException(
            status_code=403,
            detail="Insufficient permissions for model monitoring",
        )

        performance_report = await agent.get_model_performance_report()

        # Generate recommendations based on performance
    recommendations = []
    for model_id, metrics in performance_report[
            "model_performance"
    ].items():
            if metrics["drift_score"] > 0.15:
                recommendations.append(
                f"Model {model_id} shows significant drift - "
                    consider retraining""
            )
        if metrics["false_positive_rate"] > 0.05:
                recommendations.append(
                f"Model {model_id} has high false positive rate - "
                    review thresholds""
            )

        return ModelPerformanceResponse(
        model_performance=performance_report["model_performance"],
        decision_metrics=performance_report["decision_metrics"],
        compliance_status=performance_report["compliance_status"],
        recommendations=recommendations,
        report_timestamp=datetime.fromisoformat(
            performance_report["report_timestamp"]
        ),
    )

    except Exception as e:
        logger.error(f"Failed to get model performance: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/models/{model_id}/retrain")
async def trigger_model_retraining(
    model_id: str,
reason: str,
access_context: AccessContext = Depends(get_access_context),
agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Trigger model retraining."""
try:
        # Validate permissions
    if "model_management" not in access_context.permissions:
            raise HTTPException(
            status_code=403,
            detail="Insufficient permissions for model management",
        )

        # Add retraining task to background
    background_tasks.add_task(
        agent.model_lifecycle_manager.trigger_retraining, model_id, reason
    )

        return {
        "status": "success",
        "message": f"Model retraining initiated for {model_id}",
        "reason": reason,
        "initiated_by": access_context.user_id,
    }

    except Exception as e:
        logger.error(f"Failed to trigger model retraining: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/compliance/report", response_model=ComplianceReportResponse)
async def generate_compliance_report(
    request: ComplianceReportRequest,
access_context: AccessContext = Depends(get_access_context),
agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
):
    """Generate compliance report."""
try:
        # Validate permissions
    if "compliance_reporting" not in access_context.permissions:
            raise HTTPException(
            status_code=403,
            detail="Insufficient permissions for compliance reporting",
        )

        report_id = str(uuid.uuid4())

        # Generate compliance report (simulated)
    violations = []
    compliance_status = "compliant"

        # In production, this would analyze actual audit logs and compliance
    # data
    if request.report_type == "fcra":
            # Check FCRA compliance
        violations = []  # Would be populated from actual analysis
    elif request.report_type == "glba":
            # Check GLBA compliance
        violations = []

        recommendations = [
        "Continue monitoring fraud detection performance",
        "Regular review of model fairness metrics",
        "Maintain audit trail documentation",
    ]

        return ComplianceReportResponse(
        report_id=report_id,
        report_type=request.report_type,
        compliance_status=compliance_status,
        violations=violations,
        recommendations=recommendations,
        generated_at=datetime.now(timezone.utc),
    )

    except Exception as e:
        logger.error(f"Failed to generate compliance report: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/audit/trail/{audit_id}")
async def get_audit_trail(
    audit_id: str,
access_context: AccessContext = Depends(get_access_context),
agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
):
    """Get audit trail for a specific decision."""
try:
        # Validate permissions
    if "audit_access" not in access_context.permissions:
            raise HTTPException(
            status_code=403,
            detail="Insufficient permissions for audit access",
        )

        # Find audit entry
    audit_entry = None
    for entry in agent.audit_logger.audit_trail:
            if entry["audit_id"] == audit_id:
                audit_entry = entry
            break

        if not audit_entry:
            raise HTTPException(
            status_code=404, detail="Audit trail not found"
        )

        # Mask sensitive data if user doesn't have elevated access'
    if access_context.access_level != "admin":
            # Remove sensitive fields
        audit_entry = {
            k: v
            for k, v in audit_entry.items()
                if k not in ["feature_importance", "evidence"]
            }

        return {"status": "success", "audit_trail": audit_entry}

    except HTTPException:
        raise
except Exception as e:
        logger.error(f"Failed to get audit trail: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def health_check(
    agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
):
    """Health check endpoint for fraud detection service."""
try:
        # Check agent status
    capabilities = agent.get_capabilities()

        return {
        "status": "healthy",
        "capabilities": capabilities,
        "pending_reviews": len(agent.pending_reviews),
        "total_decisions": agent.decision_metrics["total_decisions"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
    return {
        "status": "unhealthy",
        "error": str(e),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/capabilities")
async def get_capabilities(
    agent: EnhancedFraudDetectionAgent = Depends(get_fraud_agent),
):
    """Get fraud detection capabilities and configuration."""
return {
    "capabilities": agent.get_capabilities(),
    "supported_analysis_types": [
        "claim_fraud",
        "application_fraud",
        "identity_fraud",
        "premium_fraud",
        "behavioral_analysis",
        "general",
    ],
    "risk_levels": [level.level for level in FraudRiskLevel],
    "explainability_methods": ["SHAP", "LIME", "rule_based"],
    "compliance_frameworks": ["GLBA", "FCRA", "NAIC"],
}
