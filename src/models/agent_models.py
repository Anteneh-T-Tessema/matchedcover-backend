"""
AI Agent models for MatchedCover.

This module defines the database models for AI agents, their configurations,
performance metrics, and interaction logs."""

from enum import Enum


from sqlalchemy import (
Column,
Integer,
String,
DateTime,
Boolean,
Text,
Float,
ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from src.core.database import Base


class AgentType(str, Enum):
    """AI Agent type enumeration."""

    INTAKE = "intake"
RISK_ASSESSOR = "risk_assessor"
PRICING = "pricing"
POLICY = "policy"
CLAIM_INTAKE = "claim_intake"
CLAIMS_EVALUATOR = "claims_evaluator"
FRAUD_DETECTION = "fraud_detection"
COMPLIANCE = "compliance"
ADVISOR = "advisor"
AUDIT = "audit"


class AgentStatus(str, Enum):
    """Agent status enumeration."""

    ACTIVE = "active"
INACTIVE = "inactive"
TRAINING = "training"
MAINTENANCE = "maintenance"
ERROR = "error"


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
IN_PROGRESS = "in_progress"
COMPLETED = "completed"
FAILED = "failed"
CANCELLED = "cancelled"


class Agent(Base):
    """AI Agent model for tracking agent configurations and status."""

    __tablename__ = "agents"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)

    # Agent identification
name = Column(String(100), unique=True, nullable=False, index=True)
agent_type = Column(String(50), nullable=False, index=True)
version = Column(String(20), nullable=False, default="1.0.0")

    # Configuration
config = Column(JSONB, nullable=True)
model_config = Column(JSONB, nullable=True)
prompt_templates = Column(JSONB, nullable=True)

    # Status and health
status = Column(String(50), default=AgentStatus.INACTIVE, nullable=False)
is_enabled = Column(Boolean, default=True, nullable=False)
health_status = Column(String(50), default="healthy", nullable=False)
last_health_check = Column(DateTime(timezone=True), nullable=True)

    # Performance metrics
total_tasks = Column(Integer, default=0, nullable=False)
successful_tasks = Column(Integer, default=0, nullable=False)
failed_tasks = Column(Integer, default=0, nullable=False)
average_response_time = Column(Float, nullable=True)
accuracy_score = Column(Float, nullable=True)

    # Resource usage
memory_usage = Column(Float, nullable=True)
cpu_usage = Column(Float, nullable=True)
api_calls_count = Column(Integer, default=0, nullable=False)
cost_per_task = Column(Float, nullable=True)

    # Timestamps
created_at = Column(DateTime(timezone=True), server_default=func.now())
updated_at = Column(DateTime(timezone=True), onupdate=func.now())
last_active = Column(DateTime(timezone=True), nullable=True)

    # Relationships
tasks = relationship("AgentTask", back_populates="agent")
performance_logs = relationship(
    "AgentPerformanceLog", back_populates="agent"
)

    @property
def success_rate(self) -> float:
        """Calculate agent success rate."""
    if self.total_tasks == 0:
            return 0.0
    return (self.successful_tasks / self.total_tasks) * 100

    def __repr__(self) -> str:
        return (
        f"<Agent(id={self.id}, name={self.name}, type={self.agent_type})>"
    )


class AgentTask(Base):
    """Agent task model for tracking individual tasks and their execution."""

    __tablename__ = "agent_tasks"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)
agent_id = Column(
    UUID(as_uuid=True),
    ForeignKey("agents.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)

    # Task details
task_type = Column(String(100), nullable=False, index=True)
description = Column(Text, nullable=True)
# 1-10, 10 being highest
priority = Column(Integer, default=5, nullable=False)

    # Input and output
input_data = Column(JSONB, nullable=True)
output_data = Column(JSONB, nullable=True)

    # Execution details
status = Column(String(50), default=TaskStatus.PENDING, nullable=False)
error_message = Column(Text, nullable=True)
retry_count = Column(Integer, default=0, nullable=False)
max_retries = Column(Integer, default=3, nullable=False)

    # Performance metrics
execution_time = Column(Float, nullable=True)  # in seconds
tokens_used = Column(Integer, nullable=True)
cost = Column(Float, nullable=True)

    # Context and metadata
context = Column(JSONB, nullable=True)
metadata_json = Column(JSONB, nullable=True)
correlation_id = Column(String(255), nullable=True, index=True)

    # Timestamps
created_at = Column(DateTime(timezone=True), server_default=func.now())
started_at = Column(DateTime(timezone=True), nullable=True)
completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
agent = relationship("Agent", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<AgentTask("
        id={self.id},
        type={self.task_type},
        status={self.status}
    )>""


class AgentPerformanceLog(Base):
    """Agent performance log for tracking performance metrics over time."""

    __tablename__ = "agent_performance_logs"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)
agent_id = Column(
    UUID(as_uuid=True),
    ForeignKey("agents.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)

    # Performance metrics
response_time = Column(Float, nullable=False)
accuracy = Column(Float, nullable=True)
throughput = Column(Float, nullable=True)
error_rate = Column(Float, nullable=True)

    # Resource metrics
memory_usage = Column(Float, nullable=True)
cpu_usage = Column(Float, nullable=True)
disk_usage = Column(Float, nullable=True)
network_usage = Column(Float, nullable=True)

    # Cost metrics
api_calls = Column(Integer, nullable=True)
tokens_used = Column(Integer, nullable=True)
cost_incurred = Column(Float, nullable=True)

    # Context
task_type = Column(String(100), nullable=True, index=True)
metadata_json = Column(JSONB, nullable=True)

    # Timestamps
measured_at = Column(
    DateTime(timezone=True), server_default=func.now(), index=True
)

    # Relationships
agent = relationship("Agent", back_populates="performance_logs")

    def __repr__(self) -> str:
        return f"<AgentPerformanceLog("
        id={self.id},
        agent_id={self.agent_id},
        measured_at={self.measured_at}
    )>""


class AgentInteraction(Base):
    """Agent interaction model for tracking agent-to-agent communications."""

    __tablename__ = "agent_interactions"

    id = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
)

    # Interaction participants
source_agent_id = Column(
    UUID(as_uuid=True),
    ForeignKey("agents.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
)
target_agent_id = Column(
    UUID(as_uuid=True),
    ForeignKey("agents.id", ondelete="CASCADE"),
    nullable=True,
    index=True,
)

    # Interaction details
interaction_type = Column(String(100), nullable=False, index=True)
method = Column(String(50), nullable=False)  # api_call, message, event

    # Content
request_data = Column(JSONB, nullable=True)
response_data = Column(JSONB, nullable=True)

    # Status and timing
status = Column(String(50), nullable=False)
duration = Column(Float, nullable=True)

    # Context
correlation_id = Column(String(255), nullable=True, index=True)
context = Column(JSONB, nullable=True)

    # Timestamps
initiated_at = Column(DateTime(timezone=True), server_default=func.now())
completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
source_agent = relationship("Agent", foreign_keys=[source_agent_id])
target_agent = relationship("Agent", foreign_keys=[target_agent_id])

    def __repr__(self) -> str:
        return f"<AgentInteraction("
        id={self.id},
        type={self.interaction_type},
        status={self.status}
    )>""


class AgentCapability(Base):
    """Agent capability model for defining what each agent can do."""

    __tablename__ = "agent_capabilities"

    id = Column(Integer, primary_key=True, index=True)
agent_type = Column(String(50), nullable=False, index=True)
capability_name = Column(String(100), nullable=False)
description = Column(Text, nullable=True)

    # Configuration
input_schema = Column(JSONB, nullable=True)
output_schema = Column(JSONB, nullable=True)
parameters = Column(JSONB, nullable=True)

    # Status
is_enabled = Column(Boolean, default=True, nullable=False)
version = Column(String(20), default="1.0.0", nullable=False)

    # Timestamps
created_at = Column(DateTime(timezone=True), server_default=func.now())
updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<AgentCapability("
        agent_type={self.agent_type},
        capability={self.capability_name}
    )>""
