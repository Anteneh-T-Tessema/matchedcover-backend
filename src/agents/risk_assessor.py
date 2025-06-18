"""
Risk Assessment Agent for MatchedCover Insurance Platform.

This agent analyzes customer data, location, history, and external factors
to provide comprehensive risk assessments for insurance underwriting.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List


class RiskLevel(Enum):
    """Risk assessment levels."""

    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class RiskFactor(Enum):
    """Types of risk factors analyzed."""

    DEMOGRAPHIC = "demographic"
    GEOGRAPHIC = "geographic"
    BEHAVIORAL = "behavioral"
    FINANCIAL = "financial"
    HISTORICAL = "historical"
    EXTERNAL = "external"


@dataclass
class RiskFactorAnalysis:
    """Individual risk factor analysis result."""

    factor_type: RiskFactor
    risk_level: RiskLevel
    confidence: float
    description: str
    contributing_elements: Dict[str, Any]


@dataclass
class RiskAssessment:
    """Complete risk assessment result."""

    assessment_id: str
    customer_id: str
    policy_type: str
    overall_risk_level: RiskLevel
    risk_factors: List[RiskFactorAnalysis]
    premium_multiplier: float
    confidence_score: float
    timestamp: str
    risk_score: float
    flags: List[str]
    notes: str
