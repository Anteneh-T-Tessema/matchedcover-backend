"""
AI Agent Integration Module

This module integrates the Guardrail AI agent and Evaluation AI agent
into the main insurance platform workflow, providing comprehensive
AI safety, compliance, and quality assurance.

Key Features:
- Coordinated AI safety and evaluation pipeline
- Real-time guardrail enforcement
- Continuous quality monitoring
- Comprehensive reporting and analytics
- Integration with existing agent orchestrator"""

import logging

from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import uuid

from src.agents.guardrail_ai_agent import GuardrailAIAgent, GuardrailAction
from src.agents.evaluation_ai_agent import EvaluationAIAgent


logger = logging.getLogger(__name__)


@dataclass
class AIDecisionContext:
    """Context for AI decision making with safety and evaluation data."""

    request_id: str
agent_id: str
task_type: str
input_data: Dict[str, Any]
timestamp: str
user_context: Dict[str, Any]
regulatory_context: List[str]


@dataclass
class IntegratedAIResult:
    """Result of integrated AI processing with guardrails and evaluation."""

    decision_id: str
original_result: Dict[str, Any]
guardrail_result: Dict[str, Any]
evaluation_result: Dict[str, Any]
final_decision: Dict[str, Any]
safety_status: str
quality_score: float
compliance_status: str
processing_summary: Dict[str, Any]
recommendations: List[str]


class AIAgentIntegrator:"""
Integrates Guardrail and Evaluation AI agents into the main workflow.
Provides comprehensive AI safety and quality assurance."""

    def __init__(self):
        """Initialize the AI Agent Integrator."""
    self.integrator_id = str(uuid.uuid4())
    self.guardrail_agent: Optional[GuardrailAIAgent] = None
    self.evaluation_agent: Optional[EvaluationAIAgent] = None
    self.initialized = False

        # Configuration
    self.config = {
        "enable_guardrails": True,
        "enable_evaluation": True,
        "blocking_violations": ["CRITICAL", "HIGH"],
        "evaluation_threshold": 0.70,
        "continuous_monitoring": True,
        "store_results": True,
    }

        # Metrics tracking
    self.metrics = {
        "total_requests": 0,
        "blocked_requests": 0,
        "flagged_requests": 0,
        "average_quality_score": 0.0,
        "compliance_rate": 0.0,
    }

    async def initialize(self):
        """Initialize the integrator and its agents."""
    try:
            # Initialize Guardrail AI Agent
        if self.config["enable_guardrails"]:
                self.guardrail_agent = GuardrailAIAgent()
            await self.guardrail_agent.initialize()
            logger.info("Guardrail AI Agent initialized")

            # Initialize Evaluation AI Agent
        if self.config["enable_evaluation"]:
                self.evaluation_agent = EvaluationAIAgent()
            await self.evaluation_agent.initialize()
            logger.info("Evaluation AI Agent initialized")

            self.initialized = True
        logger.info("AI Agent Integrator initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize AI Agent Integrator: {e}")
        raise

    async def process_ai_request(
        self, context: AIDecisionContext, ai_output: Dict[str, Any]
) -> IntegratedAIResult:"""
    Process an AI request through the integrated safety and
        evaluation pipeline.

        Args:
            context: Decision context
        ai_output: Original AI agent output

        Returns:
            Integrated result with safety and quality assessment"""
    if not self.initialized:
            await self.initialize()

        decision_id = str(uuid.uuid4())
    # timestamp = datetime.now(timezone.utc).isoformat()  # Not used
    # currently

        try:
            # Update metrics
        self.metrics["total_requests"] += 1

            # Step 1: Guardrail evaluation (safety check)
        guardrail_result = {}
        if self.guardrail_agent and self.config["enable_guardrails"]:
                guardrail_result = await self._run_guardrail_check(
                context, ai_output
            )

            # Step 2: Evaluation assessment (quality check)
        evaluation_result = {}
        if self.evaluation_agent and self.config["enable_evaluation"]:
                evaluation_result = await self._run_evaluation_check(
                context, ai_output, guardrail_result
            )

            # Step 3: Make final decision based on results
        final_decision = await self._make_final_decision(
            ai_output, guardrail_result, evaluation_result
        )

            # Step 4: Generate summary and recommendations
        processing_summary = self._create_processing_summary(
            guardrail_result, evaluation_result
        )

            recommendations = self._generate_recommendations(
            guardrail_result, evaluation_result
        )

            # Step 5: Update metrics
        await self._update_metrics(guardrail_result, evaluation_result)

            # Create integrated result
        result = IntegratedAIResult(
            decision_id=decision_id,
            original_result=ai_output,
            guardrail_result=guardrail_result,
            evaluation_result=evaluation_result,
            final_decision=final_decision,
            safety_status=self._get_safety_status(guardrail_result),
            quality_score=self._get_quality_score(evaluation_result),
            compliance_status=self._get_compliance_status(
                guardrail_result, evaluation_result
            ),
            processing_summary=processing_summary,
            recommendations=recommendations,
        )

            # Store result for analysis
        if self.config["store_results"]:
                await self._store_result(context, result)

            logger.info(f"AI request processed successfully: {decision_id}")
        return result

        except Exception as e:
            logger.error(f"AI request processing failed: {e}")
        # Return safe default result
        return IntegratedAIResult(
            decision_id=decision_id,
            original_result=ai_output,
            guardrail_result={"error": str(e)},
            evaluation_result={"error": str(e)},
            final_decision={"blocked": True, "reason": "Processing error"},
            safety_status="error",
            quality_score=0.0,
            compliance_status="failed",
            processing_summary={"error": str(e)},
            recommendations=[
                "Review system configuration",
                "Check agent status",
            ],
        )

    async def _run_guardrail_check(
        self, context: AIDecisionContext, ai_output: Dict[str, Any]
) -> Dict[str, Any]:
        """Run guardrail safety check."""
    try:
            if not self.guardrail_agent:
                return {"status": "disabled"}

            # Prepare guardrail input
        guardrail_input = {
            "ai_output": ai_output,
            "original_input": context.input_data,
            "agent_context": {
                "agent_id": context.agent_id,
                "task_type": context.task_type,
                "user_context": context.user_context,
                "regulatory_context": context.regulatory_context,
            },
        }

            # Run guardrail evaluation
        result = await self.guardrail_agent.process_task(
            "evaluate_ai_output",
            guardrail_input,
            {"request_id": context.request_id},
        )

            return result

        except Exception as e:
            logger.error(f"Guardrail check failed: {e}")
        return {
            "decision": GuardrailAction.BLOCK.value,
            "error": str(e),
            "violations": [],
            "risk_score": 1.0,
        }

    async def _run_evaluation_check(
        self,
    context: AIDecisionContext,
    ai_output: Dict[str, Any],
    guardrail_result: Dict[str, Any],
) -> Dict[str, Any]:
        """Run quality evaluation check."""
    try:
            if not self.evaluation_agent:
                return {"status": "disabled"}

            # Prepare evaluation input
        evaluation_input = {
            "output_data": ai_output,
            "agent_id": context.agent_id,
            "task_type": context.task_type,
            "context": {
                "request_id": context.request_id,
                "user_context": context.user_context,
                "guardrail_result": guardrail_result,
            },
        }

            # Run output evaluation
        result = await self.evaluation_agent.process_task(
            "evaluate_output",
            evaluation_input,
            {"request_id": context.request_id},
        )

            return result

        except Exception as e:
            logger.error(f"Evaluation check failed: {e}")
        return {
            "overall_quality": 0.0,
            "error": str(e),
            "quality_scores": {},
            "issues_found": [f"Evaluation failed: {str(e)}"],
        }

    async def _make_final_decision(
        self,
    ai_output: Dict[str, Any],
    guardrail_result: Dict[str, Any],
    evaluation_result: Dict[str, Any],
) -> Dict[str, Any]:
        """Make final decision based on guardrail and evaluation results."""
    try:
            # Check guardrail decision
        guardrail_decision = guardrail_result.get("decision", "allow")
        guardrail_violations = guardrail_result.get("violations", [])

            # Check evaluation quality
        quality_score = evaluation_result.get("overall_quality", 0.0)
        evaluation_issues = evaluation_result.get("issues_found", [])

            # Decision logic
        if guardrail_decision in ["block", "escalate"]:
                return {
                "status": "blocked",
                "reason": "Guardrail violation",
                "details": guardrail_violations,
                "output": None,
            }

            if quality_score < self.config["evaluation_threshold"]:
                return {
                "status": "flagged",
                "reason": "Quality threshold not met",
                "details": evaluation_issues,
                "output": ai_output,
                "warnings": evaluation_issues,
            }

            # Check for critical issues
        critical_issues = [
            issue
            for issue in evaluation_issues
                if "critical" in issue.lower() or "violation" in issue.lower()
            ]

            if critical_issues:
                return {
                "status": "flagged",
                "reason": "Critical issues detected",
                "details": critical_issues,
                "output": ai_output,
                "warnings": critical_issues,
            }

            # Decision approved
        return {
            "status": "approved",
            "reason": "Passed all checks",
            "output": ai_output,
            "quality_score": quality_score,
        }

        except Exception as e:
            logger.error(f"Final decision failed: {e}")
        return {
            "status": "error",
            "reason": f"Decision process failed: {str(e)}",
            "output": None,
        }

    def _create_processing_summary(
        self,
    guardrail_result: Dict[str, Any],
    evaluation_result: Dict[str, Any],
) -> Dict[str, Any]:
        """Create processing summary."""
    return {
        "guardrail_status": guardrail_result.get("decision", "unknown"),
        "evaluation_quality": evaluation_result.get(
            "overall_quality", 0.0
        ),
        "risk_score": guardrail_result.get("risk_score", 0.0),
        "violations_count": len(guardrail_result.get("violations", [])),
        "issues_count": len(evaluation_result.get("issues_found", [])),
        "processing_time_ms": (
            guardrail_result.get("processing_time_ms", 0)
            + evaluation_result.get("processing_time_ms", 0)
        ),
    }

    def _generate_recommendations(
        self,
    guardrail_result: Dict[str, Any],
    evaluation_result: Dict[str, Any],
) -> List[str]:
        """Generate improvement recommendations."""
    recommendations = []

        # Guardrail recommendations
    if "violations" in guardrail_result:
            for violation in guardrail_result["violations"]:
                if (
                    isinstance(violation, dict)
                and "mitigation_suggestions" in violation
            ):
                    recommendations.extend(violation["mitigation_suggestions"])

        # Evaluation recommendations
    if "improvement_suggestions" in evaluation_result:
            recommendations.extend(
            evaluation_result["improvement_suggestions"]
        )

        # General recommendations
    risk_score = guardrail_result.get("risk_score", 0.0)
    quality_score = evaluation_result.get("overall_quality", 1.0)

        if risk_score > 0.7:
            recommendations.append(
            "Implement additional risk mitigation measures"
        )

        if quality_score < 0.8:
            recommendations.append("Review and improve output quality")

        return list(set(recommendations))  # Remove duplicates

    def _get_safety_status(self, guardrail_result: Dict[str, Any]) -> str:
        """Get safety status from guardrail result."""
    decision = guardrail_result.get("decision", "unknown")
    risk_score = guardrail_result.get("risk_score", 0.0)

        if decision == "block":
            return "unsafe"
    elif decision == "warn" or risk_score > 0.5:
            return "caution"
    elif decision == "allow":
            return "safe"
    else:
            return "unknown"

    def _get_quality_score(self, evaluation_result: Dict[str, Any]) -> float:
        """Get quality score from evaluation result."""
    return evaluation_result.get("overall_quality", 0.0)

    def _get_compliance_status(
        self,
    guardrail_result: Dict[str, Any],
    evaluation_result: Dict[str, Any],
) -> str:
        """Get compliance status."""
    # Check guardrail compliance
    compliance_status = guardrail_result.get("compliance_status", {})
    guardrail_compliant = compliance_status.get("compliant", False)

        # Check evaluation compliance
    compliance_scores = evaluation_result.get("compliance_scores", {})
    eval_compliant = all(
        score >= 0.9 for score in compliance_scores.values()
    )

        if guardrail_compliant and eval_compliant:
            return "compliant"
    elif guardrail_compliant or eval_compliant:
            return "partial"
    else:
            return "non_compliant"

    async def _update_metrics(
        self,
    guardrail_result: Dict[str, Any],
    evaluation_result: Dict[str, Any],
):
        """Update performance metrics."""
    try:
            # Update blocking metrics
        if guardrail_result.get("decision") == "block":
                self.metrics["blocked_requests"] += 1

            # Update flagging metrics
        if (
                guardrail_result.get("decision") == "warn"
            or evaluation_result.get("overall_quality", 1.0)
            < self.config["evaluation_threshold"]
        ):
                self.metrics["flagged_requests"] += 1

            # Update quality metrics
        quality_score = evaluation_result.get("overall_quality", 0.0)
        if quality_score > 0:
                current_avg = self.metrics["average_quality_score"]
            total_requests = self.metrics["total_requests"]
            self.metrics["average_quality_score"] = (
                current_avg * (total_requests - 1) + quality_score
            ) / total_requests

            # Update compliance metrics
        compliance_status = self._get_compliance_status(
            guardrail_result, evaluation_result
        )
        if compliance_status == "compliant":
                compliant_requests = (
                self.metrics["compliance_rate"]
                * (self.metrics["total_requests"] - 1)
                + 1
            )
            self.metrics["compliance_rate"] = (
                compliant_requests / self.metrics["total_requests"]
            )
        else:
                compliant_requests = self.metrics["compliance_rate"] * (
                self.metrics["total_requests"] - 1
            )
            self.metrics["compliance_rate"] = (
                compliant_requests / self.metrics["total_requests"]
            )

        except Exception as e:
            logger.error(f"Metrics update failed: {e}")

    async def _store_result(
        self, context: AIDecisionContext, result: IntegratedAIResult
):
        """Store result for historical analysis."""
    try:
            # In a real implementation, this would store to a database
        # For now, just log the result
        logger.info(f"Stored result: {result.decision_id}")
    except Exception as e:
            logger.error(f"Result storage failed: {e}")

    async def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
    return {
        "metrics": self.metrics.copy(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "integrator_id": self.integrator_id,
    }

    async def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
    return {
        "initialized": self.initialized,
        "guardrail_agent_status": (
            "active" if self.guardrail_agent else "disabled"
        ),
        "evaluation_agent_status": (
            "active" if self.evaluation_agent else "disabled"
        ),
        "config": self.config.copy(),
        "metrics": self.metrics.copy(),
    }

    async def update_config(self, new_config: Dict[str, Any]):
        """Update configuration."""
    self.config.update(new_config)
    logger.info("Configuration updated")


# Factory function for easy instantiation
async def create_ai_agent_integrator() -> AIAgentIntegrator:
    """Create and initialize an AI Agent Integrator."""
integrator = AIAgentIntegrator()
await integrator.initialize()
return integrator


# Convenience function for one-time AI processing
async def process_ai_with_safety(
    agent_id: str,
task_type: str,
input_data: Dict[str, Any],
ai_output: Dict[str, Any],
user_context: Dict[str, Any] = None,
regulatory_context: List[str] = None,
) -> IntegratedAIResult:"""
Process AI output with integrated safety and evaluation checks.
Convenience function for one-time processing."""
integrator = await create_ai_agent_integrator()

    context = AIDecisionContext(
    request_id=str(uuid.uuid4()),
    agent_id=agent_id,
    task_type=task_type,
    input_data=input_data,
    timestamp=datetime.now(timezone.utc).isoformat(),
    user_context=user_context or {},
    regulatory_context=regulatory_context or [],
)

    return await integrator.process_ai_request(context, ai_output)
