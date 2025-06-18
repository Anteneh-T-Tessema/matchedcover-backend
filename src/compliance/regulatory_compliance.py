"""
Regulatory Compliance Implementation for Blockchain Integration.

This module implements compliance controls and monitoring for the
MatchedCover blockchain-integrated insurance platform to meet
US regulatory requirements."""

import logging

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ComplianceRegulation(Enum):
    """Enumeration of applicable compliance regulations."""

    NAIC_AI_GOVERNANCE = "naic_ai_governance"
NAIC_MODEL_672 = "naic_model_672"
GLBA_PRIVACY = "glba_privacy"
GLBA_SAFEGUARDS = "glba_safeguards"
FCRA_ADVERSE_ACTION = "fcra_adverse_action"
SOX_CONTROLS = "sox_controls"
STATE_CLAIMS_PRACTICES = "state_claims_practices"
STATE_CYBERSECURITY = "state_cybersecurity"
FTC_ALGORITHMIC_ACCOUNTABILITY = "ftc_algorithmic_accountability"
AML_BSA = "aml_bsa"
NIST_CYBERSECURITY = "nist_cybersecurity"
ISO_27001 = "iso_27001"


@dataclass
class ComplianceEvent:
    """Represents a compliance-related event."""

    event_id: str
regulation: ComplianceRegulation
event_type: str  # violation, check, audit, report
severity: str  # low, medium, high, critical
description: str
timestamp: str
details: Dict[str, Any]
remediation_required: bool
remediation_deadline: Optional[str] = None


@dataclass
class AIModelCompliance:
    """AI model compliance tracking."""

    model_id: str
model_name: str
model_version: str
validation_date: str
bias_test_date: str
performance_metrics: Dict[str, float]
fairness_metrics: Dict[str, float]
explainability_score: float
governance_approval: bool
regulatory_approval: bool
documentation_complete: bool


@dataclass
class BlockchainCompliance:
    """Blockchain compliance tracking."""

    network_id: str
chaincode_version: str
audit_trail_enabled: bool
data_retention_policy: str
immutability_verified: bool
access_controls_verified: bool
regulatory_access_enabled: bool
backup_procedures_tested: bool


class ComplianceManager:"""
Manages regulatory compliance for the blockchain-integrated
insurance platform."""

    def __init__(self):
        self.compliance_events: List[ComplianceEvent] = []
    self.ai_models: Dict[str, AIModelCompliance] = {}
    self.blockchain_compliance: Optional[BlockchainCompliance] = None
    self.compliance_config = self._load_compliance_config()

    def _load_compliance_config(self) -> Dict[str, Any]:
        """Load compliance configuration."""
    return {
        "audit_retention_days": 2555,  # 7 years
        "bias_testing_frequency_days": 90,  # Quarterly
        "model_validation_frequency_days": 365,  # Annually
        "incident_reporting_deadline_hours": 72,
        "adverse_action_notice_required": True,
        "algorithmic_transparency_required": True,
        "data_minimization_enabled": True,
        "consent_management_enabled": True,
    }

    async def validate_ai_model_compliance(
        self, model_id: str, model_data: Dict[str, Any]
) -> Dict[str, Any]:"""
    Validate AI model compliance with NAIC and FTC requirements.

        Args:
            model_id: Unique model identifier
        model_data: Model metadata and performance data

        Returns:
            Compliance validation result"""
    try:
            # Check model documentation requirements (NAIC Model #672)
        documentation_complete = all(
            [
                model_data.get("development_documentation"),
                model_data.get("validation_documentation"),
                model_data.get("monitoring_procedures"),
                model_data.get("bias_testing_results"),
                model_data.get("performance_benchmarks"),
            ]
        )

            # Check bias testing requirements (FTC guidelines)
        bias_metrics = model_data.get("bias_metrics", {})
        fairness_threshold = 0.8  # 80% fairness score minimum
        fairness_passed = (
            all(
                score >= fairness_threshold
                for score in bias_metrics.values()
                )
            if bias_metrics
                else False
        )

            # Check explainability requirements
        explainability_score = model_data.get("explainability_score", 0.0)
        explainability_passed = explainability_score >= 0.7  # 70% minimum

            # Check performance requirements
        performance_metrics = model_data.get("performance_metrics", {})
        performance_passed = (
            performance_metrics.get("accuracy", 0) >= 0.85
            and performance_metrics.get("precision", 0) >= 0.80
            and performance_metrics.get("recall", 0) >= 0.80
        )

            # Overall compliance status
        compliance_passed = all(
            [
                documentation_complete,
                fairness_passed,
                explainability_passed,
                performance_passed,
            ]
        )

            # Create compliance record
        compliance_record = AIModelCompliance(
            model_id=model_id,
            model_name=model_data.get("name", ""),
            model_version=model_data.get("version", ""),
            validation_date=datetime.now(timezone.utc).isoformat(),
            bias_test_date=model_data.get("bias_test_date", ""),
            performance_metrics=performance_metrics,
            fairness_metrics=bias_metrics,
            explainability_score=explainability_score,
            governance_approval=compliance_passed,
            regulatory_approval=False,  # Requires external approval
            documentation_complete=documentation_complete,
        )

            self.ai_models[model_id] = compliance_record

            # Log compliance event
        if not compliance_passed:
                await self._log_compliance_event(
                ComplianceEvent(
                    event_id=f"ai_compliance_{model_id}_{datetime.now("
                        ).timestamp()}","
                    regulation=ComplianceRegulation.NAIC_AI_GOVERNANCE,
                    event_type="violation",
                    severity="high",
                    description=f"AI model {model_id} failed compliance"
                        validation","
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={
                        "model_id": model_id,
                        "documentation_complete": documentation_complete,
                        "fairness_passed": fairness_passed,
                        "explainability_passed": explainability_passed,
                        "performance_passed": performance_passed,
                    },
                    remediation_required=True,
                    remediation_deadline=(
                        datetime.now(timezone.utc) + timedelta(days=30)
                    ).isoformat(),
                )
            )

            return {
            "compliance_passed": compliance_passed,
            "documentation_complete": documentation_complete,
            "fairness_passed": fairness_passed,
            "explainability_passed": explainability_passed,
            "performance_passed": performance_passed,
            "compliance_record_id": model_id,
            "next_review_date": (
                datetime.now(timezone.utc)
                + timedelta(
                    days=self.compliance_config[
                        "model_validation_frequency_days"
                    ]
                )
            ).isoformat(),
        }

        except Exception as e:
            logger.error(f"AI model compliance validation failed: {e}")
        return {"compliance_passed": False, "error": str(e)}

    async def validate_blockchain_compliance(
        self, blockchain_data: Dict[str, Any]
) -> Dict[str, Any]:"""
    Validate blockchain compliance with regulatory requirements.

        Args:
            blockchain_data: Blockchain configuration and status

        Returns:
            Blockchain compliance validation result"""
    try:
            # Check audit trail requirements
        audit_trail_enabled = blockchain_data.get(
            "audit_trail_enabled", False
        )

            # Check data retention compliance
        retention_policy = blockchain_data.get("data_retention_policy")
        retention_compliant = (
            retention_policy
            and int(retention_policy.split("_")[0])
            >= 2555  # 7 years minimum
        )

            # Check immutability verification
        immutability_verified = blockchain_data.get(
            "immutability_verified", False
        )

            # Check access controls
        access_controls = blockchain_data.get("access_controls", {})
        access_controls_compliant = all(
            [
                access_controls.get("role_based_access"),
                access_controls.get("audit_logging"),
                access_controls.get("regulatory_access"),
                access_controls.get("data_encryption"),
            ]
        )

            # Check regulatory access
        regulatory_access = blockchain_data.get(
            "regulatory_access_enabled", False
        )

            # Check backup and recovery
        backup_tested = blockchain_data.get(
            "backup_procedures_tested", False
        )

            # Overall compliance
        compliance_passed = all(
            [
                audit_trail_enabled,
                retention_compliant,
                immutability_verified,
                access_controls_compliant,
                regulatory_access,
                backup_tested,
            ]
        )

            # Create compliance record
        self.blockchain_compliance = BlockchainCompliance(
            network_id=blockchain_data.get("network_id", ""),
            chaincode_version=blockchain_data.get("chaincode_version", ""),
            audit_trail_enabled=audit_trail_enabled,
            data_retention_policy=retention_policy or "",
            immutability_verified=immutability_verified,
            access_controls_verified=access_controls_compliant,
            regulatory_access_enabled=regulatory_access,
            backup_procedures_tested=backup_tested,
        )

            # Log compliance event if failed
        if not compliance_passed:
                await self._log_compliance_event(
                ComplianceEvent(
                    event_id=f"blockchain_compliance_{datetime.now("
                        ).timestamp()}","
                    regulation=ComplianceRegulation.STATE_CYBERSECURITY,
                    event_type="violation",
                    severity="high",
                    description=(
                        "Blockchain configuration failed compliance "
                        "validation",
                    )
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={
                        "audit_trail_enabled": audit_trail_enabled,
                        "retention_compliant": retention_compliant,
                        "immutability_verified": immutability_verified,
                        "access_controls_compliant":
                                access_controls_compliant,
                        "regulatory_access": regulatory_access,
                        "backup_tested": backup_tested,
                    },
                    remediation_required=True,
                    remediation_deadline=(
                        datetime.now(timezone.utc) + timedelta(days=15)
                    ).isoformat(),
                )
            )

            return {
            "compliance_passed": compliance_passed,
            "audit_trail_enabled": audit_trail_enabled,
            "retention_compliant": retention_compliant,
            "immutability_verified": immutability_verified,
            "access_controls_compliant": access_controls_compliant,
            "regulatory_access_enabled": regulatory_access,
            "backup_procedures_tested": backup_tested,
            "next_review_date": (
                datetime.now(timezone.utc) + timedelta(days=90)
            ).isoformat(),
        }

        except Exception as e:
            logger.error(f"Blockchain compliance validation failed: {e}")
        return {"compliance_passed": False, "error": str(e)}

    async def check_adverse_action_requirements(
        self, decision_data: Dict[str, Any]
) -> Dict[str, Any]:"""
    Check if adverse action notice is required under FCRA.

        Args:
            decision_data: AI decision details

        Returns:
            Adverse action requirements check result"""
    try:
            # Check if decision is adverse
        is_adverse = any(
            [
                decision_data.get("application_denied"),
                decision_data.get("coverage_limited"),
                decision_data.get("premium_increased"),
                decision_data.get("claim_denied"),
                decision_data.get("fraud_detected"),
            ]
        )

            # Check if consumer data was used
        consumer_data_used = any(
            [
                decision_data.get("credit_report_used"),
                decision_data.get("external_data_used"),
                decision_data.get("third_party_data_used"),
            ]
        )

            # FCRA adverse action notice required
        adverse_action_required = is_adverse and consumer_data_used

            if adverse_action_required:
                # Log compliance requirement
            await self._log_compliance_event(
                ComplianceEvent(
                    event_id=f"adverse_action_{decision_data.get("
                        'customer_id')}_{datetime.now().timestamp()}","
                    regulation=ComplianceRegulation.FCRA_ADVERSE_ACTION,
                    event_type="requirement",
                    severity="medium",
                    description="Adverse action notice required under"
                        FCRA","
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={
                        "customer_id": decision_data.get("customer_id"),
                        "decision_type": decision_data.get(
                            "decision_type"
                        ),
                        "is_adverse": is_adverse,
                        "consumer_data_used": consumer_data_used,
                        "data_sources": decision_data.get(
                            "data_sources", []
                        ),
                    },
                    remediation_required=True,
                    remediation_deadline=(
                        datetime.now(timezone.utc) + timedelta(days=15)
                    ).isoformat(),
                )
            )

            return {
            "adverse_action_required": adverse_action_required,
            "is_adverse_decision": is_adverse,
            "consumer_data_used": consumer_data_used,
            "notice_deadline": (
                (
                    datetime.now(timezone.utc) + timedelta(days=15)
                ).isoformat()
                if adverse_action_required
                    else None
            ),
            "required_disclosures": (
                [
                    "Nature of adverse action",
                    "Information sources used",
                    "Consumer rights under FCRA",
                    "Contact information for data sources",
                ]
                if adverse_action_required
                    else []
            ),
        }

        except Exception as e:
            logger.error(f"Adverse action check failed: {e}")
        return {"adverse_action_required": False, "error": str(e)}

    async def monitor_data_privacy_compliance(
        self, data_processing: Dict[str, Any]
) -> Dict[str, Any]:"""
    Monitor GLBA privacy and other data protection compliance.

        Args:
            data_processing: Data processing activity details

        Returns:
            Privacy compliance monitoring result"""
    try:
            # Check consent requirements
        consent_obtained = data_processing.get("consent_obtained", False)
        consent_documented = data_processing.get(
            "consent_documented", False
        )

            # Check data minimization
        data_minimized = data_processing.get("data_minimized", False)
        purpose_limited = data_processing.get("purpose_limited", False)

            # Check security measures
        data_encrypted = data_processing.get("data_encrypted", False)
        access_controlled = data_processing.get("access_controlled", False)

            # Check retention compliance
        retention_policy_applied = data_processing.get(
            "retention_policy_applied", False
        )

            # Overall privacy compliance
        privacy_compliant = all(
            [
                consent_obtained,
                consent_documented,
                data_minimized,
                purpose_limited,
                data_encrypted,
                access_controlled,
                retention_policy_applied,
            ]
        )

            if not privacy_compliant:
                await self._log_compliance_event(
                ComplianceEvent(
                    event_id=f"privacy_violation_{datetime.now("
                        ).timestamp()}","
                    regulation=ComplianceRegulation.GLBA_PRIVACY,
                    event_type="violation",
                    severity="high",
                    description="Data privacy compliance violation"
                        detected","
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details=data_processing,
                    remediation_required=True,
                    remediation_deadline=(
                        datetime.now(timezone.utc) + timedelta(days=7)
                    ).isoformat(),
                )
            )

            return {
            "privacy_compliant": privacy_compliant,
            "consent_status": {
                "obtained": consent_obtained,
                "documented": consent_documented,
            },
            "data_protection": {
                "minimized": data_minimized,
                "purpose_limited": purpose_limited,
                "encrypted": data_encrypted,
                "access_controlled": access_controlled,
            },
            "retention_compliant": retention_policy_applied,
            "recommendations": (
                [
                    "Implement consent management system",
                    "Apply data minimization principles",
                    "Enhance encryption standards",
                    "Strengthen access controls",
                    "Document retention procedures",
                ]
                if not privacy_compliant
                    else []
            ),
        }

        except Exception as e:
            logger.error(f"Privacy compliance monitoring failed: {e}")
        return {"privacy_compliant": False, "error": str(e)}

    async def generate_compliance_report(
        self, start_date: str, end_date: str
) -> Dict[str, Any]:"""
    Generate comprehensive compliance report for regulatory submission.

        Args:
            start_date: Report start date (ISO format)
        end_date: Report end date (ISO format)

        Returns:
            Comprehensive compliance report"""
    try:
            # Filter compliance events by date range
        report_events = [
            event
            for event in self.compliance_events
                if start_date <= event.timestamp <= end_date
            ]

            # Categorize events by regulation
        events_by_regulation = {}
        for event in report_events:
                regulation = event.regulation.value
            if regulation not in events_by_regulation:
                    events_by_regulation[regulation] = []
            events_by_regulation[regulation].append(event)

            # Count violations and remediation status
        total_violations = len(
            [e for e in report_events if e.event_type == "violation"]
        )
        resolved_violations = len(
            [
                e
                for e in report_events
                    if e.event_type == "violation"
                    and not e.remediation_required
            ]
        )
        pending_violations = total_violations - resolved_violations

            # AI model compliance summary
        ai_models_compliant = len(
            [m for m in self.ai_models.values() if m.governance_approval]
        )
        ai_models_total = len(self.ai_models)

            # Generate report
        compliance_report = {
            "report_period": {
                "start_date": start_date,
                "end_date": end_date,
                "generated_date": datetime.now(timezone.utc).isoformat(),
            },
            "executive_summary": {
                "total_compliance_events": len(report_events),
                "total_violations": total_violations,
                "resolved_violations": resolved_violations,
                "pending_violations": pending_violations,
                "overall_compliance_score": (
                    (resolved_violations / total_violations * 100)
                    if total_violations > 0
                        else 100
                ),
            },
            "ai_model_compliance": {
                "total_models": ai_models_total,
                "compliant_models": ai_models_compliant,
                "compliance_rate": (
                    (ai_models_compliant / ai_models_total * 100)
                    if ai_models_total > 0
                        else 0
                ),
                "models_detail": [
                    {
                        "model_id": model.model_id,
                        "model_name": model.model_name,
                        "compliance_status": (
                            "compliant"
                            if model.governance_approval
                                else "non_compliant"
                        ),
                        "last_validation": model.validation_date,
                        "bias_test_date": model.bias_test_date,
                        "explainability_score": model.explainability_score,
                    }
                    for model in self.ai_models.values()
                    ],
            },
            "blockchain_compliance": {
                "network_compliant": (
                    self.blockchain_compliance is not None
                    and self.blockchain_compliance.audit_trail_enabled
                    and self.blockchain_compliance
                        .regulatory_access_enabled
                ),
                "audit_trail_status": (
                    self.blockchain_compliance.audit_trail_enabled
                    if self.blockchain_compliance
                        else False
                ),
                "regulatory_access": (
                    self.blockchain_compliance.regulatory_access_enabled
                    if self.blockchain_compliance
                        else False
                ),
                "data_retention_compliant": (
                    "2555"
                    in (
                        self.blockchain_compliance.data_retention_policy
                        or ""
                    )
                    if self.blockchain_compliance
                        else False
                ),
            },
            "regulation_compliance": {
                regulation: {
                    "total_events": len(events),
                    "violations": len(
                        [e for e in events if e.event_type == "violation"]
                    ),
                    "compliance_checks": len(
                        [e for e in events if e.event_type == "check"]
                    ),
                    "pending_remediations": len(
                        [
                            e
                            for e in events
                                if e.remediation_required
                                and e.event_type == "violation"
                        ]
                    ),
                }
                for regulation, events in events_by_regulation.items()
                },
            "recommendations": [
                "Implement automated compliance monitoring",
                "Enhance AI model documentation",
                "Strengthen blockchain audit capabilities",
                "Improve data privacy controls",
                "Regular third-party compliance assessments",
            ],
            "regulatory_contacts": {
                "primary_regulator": "State Insurance Department",
                "federal_oversight": "Federal Insurance Office",
                "compliance_officer": "compliance@matchedcover.com",
                "next_submission_date": (
                    datetime.now(timezone.utc) + timedelta(days=90)
                ).isoformat(),
            },
        }

            return compliance_report

        except Exception as e:
            logger.error(f"Compliance report generation failed: {e}")
        return {"error": str(e), "report_generated": False}

    async def _log_compliance_event(self, event: ComplianceEvent) -> None:
        """Log a compliance event."""
    self.compliance_events.append(event)
    logger.info(
        f"Compliance event logged: {event.regulation.value} - "
            {event.event_type}""
    )

    async def get_compliance_dashboard(self) -> Dict[str, Any]:
        """Get real-time compliance dashboard data."""
    try:
            # Current compliance status
        recent_events = [
            e
            for e in self.compliance_events
                if datetime.fromisoformat(e.timestamp.replace("Z", "+00:00"))
                > datetime.now(timezone.utc) - timedelta(days=30)
        ]

            pending_violations = [
            e for e in recent_events if e.remediation_required
        ]

            return {
            "overall_status": (
                "compliant"
                if len(pending_violations) == 0
                    else "attention_required"
            ),
            "recent_events_count": len(recent_events),
            "pending_violations_count": len(pending_violations),
            "ai_models_compliant": len(
                [
                    m
                    for m in self.ai_models.values()
                        if m.governance_approval
                    ]
            ),
            "blockchain_compliant": (
                self.blockchain_compliance is not None
                and self.blockchain_compliance.audit_trail_enabled
            ),
            "next_reviews": [
                {
                    "type": "AI Model Validation",
                    "due_date": (
                        datetime.now(timezone.utc) + timedelta(days=90)
                    ).isoformat(),
                },
                {
                    "type": "Blockchain Security Audit",
                    "due_date": (
                        datetime.now(timezone.utc) + timedelta(days=180)
                    ).isoformat(),
                },
                {
                    "type": "Privacy Impact Assessment",
                    "due_date": (
                        datetime.now(timezone.utc) + timedelta(days=365)
                    ).isoformat(),
                },
            ],
            "critical_deadlines": [
                {
                    "description": event.description,
                    "deadline": event.remediation_deadline,
                    "severity": event.severity,
                }
                for event in pending_violations
                    if event.remediation_deadline
                ],
        }

        except Exception as e:
            logger.error(f"Compliance dashboard generation failed: {e}")
        return {"error": str(e)}


# Global compliance manager instance
compliance_manager = ComplianceManager()


async def get_compliance_manager() -> ComplianceManager:
    """Get the global compliance manager instance."""
return compliance_manager
