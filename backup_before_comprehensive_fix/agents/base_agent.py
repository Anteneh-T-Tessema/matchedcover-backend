""""
Base Agent class for MatchedCover.

This module defines the abstract base class that all AI agents inherit from,
providing common functionality and interface definitions.
""""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """"
Abstract base class for all AI agents in the MatchedCover platform.

    This class provides common functionality including:
    - Task processing interface
- Configuration management
- Status tracking
- Performance metrics
- Error handling
""""

    def __init__(self, agent_type: str, name: str):
        self.agent_type = agent_type
    self.name = name
    self.agent_id = str(uuid.uuid4())
    self.config: Dict[str, Any] = {}
    self.is_initialized = False
    self.is_active = False
    self.task_count = 0
    self.success_count = 0
    self.error_count = 0
    self.start_time = None

        # Performance tracking
    self.performance_metrics = {
        "total_tasks": 0,
        "successful_tasks": 0,
        "failed_tasks": 0,
        "average_response_time": 0.0,
        "total_response_time": 0.0,
        "last_active": None,
    }

    async def initialize(self) -> None:
        """Initialize the agent with default configuration."""
    logger.info(f"Initializing {self.name} agent...")

        try:
            # Load default configuration
        self.config = await self._load_default_config()

            # Initialize agent-specific resources
        await self._initialize_resources()

            self.is_initialized = True
        self.is_active = True
        self.start_time = datetime.utcnow()

            logger.info(f"{self.name} agent initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize {self.name} agent: {e}")
        raise

    async def shutdown(self) -> None:
        """Shutdown the agent and cleanup resources."""
    logger.info(f"Shutting down {self.name} agent...")

        try:
            self.is_active = False
        await self._cleanup_resources()
        logger.info(f"{self.name} agent shutdown successfully")

        except Exception as e:
            logger.error(f"Error shutting down {self.name} agent: {e}")

    async def process_task(
        self,
    task_type: str,
    input_data: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
        """"
    Process a task and return the result.

        Args:
            task_type: Type of task to process
        input_data: Input data for the task
        context: Additional context information

        Returns:
            Dict containing the task result
    """"
    if not self.is_active:
            raise RuntimeError(f"Agent {self.name} is not active")

        start_time = datetime.utcnow()
    task_id = context.get("task_id") if context else str(uuid.uuid4())

        logger.info(
        f"{self.name} processing task {task_id} of type {task_type}"
    )

        try:
            # Validate input
        await self._validate_input(task_type, input_data)

            # Process the task
        result = await self._process_task_impl(
            task_type, input_data, context
        )

            # Update metrics
        end_time = datetime.utcnow()
        response_time = (end_time - start_time).total_seconds()
        await self._update_performance_metrics(True, response_time)

            logger.info(f"{self.name} completed task {task_id} successfully")
        return result

        except Exception as e:
            # Update error metrics
        end_time = datetime.utcnow()
        response_time = (end_time - start_time).total_seconds()
        await self._update_performance_metrics(False, response_time)

            logger.error(f"{self.name} failed to process task {task_id}: {e}")
        raise

    async def get_status(self) -> Dict[str, Any]:
        """Get current agent status and metrics."""
    return {
        "agent_id": self.agent_id,
        "name": self.name,
        "type": self.agent_type,
        "is_active": self.is_active,
        "is_initialized": self.is_initialized,
        "start_time": (
            self.start_time.isoformat() if self.start_time else None
        ),
        "performance_metrics": self.performance_metrics.copy(),
        "config": self.config.copy(),
    }

    async def update_config(self, new_config: Dict[str, Any]) -> bool:
        """Update agent configuration."""
    try:
            # Validate configuration
        await self._validate_config(new_config)

            # Update configuration
        self.config.update(new_config)

            # Apply configuration changes
        await self._apply_config_changes()

            logger.info(f"{self.name} configuration updated successfully")
        return True

        except Exception as e:
            logger.error(f"Failed to update {self.name} configuration: {e}")
        return False

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check and return status."""
    try:
            # Check agent-specific health
        health_status = await self._check_health()

            return {
            "healthy": health_status["healthy"],
            "status": health_status.get("status", "unknown"),
            "details": health_status.get("details", {}),
            "checked_at": datetime.utcnow().isoformat(),
        }

        except Exception as e:
            logger.error(f"Health check failed for {self.name}: {e}")
        return {
            "healthy": False,
            "status": "error",
            "error": str(e),
            "checked_at": datetime.utcnow().isoformat(),
        }

    @abstractmethod
async def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration for the agent."""
    pass

    @abstractmethod
async def _initialize_resources(self) -> None:
        """Initialize agent-specific resources."""
    pass

    @abstractmethod
async def _cleanup_resources(self) -> None:
        """Cleanup agent-specific resources."""
    pass

    @abstractmethod
async def _process_task_impl(
        self,
    task_type: str,
    input_data: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
        """Implement the actual task processing logic."""
    pass

    @abstractmethod
async def _validate_input(
        self, task_type: str, input_data: Dict[str, Any]
) -> None:
        """Validate input data for the task."""
    pass

    async def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration (default implementation)."""
    # Override in subclasses for specific validation
    pass

    async def _apply_config_changes(self) -> None:
        """Apply configuration changes (default implementation)."""
    # Override in subclasses for specific config application
    pass

    async def _check_health(self) -> Dict[str, Any]:
        """Check agent health (default implementation)."""
    return {
        "healthy": self.is_active and self.is_initialized,
        "status": "active" if self.is_active else "inactive",
    }

    async def _update_performance_metrics(
        self, success: bool, response_time: float
) -> None:
        """Update performance metrics."""
    self.performance_metrics["total_tasks"] += 1
    self.performance_metrics["total_response_time"] += response_time
    self.performance_metrics["last_active"] = datetime.utcnow().isoformat()

        if success:
            self.performance_metrics["successful_tasks"] += 1
    else:
            self.performance_metrics["failed_tasks"] += 1

        # Calculate average response time
    total_tasks = self.performance_metrics["total_tasks"]
    total_time = self.performance_metrics["total_response_time"]
    self.performance_metrics["average_response_time"] = (
        total_time / total_tasks
    )

    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
    # Override in subclasses to return specific capabilities
    return []

    async def log_interaction(
        self, interaction_type: str, details: Dict[str, Any]
) -> None:
        """Log agent interaction for audit purposes."""
    log_entry = {
        "agent_id": self.agent_id,
        "agent_name": self.name,
        "interaction_type": interaction_type,
        "details": details,
        "timestamp": datetime.utcnow().isoformat(),
    }

        # In a real implementation, this would be sent to a logging service
    logger.info(f"Agent interaction logged: {log_entry}")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}("
        name={self.name},
        active={self.is_active}
    )>""
