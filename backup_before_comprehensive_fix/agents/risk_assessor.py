""""
Risk Assessment Agent for MatchedCover Insurance Platform.

This agent analyzes customer data, location, history, and external factors
to provide comprehensive risk assessments for insurance underwriting.
""""

import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler


from src.agents.base_agent import BaseAgent
from src.core.config import get_settings
from src.quantum.crypto import QuantumResistantSigner

logger = logging.getLogger(__name__)
settings = get_settings()


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
score: float  # 0.0 to 1.0
confidence: float  # 0.0 to 1.0
details: Dict[str, Any]
recommendations: List[str]


@dataclass
class RiskAssessment:
    """Comprehensive risk assessment result."""

    customer_id: str
overall_risk_level: RiskLevel
risk_score: float  # 0.0 to 1.0
confidence_score: float  # 0.0 to 1.0
factor_analyses: List[RiskFactorAnalysis]
premium_multiplier: float
coverage_limitations: List[str]
required_conditions: List[str]
assessment_timestamp: datetime
quantum_signature: str


class RiskAssessorAgent(BaseAgent):
    """"
AI agent for comprehensive risk assessment and underwriting.

    Analyzes multiple risk factors using machine learning models,
external data sources, and behavioral analytics to provide
accurate risk assessments for insurance policies.
""""

    def __init__(self):
        super().__init__(
        name="RiskAssessor",
        description="Comprehensive risk assessment and underwriting agent",
        capabilities=[
            "demographic_analysis",
            "geographic_risk_assessment",
            "behavioral_analytics",
            "credit_scoring",
            "claims_history_analysis",
            "external_data_integration",
        ],
    )
    self.quantum_signer = QuantumResistantSigner()
    self.ml_models = {}
    self.scalers = {}
    self._initialize_models()

    def _initialize_models(self):
        """Initialize machine learning models for risk assessment."""
    try:
            # Risk classification model
        self.ml_models["risk_classifier"] = RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42
        )

            # Premium multiplier regression model
        self.ml_models["premium_regressor"] = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42,
        )

            # Feature scalers
        self.scalers["demographic"] = StandardScaler()
        self.scalers["financial"] = StandardScaler()
        self.scalers["behavioral"] = StandardScaler()

            # In production, load pre-trained models
        # self._load_pretrained_models()

            logger.info("Risk assessment models initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize ML models: {str(e)}")
        raise

    async def assess_risk(
        self,
    customer_data: Dict[str, Any],
    policy_type: str,
    coverage_amount: float,
) -> RiskAssessment:
        """"
    Perform comprehensive risk assessment for a customer.

        Args:
            customer_data: Customer information and history
        policy_type: Type of insurance policy
        coverage_amount: Requested coverage amount

        Returns:
            Complete risk assessment with recommendations
    """"
    try:
            logger.info(
            f"Starting risk assessment for customer {customer_data.get("
                'customer_id')}""
        )

            # Perform individual risk factor analyses
        factor_analyses = []

            # Demographic analysis
        demographic_analysis = await self._analyze_demographic_risk(
            customer_data
        )
        factor_analyses.append(demographic_analysis)

            # Geographic risk analysis
        geographic_analysis = await self._analyze_geographic_risk(
            customer_data
        )
        factor_analyses.append(geographic_analysis)

            # Behavioral risk analysis
        behavioral_analysis = await self._analyze_behavioral_risk(
            customer_data
        )
        factor_analyses.append(behavioral_analysis)

            # Financial risk analysis
        financial_analysis = await self._analyze_financial_risk(
            customer_data
        )
        factor_analyses.append(financial_analysis)

            # Historical claims analysis
        historical_analysis = await self._analyze_historical_risk(
            customer_data
        )
        factor_analyses.append(historical_analysis)

            # External data analysis
        external_analysis = await self._analyze_external_risk(
            customer_data, policy_type
        )
        factor_analyses.append(external_analysis)

            # Calculate overall risk assessment
        overall_assessment = await self._calculate_overall_risk(
            factor_analyses, policy_type, coverage_amount
        )

            # Create comprehensive risk assessment
        risk_assessment = RiskAssessment(
            customer_id=customer_data.get("customer_id"),
            overall_risk_level=overall_assessment["risk_level"],
            risk_score=overall_assessment["risk_score"],
            confidence_score=overall_assessment["confidence"],
            factor_analyses=factor_analyses,
            premium_multiplier=overall_assessment["premium_multiplier"],
            coverage_limitations=overall_assessment["limitations"],
            required_conditions=overall_assessment["conditions"],
            assessment_timestamp=datetime.utcnow(),
            quantum_signature="",
        )

            # Add quantum signature for integrity
        assessment_data = json.dumps(
            {
                "customer_id": risk_assessment.customer_id,
                "risk_score": risk_assessment.risk_score,
                "timestamp": risk_assessment
                    .assessment_timestamp.isoformat(),
            }
        )
        risk_assessment.quantum_signature = await self.quantum_signer.sign(
            assessment_data
        )

            logger.info(
            f"Risk assessment completed: {overall_assessment['risk_level']"
                .value}""
        )
        return risk_assessment

        except Exception as e:
            logger.error(f"Risk assessment failed: {str(e)}")
        raise

    async def _analyze_demographic_risk(
        self, customer_data: Dict[str, Any]
) -> RiskFactorAnalysis:
        """Analyze demographic risk factors."""
    try:
            age = customer_data.get("age", 0)
        # gender = ...  # Unused variable
        marital_status = customer_data.get("marital_status", "unknown")
        occupation = customer_data.get("occupation", "unknown")
        # education = ...  # Unused variable

            # Age-based risk scoring
        age_risk = self._calculate_age_risk(age)

            # Occupation-based risk scoring
        occupation_risk = self._calculate_occupation_risk(occupation)

            # Combined demographic score
        demographic_score = age_risk * 0.4 + occupation_risk * 0.6

            # Risk recommendations
        recommendations = []
        if age < 25:
                recommendations.append(
                "Consider additional driver training for young drivers"
            )
        if occupation_risk > 0.7:
                recommendations.append(
                "High-risk occupation requires specialized coverage"
            )

            return RiskFactorAnalysis(
            factor_type=RiskFactor.DEMOGRAPHIC,
            score=demographic_score,
            confidence=0.85,
            details={
                "age_risk": age_risk,
                "occupation_risk": occupation_risk,
                "age": age,
                "occupation": occupation,
                "marital_status": marital_status,
            },
            recommendations=recommendations,
        )

        except Exception as e:
            logger.error(f"Demographic analysis failed: {str(e)}")
        return self._create_default_analysis(RiskFactor.DEMOGRAPHIC)

    async def _analyze_geographic_risk(
        self, customer_data: Dict[str, Any]
) -> RiskFactorAnalysis:
        """Analyze geographic and location-based risk factors."""
    try:
            address = customer_data.get("address", {})
        zip_code = address.get("zip_code", "")
        city = address.get("city", "")
        state = address.get("state", "")

            # Crime rate analysis
        crime_risk = await self._get_crime_rate_risk(zip_code)

            # Natural disaster risk
        disaster_risk = await self._get_natural_disaster_risk(
            zip_code, state
        )

            # Economic stability risk
        economic_risk = await self._get_economic_stability_risk(zip_code)

            # Combined geographic score
        geographic_score = (
            crime_risk * 0.4 + disaster_risk * 0.3 + economic_risk * 0.3
        )

            recommendations = []
        if crime_risk > 0.7:
                recommendations.append("Consider enhanced security measures")
        if disaster_risk > 0.6:
                recommendations.append(
                "Natural disaster coverage strongly recommended"
            )

            return RiskFactorAnalysis(
            factor_type=RiskFactor.GEOGRAPHIC,
            score=geographic_score,
            confidence=0.75,
            details={
                "crime_risk": crime_risk,
                "disaster_risk": disaster_risk,
                "economic_risk": economic_risk,
                "location": f"{city}, {state} {zip_code}",
            },
            recommendations=recommendations,
        )

        except Exception as e:
            logger.error(f"Geographic analysis failed: {str(e)}")
        return self._create_default_analysis(RiskFactor.GEOGRAPHIC)

    async def _analyze_behavioral_risk(
        self, customer_data: Dict[str, Any]
) -> RiskFactorAnalysis:
        """Analyze behavioral patterns and lifestyle factors."""
    try:
            # Driving behavior (if applicable)
        driving_record = customer_data.get("driving_record", {})
        violations = driving_record.get("violations", [])
        accidents = driving_record.get("accidents", [])

            # Lifestyle factors
        smoking = customer_data.get("smoking", False)
        alcohol_consumption = customer_data.get(
            "alcohol_consumption", "moderate"
        )
        exercise_frequency = customer_data.get(
            "exercise_frequency", "regular"
        )

            # Calculate behavioral scores
        driving_score = self._calculate_driving_risk(violations, accidents)
        lifestyle_score = self._calculate_lifestyle_risk(
            smoking, alcohol_consumption, exercise_frequency
        )

            behavioral_score = driving_score * 0.6 + lifestyle_score * 0.4

            recommendations = []
        if len(violations) > 2:
                recommendations.append("Consider defensive driving course")
        if smoking:
                recommendations.append("Smoking cessation programs available")

            return RiskFactorAnalysis(
            factor_type=RiskFactor.BEHAVIORAL,
            score=behavioral_score,
            confidence=0.80,
            details={
                "driving_score": driving_score,
                "lifestyle_score": lifestyle_score,
                "violations_count": len(violations),
                "accidents_count": len(accidents),
                "smoking": smoking,
            },
            recommendations=recommendations,
        )

        except Exception as e:
            logger.error(f"Behavioral analysis failed: {str(e)}")
        return self._create_default_analysis(RiskFactor.BEHAVIORAL)

    async def _analyze_financial_risk(
        self, customer_data: Dict[str, Any]
) -> RiskFactorAnalysis:
        """Analyze financial stability and credit risk."""
    try:
            credit_score = customer_data.get("credit_score", 650)
        annual_income = customer_data.get("annual_income", 50000)
        debt_to_income = customer_data.get("debt_to_income_ratio", 0.3)
        employment_years = customer_data.get("employment_years", 2)

            # Credit risk scoring
        credit_risk = self._calculate_credit_risk(credit_score)

            # Income stability risk
        income_risk = self._calculate_income_risk(
            annual_income, employment_years
        )

            # Debt risk
        debt_risk = self._calculate_debt_risk(debt_to_income)

            financial_score = (
            credit_risk * 0.4 + income_risk * 0.3 + debt_risk * 0.3
        )

            recommendations = []
        if credit_score < 600:
                recommendations.append("Consider credit improvement programs")
        if debt_to_income > 0.4:
                recommendations.append(
                "High debt-to-income ratio may affect coverage"
            )

            return RiskFactorAnalysis(
            factor_type=RiskFactor.FINANCIAL,
            score=financial_score,
            confidence=0.90,
            details={
                "credit_risk": credit_risk,
                "income_risk": income_risk,
                "debt_risk": debt_risk,
                "credit_score": credit_score,
                "annual_income": annual_income,
                "debt_to_income": debt_to_income,
            },
            recommendations=recommendations,
        )

        except Exception as e:
            logger.error(f"Financial analysis failed: {str(e)}")
        return self._create_default_analysis(RiskFactor.FINANCIAL)

    async def _analyze_historical_risk(
        self, customer_data: Dict[str, Any]
) -> RiskFactorAnalysis:
        """Analyze historical claims and insurance patterns."""
    try:
            claims_history = customer_data.get("claims_history", [])
        policy_history = customer_data.get("policy_history", [])

            # Claims frequency analysis
        claims_frequency = len(claims_history) / max(
            len(policy_history), 1
        )

            # Claims severity analysis
        total_claim_amount = sum(
            claim.get("amount", 0) for claim in claims_history
        )
        avg_claim_amount = total_claim_amount / max(len(claims_history), 1)

            # Policy lapse analysis
        lapses = sum(
            1
            for policy in policy_history
                if policy.get("status") == "lapsed"
            )
        lapse_rate = lapses / max(len(policy_history), 1)

            # Combined historical score
        frequency_score = min(claims_frequency * 0.5, 1.0)
        severity_score = min(
            avg_claim_amount / 10000, 1.0
        )  # Normalize to 10k
        lapse_score = lapse_rate

            historical_score = (
            frequency_score * 0.4
            + severity_score * 0.4
            + lapse_score * 0.2
        )

            recommendations = []
        if claims_frequency > 0.5:
                recommendations.append(
                "High claims frequency requires careful review"
            )
        if lapse_rate > 0.3:
                recommendations.append("History of policy lapses noted")

            return RiskFactorAnalysis(
            factor_type=RiskFactor.HISTORICAL,
            score=historical_score,
            confidence=0.95,
            details={
                "claims_frequency": claims_frequency,
                "avg_claim_amount": avg_claim_amount,
                "lapse_rate": lapse_rate,
                "total_claims": len(claims_history),
                "total_policies": len(policy_history),
            },
            recommendations=recommendations,
        )

        except Exception as e:
            logger.error(f"Historical analysis failed: {str(e)}")
        return self._create_default_analysis(RiskFactor.HISTORICAL)

    async def _analyze_external_risk(
        self, customer_data: Dict[str, Any], policy_type: str
) -> RiskFactorAnalysis:
        """Analyze external risk factors and market conditions."""
    try:
            # Market volatility risk
        market_risk = await self._get_market_volatility_risk(policy_type)

            # Regulatory environment risk
        regulatory_risk = await self._get_regulatory_risk(policy_type)

            # Economic indicators risk
        economic_risk = await self._get_economic_indicators_risk()

            # Industry-specific risks
        industry_risk = await self._get_industry_specific_risk(policy_type)

            external_score = (
            market_risk * 0.25
            + regulatory_risk * 0.25
            + economic_risk * 0.25
            + industry_risk * 0.25
        )

            recommendations = []
        if market_risk > 0.7:
                recommendations.append(
                "Market volatility may affect coverage terms"
            )
        if regulatory_risk > 0.6:
                recommendations.append("Regulatory changes may impact policy")

            return RiskFactorAnalysis(
            factor_type=RiskFactor.EXTERNAL,
            score=external_score,
            confidence=0.70,
            details={
                "market_risk": market_risk,
                "regulatory_risk": regulatory_risk,
                "economic_risk": economic_risk,
                "industry_risk": industry_risk,
                "policy_type": policy_type,
            },
            recommendations=recommendations,
        )

        except Exception as e:
            logger.error(f"External analysis failed: {str(e)}")
        return self._create_default_analysis(RiskFactor.EXTERNAL)

    async def _calculate_overall_risk(
        self,
    factor_analyses: List[RiskFactorAnalysis],
    policy_type: str,
    coverage_amount: float,
) -> Dict[str, Any]:
        """Calculate overall risk assessment from individual factors."""
    try:
            # Weight factors based on policy type
        weights = self._get_factor_weights(policy_type)

            # Calculate weighted risk score
        weighted_score = 0.0
        total_weight = 0.0

            for analysis in factor_analyses:
                weight = weights.get(analysis.factor_type, 0.1)
            weighted_score += analysis.score * weight
            total_weight += weight

            overall_score = (
            weighted_score / total_weight if total_weight > 0 else 0.5
        )

            # Determine risk level
        risk_level = self._score_to_risk_level(overall_score)

            # Calculate premium multiplier
        premium_multiplier = self._calculate_premium_multiplier(
            overall_score, coverage_amount
        )

            # Determine coverage limitations
        limitations = self._determine_coverage_limitations(
            factor_analyses, overall_score
        )

            # Required conditions
        conditions = self._determine_required_conditions(
            factor_analyses, overall_score
        )

            # Calculate confidence
        confidence = np.mean(
            [analysis.confidence for analysis in factor_analyses]
        )

            return {
            "risk_level": risk_level,
            "risk_score": overall_score,
            "confidence": confidence,
            "premium_multiplier": premium_multiplier,
            "limitations": limitations,
            "conditions": conditions,
        }

        except Exception as e:
            logger.error(f"Overall risk calculation failed: {str(e)}")
        return {
            "risk_level": RiskLevel.MEDIUM,
            "risk_score": 0.5,
            "confidence": 0.5,
            "premium_multiplier": 1.0,
            "limitations": [],
            "conditions": [],
        }

    # Helper methods for risk calculations
def _calculate_age_risk(self, age: int) -> float:
        """Calculate age-based risk score."""
    if age < 18 or age > 80:
            return 0.8
    elif age < 25 or age > 65:
            return 0.6
    elif 25 <= age <= 45:
            return 0.3
    else:
            return 0.4

    def _calculate_occupation_risk(self, occupation: str) -> float:
        """Calculate occupation-based risk score."""
    high_risk_occupations = [
        "pilot",
        "miner",
        "logger",
        "fisherman",
        "roofer",
    ]
    medium_risk_occupations = [
        "police",
        "firefighter",
        "construction",
        "driver",
    ]

        occupation_lower = occupation.lower()

        if any(
            risk_job in occupation_lower for risk_job in high_risk_occupations
    ):
            return 0.8
    elif any(
            risk_job in occupation_lower
        for risk_job in medium_risk_occupations
        ):
            return 0.6
    else:
            return 0.3

    def _calculate_driving_risk(
        self, violations: List, accidents: List
) -> float:
        """Calculate driving behavior risk score."""
    violation_score = min(len(violations) * 0.2, 1.0)
    accident_score = min(len(accidents) * 0.3, 1.0)
    return (violation_score + accident_score) / 2

    def _calculate_lifestyle_risk(
        self, smoking: bool, alcohol: str, exercise: str
) -> float:
        """Calculate lifestyle risk score."""
    risk_score = 0.0

        if smoking:
            risk_score += 0.4

        alcohol_risk = {
        "heavy": 0.3,
        "moderate": 0.1,
        "light": 0.05,
        "none": 0.0,
    }
    risk_score += alcohol_risk.get(alcohol, 0.1)

        exercise_risk = {
        "never": 0.3,
        "rarely": 0.2,
        "sometimes": 0.1,
        "regular": 0.0,
    }
    risk_score += exercise_risk.get(exercise, 0.1)

        return min(risk_score, 1.0)

    def _calculate_credit_risk(self, credit_score: int) -> float:
        """Calculate credit-based risk score."""
    if credit_score >= 750:
            return 0.1
    elif credit_score >= 650:
            return 0.3
    elif credit_score >= 550:
            return 0.6
    else:
            return 0.9

    def _calculate_income_risk(
        self, income: float, employment_years: int
) -> float:
        """Calculate income stability risk."""
    income_risk = max(0.0, (50000 - income) / 50000) * 0.5
    employment_risk = max(0.0, (3 - employment_years) / 3) * 0.5
    return min(income_risk + employment_risk, 1.0)

    def _calculate_debt_risk(self, debt_to_income: float) -> float:
        """Calculate debt-to-income risk."""
    if debt_to_income <= 0.2:
            return 0.1
    elif debt_to_income <= 0.4:
            return 0.4
    elif debt_to_income <= 0.6:
            return 0.7
    else:
            return 0.9

    async def _get_crime_rate_risk(self, zip_code: str) -> float:
        """Get crime rate risk for location (mock implementation)."""
    # In production, integrate with crime databases
    return np.random.uniform(0.2, 0.8)

    async def _get_natural_disaster_risk(
        self, zip_code: str, state: str
) -> float:
        """Get natural disaster risk for location (mock implementation)."""
    # In production, integrate with FEMA, NOAA data
    high_risk_states = ["FL", "CA", "TX", "LA", "NC"]
    return 0.7 if state in high_risk_states else 0.3

    async def _get_economic_stability_risk(self, zip_code: str) -> float:
        """Get economic stability risk for location (mock implementation)."""
    # In production, integrate with economic indicators
    return np.random.uniform(0.1, 0.6)

    async def _get_market_volatility_risk(self, policy_type: str) -> float:
        """Get market volatility risk (mock implementation)."""
    return np.random.uniform(0.2, 0.7)

    async def _get_regulatory_risk(self, policy_type: str) -> float:
        """Get regulatory environment risk (mock implementation)."""
    return np.random.uniform(0.1, 0.5)

    async def _get_economic_indicators_risk(self) -> float:
        """Get economic indicators risk (mock implementation)."""
    return np.random.uniform(0.2, 0.6)

    async def _get_industry_specific_risk(self, policy_type: str) -> float:
        """Get industry-specific risk (mock implementation)."""
    industry_risks = {
        "auto": 0.4,
        "home": 0.3,
        "health": 0.5,
        "life": 0.2,
        "business": 0.6,
    }
    return industry_risks.get(policy_type, 0.4)

    def _get_factor_weights(self, policy_type: str) -> Dict[RiskFactor, float]:
        """Get factor weights based on policy type."""
    base_weights = {
        RiskFactor.DEMOGRAPHIC: 0.2,
        RiskFactor.GEOGRAPHIC: 0.15,
        RiskFactor.BEHAVIORAL: 0.25,
        RiskFactor.FINANCIAL: 0.2,
        RiskFactor.HISTORICAL: 0.15,
        RiskFactor.EXTERNAL: 0.05,
    }

        # Adjust weights based on policy type
    if policy_type == "auto":
            base_weights[RiskFactor.BEHAVIORAL] = 0.35
        base_weights[RiskFactor.GEOGRAPHIC] = 0.20
    elif policy_type == "home":
            base_weights[RiskFactor.GEOGRAPHIC] = 0.35
        base_weights[RiskFactor.FINANCIAL] = 0.25
    elif policy_type == "health":
            base_weights[RiskFactor.DEMOGRAPHIC] = 0.30
        base_weights[RiskFactor.BEHAVIORAL] = 0.30

        return base_weights

    def _score_to_risk_level(self, score: float) -> RiskLevel:
        """Convert numeric score to risk level."""
    if score <= 0.2:
            return RiskLevel.VERY_LOW
    elif score <= 0.4:
            return RiskLevel.LOW
    elif score <= 0.6:
            return RiskLevel.MEDIUM
    elif score <= 0.8:
            return RiskLevel.HIGH
    else:
            return RiskLevel.VERY_HIGH

    def _calculate_premium_multiplier(
        self, risk_score: float, coverage_amount: float
) -> float:
        """Calculate premium multiplier based on risk."""
    base_multiplier = 0.5 + (risk_score * 1.5)  # Range: 0.5 to 2.0

        # Adjust for coverage amount
    if coverage_amount > 500000:
            base_multiplier *= 1.1
    elif coverage_amount > 1000000:
            base_multiplier *= 1.2

        return round(base_multiplier, 2)

    def _determine_coverage_limitations(
        self, factor_analyses: List[RiskFactorAnalysis], overall_score: float
) -> List[str]:
        """Determine coverage limitations based on risk factors."""
    limitations = []

        if overall_score > 0.8:
            limitations.append("Higher deductible required")
        limitations.append("Coverage cap applies")

        for analysis in factor_analyses:
            if (
                analysis.factor_type == RiskFactor.GEOGRAPHIC
            and analysis.score > 0.7
        ):
                limitations.append("Natural disaster exclusions apply")
        elif (
                analysis.factor_type == RiskFactor.BEHAVIORAL
            and analysis.score > 0.7
        ):
                limitations.append("High-risk activity exclusions")
        elif (
                analysis.factor_type == RiskFactor.FINANCIAL
            and analysis.score > 0.8
        ):
                limitations.append("Payment monitoring required")

        return limitations

    def _determine_required_conditions(
        self, factor_analyses: List[RiskFactorAnalysis], overall_score: float
) -> List[str]:
        """Determine required conditions for coverage."""
    conditions = []

        if overall_score > 0.7:
            conditions.append("Annual risk review required")

        for analysis in factor_analyses:
            if (
                analysis.factor_type == RiskFactor.BEHAVIORAL
            and analysis.score > 0.6
        ):
                conditions.append("Completion of safety course required")
        elif (
                analysis.factor_type == RiskFactor.FINANCIAL
            and analysis.score > 0.7
        ):
                conditions.append("Financial verification required")

        return conditions

    def _create_default_analysis(
        self, factor_type: RiskFactor
) -> RiskFactorAnalysis:
        """Create default risk factor analysis for error cases."""
    return RiskFactorAnalysis(
        factor_type=factor_type,
        score=0.5,
        confidence=0.3,
        details={"error": "Analysis failed, using default values"},
        recommendations=[
            "Manual review recommended due to analysis error"
        ],
    )
