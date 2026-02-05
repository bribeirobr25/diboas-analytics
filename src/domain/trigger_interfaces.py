"""
Abstract interfaces for the trigger system.

This module provides abstract interfaces that validators and other domains
can depend on, without coupling directly to the concrete implementations
in src/triggers/.

DDD Principle 1: Domains don't directly call each other. Validators depend
on these abstract interfaces rather than concrete trigger implementations.

Usage:
    # In validators (like Gate 3):
    from src.domain.trigger_interfaces import (
        TriggerResultInterface,
        TriggerPriority,
        TriggerAction,
    )

    # The actual implementations in src/triggers/ implement these interfaces
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol


class TriggerPriority(Enum):
    """
    Alert priority levels (abstract interface).

    These mirror IntelligenceTriggerPriority in src/triggers/base.py
    but provide a decoupled interface for other domains.

    P0_CRITICAL: Immediate action required (crisis-level events)
    P1_HIGH: Urgent attention needed (significant market events)
    P2_MEDIUM: Important but not urgent (notable changes)
    P3_INFO: Informational only (minor observations)
    """
    P0_CRITICAL = "P0"
    P1_HIGH = "P1"
    P2_MEDIUM = "P2"
    P3_INFO = "P3"


class TriggerCategory(Enum):
    """Categories of triggers (abstract interface)."""
    PROTOCOL_HEALTH = "protocol_health"
    MARKET_CONDITION = "market_condition"
    ESTATE_WALLET = "estate_wallet"
    WHALE_ACTIVITY = "whale_activity"
    MACRO_INDICATOR = "macro_indicator"


class TriggerAction(Enum):
    """Actions to take when trigger fires (abstract interface)."""
    CRISIS_TEMPLATE = "crisis_template"
    PROTOCOL_ALERT = "protocol_alert"
    SMART_MONEY_INSIGHT = "smart_money_insight"
    PERFORMANCE_ALERT = "performance_alert"
    INTERNAL_ONLY = "internal_only"


@dataclass
class TriggerResultInterface:
    """
    Abstract interface for trigger evaluation results.

    This dataclass defines the expected structure for trigger results
    that validators and other domains can depend on.
    """
    trigger_id: str
    trigger_name: str
    fired: bool
    priority: TriggerPriority
    category: TriggerCategory
    action: TriggerAction
    affected_strategies: List[int]
    condition_description: str
    threshold: Any
    actual_value: Any
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "trigger_id": self.trigger_id,
            "trigger_name": self.trigger_name,
            "fired": self.fired,
            "priority": self.priority.value,
            "category": self.category.value,
            "action": self.action.value,
            "affected_strategies": self.affected_strategies,
            "condition_description": self.condition_description,
            "threshold": self.threshold,
            "actual_value": self.actual_value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "correlation_id": self.correlation_id,
        }


class TriggerEvaluator(Protocol):
    """
    Protocol (structural subtyping) for trigger evaluators.

    Any class with these methods can be used as a trigger evaluator,
    without inheriting from a specific base class.
    """

    @property
    def trigger_id(self) -> str:
        """Unique trigger identifier."""
        ...

    @property
    def trigger_name(self) -> str:
        """Human-readable trigger name."""
        ...

    def evaluate(self, data: Dict[str, Any]) -> TriggerResultInterface:
        """Evaluate trigger conditions against provided data."""
        ...


class NotificationBackendInterface(Protocol):
    """
    Protocol for notification backends.

    Service-agnostic interface allows swapping implementations
    (e.g., Slack webhook, email, PagerDuty) without code changes.
    """

    def send_alert(self, alert: TriggerResultInterface) -> bool:
        """Send alert through this backend. Returns success status."""
        ...

    def get_backend_name(self) -> str:
        """Return human-readable backend name."""
        ...


# Utility functions for working with interface types

def convert_priority(priority: 'TriggerPriority') -> str:
    """Convert priority to string value."""
    return priority.value


def convert_action(action: 'TriggerAction') -> str:
    """Convert action to string value."""
    return action.value


def is_critical_priority(priority: TriggerPriority) -> bool:
    """Check if priority is critical level."""
    return priority == TriggerPriority.P0_CRITICAL


def is_high_or_above(priority: TriggerPriority) -> bool:
    """Check if priority is high or above."""
    return priority in (TriggerPriority.P0_CRITICAL, TriggerPriority.P1_HIGH)
