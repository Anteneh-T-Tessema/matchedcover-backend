""""
Guardrail AI Agent for Insurance Platform

This agent implements comprehensive safety, compliance, and ethical guardrails
for all AI operations in the insurance platform. It ensures that AI decisions
comply with regulatory requirements, ethical standards, and business policies.

Key Features:
- Real-time bias detection and mitigation
- Regulatory compliance enforcement
- Ethical AI decision validation
- Content safety filtering
- Privacy protection enforcement
- Fair lending compliance
- Output sanitization and validation
""""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import re
import uuid

from src.agents.base_agent import BaseAgent
from src.compliance.regulatory_compliance import get_compliance_manager

logger = logging.getLogger(__name__)


class GuardrailViolationType(Enum):
    """Types of guardrail violations."""

    BIAS_DETECTED = "bias_detected"
DISCRIMINATION = "discrimination"
PRIVACY_VIOLATION = "privacy_violation"
FAIRNESS_VIOLATION = "fairness_violation"
REGULATORY_VIOLATION = "regulatory_violation"
CONTENT_UNSAFE = "content_unsafe"
DATA_LEAK = "data_leak"
ETHICAL_CONCERN = "ethical_concern"
BUSINESS_POLICY_VIOLATION = "business_policy_violation"


class GuardrailSeverity(Enum):
    """Severity levels for guardrail violations."""

    LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"


class GuardrailAction(Enum):
    """Actions to take when guardrails are triggered."""

    ALLOW = "allow"
WARN = "warn"
BLOCK = "block"
MODIFY = "modify"
ESCALATE = "escalate"


@dataclass
class GuardrailViolation:
    """Represents a guardrail violation."""

    violation_id: str
violation_type: GuardrailViolationType
severity: GuardrailSeverity
description: str
affected_data: Dict[str, Any]
confidence_score: float
timestamp: str
source_agent: str
recommended_action: GuardrailAction
mitigation_suggestions: List[str]
regulatory_implications: List[str]


@dataclass
class GuardrailResult:
    """Result of guardrail evaluation."""

    decision: GuardrailAction
violations: List[GuardrailViolation]
safe_output: Optional[Dict[str, Any]]
risk_score: float
compliance_status: Dict[str, Any]
explanation: str
processing_time_ms: float


@dataclass
class ProtectedAttribute:
    """Represents a protected attribute for bias detection."""

    name: str
category: str  # demographic, financial, geographic, etc.
sensitivity_level: str  # low, medium, high, critical
regulatory_protection: List[str]  # ECOA, FHA, etc.


class GuardrailAIAgent(BaseAgent):
    """"
Guardrail AI Agent that enforces safety, compliance, and ethical standards
across all AI operations in the insurance platform.
""""

    def __init__(self):
        """Initialize the Guardrail AI Agent."""
    super().__init__("guardrail_ai", "Guardrail AI Agent")
    self.agent_id = "guardrail_ai_agent"
    self.agent_name = "Guardrail AI Agent"
    self.agent_version = "1.0.0"
    self.compliance_manager = None

        # Protected attributes for bias detection
    self.protected_attributes = self._load_protected_attributes()

        # Bias detection thresholds
    self.bias_thresholds = {
        "demographic_parity": 0.80,  # 80% minimum
        "equal_opportunity": 0.80,
        "calibration": 0.85,
        "predictive_parity": 0.80,
        "statistical_parity": 0.80,
    }

        # Content safety patterns
    self.unsafe_patterns = self._load_unsafe_patterns()

        # Privacy protection rules
    self.privacy_rules = self._load_privacy_rules()

        # Regulatory compliance rules
    self.regulatory_rules = self._load_regulatory_rules()

    async def initialize(self):
        """Initialize the guardrail agent."""
    await super().initialize()

        try:
            self.compliance_manager = await get_compliance_manager()
        logger.info("Guardrail AI Agent initialized successfully")
    except Exception as e:
            logger.error(f"Failed to initialize guardrail agent: {e}")
        raise

    async def process_task(
        self,
    task_type: str,
    input_data: Dict[str, Any],
    context: Dict[str, Any],
) -> Dict[str, Any]:
        """"
    Process guardrail evaluation tasks.

        Args:
            task_type: Type of guardrail task
        input_data: Data to evaluate
        context: Additional context

        Returns:
            Guardrail evaluation result
    """"
    start_time = datetime.now()

        try:
            if task_type == "evaluate_ai_output":
                result = await self._evaluate_ai_output(
                input_data.get("ai_output", {}),
                input_data.get("original_input", {}),
                context,
            )
        elif task_type == "check_bias":
                result = await self._check_bias(
                input_data.get("model_outputs", []),
                input_data.get("protected_attributes", {}),
                context,
            )
        elif task_type == "validate_compliance":
                result = await self._validate_compliance(
                input_data.get("decision_data", {}),
                input_data.get("regulations", []),
                context,
            )
        elif task_type == "sanitize_output":
                result = await self._sanitize_output(
                input_data.get("raw_output", {}), context
            )
        else:
                raise ValueError(f"Unknown guardrail task type: {task_type}")

            processing_time = (
            datetime.now() - start_time
        ).total_seconds() * 1000
        result["processing_time_ms"] = processing_time

            return result

        except Exception as e:
            logger.error(f"Guardrail task processing failed: {e}")
        return {
            "decision": GuardrailAction.BLOCK.value,
            "error": str(e),
            "safe_output": None,
            "risk_score": 1.0,
            "processing_time_ms": (
                datetime.now() - start_time
            ).total_seconds()
            * 1000,
        }

    async def _evaluate_ai_output(
        self,
    ai_output: Dict[str, Any],
    original_input: Dict[str, Any],
    context: Dict[str, Any],
) -> Dict[str, Any]:
        """"
    Comprehensive evaluation of AI output for safety and compliance.

        Args:
            ai_output: AI model output to evaluate
        original_input: Original input to the AI model
        context: Additional context

        Returns:
            Comprehensive guardrail evaluation result
    """"
    violations = []
    # risk_factors = ...  # Unused variable

        # 1. Check for bias in decisions
    bias_violations = await self._detect_bias_in_output(
        ai_output, original_input
    )
    violations.extend(bias_violations)

        # 2. Check regulatory compliance
    compliance_violations = await self._check_regulatory_compliance(
        ai_output, context
    )
    violations.extend(compliance_violations)

        # 3. Check for privacy violations
    privacy_violations = await self._check_privacy_violations(
        ai_output, original_input
    )
    violations.extend(privacy_violations)

        # 4. Check content safety
    content_violations = await self._check_content_safety(ai_output)
    violations.extend(content_violations)

        # 5. Check fairness metrics
    fairness_violations = await self._check_fairness_metrics(
        ai_output, original_input
    )
    violations.extend(fairness_violations)

        # 6. Check business policy compliance
    policy_violations = await self._check_business_policies(
        ai_output, context
    )
    violations.extend(policy_violations)

        # Calculate overall risk score
    risk_score = self._calculate_risk_score(violations)

        # Determine action based on violations and risk
    decision = self._determine_action(violations, risk_score)

        # Generate safe output if needed
    safe_output = None
    if decision in [GuardrailAction.ALLOW, GuardrailAction.WARN]:
            safe_output = ai_output
    elif decision == GuardrailAction.MODIFY:
            safe_output = await self._generate_safe_output(
            ai_output, violations
        )

        # Generate compliance status
    compliance_status = await self._generate_compliance_status(violations)

        # Generate explanation
    explanation = self._generate_explanation(
        violations, decision, risk_score
    )

        return GuardrailResult(
        decision=decision,
        violations=violations,
        safe_output=safe_output,
        risk_score=risk_score,
        compliance_status=compliance_status,
        explanation=explanation,
        processing_time_ms=0,  # Will be set by caller
    ).__dict__

    async def _detect_bias_in_output(
        self, ai_output: Dict[str, Any], original_input: Dict[str, Any]
) -> List[GuardrailViolation]:
        """Detect bias in AI output."""
    violations = []

        try:
            # Check for direct discrimination
        decision = ai_output.get("decision", "")
        # confidence = ...  # Unused variable
        reasoning = ai_output.get("explanation", {})

            # Check if decision is influenced by protected attributes
        for attr in self.protected_attributes:
                if self._is_decision_influenced_by_attribute(
                    decision, reasoning, attr, original_input
            ):
                    violations.append(
                    GuardrailViolation(
                        violation_id=str(uuid.uuid4()),
                        violation_type=GuardrailViolationType
                            .BIAS_DETECTED,
                        severity=GuardrailSeverity.HIGH,
                        description=f"Decision appears influenced by"
                            protected attribute: {attr.name}","
                        affected_data={
                            "attribute": attr.name,
                            "decision": decision,
                        },
                        confidence_score=0.85,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        source_agent=self.agent_id,
                        recommended_action=GuardrailAction.BLOCK,
                        mitigation_suggestions=[
                            f"Remove {attr"
                                .name} influence from decision logic","
                            "Retrain model with bias mitigation"
                                techniques","
                            "Add fairness constraints to model",
                        ],
                        regulatory_implications=attr.regulatory_protection,
                    )
                )

            # Check statistical fairness metrics if available
        if "fairness_metrics" in ai_output:
                fairness_metrics = ai_output["fairness_metrics"]
            for metric_name, threshold in self.bias_thresholds.items():
                    if metric_name in fairness_metrics:
                        metric_value = fairness_metrics[metric_name]
                    if metric_value < threshold:
                            violations.append(
                            GuardrailViolation(
                                violation_id=str(uuid.uuid4()),
                                violation_type=GuardrailViolationType
                                    .FAIRNESS_VIOLATION,
                                severity=GuardrailSeverity.MEDIUM,
                                description=f"Fairness metric {metric_name}"
                                    below threshold: {metric_value:.3f} <
                                    {threshold}","
                                affected_data={
                                    "metric": metric_name,
                                    "value": metric_value,
                                    "threshold": threshold,
                                },
                                confidence_score=0.95,
                                timestamp=datetime.now(
                                    timezone.utc
                                ).isoformat(),
                                source_agent=self.agent_id,
                                recommended_action=GuardrailAction.WARN,
                                mitigation_suggestions=[
                                    f"Improve {metric_name} through model"
                                        adjustment","
                                    "Apply post-processing fairness"
                                        techniques","
                                    "Collect more balanced training data",
                                ],
                                regulatory_implications=[
                                    "ECOA",
                                    "FHA",
                                    "State Anti-Discrimination Laws",
                                ],
                            )
                        )

        except Exception as e:
            logger.error(f"Bias detection failed: {e}")

        return violations

    async def _check_regulatory_compliance(
        self, ai_output: Dict[str, Any], context: Dict[str, Any]
) -> List[GuardrailViolation]:
        """Check regulatory compliance of AI output."""
    violations = []

        try:
            # Check FCRA compliance for adverse actions
        if ai_output.get("adverse_action", False):
                if not self._has_required_fcra_disclosures(ai_output):
                    violations.append(
                    GuardrailViolation(
                        violation_id=str(uuid.uuid4()),
                        violation_type=GuardrailViolationType
                            .REGULATORY_VIOLATION,
                        severity=GuardrailSeverity.CRITICAL,
                        description="FCRA adverse action disclosures"
                            missing","
                        affected_data={
                            "regulation": "FCRA",
                            "requirement": "adverse_action_notice",
                        },
                        confidence_score=1.0,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        source_agent=self.agent_id,
                        recommended_action=GuardrailAction.BLOCK,
                        mitigation_suggestions=[
                            "Add required FCRA adverse action disclosures",
                            "Include data sources used in decision",
                            "Provide consumer rights information",
                        ],
                        regulatory_implications=[
                            "FCRA",
                            "FTC Enforcement",
                        ],
                    )
                )

            # Check AI transparency requirements
        if not self._has_adequate_explanation(ai_output):
                violations.append(
                GuardrailViolation(
                    violation_id=str(uuid.uuid4()),
                    violation_type=GuardrailViolationType
                        .REGULATORY_VIOLATION,
                    severity=GuardrailSeverity.MEDIUM,
                    description="Insufficient AI decision explanation",
                    affected_data={"requirement": "ai_transparency"},
                    confidence_score=0.9,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    source_agent=self.agent_id,
                    recommended_action=GuardrailAction.MODIFY,
                    mitigation_suggestions=[
                        "Enhance decision explanation",
                        "Add feature importance information",
                        "Provide plain language reasoning",
                    ],
                    regulatory_implications=[
                        "NAIC AI Model Governance",
                        "State AI Transparency Laws",
                    ],
                )
            )

        except Exception as e:
            logger.error(f"Regulatory compliance check failed: {e}")

        return violations

    async def _check_privacy_violations(
        self, ai_output: Dict[str, Any], original_input: Dict[str, Any]
) -> List[GuardrailViolation]:
        """Check for privacy violations in AI output."""
    violations = []

        try:
            # Check for PII exposure in output
        pii_found = self._detect_pii_in_output(ai_output)
        if pii_found:
                violations.append(
                GuardrailViolation(
                    violation_id=str(uuid.uuid4()),
                    violation_type=GuardrailViolationType
                        .PRIVACY_VIOLATION,
                    severity=GuardrailSeverity.HIGH,
                    description=(
                        "Personally Identifiable Information detected "
                        "in output",
                    )
                    affected_data={"pii_types": pii_found},
                    confidence_score=0.95,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    source_agent=self.agent_id,
                    recommended_action=GuardrailAction.MODIFY,
                    mitigation_suggestions=[
                        "Remove or mask PII from output",
                        "Implement data anonymization",
                        "Review data handling procedures",
                    ],
                    regulatory_implications=[
                        "GLBA",
                        "HIPAA",
                        "State Privacy Laws",
                    ],
                )
            )

            # Check for data minimization compliance
        if self._violates_data_minimization(ai_output, original_input):
                violations.append(
                GuardrailViolation(
                    violation_id=str(uuid.uuid4()),
                    violation_type=GuardrailViolationType
                        .PRIVACY_VIOLATION,
                    severity=GuardrailSeverity.MEDIUM,
                    description="Output includes excessive personal data",
                    affected_data={"principle": "data_minimization"},
                    confidence_score=0.8,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    source_agent=self.agent_id,
                    recommended_action=GuardrailAction.MODIFY,
                    mitigation_suggestions=[
                        "Limit output to necessary information",
                        "Apply data minimization principles",
                        "Review data sharing policies",
                    ],
                    regulatory_implications=[
                        "CCPA",
                        "GDPR",
                        "Privacy by Design",
                    ],
                )
            )

        except Exception as e:
            logger.error(f"Privacy violation check failed: {e}")

        return violations

    def _violates_data_minimization(
        self, ai_output: Dict[str, Any], original_input: Dict[str, Any]
) -> bool:
        """Check if the AI output violates data minimization principles."""
    try:
            # Extract text content from ai_output
        output_text = ""
        if isinstance(ai_output, dict):
                output_text = (
                str(ai_output.get("decision", ""))
                + " "
                + str(ai_output.get("explanation", ""))
            )
        else:
                output_text = str(ai_output)

            # Check for excessive personal data in output
        sensitive_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{16}\b",  # Credit card
            r"\b\d{3}-\d{3}-\d{4}\b",  # Phone number
            # Email
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            # Address
            r"\b\d{1,5}\s+("
                [A-Za-z\s]+)\s+(St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard)\b","
        ]

            import re

            for pattern in sensitive_patterns:
                if re.search(pattern, output_text, re.IGNORECASE):
                    return True

            # Check if output includes more personal data than necessary for
        # the task
        if "personal_information" in original_input:
                input_pi_count = len(
                str(original_input["personal_information"])
            )
            output_pi_mentions = len(
                re.findall(
                    r"\b(name|address|phone|email|ssn|dob|age)\b",
                    output_text,
                    re.IGNORECASE,
                )
            )

                # If output mentions more personal info than input, it might be
            # excessive
            if (
                    output_pi_mentions > input_pi_count / 20
            ):  # Heuristic threshold
                return True

            return False

        except Exception as e:
            logger.error(f"Data minimization check failed: {e}")
        return False

    async def _check_content_safety(
        self, ai_output: Dict[str, Any]
) -> List[GuardrailViolation]:
        """Check content safety of AI output."""
    violations = []

        try:
            # Convert output to text for analysis
        output_text = self._extract_text_from_output(ai_output)

            # Check against unsafe content patterns
        for pattern_type, patterns in self.unsafe_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, output_text, re.IGNORECASE):
                        violations.append(
                        GuardrailViolation(
                            violation_id=str(uuid.uuid4()),
                            violation_type=GuardrailViolationType
                                .CONTENT_UNSAFE,
                            severity=GuardrailSeverity.HIGH,
                            description=f"Unsafe content detected:"
                                {pattern_type}","
                            affected_data={
                                "content_type": pattern_type,
                                "pattern": pattern,
                            },
                            confidence_score=0.85,
                            timestamp=datetime.now(
                                timezone.utc
                            ).isoformat(),
                            source_agent=self.agent_id,
                            recommended_action=GuardrailAction.BLOCK,
                            mitigation_suggestions=[
                                f"Remove {pattern_type} content",
                                "Implement content filtering",
                                "Review content generation logic",
                            ],
                            regulatory_implications=[
                                "Consumer Protection Laws",
                                "Business Ethics",
                            ],
                        )
                    )

        except Exception as e:
            logger.error(f"Content safety check failed: {e}")

        return violations

    async def _check_fairness_metrics(
        self, ai_output: Dict[str, Any], original_input: Dict[str, Any]
) -> List[GuardrailViolation]:
        """Check fairness metrics of AI decisions."""
    violations = []

        try:
            # This would integrate with actual fairness testing
        # For now, we'll simulate fairness checks'

            decision_outcome = ai_output.get("decision", "")
        confidence = ai_output.get("confidence", 0.0)

            # Check for suspiciously high confidence on sensitive decisions
        if confidence > 0.95 and self._is_sensitive_decision(
                decision_outcome
        ):
                violations.append(
                GuardrailViolation(
                    violation_id=str(uuid.uuid4()),
                    violation_type=GuardrailViolationType
                        .FAIRNESS_VIOLATION,
                    severity=GuardrailSeverity.MEDIUM,
                    description="Suspiciously high confidence on sensitive"
                        decision","
                    affected_data={
                        "confidence": confidence,
                        "decision": decision_outcome,
                    },
                    confidence_score=0.7,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    source_agent=self.agent_id,
                    recommended_action=GuardrailAction.WARN,
                    mitigation_suggestions=[
                        "Review model calibration",
                        "Add uncertainty quantification",
                        "Implement human review for high-confidence"
                            decisions","
                    ],
                    regulatory_implications=[
                        "Model Risk Management",
                        "Fair Lending",
                    ],
                )
            )

        except Exception as e:
            logger.error(f"Fairness metrics check failed: {e}")

        return violations

    async def _check_business_policies(
        self, ai_output: Dict[str, Any], context: Dict[str, Any]
) -> List[GuardrailViolation]:
        """Check business policy compliance."""
    violations = []

        try:
            # Check claim amount limits
        if "claim_amount" in ai_output:
                claim_amount = float(ai_output["claim_amount"])
            max_auto_approval = context.get(
                "max_auto_approval_amount", 50000
            )

                if claim_amount > max_auto_approval and ai_output.get(
                    "auto_approved", False
            ):
                    violations.append(
                    GuardrailViolation(
                        violation_id=str(uuid.uuid4()),
                        violation_type=GuardrailViolationType
                            .BUSINESS_POLICY_VIOLATION,
                        severity=GuardrailSeverity.HIGH,
                        description=f"Auto-approval exceeds policy limit: ${claim_amount:,"
                            .2f} > ${max_auto_approval:,.2f}","
                        affected_data={
                            "claim_amount": claim_amount,
                            "policy_limit": max_auto_approval,
                        },
                        confidence_score=1.0,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        source_agent=self.agent_id,
                        recommended_action=GuardrailAction.BLOCK,
                        mitigation_suggestions=[
                            "Require human review for high-value claims",
                            "Update auto-approval logic",
                            "Review business policy limits",
                        ],
                        regulatory_implications=[
                            "Internal Controls",
                            "Risk Management",
                        ],
                    )
                )

        except Exception as e:
            logger.error(f"Business policy check failed: {e}")

        return violations

    def _calculate_risk_score(
        self, violations: List[GuardrailViolation]
) -> float:
        """Calculate overall risk score based on violations."""
    if not violations:
            return 0.0

        severity_weights = {
        GuardrailSeverity.LOW: 0.1,
        GuardrailSeverity.MEDIUM: 0.3,
        GuardrailSeverity.HIGH: 0.7,
        GuardrailSeverity.CRITICAL: 1.0,
    }

        total_risk = 0.0
    for violation in violations:
            weight = severity_weights.get(violation.severity, 0.5)
        confidence = violation.confidence_score
        total_risk += weight * confidence

        # Normalize to 0-1 scale
    return min(total_risk / len(violations), 1.0)

    def _determine_action(
        self, violations: List[GuardrailViolation], risk_score: float
) -> GuardrailAction:
        """Determine action based on violations and risk score."""
    if not violations:
            return GuardrailAction.ALLOW

        # Check for critical violations
    critical_violations = [
        v for v in violations if v.severity == GuardrailSeverity.CRITICAL
    ]
    if critical_violations:
            return GuardrailAction.BLOCK

        # Check for high-severity violations
    high_violations = [
        v for v in violations if v.severity == GuardrailSeverity.HIGH
    ]
    if high_violations:
            return (
            GuardrailAction.MODIFY
            if len(high_violations) == 1
                else GuardrailAction.BLOCK
        )

        # Check overall risk score
    if risk_score > 0.7:
            return GuardrailAction.BLOCK
    elif risk_score > 0.4:
            return GuardrailAction.MODIFY
    elif risk_score > 0.2:
            return GuardrailAction.WARN
    else:
            return GuardrailAction.ALLOW

    async def _generate_safe_output(
        self, ai_output: Dict[str, Any], violations: List[GuardrailViolation]
) -> Dict[str, Any]:
        """Generate safe version of AI output."""
    safe_output = ai_output.copy()

        for violation in violations:
            if (
                violation.violation_type
            == GuardrailViolationType.PRIVACY_VIOLATION
        ):
                # Remove or mask PII
            safe_output = self._mask_pii(safe_output)
        elif (
                violation.violation_type
            == GuardrailViolationType.CONTENT_UNSAFE
        ):
                # Remove unsafe content
            safe_output = self._sanitize_content(safe_output)
        elif (
                violation.violation_type
            == GuardrailViolationType.REGULATORY_VIOLATION
        ):
                # Add required disclosures
            safe_output = self._add_regulatory_disclosures(
                safe_output, violation
            )

        # Add guardrail notice
    safe_output["guardrail_applied"] = True
    safe_output["guardrail_modifications"] = [
        v.description for v in violations
    ]

        return safe_output

    async def _generate_compliance_status(
        self, violations: List[GuardrailViolation]
) -> Dict[str, Any]:
        """Generate compliance status summary."""
    status = {
        "overall_compliant": len(violations) == 0,
        "total_violations": len(violations),
        "violation_types": list(
            set(v.violation_type.value for v in violations)
        ),
        "severity_breakdown": {
            "critical": len(
                [
                    v
                    for v in violations
                        if v.severity == GuardrailSeverity.CRITICAL
                    ]
            ),
            "high": len(
                [
                    v
                    for v in violations
                        if v.severity == GuardrailSeverity.HIGH
                    ]
            ),
            "medium": len(
                [
                    v
                    for v in violations
                        if v.severity == GuardrailSeverity.MEDIUM
                    ]
            ),
            "low": len(
                [
                    v
                    for v in violations
                        if v.severity == GuardrailSeverity.LOW
                    ]
            ),
        },
        "regulatory_implications": list(
            set(
                [
                    impl
                    for v in violations
                        for impl in v.regulatory_implications
                    ]
            )
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

        return status

    def _generate_explanation(
        self,
    violations: List[GuardrailViolation],
    decision: GuardrailAction,
    risk_score: float,
) -> str:
        """Generate human-readable explanation."""
    if not violations:
            return "Output passed all guardrail checks and is safe to use."

        explanation = (
        f"Guardrail analysis detected {len(violations)} violation(s) "
    )
    explanation += f"with overall risk score of {risk_score:.2f}. "

        if decision == GuardrailAction.BLOCK:
            explanation += (
            "Output blocked due to safety or compliance concerns."
        )
    elif decision == GuardrailAction.MODIFY:
            explanation += (
            "Output modified to address safety and compliance issues."
        )
    elif decision == GuardrailAction.WARN:
            explanation += (
            "Output allowed with warnings about potential issues."
        )

        violation_summary = ", ".join(
        set(v.violation_type.value for v in violations)
    )
    explanation += f" Issues found: {violation_summary}."

        return explanation

    # Abstract method implementations

    async def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration for the Guardrail AI Agent."""
    return {
        "bias_detection_threshold": 0.8,
        "enable_content_filtering": True,
        "enable_privacy_protection": True,
        "enable_regulatory_checks": True,
        "max_processing_time_ms": 5000,
        "escalation_threshold": 0.9,
    }

    async def _initialize_resources(self) -> None:
        """Initialize agent-specific resources."""
    try:
            # Initialize compliance manager
        self.compliance_manager = await get_compliance_manager()
        logger.info("Guardrail agent resources initialized")
    except Exception as e:
            logger.error(f"Failed to initialize guardrail resources: {e}")
        raise

    async def _cleanup_resources(self) -> None:
        """Cleanup agent-specific resources."""
    try:
            # Clean up any resources
        logger.info("Guardrail agent resources cleaned up")
    except Exception as e:
            logger.error(f"Failed to cleanup guardrail resources: {e}")

    async def _process_task_impl(
        self,
    task_type: str,
    input_data: Dict[str, Any],
    context: Dict[str, Any] = None,
) -> Dict[str, Any]:
        """Implement the actual task processing logic."""
    return await self.process_task(task_type, input_data, context or {})

    async def _validate_input(
        self, task_type: str, input_data: Dict[str, Any]
) -> None:
        """Validate input data for the task."""
    if not isinstance(input_data, dict):
            raise ValueError("Input data must be a dictionary")

        if task_type == "evaluate_ai_output":
            if "ai_output" not in input_data:
                raise ValueError("Missing required field: ai_output")
    elif task_type == "check_bias":
            if "model_outputs" not in input_data:
                raise ValueError("Missing required field: model_outputs")
    elif task_type == "validate_compliance":
            if "decision_data" not in input_data:
                raise ValueError("Missing required field: decision_data")

    # Helper methods implementation

    def _load_protected_attributes(self) -> List[ProtectedAttribute]:
        """Load protected attributes for bias detection."""
    return [
        ProtectedAttribute(
            name="race",
            category="demographic",
            sensitivity_level="critical",
            regulatory_protection=["ECOA", "FHA", "Civil Rights Act"],
        ),
        ProtectedAttribute(
            name="gender",
            category="demographic",
            sensitivity_level="critical",
            regulatory_protection=["ECOA", "Title VII"],
        ),
        ProtectedAttribute(
            name="age",
            category="demographic",
            sensitivity_level="high",
            regulatory_protection=["ADEA", "ECOA"],
        ),
        ProtectedAttribute(
            name="religion",
            category="demographic",
            sensitivity_level="critical",
            regulatory_protection=["ECOA", "Title VII"],
        ),
        ProtectedAttribute(
            name="national_origin",
            category="demographic",
            sensitivity_level="critical",
            regulatory_protection=["ECOA", "Civil Rights Act"],
        ),
        ProtectedAttribute(
            name="disability",
            category="demographic",
            sensitivity_level="critical",
            regulatory_protection=["ADA", "FHA"],
        ),
    ]

    def _load_unsafe_patterns(self) -> Dict[str, List[str]]:
        """Load unsafe content patterns."""
    return {
        "illegal_content": [r"\b(?:illegal|fraud|scam)\b"],
        "pii_exposure": [r"\bpii\b.*\b(?:social|ssn|license)\b"],
        "discrimination": [r"\b(?:discriminat|bias|prejudice)\b"],
        "security_threats": [r"\b(?:hack|exploit|vulnerabilit)\b"],
    }

    def _load_privacy_rules(self) -> List[Dict[str, Any]]:
        """Load privacy protection rules."""
    return [
        {
            "rule": "no_pii_in_output",
            "description": "Output must not contain PII",
        },
        {
            "rule": "consent_required",
            "description": "Data usage requires consent",
        },
        {
            "rule": "data_minimization",
            "description": "Use minimum necessary data",
        },
        {
            "rule": "purpose_limitation",
            "description": "Data used only for stated purpose",
        },
    ]

    def _load_regulatory_rules(self) -> List[Dict[str, Any]]:
        """Load regulatory compliance rules."""
    return [
        {
            "regulation": "FCRA",
            "requirement": "adverse_action_notice",
            "mandatory": True,
        },
        {
            "regulation": "ECOA",
            "requirement": "non_discrimination",
            "mandatory": True,
        },
        {
            "regulation": "GDPR",
            "requirement": "data_protection",
            "mandatory": True,
        },
        {
            "regulation": "CCPA",
            "requirement": "privacy_rights",
            "mandatory": True,
        },
    ]

    def _is_decision_influenced_by_attribute(
        self,
    decision: str,
    reasoning: Dict[str, Any],
    attribute: ProtectedAttribute,
    input_data: Dict[str, Any],
) -> bool:
        """Check if decision is influenced by protected attribute."""
    try:
            # Simple heuristic checks
        attr_name = attribute.name.lower()

            # Check if attribute is mentioned in reasoning
        reasoning_text = str(reasoning).lower()
        if attr_name in reasoning_text:
                return True

            # Check for related terms
        related_terms = {
            "race": ["ethnicity", "color", "ancestry"],
            "gender": ["sex", "male", "female"],
            "age": ["old", "young", "elderly"],
            "religion": ["faith", "belief", "church"],
            "national_origin": ["nationality", "country", "immigrant"],
            "disability": ["handicap", "impaired", "disabled"],
        }

            if attr_name in related_terms:
                for term in related_terms[attr_name]:
                    if term in reasoning_text:
                        return True

            return False

        except Exception as e:
            logger.error(f"Error checking attribute influence: {e}")
        return False

    def _has_required_fcra_disclosures(
        self, ai_output: Dict[str, Any]
) -> bool:
        """Check if output has required FCRA disclosures."""
    try:
            # Check for required FCRA elements
        required_elements = [
            "adverse_action_notice",
            "credit_reporting_agency",
            "dispute_rights",
        ]

            disclosures = ai_output.get("disclosures", {})
        for element in required_elements:
                if element not in disclosures:
                    return False

            return True

        except Exception as e:
            logger.error(f"Error checking FCRA disclosures: {e}")
        return False

    def _has_adequate_explanation(self, ai_output: Dict[str, Any]) -> bool:
        """Check if AI output has adequate explanation."""
    try:
            reasoning = ai_output.get("reasoning", {})
        explanation = ai_output.get("explanation", "")
        confidence = ai_output.get("confidence", 0.0)

            # Check for explanation content
        if not reasoning and not explanation:
                return False

            # Check explanation length for high-stakes decisions
        if confidence > 0.8:
                min_explanation_length = 50
            explanation_text = str(reasoning) + str(explanation)
            if len(explanation_text) < min_explanation_length:
                    return False

            return True

        except Exception as e:
            logger.error(f"Error checking explanation adequacy: {e}")
        return False

    def _detect_pii_in_output(self, ai_output: Dict[str, Any]) -> List[str]:
        """Detect PII in AI output."""
    try:
            pii_found = []
        output_text = str(ai_output)

            # Simple PII patterns
        pii_patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,"
                }\b","
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        }

            for pii_type, pattern in pii_patterns.items():
                if re.search(pattern, output_text):
                    pii_found.append(pii_type)

            return pii_found

        except Exception as e:
            logger.error(f"Error detecting PII: {e}")
        return []

    def _extract_text_from_output(self, ai_output: Dict[str, Any]) -> str:
        """Extract text content from AI output."""
    try:
            # Extract all text-like values from the output
        text_parts = []

            def extract_text_recursive(obj):
                if isinstance(obj, str):
                    text_parts.append(obj)
            elif isinstance(obj, dict):
                    for value in obj.values():
                        extract_text_recursive(value)
            elif isinstance(obj, list):
                    for item in obj:
                        extract_text_recursive(item)

            extract_text_recursive(ai_output)
        return " ".join(text_parts)

        except Exception as e:
            logger.error(f"Error extracting text: {e}")
        return ""


# Factory function for easy instantiation
async def create_guardrail_ai_agent() -> GuardrailAIAgent:
    """Create and initialize a Guardrail AI Agent."""
agent = GuardrailAIAgent()
await agent.initialize()
return agent
