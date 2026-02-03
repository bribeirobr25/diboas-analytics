"""
Abstract base class for Intelligence Triggers.

Provides the foundation for all Layer 4 trigger implementations.
Triggers evaluate market conditions and generate prioritized alerts.

Pattern: [DOMAIN]-[ENTITY]-[LEVEL] for trigger IDs
Example: SKY-DEPEG-L2 (Sky protocol, depeg condition, Level 2 severity)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol


class IntelligenceTriggerPriority(Enum):
    """
    Alert priority levels.

    P0_CRITICAL: Immediate action required (crisis-level events)
    P1_HIGH: Urgent attention needed (significant market events)
    P2_MEDIUM: Important but not urgent (notable changes)
    P3_INFO: Informational only (minor observations)
    """
    P0_CRITICAL = "P0"
    P1_HIGH = "P1"
    P2_MEDIUM = "P2"
    P3_INFO = "P3"


class IntelligenceTriggerCategory(Enum):
    """Categories of intelligence triggers."""
    PROTOCOL_HEALTH = "protocol_health"
    MARKET_CONDITION = "market_condition"
    ESTATE_WALLET = "estate_wallet"
    WHALE_ACTIVITY = "whale_activity"
    MACRO_INDICATOR = "macro_indicator"


class IntelligenceTriggerAction(Enum):
    """Actions to take when trigger fires."""
    CRISIS_TEMPLATE = "crisis_template"
    PROTOCOL_ALERT = "protocol_alert"
    SMART_MONEY_INSIGHT = "smart_money_insight"
    PERFORMANCE_ALERT = "performance_alert"
    INTERNAL_ONLY = "internal_only"


@dataclass
class IntelligenceTriggerResult:
    """
    Result from a trigger evaluation.

    Contains all context needed for alert processing and routing.
    """
    trigger_id: str
    trigger_name: str
    fired: bool
    priority: IntelligenceTriggerPriority
    category: IntelligenceTriggerCategory
    action: IntelligenceTriggerAction
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


class NotificationBackend(Protocol):
    """
    Protocol for notification backends.

    Service-agnostic interface allows swapping implementations
    (e.g., Slack webhook, email, PagerDuty) without code changes.
    """

    def send_alert(self, alert: IntelligenceTriggerResult) -> bool:
        """Send alert through this backend. Returns success status."""
        ...

    def get_backend_name(self) -> str:
        """Return human-readable backend name."""
        ...


class IntelligenceTriggerBase(ABC):
    """
    Abstract base for all intelligence triggers.

    Subclasses must implement:
    - trigger_id: Unique identifier (pattern: [DOMAIN]-[ENTITY]-[LEVEL])
    - trigger_name: Human-readable name
    - category: One of IntelligenceTriggerCategory
    - priority: One of IntelligenceTriggerPriority
    - action: What action to take when fired
    - affected_strategies: List of strategy IDs impacted
    - evaluate(): Core logic to check if trigger fires

    Future hooks (implement as no-op for now):
    - emit_event(): Event-driven architecture (Phase 2+)
    - verify(): Decentralized verification (Phase 4)
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize trigger with optional configuration.

        Args:
            config: Configuration dict with trigger-specific settings
        """
        self.config = config or {}
        self.enabled = self.config.get("enabled", True)

    @property
    @abstractmethod
    def trigger_id(self) -> str:
        """
        Unique trigger identifier.

        Pattern: [DOMAIN]-[ENTITY]-[LEVEL]
        Example: SKY-DEPEG-L2
        """
        pass

    @property
    @abstractmethod
    def trigger_name(self) -> str:
        """Human-readable trigger name."""
        pass

    @property
    @abstractmethod
    def category(self) -> IntelligenceTriggerCategory:
        """Trigger category for grouping."""
        pass

    @property
    @abstractmethod
    def priority(self) -> IntelligenceTriggerPriority:
        """Default priority when trigger fires."""
        pass

    @property
    @abstractmethod
    def action(self) -> IntelligenceTriggerAction:
        """Action to take when trigger fires."""
        pass

    @property
    @abstractmethod
    def affected_strategies(self) -> List[int]:
        """Strategy IDs affected by this trigger."""
        pass

    @abstractmethod
    def evaluate(self, data: Dict[str, Any]) -> IntelligenceTriggerResult:
        """
        Evaluate trigger conditions against provided data.

        Args:
            data: Market/protocol data to evaluate

        Returns:
            IntelligenceTriggerResult with fired=True/False
        """
        pass

    def emit_event(self, result: IntelligenceTriggerResult) -> None:
        """
        Emit event for event-driven architecture.

        Future hook for Phase 2+ integration with message queues,
        webhooks, or event streaming platforms.

        Default: No-op
        """
        pass

    def verify(self, result: IntelligenceTriggerResult) -> bool:
        """
        Verify trigger result for decentralized validation.

        Future hook for Phase 4 integration with blockchain-based
        verification or multi-party validation.

        Default: Always returns True (trusted)
        """
        return True

    def _create_result(
        self,
        fired: bool,
        threshold: Any,
        actual_value: Any,
        metadata: Dict[str, Any] = None,
    ) -> IntelligenceTriggerResult:
        """
        Helper to create consistent IntelligenceTriggerResult.

        Args:
            fired: Whether trigger condition was met
            threshold: The threshold value that was checked
            actual_value: The actual value from the data
            metadata: Additional context

        Returns:
            Populated IntelligenceTriggerResult
        """
        return IntelligenceTriggerResult(
            trigger_id=self.trigger_id,
            trigger_name=self.trigger_name,
            fired=fired,
            priority=self.priority,
            category=self.category,
            action=self.action,
            affected_strategies=self.affected_strategies,
            condition_description=f"{self.trigger_name} check",
            threshold=threshold,
            actual_value=actual_value,
            metadata=metadata or {},
        )
