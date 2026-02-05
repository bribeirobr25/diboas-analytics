"""
Alerting utilities for monitoring and notifications.

Principle 12 (Monitoring & Observability):
-----------------------------------------
Provides zero-budget alerting via Slack webhooks.
Falls back gracefully when no webhook is configured.

Usage:
    from src.utils.alerting import send_alert, AlertSeverity

    # Send alert
    send_alert("Database connection failed", AlertSeverity.ERROR)

    # Or use string severity
    send_alert("Processing complete", severity="info")

Environment Variables:
    SLACK_WEBHOOK_URL: Slack incoming webhook URL
    ALERT_ENABLED: Set to "false" to disable all alerts
"""

import os
import json
import logging
from enum import Enum
from typing import Any, Dict, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


# Emoji map for Slack
SEVERITY_EMOJI = {
    AlertSeverity.INFO: "ℹ️",
    AlertSeverity.WARNING: "⚠️",
    AlertSeverity.ERROR: "❌",
    AlertSeverity.CRITICAL: "🚨",
    "info": "ℹ️",
    "warning": "⚠️",
    "error": "❌",
    "critical": "🚨",
}


def _get_webhook_url() -> Optional[str]:
    """Get Slack webhook URL from environment."""
    return os.getenv("SLACK_WEBHOOK_URL")


def _is_alerting_enabled() -> bool:
    """Check if alerting is enabled."""
    return os.getenv("ALERT_ENABLED", "true").lower() != "false"


def send_alert(
    message: str,
    severity: Union[str, AlertSeverity] = AlertSeverity.INFO,
    context: Dict[str, Any] = None,
    source: str = "diBoaS Analytics",
) -> bool:
    """
    Send an alert notification.

    Currently supports Slack webhooks. Falls back to logging
    when no webhook is configured.

    Args:
        message: Alert message
        severity: Alert severity level
        context: Additional context data
        source: Alert source identifier

    Returns:
        True if alert was sent successfully
    """
    if not _is_alerting_enabled():
        logger.debug(f"Alerting disabled, skipping: {message}")
        return False

    # Normalize severity
    if isinstance(severity, str):
        severity_str = severity.lower()
    else:
        severity_str = severity.value

    emoji = SEVERITY_EMOJI.get(severity, SEVERITY_EMOJI.get(severity_str, "❓"))

    # Build alert message
    timestamp = datetime.utcnow().isoformat()
    formatted_message = f"{emoji} [{severity_str.upper()}] {message}"

    if context:
        context_lines = [f"  • {k}: {v}" for k, v in context.items()]
        formatted_message += "\n" + "\n".join(context_lines)

    # Try Slack webhook
    webhook_url = _get_webhook_url()
    if webhook_url:
        return _send_slack_alert(webhook_url, formatted_message, severity_str, source)

    # Fallback to logging
    log_level = _get_log_level(severity_str)
    logger.log(log_level, f"[ALERT] {formatted_message}")
    return True


def _send_slack_alert(
    webhook_url: str,
    message: str,
    severity: str,
    source: str,
) -> bool:
    """
    Send alert to Slack via webhook.

    Args:
        webhook_url: Slack webhook URL
        message: Formatted message
        severity: Severity string
        source: Alert source

    Returns:
        True if successful
    """
    try:
        import urllib.request

        # Build Slack payload
        color_map = {
            "info": "#36a64f",  # Green
            "warning": "#ffcc00",  # Yellow
            "error": "#ff0000",  # Red
            "critical": "#8b0000",  # Dark red
        }

        payload = {
            "attachments": [
                {
                    "color": color_map.get(severity, "#808080"),
                    "title": source,
                    "text": message,
                    "ts": datetime.utcnow().timestamp(),
                }
            ]
        }

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            if response.status == 200:
                logger.debug(f"Slack alert sent: {severity}")
                return True
            else:
                logger.warning(f"Slack webhook returned status {response.status}")
                return False

    except Exception as e:
        logger.error(f"Failed to send Slack alert: {e}")
        return False


def _get_log_level(severity: str) -> int:
    """Map severity to logging level."""
    level_map = {
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }
    return level_map.get(severity, logging.INFO)


# Convenience functions for common alert types


def alert_crisis_detected(
    crisis_level: int,
    trigger_id: str,
    message: str,
    affected_strategies: list = None,
) -> bool:
    """
    Send crisis detection alert.

    Args:
        crisis_level: Crisis level (1-5)
        trigger_id: Trigger that fired
        message: Crisis description
        affected_strategies: List of affected strategy IDs

    Returns:
        True if alert sent
    """
    severity = AlertSeverity.CRITICAL if crisis_level >= 4 else AlertSeverity.ERROR
    context = {
        "crisis_level": crisis_level,
        "trigger_id": trigger_id,
        "affected_strategies": affected_strategies or [],
    }
    return send_alert(message, severity=severity, context=context)


def alert_circuit_opened(
    circuit_name: str,
    failure_count: int,
    last_error: str = None,
) -> bool:
    """
    Send circuit breaker opened alert.

    Args:
        circuit_name: Name of circuit breaker
        failure_count: Number of failures
        last_error: Last error message

    Returns:
        True if alert sent
    """
    context = {
        "circuit_name": circuit_name,
        "failure_count": failure_count,
    }
    if last_error:
        context["last_error"] = last_error[:100]  # Truncate

    return send_alert(
        f"Circuit breaker '{circuit_name}' opened after {failure_count} failures",
        severity=AlertSeverity.ERROR,
        context=context,
    )


def alert_validation_failure(
    gate: str,
    error_count: int,
    issues: list = None,
) -> bool:
    """
    Send validation failure alert.

    Args:
        gate: Validation gate name
        error_count: Number of errors
        issues: List of issue descriptions

    Returns:
        True if alert sent
    """
    context = {
        "gate": gate,
        "error_count": error_count,
    }
    if issues:
        context["issues"] = issues[:5]  # Limit to 5

    return send_alert(
        f"Validation {gate} failed with {error_count} errors",
        severity=AlertSeverity.WARNING,
        context=context,
    )


def alert_execution_failed(
    command: str,
    error: str,
    correlation_id: str = None,
) -> bool:
    """
    Send execution failure alert.

    Args:
        command: CLI command that failed
        error: Error message
        correlation_id: Correlation ID for tracing

    Returns:
        True if alert sent
    """
    context = {
        "command": command,
        "error": error[:200],  # Truncate
    }
    if correlation_id:
        context["correlation_id"] = correlation_id

    return send_alert(
        f"Command '{command}' failed",
        severity=AlertSeverity.ERROR,
        context=context,
    )
