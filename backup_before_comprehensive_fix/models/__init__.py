""""
Models package for MatchedCover.

This module imports all model classes to make them available
for database initialization and imports.
""""

from . import user_models
from . import customer_models
from . import agent_models

# Import specific model classes for easier access
from .user_models import (
User,
UserSession,
Permission,
RolePermission,
AuditLog,
UserRole,
UserStatus,
)

from .customer_models import (
Customer,
CustomerDocument,
CustomerInteraction,
CustomerStatus,
CustomerType,
RiskCategory,
)

from .agent_models import (
Agent,
AgentTask,
AgentPerformanceLog,
AgentInteraction,
AgentCapability,
AgentType,
AgentStatus,
TaskStatus,
)

__all__ = [
# Modules
"user_models",
"customer_models",
"agent_models",
# User models
"User",
"UserSession",
"Permission",
"RolePermission",
"AuditLog",
"UserRole",
"UserStatus",
# Customer models
"Customer",
"CustomerDocument",
"CustomerInteraction",
"CustomerStatus",
"CustomerType",
"RiskCategory",
# Agent models
"Agent",
"AgentTask",
"AgentPerformanceLog",
"AgentInteraction",
"AgentCapability",
"AgentType",
"AgentStatus",
"TaskStatus",
]
