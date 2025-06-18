"""
Monitoring service for MatchedCover Insurance Platform.

This module provides monitoring and metrics collection capabilities
for tracking system performance and health."""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class MetricsService:"""
Service for collecting and managing system metrics."""

    def __init__(self):
        self.metrics_cache: Dict[str, Any] = {}
    self.health_status: Dict[str, bool] = {}
    self.is_running = False
    self.collection_interval = 60  # seconds

    async def start_collection(self) -> None:
        """Start metrics collection."""
    self.is_running = True
    logger.info("Starting metrics collection service")

        # Start background task for metrics collection
    asyncio.create_task(self._collect_metrics_periodically())

    async def stop_collection(self) -> None:
        """Stop metrics collection."""
    self.is_running = False
    logger.info("Stopping metrics collection service")

    async def _collect_metrics_periodically(self) -> None:
        """Collect metrics periodically."""
    while self.is_running:
            try:
                await self._collect_system_metrics()
            await asyncio.sleep(self.collection_interval)
        except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
            await asyncio.sleep(self.collection_interval)

    async def _collect_system_metrics(self) -> None:
        """Collect system-wide metrics."""
    timestamp = datetime.utcnow().isoformat()

        # Collect various metrics
    metrics = {
        "timestamp": timestamp,
        "system": await self._get_system_metrics(),
        "agents": await self._get_agent_metrics(),
        "api": await self._get_api_metrics(),
        "database": await self._get_database_metrics(),
        "redis": await self._get_redis_metrics(),
    }

        # Cache metrics
    self.metrics_cache["latest"] = metrics

        # Store historical metrics (simplified)
    history_key = f"metrics_{timestamp[:13]}"  # Hour-based key
    self.metrics_cache[history_key] = metrics

        logger.debug(f"Collected metrics at {timestamp}")

    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system-level metrics."""
    # In a real implementation, this would collect actual system metrics
    return {
        "cpu_usage": 45.2,
        "memory_usage": 67.8,
        "disk_usage": 34.1,
        "network_io": {"bytes_sent": 1024000, "bytes_received": 2048000},
        "uptime": 86400,  # seconds
        "load_average": [1.2, 1.5, 1.8],
    }

    async def _get_agent_metrics(self) -> Dict[str, Any]:
        """Get AI agent metrics."""
    return {
        "total_agents": 10,
        "active_agents": 9,
        "total_tasks_processed": 15247,
        "tasks_in_queue": 23,
        "average_response_time": 2.3,
        "success_rate": 96.5,
        "agent_status": {
            "intake": "healthy",
            "risk_assessor": "healthy",
            "pricing": "healthy",
            "policy": "healthy",
            "claim_intake": "healthy",
            "claims_evaluator": "healthy",
            "fraud_detection": "healthy",
            "compliance": "healthy",
            "advisor": "healthy",
            "audit": "degraded",  # Example of degraded service
        },
    }

    async def _get_api_metrics(self) -> Dict[str, Any]:
        """Get API metrics."""
    return {
        "total_requests": 45231,
        "requests_per_minute": 127,
        "average_response_time": 145,  # milliseconds
        "error_rate": 2.1,  # percentage
        "status_codes": {
            "200": 42156,
            "400": 1247,
            "401": 523,
            "403": 145,
            "404": 267,
            "500": 893,
        },
        "endpoints": {
            "/api/v1/customers": {"requests": 12453, "avg_time": 120},
            "/api/v1/policies": {"requests": 8967, "avg_time": 156},
            "/api/v1/claims": {"requests": 6734, "avg_time": 234},
            "/api/v1/agents": {"requests": 4523, "avg_time": 89},
        },
    }

    async def _get_database_metrics(self) -> Dict[str, Any]:
        """Get database metrics."""
    return {
        "connection_pool": {
            "active_connections": 15,
            "idle_connections": 5,
            "max_connections": 50,
        },
        "query_performance": {
            "average_query_time": 45,  # milliseconds
            "slow_queries": 12,
            "total_queries": 23456,
        },
        "storage": {
            "total_size": "2.3GB",
            "available_space": "47.7GB",
            "usage_percentage": 4.6,
        },
    }

    async def _get_redis_metrics(self) -> Dict[str, Any]:
        """Get Redis metrics."""
    return {
        "memory_usage": "256MB",
        "connected_clients": 8,
        "operations_per_second": 1247,
        "cache_hit_rate": 94.2,
        "key_count": 15673,
        "expired_keys": 234,
    }

    async def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
    return self.metrics_cache.get("latest", {})

    async def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status."""
    current_metrics = await self.get_current_metrics()

        # Determine overall health based on metrics
    health_checks = {
        "system": self._check_system_health(
            current_metrics.get("system", {})
        ),
        "agents": self._check_agents_health(
            current_metrics.get("agents", {})
        ),
        "api": self._check_api_health(current_metrics.get("api", {})),
        "database": self._check_database_health(
            current_metrics.get("database", {})
        ),
        "redis": self._check_redis_health(
            current_metrics.get("redis", {})
        ),
    }

        # Calculate overall health
    healthy_services = sum(
        1 for status in health_checks.values() if status["healthy"]
    )
    total_services = len(health_checks)
    overall_health = healthy_services == total_services

        return {
        "overall_healthy": overall_health,
        "health_score": (healthy_services / total_services) * 100,
        "services": health_checks,
        "timestamp": datetime.utcnow().isoformat(),
    }

    def _check_system_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Check system health."""
    cpu_ok = metrics.get("cpu_usage", 0) < 80
    memory_ok = metrics.get("memory_usage", 0) < 85
    disk_ok = metrics.get("disk_usage", 0) < 90

        healthy = cpu_ok and memory_ok and disk_ok

        return {
        "healthy": healthy,
        "details": {
            "cpu_ok": cpu_ok,
            "memory_ok": memory_ok,
            "disk_ok": disk_ok,
        },
    }

    def _check_agents_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Check agents health."""
    success_rate_ok = metrics.get("success_rate", 0) > 90
    response_time_ok = metrics.get("average_response_time", 0) < 5
    queue_ok = metrics.get("tasks_in_queue", 0) < 100

        healthy = success_rate_ok and response_time_ok and queue_ok

        return {
        "healthy": healthy,
        "details": {
            "success_rate_ok": success_rate_ok,
            "response_time_ok": response_time_ok,
            "queue_ok": queue_ok,
        },
    }

    def _check_api_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Check API health."""
    error_rate_ok = metrics.get("error_rate", 0) < 5
    response_time_ok = metrics.get("average_response_time", 0) < 500

        healthy = error_rate_ok and response_time_ok

        return {
        "healthy": healthy,
        "details": {
            "error_rate_ok": error_rate_ok,
            "response_time_ok": response_time_ok,
        },
    }

    def _check_database_health(
        self, metrics: Dict[str, Any]
) -> Dict[str, Any]:
        """Check database health."""
    pool_metrics = metrics.get("connection_pool", {})
    query_metrics = metrics.get("query_performance", {})

        connections_ok = pool_metrics.get("active_connections", 0) < 40
    query_time_ok = query_metrics.get("average_query_time", 0) < 100

        healthy = connections_ok and query_time_ok

        return {
        "healthy": healthy,
        "details": {
            "connections_ok": connections_ok,
            "query_time_ok": query_time_ok,
        },
    }

    def _check_redis_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Check Redis health."""
    hit_rate_ok = metrics.get("cache_hit_rate", 0) > 80
    clients_ok = metrics.get("connected_clients", 0) < 50

        healthy = hit_rate_ok and clients_ok

        return {
        "healthy": healthy,
        "details": {"hit_rate_ok": hit_rate_ok, "clients_ok": clients_ok},
    }

    async def get_metrics_history(
        self, hours: int = 24
) -> List[Dict[str, Any]]:
        """Get metrics history for the specified number of hours."""
    history = []
    current_time = datetime.utcnow()

        for i in range(hours):
            hour_time = current_time - timedelta(hours=i)
        hour_key = f"metrics_{hour_time.isoformat()[:13]}"

            if hour_key in self.metrics_cache:
                history.append(self.metrics_cache[hour_key])

        return list(reversed(history))  # Return in chronological order

    async def log_custom_metric(
        self,
    metric_name: str,
    value: Any,
    tags: Optional[Dict[str, str]] = None,
) -> None:
        """Log a custom metric."""
    metric_entry = {
        "name": metric_name,
        "value": value,
        "tags": tags or {},
        "timestamp": datetime.utcnow().isoformat(),
    }

        # Store custom metric
    custom_metrics = self.metrics_cache.setdefault("custom", [])
    custom_metrics.append(metric_entry)

        # Keep only last 1000 custom metrics
    if len(custom_metrics) > 1000:
            custom_metrics[:] = custom_metrics[-1000:]

        logger.info(f"Custom metric logged: {metric_name} = {value}")

    async def generate_alert(
        self, alert_type: str, message: str, severity: str = "warning"
) -> None:
        """Generate an alert."""
    alert = {
        "type": alert_type,
        "message": message,
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat(),
        "acknowledged": False,
    }

        # Store alert
    alerts = self.metrics_cache.setdefault("alerts", [])
    alerts.append(alert)

        # Keep only last 100 alerts
    if len(alerts) > 100:
            alerts[:] = alerts[-100:]

        logger.warning(f"Alert generated: {alert_type} - {message}")

    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get list of active (unacknowledged) alerts."""
    all_alerts = self.metrics_cache.get("alerts", [])
    return [
        alert
        for alert in all_alerts
            if not alert.get("acknowledged", False)
        ]
