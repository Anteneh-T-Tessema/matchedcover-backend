"""
Base Agent class for MatchedCover.

This module defines the abstract base class that all AI agents inherit from,
providing common functionality and interface definitions."""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents in the MatchedCover platform.

    This class provides common functionality including:
    - Task processing interface
    - Configuration management
    - Status tracking
    - Performance metrics
    - Error handling
    """

    def __init__(self, agent_type: str = "", name: str = ""):
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
            
            # Initialize resources
            await self._initialize_resources()
            
            self.is_initialized = True
            self.start_time = datetime.now()
            logger.info(f"{self.name} agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize {self.name} agent: {str(e)}")
            raise
            
    async def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration for the agent."""
        return {
            "log_level": "INFO",
            "max_concurrent_tasks": 10,
            "timeout_seconds": 30,
        }
        
    async def _initialize_resources(self) -> None:
        """Initialize agent-specific resources."""
        # Base implementation does nothing
        pass
        
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task with the agent.
        
        Args:
            task_data: The task input data
            
        Returns:
            Task result data
        """
        if not self.is_initialized:
            await self.initialize()
            
        if not self.is_active:
            self.activate()
            
        task_id = task_data.get("task_id", str(uuid.uuid4()))
        logger.info(f"{self.name} processing task {task_id}")
        
        start_time = datetime.now()
        
        try:
            # Process the task
            self.task_count += 1
            self.performance_metrics["total_tasks"] += 1
            
            result = await self._process_task_impl(task_data)
            
            # Track success
            self.success_count += 1
            self.performance_metrics["successful_tasks"] += 1
            
            return result
            
        except Exception as e:
            # Track failure
            self.error_count += 1
            self.performance_metrics["failed_tasks"] += 1
            logger.error(f"Error processing task {task_id}: {str(e)}")
            raise
            
        finally:
            # Update performance metrics
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            self.performance_metrics["total_response_time"] += response_time
            self.performance_metrics["average_response_time"] = (
                self.performance_metrics["total_response_time"] / 
                self.performance_metrics["total_tasks"]
            )
            self.performance_metrics["last_active"] = end_time
            
    async def _process_task_impl(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implementation of task processing logic.
        
        Args:
            task_data: The task input data
            
        Returns:
            Task result data
        """
        raise NotImplementedError("Subclasses must implement this method")
        
    def activate(self) -> None:
        """Activate the agent."""
        self.is_active = True
        logger.info(f"{self.name} agent activated")
        
    def deactivate(self) -> None:
        """Deactivate the agent."""
        self.is_active = False
        logger.info(f"{self.name} agent deactivated")
        
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.agent_type,
            "is_active": self.is_active,
            "is_initialized": self.is_initialized,
            "task_count": self.task_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "start_time": self.start_time,
            "uptime_seconds": (
                (datetime.now() - self.start_time).total_seconds()
                if self.start_time else 0
            ),
            "performance": self.performance_metrics,
        }
        
    def reset_metrics(self) -> None:
        """Reset performance metrics."""
        self.performance_metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "average_response_time": 0.0,
            "total_response_time": 0.0,
            "last_active": None,
        }
        logger.info(f"{self.name} agent metrics reset")
        
    async def update_config(self, config_updates: Dict[str, Any]) -> None:
        """
        Update agent configuration.
        
        Args:
            config_updates: Configuration parameters to update
        """
        self.config.update(config_updates)
        logger.info(f"{self.name} agent configuration updated")
        
    async def get_capabilities(self) -> List[str]:
        """
        Get the list of agent capabilities.
        
        Returns:
            List of capability descriptions
        """
        return ["Base agent functionality"]
