"""
AI Agent Orchestrator for MatchedCover.

This module coordinates all AI agents and manages their interactions,
task distribution, and workflow execution."""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from uuid import uuid4

from datetime import datetime


from src.agents.base_agent import BaseAgent
from src.agents.intake_agent import IntakeAgent
from src.agents.risk_assessor import RiskAssessorAgent
from src.agents.pricing_agent import PricingAgent
from src.agents.policy_agent import PolicyAgent
from src.agents.claim_intake_agent import ClaimIntakeAgent
from src.agents.claims_evaluator import ClaimsEvaluatorAgent
from src.agents.fraud_detection_agent import FraudDetectionAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.advisor_agent import AdvisorAgent
from src.agents.audit_agent import AuditAgent
from src.core.redis_client import RedisService


logger = logging.getLogger(__name__)


class AgentOrchestrator:"""
Orchestrates all AI agents and manages their lifecycle, task distribution,
and inter-agent communication."""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
    self.task_queue: asyncio.Queue = asyncio.Queue()
    self.redis_service = RedisService()
    self.is_running = False
    self.worker_tasks: List[asyncio.Task] = []

        # Agent registry
    self.agent_classes = {
        "intake": IntakeAgent,
        "risk_assessor": RiskAssessorAgent,
        "pricing": PricingAgent,
        "policy": PolicyAgent,
        "claim_intake": ClaimIntakeAgent,
        "claims_evaluator": ClaimsEvaluatorAgent,
        "fraud_detection": FraudDetectionAgent,
        "compliance": ComplianceAgent,
        "advisor": AdvisorAgent,
        "audit": AuditAgent,
    }

        # Workflow definitions
    self.workflows = {
        "new_policy_application": [
            "intake",
            "risk_assessor",
            "pricing",
            "compliance",
            "policy",
        ],
        "claim_processing": [
            "claim_intake",
            "fraud_detection",
            "claims_evaluator",
            "compliance",
            "policy",
        ],
        "customer_inquiry": ["advisor", "compliance"],
        "policy_renewal": [
            "risk_assessor",
            "pricing",
            "compliance",
            "policy",
        ],
    }

    async def initialize(self) -> None:
        """Initialize the agent orchestrator and all agents."""
    logger.info("Initializing Agent Orchestrator...")

        try:
            # Initialize all agents
        for agent_type, agent_class in self.agent_classes.items():
                logger.info(f"Initializing {agent_type} agent...")
            agent = agent_class()
            await agent.initialize()
            self.agents[agent_type] = agent
            logger.info(f"{agent_type} agent initialized successfully")

            # Start task processor workers
        self.is_running = True
        for i in range(5):  # Start 5 worker tasks
                task = asyncio.create_task(self._process_tasks())
            self.worker_tasks.append(task)

            logger.info("Agent Orchestrator initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Agent Orchestrator: {e}")
        raise

    async def shutdown(self) -> None:
        """Shutdown the agent orchestrator and all agents."""
    logger.info("Shutting down Agent Orchestrator...")

        self.is_running = False

        # Cancel worker tasks
    for task in self.worker_tasks:
            task.cancel()

        # Wait for tasks to complete
    if self.worker_tasks:
            await asyncio.gather(*self.worker_tasks, return_exceptions=True)

        # Shutdown all agents
    for agent_name, agent in self.agents.items():
            try:
                await agent.shutdown()
            logger.info(f"{agent_name} agent shutdown successfully")
        except Exception as e:
                logger.error(f"Error shutting down {agent_name} agent: {e}")

        logger.info("Agent Orchestrator shutdown complete")

    async def execute_workflow(
        self,
    workflow_name: str,
    input_data: Dict[str, Any],
    correlation_id: Optional[str] = None,
) -> Dict[str, Any]:
        """Execute a predefined workflow."""
    if correlation_id is None:
            correlation_id = str(uuid4())

        logger.info(
        f"Starting workflow: {workflow_name} (ID: {correlation_id})"
    )

        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")

        agent_sequence = self.workflows[workflow_name]
    current_data = input_data.copy()
    workflow_results = {"steps": [], "correlation_id": correlation_id}

        for agent_type in agent_sequence:
            try:
                logger.info(
                f"Executing {agent_type} in workflow {workflow_name}"
            )

                # Execute agent task
            result = await self.execute_agent_task(
                agent_type=agent_type,
                task_type=f"{workflow_name}_{agent_type}",
                input_data=current_data,
                correlation_id=correlation_id,
            )

                # Update data for next step
            if result.get("success"):
                    current_data.update(result.get("output_data", {}))
                workflow_results["steps"].append(
                    {
                        "agent": agent_type,
                        "status": "success",
                        "output": result.get("output_data", {}),
                    }
                )
            else:
                    workflow_results["steps"].append(
                    {
                        "agent": agent_type,
                        "status": "failed",
                        "error": result.get("error", "Unknown error"),
                    }
                )
                workflow_results["success"] = False
                workflow_results["error"] = f"Failed at {agent_type} step"
                break

            except Exception as e:
                logger.error(
                f"Error in workflow {workflow_name} at {agent_type}: {e}"
            )
            workflow_results["steps"].append(
                {"agent": agent_type, "status": "error", "error": str(e)}
            )
            workflow_results["success"] = False
            workflow_results["error"] = str(e)
            break
    else:
            workflow_results["success"] = True
        workflow_results["final_output"] = current_data

        logger.info(
        f"Workflow {workflow_name} completed:"
            {workflow_results['success']}""
    )
    return workflow_results

    async def execute_agent_task(
        self,
    agent_type: str,
    task_type: str,
    input_data: Dict[str, Any],
    correlation_id: Optional[str] = None,
    priority: int = 5,
) -> Dict[str, Any]:
        """Execute a single agent task."""
    if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")

        if correlation_id is None:
            correlation_id = str(uuid4())

        # Create task record
    task_id = str(uuid4())
    task_data = {
        "id": task_id,
        "agent_type": agent_type,
        "task_type": task_type,
        "input_data": input_data,
        "correlation_id": correlation_id,
        "priority": priority,
        "created_at": datetime.utcnow().isoformat(),
    }

        # Add to task queue
    await self.task_queue.put(task_data)

        # Wait for task completion (simplified for now)
    # In production, this would use a more sophisticated result retrieval
    # mechanism
    await asyncio.sleep(0.1)  # Allow task to be processed

        # Get result from Redis
    result_key = f"task_result:{task_id}"
    result = await self.redis_service.get(result_key)

        if result is None:
            return {
            "success": False,
            "error": "Task result not found",
            "task_id": task_id,
        }

        return result

    async def _process_tasks(self) -> None:
        """Process tasks from the task queue."""
    while self.is_running:
            try:
                # Get task from queue with timeout
            task_data = await asyncio.wait_for(
                self.task_queue.get(), timeout=1.0
            )

                await self._execute_task(task_data)

            except asyncio.TimeoutError:
                continue
        except Exception as e:
                logger.error(f"Error processing task: {e}")

    async def _execute_task(self, task_data: Dict[str, Any]) -> None:
        """Execute a single task."""
    task_id = task_data["id"]
    agent_type = task_data["agent_type"]

        try:
            logger.info(f"Executing task {task_id} with {agent_type} agent")

            # Get agent
        agent = self.agents[agent_type]

            # Execute task
        result = await agent.process_task(
            task_type=task_data["task_type"],
            input_data=task_data["input_data"],
            context={
                "task_id": task_id,
                "correlation_id": task_data["correlation_id"],
            },
        )

            # Store result in Redis
        result_key = f"task_result:{task_id}"
        await self.redis_service.set(
            result_key,
            {
                "success": True,
                "output_data": result,
                "task_id": task_id,
                "completed_at": datetime.utcnow().isoformat(),
            },
            expire=3600,  # 1 hour
        )

            logger.info(f"Task {task_id} completed successfully")

        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")

            # Store error result
        result_key = f"task_result:{task_id}"
        await self.redis_service.set(
            result_key,
            {
                "success": False,
                "error": str(e),
                "task_id": task_id,
                "failed_at": datetime.utcnow().isoformat(),
            },
            expire=3600,
        )

    async def get_agent_status(
        self, agent_type: Optional[str] = None
) -> Dict[str, Any]:
        """Get status of agents."""
    if agent_type:
            if agent_type not in self.agents:
                raise ValueError(f"Unknown agent type: {agent_type}")

            agent = self.agents[agent_type]
        return await agent.get_status()

        # Get status of all agents
    status = {}
    for agent_name, agent in self.agents.items():
            status[agent_name] = await agent.get_status()

        return status

    async def update_agent_config(
        self, agent_type: str, config: Dict[str, Any]
) -> bool:
        """Update agent configuration."""
    if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent = self.agents[agent_type]
    return await agent.update_config(config)

    async def get_workflow_status(self, correlation_id: str) -> Dict[str, Any]:
        """Get status of a workflow execution."""
    workflow_key = f"workflow:{correlation_id}"
    return await self.redis_service.get(workflow_key)

    def get_available_workflows(self) -> List[str]:
        """Get list of available workflows."""
    return list(self.workflows.keys())

    def get_available_agents(self) -> List[str]:
        """Get list of available agent types."""
    return list(self.agent_classes.keys())
