"""
Layer 4 Intelligence Triggers.

Provides automated market condition monitoring and alert generation.
Triggers evaluate protocol health, market conditions, wallet movements,
and macro indicators to generate actionable intelligence.

Components:
- IntelligenceTriggerBase: Abstract base for all triggers
- IntelligenceTriggerEvaluator: Main evaluation engine
- IntelligenceCooldownManager: Prevent trigger spam
- IntelligenceAlertConsolidator: Group related alerts

Usage:
    from src.triggers import IntelligenceTriggerEvaluator

    evaluator = IntelligenceTriggerEvaluator()
    results = evaluator.evaluate_all(market_data)
"""

from src.triggers.base import (
    IntelligenceTriggerPriority,
    IntelligenceTriggerCategory,
    IntelligenceTriggerAction,
    IntelligenceTriggerResult,
    IntelligenceTriggerBase,
    NotificationBackend,
)
from src.triggers.intelligence_trigger_evaluator import IntelligenceTriggerEvaluator
from src.triggers.intelligence_cooldown_manager import IntelligenceCooldownManager
from src.triggers.intelligence_alert_consolidator import IntelligenceAlertConsolidator

# Import protocol triggers to register them
from src.triggers import protocol  # noqa: F401
from src.triggers import market  # noqa: F401
from src.triggers import wallet  # noqa: F401
from src.triggers import macro  # noqa: F401

__all__ = [
    # Base types
    "IntelligenceTriggerPriority",
    "IntelligenceTriggerCategory",
    "IntelligenceTriggerAction",
    "IntelligenceTriggerResult",
    "IntelligenceTriggerBase",
    "NotificationBackend",
    # Core components
    "IntelligenceTriggerEvaluator",
    "IntelligenceCooldownManager",
    "IntelligenceAlertConsolidator",
]
