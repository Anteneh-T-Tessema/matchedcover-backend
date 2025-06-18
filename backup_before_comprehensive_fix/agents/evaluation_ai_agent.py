""""
Evaluation AI Agent for Insurance Platform

This agent implements comprehensive evaluation and assessment capabilities
for AI models, outputs, and decisions in the insurance platform. It provides
systematic quality assurance, performance monitoring, and continuous
improvement insights.

Key Features:
- AI model performance evaluation
- Output quality assessment
- Decision accuracy validation
- Bias and fairness evaluation
- Regulatory compliance assessment
- Business impact analysis
- Model drift detection
- A/B testing support
- Continuous monitoring
""""

import logging
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from sklearn.metrics import (
accuracy_score,
precision_score,
recall_score,
f1_score,
)

from src.agents.base_agent import BaseAgent
from src.compliance.regulatory_compliance import get_compliance_manager

logger = logging.getLogger(__name__)


class EvaluationMetricType(Enum):
    """Types of evaluation metrics."""

    ACCURACY = "accuracy"
PRECISION = "precision"
RECALL = "recall"
F1_SCORE = "f1_score"
AUC_ROC = "auc_roc"
BIAS_SCORE = "bias_score"
FAIRNESS_SCORE = "fairness_score"
COMPLIANCE_SCORE = "compliance_score"
BUSINESS_IMPACT = "business_impact"
MODEL_DRIFT = "model_drift"
RESPONSE_TIME = "response_time"
THROUGHPUT = "throughput"
ERROR_RATE = "error_rate"


class EvaluationCategory(Enum):
    """Categories of evaluation."""

    MODEL_PERFORMANCE = "model_performance"
OUTPUT_QUALITY = "output_quality"
BIAS_FAIRNESS = "bias_fairness"
COMPLIANCE = "compliance"
BUSINESS_METRICS = "business_metrics"
OPERATIONAL = "operational"
SAFETY = "safety"


class EvaluationStatus(Enum):
    """Status of evaluation results."""

    PASS = "pass"
WARNING = "warning"
FAIL = "fail"
UNKNOWN = "unknown"


@dataclass
class EvaluationMetric:
    """Represents an evaluation metric."""

    metric_id: str
metric_type: EvaluationMetricType
category: EvaluationCategory
value: float
threshold: float
status: EvaluationStatus
description: str
timestamp: str
metadata: Dict[str, Any]


@dataclass
class ModelEvaluation:
    """Comprehensive model evaluation results."""

    evaluation_id: str
model_id: str
model_version: str
evaluation_timestamp: str
metrics: List[EvaluationMetric]
overall_score: float
overall_status: EvaluationStatus
recommendations: List[str]
compliance_assessment: Dict[str, Any]
bias_analysis: Dict[str, Any]
performance_summary: Dict[str, Any]
drift_analysis: Dict[str, Any]


@dataclass
class OutputEvaluation:
    """Evaluation of AI output quality."""

    output_id: str
agent_id: str
task_type: str
evaluation_timestamp: str
quality_scores: Dict[str, float]
compliance_scores: Dict[str, float]
safety_scores: Dict[str, float]
overall_quality: float
issues_found: List[str]
improvement_suggestions: List[str]


@dataclass
class BiasEvaluation:
    """Bias evaluation results."""

    evaluation_id: str
protected_attributes: List[str]
bias_metrics: Dict[str, float]
fairness_metrics: Dict[str, float]
demographic_parity: float
equal_opportunity: float
equalized_odds: float
statistical_parity: float
overall_bias_score: float
bias_status: EvaluationStatus
mitigation_recommendations: List[str]


class EvaluationAIAgent(BaseAgent):
    """"
Evaluation AI Agent that provides comprehensive assessment and monitoring
of AI models, outputs, and decisions in the insurance platform.
""""

    def __init__(self):
        """Initialize the Evaluation AI Agent."""
    super().__init__("evaluation_ai", "Evaluation AI Agent")
    self.agent_id = "evaluation_ai_agent"
    self.agent_name = "Evaluation AI Agent"
    self.agent_version = "1.0.0"
    self.compliance_manager = None

        # Evaluation thresholds
    self.performance_thresholds = {
        "accuracy": 0.85,
        "precision": 0.80,
        "recall": 0.80,
        "f1_score": 0.82,
        "auc_roc": 0.85,
    }

        self.bias_thresholds = {
        "demographic_parity": 0.80,
        "equal_opportunity": 0.80,
        "equalized_odds": 0.80,
        "statistical_parity": 0.80,
    }

        self.compliance_thresholds = {
        "regulatory_compliance": 0.95,
        "privacy_protection": 0.98,
        "data_security": 0.99,
        "audit_readiness": 0.90,
    }

        # Historical data for drift detection
    self.baseline_metrics = {}
    self.evaluation_history = []

    async def initialize(self):
        """Initialize the evaluation agent."""
    await super().initialize()

        try:
            self.compliance_manager = await get_compliance_manager()
        await self._load_baseline_metrics()
        logger.info("Evaluation AI Agent initialized successfully")
    except Exception as e:
            logger.error(f"Failed to initialize evaluation agent: {e}")
        raise

    async def process_task(
        self,
    task_type: str,
    input_data: Dict[str, Any],
    context: Dict[str, Any],
) -> Dict[str, Any]:
        """"
    Process evaluation tasks.

        Args:
            task_type: Type of evaluation task
        input_data: Data to evaluate
        context: Additional context

        Returns:
            Evaluation result
    """"
    start_time = datetime.now()

        try:
            if task_type == "evaluate_model":
                model_id = input_data.get("model_id")
            test_data = input_data.get("test_data")
            predictions = input_data.get("predictions")
            ground_truth = input_data.get("ground_truth")

                if not all(
                    [
                    model_id,
                    test_data is not None,
                    predictions is not None,
                    ground_truth is not None,
                ]
            ):
                    raise ValueError(
                    "Missing required parameters for model evaluation"
                )

                eval_result = await self._evaluate_model(
                str(model_id),
                test_data if isinstance(test_data, dict) else {},
                predictions if isinstance(predictions, list) else [],
                ground_truth if isinstance(ground_truth, list) else [],
                context,
            )
            result = asdict(eval_result)
        elif task_type == "evaluate_output":
                output_data = input_data.get("output_data")
            agent_id = input_data.get("agent_id")
            task_type_val = input_data.get("task_type")

                if not all([output_data is not None, agent_id, task_type_val]):
                    raise ValueError(
                    "Missing required parameters for output evaluation"
                )

                eval_result = await self._evaluate_output(
                output_data if isinstance(output_data, dict) else {},
                str(agent_id),
                str(task_type_val),
                context,
            )
            result = asdict(eval_result)
        elif task_type == "evaluate_bias":
                predictions = input_data.get("predictions")
            protected_attributes = input_data.get("protected_attributes")
            ground_truth = input_data.get("ground_truth")

                if not all(
                    [
                    predictions is not None,
                    protected_attributes is not None,
                    ground_truth is not None,
                ]
            ):
                    raise ValueError(
                    "Missing required parameters for bias evaluation"
                )

                eval_result = await self._evaluate_bias(
                predictions if isinstance(predictions, list) else [],
                (
                    protected_attributes
                    if isinstance(protected_attributes, dict)
                        else {}
                ),
                ground_truth if isinstance(ground_truth, list) else [],
                context,
            )
            result = asdict(eval_result)
        elif task_type == "detect_drift":
                current_metrics = input_data.get("current_metrics")
            model_id = input_data.get("model_id")

                if not all([current_metrics is not None, model_id]):
                    raise ValueError(
                    "Missing required parameters for drift detection"
                )

                result = await self._detect_drift(
                (
                    current_metrics
                    if isinstance(current_metrics, dict)
                        else {}
                ),
                str(model_id),
                context,
            )
        elif task_type == "compliance_evaluation":
                decision_data = input_data.get("decision_data")
            regulations = input_data.get("regulations")

                if not all(
                    [decision_data is not None, regulations is not None]
            ):
                    raise ValueError(
                    "Missing required parameters for compliance evaluation"
                )

                result = await self._evaluate_compliance(
                decision_data if isinstance(decision_data, dict) else {},
                regulations if isinstance(regulations, list) else [],
                context,
            )
        elif task_type == "continuous_monitoring":
                monitoring_config = input_data.get("monitoring_config")

                if monitoring_config is None:
                    raise ValueError(
                    "Missing required parameters for continuous monitoring"
                )

                result = await self._continuous_monitoring(
                (
                    monitoring_config
                    if isinstance(monitoring_config, dict)
                        else {}
                ),
                context,
            )
        else:
                raise ValueError(f"Unknown evaluation task type: {task_type}")

            processing_time = (
            datetime.now() - start_time
        ).total_seconds() * 1000
        result["processing_time_ms"] = processing_time

            # Store evaluation results for historical analysis
        await self._store_evaluation_result(task_type, result)

            return result

        except Exception as e:
            logger.error(f"Evaluation task processing failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "processing_time_ms": (
                datetime.now() - start_time
            ).total_seconds()
            * 1000,
        }

    async def _evaluate_model(
        self,
    model_id: str,
    test_data: Dict[str, Any],
    predictions: List[Any],
    ground_truth: List[Any],
    context: Dict[str, Any],
) -> ModelEvaluation:
        """"
    Comprehensive model evaluation.

        Args:
            model_id: Identifier of the model
        test_data: Test dataset
        predictions: Model predictions
        ground_truth: True labels
        context: Evaluation context

        Returns:
            Comprehensive model evaluation
    """"
    evaluation_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

        try:
            # Calculate performance metrics
        performance_metrics = await self._calculate_performance_metrics(
            predictions, ground_truth
        )

            # Bias analysis
        bias_analysis = await self._analyze_bias(
            predictions,
            ground_truth,
            test_data.get("protected_attributes", {}),
        )

            # Compliance assessment
        compliance_assessment = await self._assess_compliance(
            model_id, predictions, test_data, context
        )

            # Drift detection
        drift_analysis = await self._analyze_drift(
            model_id, performance_metrics
        )

            # Overall evaluation
        overall_score = self._calculate_overall_score(
            performance_metrics, bias_analysis, compliance_assessment
        )

            overall_status = self._determine_overall_status(overall_score)

            recommendations = self._generate_recommendations(
            performance_metrics,
            bias_analysis,
            compliance_assessment,
            drift_analysis,
        )

            return ModelEvaluation(
            evaluation_id=evaluation_id,
            model_id=model_id,
            model_version=context.get("model_version", "unknown"),
            evaluation_timestamp=timestamp,
            metrics=performance_metrics,
            overall_score=overall_score,
            overall_status=overall_status,
            recommendations=recommendations,
            compliance_assessment=compliance_assessment,
            bias_analysis=bias_analysis,
            performance_summary=self._create_performance_summary(
                performance_metrics
            ),
            drift_analysis=drift_analysis,
        )

        except Exception as e:
            logger.error(f"Model evaluation failed: {e}")
        raise

    async def _evaluate_output(
        self,
    output_data: Dict[str, Any],
    agent_id: str,
    task_type: str,
    context: Dict[str, Any],
) -> OutputEvaluation:
        """"
    Evaluate AI output quality.

        Args:
            output_data: AI output to evaluate
        agent_id: ID of the agent that produced the output
        task_type: Type of task
        context: Evaluation context

        Returns:
            Output quality evaluation
    """"
    output_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

        try:
            # Quality assessment
        quality_scores = await self._assess_output_quality(
            output_data, task_type
        )

            # Compliance assessment
        compliance_scores = await self._assess_output_compliance(
            output_data, context
        )

            # Safety assessment
        safety_scores = await self._assess_output_safety(output_data)

            # Overall quality calculation
        overall_quality = self._calculate_output_quality(
            quality_scores, compliance_scores, safety_scores
        )

            # Issue detection
        issues_found = self._detect_output_issues(
            output_data, quality_scores, compliance_scores, safety_scores
        )

            # Improvement suggestions
        improvement_suggestions = self._generate_output_improvements(
            quality_scores, compliance_scores, safety_scores, issues_found
        )

            return OutputEvaluation(
            output_id=output_id,
            agent_id=agent_id,
            task_type=task_type,
            evaluation_timestamp=timestamp,
            quality_scores=quality_scores,
            compliance_scores=compliance_scores,
            safety_scores=safety_scores,
            overall_quality=overall_quality,
            issues_found=issues_found,
            improvement_suggestions=improvement_suggestions,
        )

        except Exception as e:
            logger.error(f"Output evaluation failed: {e}")
        raise

    async def _evaluate_bias(
        self,
    predictions: List[Any],
    protected_attributes: Dict[str, List[Any]],
    ground_truth: List[Any],
    context: Dict[str, Any],
) -> BiasEvaluation:
        """"
    Comprehensive bias evaluation.

        Args:
            predictions: Model predictions
        protected_attributes: Protected attribute values
        ground_truth: True labels
        context: Evaluation context

        Returns:
            Bias evaluation results
    """"
    evaluation_id = str(uuid.uuid4())

        try:
            # Calculate bias metrics
        bias_metrics = {}
        fairness_metrics = {}

            for attr_name, attr_values in protected_attributes.items():
                # Demographic parity
            bias_metrics[f"{attr_name}_demographic_parity"] = (
                self._calculate_demographic_parity(
                    predictions, attr_values
                )
            )

                # Equal opportunity
            bias_metrics[f"{attr_name}_equal_opportunity"] = (
                self._calculate_equal_opportunity(
                    predictions, ground_truth, attr_values
                )
            )

                # Equalized odds
            bias_metrics[f"{attr_name}_equalized_odds"] = (
                self._calculate_equalized_odds(
                    predictions, ground_truth, attr_values
                )
            )

                # Statistical parity
            fairness_metrics[f"{attr_name}_statistical_parity"] = (
                self._calculate_statistical_parity(
                    predictions, attr_values
                )
            )

            # Overall bias assessment
        demographic_parity = np.mean(
            [
                v
                for k, v in bias_metrics.items()
                    if "demographic_parity" in k
                ]
        )

            equal_opportunity = np.mean(
            [
                v
                for k, v in bias_metrics.items()
                    if "equal_opportunity" in k
                ]
        )

            equalized_odds = np.mean(
            [v for k, v in bias_metrics.items() if "equalized_odds" in k]
        )

            statistical_parity = np.mean(
            [
                v
                for k, v in fairness_metrics.items()
                    if "statistical_parity" in k
                ]
        )

            overall_bias_score = np.mean(
            [
                demographic_parity,
                equal_opportunity,
                equalized_odds,
                statistical_parity,
            ]
        )

            # Determine bias status
        bias_status = self._determine_bias_status(overall_bias_score)

            # Generate mitigation recommendations
        mitigation_recommendations = self._generate_bias_mitigation(
            bias_metrics, fairness_metrics, protected_attributes
        )

            return BiasEvaluation(
            evaluation_id=evaluation_id,
            protected_attributes=list(protected_attributes.keys()),
            bias_metrics=bias_metrics,
            fairness_metrics=fairness_metrics,
            demographic_parity=demographic_parity,
            equal_opportunity=equal_opportunity,
            equalized_odds=equalized_odds,
            statistical_parity=statistical_parity,
            overall_bias_score=overall_bias_score,
            bias_status=bias_status,
            mitigation_recommendations=mitigation_recommendations,
        )

        except Exception as e:
            logger.error(f"Bias evaluation failed: {e}")
        raise

    async def _detect_drift(
        self,
    current_metrics: Dict[str, float],
    model_id: str,
    context: Dict[str, Any],
) -> Dict[str, Any]:
        """"
    Detect model drift by comparing current metrics to baseline.

        Args:
            current_metrics: Current model performance metrics
        model_id: Model identifier
        context: Drift detection context

        Returns:
            Drift detection results
    """"
    try:
            baseline_metrics = self.baseline_metrics.get(model_id, {})

            if not baseline_metrics:
                logger.warning(
                f"No baseline metrics found for model {model_id}"
            )
            return {
                "drift_detected": False,
                "drift_score": 0.0,
                "message": "No baseline metrics available",
            }

            drift_scores = {}
        significant_drifts = []

            for metric_name, current_value in current_metrics.items():
                if metric_name in baseline_metrics:
                    baseline_value = baseline_metrics[metric_name]

                    # Calculate drift as percentage change
                if baseline_value != 0:
                        drift = (
                        abs(current_value - baseline_value)
                        / baseline_value
                    )
                else:
                        drift = abs(current_value - baseline_value)

                    drift_scores[metric_name] = drift

                    # Check for significant drift (>10% change)
                if drift > 0.10:
                        significant_drifts.append(
                        {
                            "metric": metric_name,
                            "baseline_value": baseline_value,
                            "current_value": current_value,
                            "drift_score": drift,
                        }
                    )

            overall_drift_score = (
            np.mean(list(drift_scores.values())) if drift_scores else 0.0
        )
        drift_detected = overall_drift_score > 0.05  # 5% threshold

            return {
            "drift_detected": drift_detected,
            "overall_drift_score": overall_drift_score,
            "metric_drift_scores": drift_scores,
            "significant_drifts": significant_drifts,
            "recommendations": self._generate_drift_recommendations(
                significant_drifts
            ),
        }

        except Exception as e:
            logger.error(f"Drift detection failed: {e}")
        return {"drift_detected": False, "error": str(e)}

    async def _evaluate_compliance(
        self,
    decision_data: Dict[str, Any],
    regulations: List[str],
    context: Dict[str, Any],
) -> Dict[str, Any]:
        """"
    Evaluate compliance with regulatory requirements.

        Args:
            decision_data: Decision data to evaluate
        regulations: List of applicable regulations
        context: Compliance context

        Returns:
            Compliance evaluation results
    """"
    try:
            compliance_scores = {}
        violations = []

            if self.compliance_manager:
                for regulation in regulations:
                    try:
                        # Assess compliance for each regulation
                    assessment = (
                        await self.compliance_manager.assess_compliance(
                            regulation, decision_data, context
                        )
                    )

                        compliance_scores[regulation] = assessment.get(
                        "score", 0.0
                    )

                        if not assessment.get("compliant", False):
                            violations.append(
                            {
                                "regulation": regulation,
                                "issues": assessment.get("issues", []),
                                "severity": assessment.get(
                                    "severity", "medium"
                                ),
                            }
                        )

                    except Exception as e:
                        logger.error(
                        f"Compliance assessment failed for {regulation}:"
                            {e}""
                    )
                    compliance_scores[regulation] = 0.0
                    violations.append(
                        {
                            "regulation": regulation,
                            "issues": [f"Assessment failed: {str(e)}"],
                            "severity": "high",
                        }
                    )

            overall_compliance_score = (
            np.mean(list(compliance_scores.values()))
            if compliance_scores
                else 0.0
        )

            return {
            "overall_compliance_score": overall_compliance_score,
            "regulation_scores": compliance_scores,
            "violations": violations,
            "compliant": len(violations) == 0,
            "recommendations": self._generate_compliance_recommendations(
                violations
            ),
        }

        except Exception as e:
            logger.error(f"Compliance evaluation failed: {e}")
        return {"overall_compliance_score": 0.0, "error": str(e)}

    async def _continuous_monitoring(
        self, monitoring_config: Dict[str, Any], context: Dict[str, Any]
) -> Dict[str, Any]:
        """"
    Perform continuous monitoring of AI systems.

        Args:
            monitoring_config: Configuration for monitoring
        context: Monitoring context

        Returns:
            Monitoring results
    """"
    try:
            results = {
            "monitoring_timestamp": datetime.now(timezone.utc).isoformat(),
            "alerts": [],
            "metrics": {},
            "status": "healthy",
        }

            # Monitor model performance
        if monitoring_config.get("monitor_performance", True):
                performance_status = await self._monitor_performance()
            results["metrics"]["performance"] = performance_status

                if performance_status.get("status") != "healthy":
                    results["alerts"].append(
                    {
                        "type": "performance_degradation",
                        "severity": "medium",
                        "message": "Model performance degradation"
                            detected","
                    }
                )

            # Monitor bias levels
        if monitoring_config.get("monitor_bias", True):
                bias_status = await self._monitor_bias()
            results["metrics"]["bias"] = bias_status

                if bias_status.get("status") != "healthy":
                    results["alerts"].append(
                    {
                        "type": "bias_increase",
                        "severity": "high",
                        "message": "Increased bias levels detected",
                    }
                )

            # Monitor compliance
        if monitoring_config.get("monitor_compliance", True):
                compliance_status = await self._monitor_compliance()
            results["metrics"]["compliance"] = compliance_status

                if compliance_status.get("status") != "healthy":
                    results["alerts"].append(
                    {
                        "type": "compliance_violation",
                        "severity": "critical",
                        "message": "Compliance violations detected",
                    }
                )

            # Overall system status
        if results["alerts"]:
                results["status"] = (
                "degraded"
                if any(
                        alert["severity"] in ["medium", "high"]
                    for alert in results["alerts"]
                    )
                else "critical"
            )

            return results

        except Exception as e:
            logger.error(f"Continuous monitoring failed: {e}")
        return {"status": "error", "error": str(e)}

    # Helper methods for calculations

    async def _calculate_performance_metrics(
        self, predictions: List[Any], ground_truth: List[Any]
) -> List[EvaluationMetric]:
        """Calculate standard performance metrics."""
    metrics = []
    timestamp = datetime.now(timezone.utc).isoformat()

        try:
            # Convert to numpy arrays for easier computation
        y_true = np.array(ground_truth)
        y_pred = np.array(predictions)

            # Accuracy
        accuracy = accuracy_score(y_true, y_pred)
        metrics.append(
            EvaluationMetric(
                metric_id=str(uuid.uuid4()),
                metric_type=EvaluationMetricType.ACCURACY,
                category=EvaluationCategory.MODEL_PERFORMANCE,
                value=accuracy,
                threshold=self.performance_thresholds["accuracy"],
                status=(
                    EvaluationStatus.PASS
                    if accuracy >= self.performance_thresholds["accuracy"]
                        else EvaluationStatus.FAIL
                ),
                description="Model accuracy on test data",
                timestamp=timestamp,
                metadata={"sample_size": len(y_true)},
            )
        )

            # Precision, Recall, F1 (for binary/multiclass)
        if len(np.unique(y_true)) <= 10:  # Assuming classification
                precision = precision_score(
                y_true, y_pred, average="weighted", zero_division=0
            )
            recall = recall_score(
                y_true, y_pred, average="weighted", zero_division=0
            )
            f1 = f1_score(
                y_true, y_pred, average="weighted", zero_division=0
            )

                metrics.extend(
                [
                    EvaluationMetric(
                        metric_id=str(uuid.uuid4()),
                        metric_type=EvaluationMetricType.PRECISION,
                        category=EvaluationCategory.MODEL_PERFORMANCE,
                        value=precision,
                        threshold=self.performance_thresholds["precision"],
                        status=(
                            EvaluationStatus.PASS
                            if precision
                                >= self.performance_thresholds["precision"]
                            else EvaluationStatus.FAIL
                        ),
                        description="Model precision (weighted average)",
                        timestamp=timestamp,
                        metadata={"average_type": "weighted"},
                    ),
                    EvaluationMetric(
                        metric_id=str(uuid.uuid4()),
                        metric_type=EvaluationMetricType.RECALL,
                        category=EvaluationCategory.MODEL_PERFORMANCE,
                        value=recall,
                        threshold=self.performance_thresholds["recall"],
                        status=(
                            EvaluationStatus.PASS
                            if recall
                                >= self.performance_thresholds["recall"]
                            else EvaluationStatus.FAIL
                        ),
                        description="Model recall (weighted average)",
                        timestamp=timestamp,
                        metadata={"average_type": "weighted"},
                    ),
                    EvaluationMetric(
                        metric_id=str(uuid.uuid4()),
                        metric_type=EvaluationMetricType.F1_SCORE,
                        category=EvaluationCategory.MODEL_PERFORMANCE,
                        value=f1,
                        threshold=self.performance_thresholds["f1_score"],
                        status=(
                            EvaluationStatus.PASS
                            if f1
                                >= self.performance_thresholds["f1_score"]
                            else EvaluationStatus.FAIL
                        ),
                        description="Model F1 score (weighted average)",
                        timestamp=timestamp,
                        metadata={"average_type": "weighted"},
                    ),
                ]
            )

            return metrics

        except Exception as e:
            logger.error(f"Performance metrics calculation failed: {e}")
        return []

    def _calculate_demographic_parity(
        self, predictions: List[Any], protected_attribute: List[Any]
) -> float:
        """Calculate demographic parity metric."""
    try:
            df = pd.DataFrame(
            {
                "prediction": predictions,
                "protected_attr": protected_attribute,
            }
        )

            # Calculate positive prediction rates for each group
        positive_rates = df.groupby("protected_attr")["prediction"].mean()

            # Demographic parity is the ratio of min to max positive rates
        if len(positive_rates) > 1:
                return (
                positive_rates.min() / positive_rates.max()
                if positive_rates.max() > 0
                    else 1.0
            )
        else:
                return 1.0

        except Exception as e:
            logger.error(f"Demographic parity calculation failed: {e}")
        return 0.0

    def _calculate_equal_opportunity(
        self,
    predictions: List[Any],
    ground_truth: List[Any],
    protected_attribute: List[Any],
) -> float:
        """Calculate equal opportunity metric."""
    try:
            df = pd.DataFrame(
            {
                "prediction": predictions,
                "ground_truth": ground_truth,
                "protected_attr": protected_attribute,
            }
        )

            # Filter to positive class only
        positive_class = df[df["ground_truth"] == 1]

            if len(positive_class) == 0:
                return 1.0

            # Calculate true positive rates for each group
        tpr_by_group = positive_class.groupby("protected_attr")[
            "prediction"
        ].mean()

            # Equal opportunity is the ratio of min to max TPR
        if len(tpr_by_group) > 1:
                return (
                tpr_by_group.min() / tpr_by_group.max()
                if tpr_by_group.max() > 0
                    else 1.0
            )
        else:
                return 1.0

        except Exception as e:
            logger.error(f"Equal opportunity calculation failed: {e}")
        return 0.0

    def _calculate_equalized_odds(
        self,
    predictions: List[Any],
    ground_truth: List[Any],
    protected_attribute: List[Any],
) -> float:
        """Calculate equalized odds metric."""
    try:
            # Equal opportunity for both positive and negative classes
        eo_positive = self._calculate_equal_opportunity(
            predictions, ground_truth, protected_attribute
        )

            # Flip ground truth and predictions for negative class
        eo_negative = self._calculate_equal_opportunity(
            [1 - p for p in predictions],
            [1 - gt for gt in ground_truth],
            protected_attribute,
        )

            # Return the minimum of the two
        return min(eo_positive, eo_negative)

        except Exception as e:
            logger.error(f"Equalized odds calculation failed: {e}")
        return 0.0

    def _calculate_statistical_parity(
        self, predictions: List[Any], protected_attribute: List[Any]
) -> float:
        """Calculate statistical parity metric."""
    # Statistical parity is the same as demographic parity
    return self._calculate_demographic_parity(
        predictions, protected_attribute
    )

    def _calculate_overall_score(
        self,
    performance_metrics: List[EvaluationMetric],
    bias_analysis: Dict[str, Any],
    compliance_assessment: Dict[str, Any],
) -> float:
        """Calculate overall evaluation score."""
    try:
            # Performance score (average of all performance metrics)
        performance_values = [m.value for m in performance_metrics]
        performance_score = (
            np.mean(performance_values) if performance_values else 0.0
        )

            # Bias score
        bias_score = bias_analysis.get("overall_bias_score", 0.0)

            # Compliance score
        compliance_score = compliance_assessment.get(
            "overall_compliance_score", 0.0
        )

            # Weighted average (performance 40%, bias 30%, compliance 30%)
        overall_score = (
            0.4 * performance_score
            + 0.3 * bias_score
            + 0.3 * compliance_score
        )

            return overall_score

        except Exception as e:
            logger.error(f"Overall score calculation failed: {e}")
        return 0.0

    def _determine_overall_status(
        self, overall_score: float
) -> EvaluationStatus:
        """Determine overall evaluation status based on score."""
    if overall_score >= 0.90:
            return EvaluationStatus.PASS
    elif overall_score >= 0.70:
            return EvaluationStatus.WARNING
    else:
            return EvaluationStatus.FAIL

    def _determine_bias_status(self, bias_score: float) -> EvaluationStatus:
        """Determine bias status based on score."""
    if bias_score >= 0.85:
            return EvaluationStatus.PASS
    elif bias_score >= 0.70:
            return EvaluationStatus.WARNING
    else:
            return EvaluationStatus.FAIL

    # Additional helper methods...

    async def _load_baseline_metrics(self):
        """Load baseline metrics for drift detection."""
    try:
            # In a real implementation, this would load from a database
        # For now, initialize empty baseline metrics
        self.baseline_metrics = {}
        logger.info("Baseline metrics loaded")
    except Exception as e:
            logger.error(f"Failed to load baseline metrics: {e}")

    async def _store_evaluation_result(
        self, task_type: str, result: Dict[str, Any]
):
        """Store evaluation result for historical analysis."""
    try:
            # In a real implementation, this would store to a database
        self.evaluation_history.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "task_type": task_type,
                "result": result,
            }
        )

            # Keep only last 1000 results to prevent memory issues
        if len(self.evaluation_history) > 1000:
                self.evaluation_history = self.evaluation_history[-1000:]

        except Exception as e:
            logger.error(f"Failed to store evaluation result: {e}")

    def _generate_recommendations(
        self,
    performance_metrics: List[EvaluationMetric],
    bias_analysis: Dict[str, Any],
    compliance_assessment: Dict[str, Any],
    drift_analysis: Dict[str, Any],
) -> List[str]:
        """Generate improvement recommendations."""
    recommendations = []

        # Performance recommendations
    failing_metrics = [
        m for m in performance_metrics if m.status == EvaluationStatus.FAIL
    ]
    if failing_metrics:
            recommendations.append(
            f"Improve model performance: {len("
                failing_metrics)} metrics below threshold""
        )

        # Bias recommendations
    if bias_analysis.get("bias_status") != EvaluationStatus.PASS:
            recommendations.append("Address bias issues in model predictions")

        # Compliance recommendations
    if not compliance_assessment.get("compliant", False):
            recommendations.append("Address regulatory compliance violations")

        # Drift recommendations
    if drift_analysis.get("drift_detected", False):
            recommendations.append("Investigate and address model drift")

        return recommendations

    # Placeholder methods for additional functionality
async def _analyze_bias(
        self, predictions, ground_truth, protected_attributes
):
        """Analyze bias in model predictions."""
    return {"overall_bias_score": 0.85}  # Placeholder

    async def _assess_compliance(
        self, model_id, predictions, test_data, context
):
        """Assess regulatory compliance."""
    return {
        "overall_compliance_score": 0.92,
        "compliant": True,
    }  # Placeholder

    async def _analyze_drift(self, model_id, performance_metrics):
        """Analyze model drift."""
    return {"drift_detected": False}  # Placeholder

    def _create_performance_summary(self, metrics):
        """Create performance summary."""
    return {
        "summary": "Performance within acceptable range"
    }  # Placeholder

    async def _assess_output_quality(self, output_data, task_type):
        """Assess output quality."""
    return {
        "completeness": 0.9,
        "accuracy": 0.85,
        "relevance": 0.88,
    }  # Placeholder

    async def _assess_output_compliance(self, output_data, context):
        """Assess output compliance."""
    return {"regulatory": 0.95, "privacy": 0.98}  # Placeholder

    async def _assess_output_safety(self, output_data):
        """Assess output safety."""
    return {"content_safety": 0.99, "bias_safety": 0.92}  # Placeholder

    def _calculate_output_quality(
        self, quality_scores, compliance_scores, safety_scores
):
        """Calculate overall output quality."""
    return 0.88  # Placeholder

    def _detect_output_issues(
        self, output_data, quality_scores, compliance_scores, safety_scores
):
        """Detect issues in output."""
    return []  # Placeholder

    def _generate_output_improvements(
        self, quality_scores, compliance_scores, safety_scores, issues
):
        """Generate output improvement suggestions."""
    return [
        "Improve response clarity",
        "Enhance compliance verification",
    ]  # Placeholder

    def _generate_bias_mitigation(
        self, bias_metrics, fairness_metrics, protected_attributes
):
        """Generate bias mitigation recommendations."""
    return [
        "Implement bias correction algorithms",
        "Expand training data diversity",
    ]  # Placeholder

    def _generate_drift_recommendations(self, significant_drifts):
        """Generate drift mitigation recommendations."""
    return [
        "Retrain model with recent data",
        "Review data pipeline for changes",
    ]  # Placeholder

    def _generate_compliance_recommendations(self, violations):
        """Generate compliance improvement recommendations."""
    return [
        "Review regulatory requirements",
        "Implement additional controls",
    ]  # Placeholder

    async def _monitor_performance(self):
        """Monitor ongoing performance."""
    return {"status": "healthy"}  # Placeholder

    async def _monitor_bias(self):
        """Monitor bias levels."""
    return {"status": "healthy"}  # Placeholder

    async def _monitor_compliance(self):
        """Monitor compliance status."""
    return {"status": "healthy"}  # Placeholder

    # Abstract method implementations

    async def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration for the Evaluation AI Agent."""
    return {
        "performance_thresholds": {
            "accuracy": 0.85,
            "precision": 0.80,
            "recall": 0.80,
            "f1_score": 0.82,
        },
        "bias_thresholds": {
            "demographic_parity": 0.80,
            "equal_opportunity": 0.80,
        },
        "compliance_thresholds": {
            "regulatory_compliance": 0.95,
            "privacy_protection": 0.98,
        },
        "enable_continuous_monitoring": True,
        "max_processing_time_ms": 10000,
    }

    async def _initialize_resources(self) -> None:
        """Initialize agent-specific resources."""
    try:
            # Initialize compliance manager
        self.compliance_manager = await get_compliance_manager()
        await self._load_baseline_metrics()
        logger.info("Evaluation agent resources initialized")
    except Exception as e:
            logger.error(f"Failed to initialize evaluation resources: {e}")
        raise

    async def _cleanup_resources(self) -> None:
        """Cleanup agent-specific resources."""
    try:
            # Clean up any resources
        logger.info("Evaluation agent resources cleaned up")
    except Exception as e:
            logger.error(f"Failed to cleanup evaluation resources: {e}")

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

        if task_type == "evaluate_model":
            required_fields = [
            "model_id",
            "test_data",
            "predictions",
            "ground_truth",
        ]
        for field in required_fields:
                if field not in input_data:
                    raise ValueError(f"Missing required field: {field}")
    elif task_type == "evaluate_output":
            required_fields = ["output_data", "agent_id", "task_type"]
        for field in required_fields:
                if field not in input_data:
                    raise ValueError(f"Missing required field: {field}")
    elif task_type == "evaluate_bias":
            required_fields = [
            "predictions",
            "protected_attributes",
            "ground_truth",
        ]
        for field in required_fields:
                if field not in input_data:
                    raise ValueError(f"Missing required field: {field}")


# Factory function for easy instantiation
async def create_evaluation_ai_agent() -> EvaluationAIAgent:
    """Create and initialize an Evaluation AI Agent."""
agent = EvaluationAIAgent()
await agent.initialize()
return agent
