"""
Gate 3 Validation Rules - Rules for trigger output validation.

From VALIDATION_GATES_CTO_HANDOFF_v2.md Section 5.
"""

from typing import Set, Dict, Optional

from src.triggers.base import (
    IntelligenceTriggerPriority,
    IntelligenceTriggerAction,
)


# Valid strategy IDs (1-10)
VALID_STRATEGY_IDS: Set[int] = set(range(1, 11))

# Priority to valid actions mapping
# Some actions only make sense for certain priority levels
VALID_PRIORITY_ACTIONS: Dict[IntelligenceTriggerPriority, Set[IntelligenceTriggerAction]] = {
    IntelligenceTriggerPriority.P0_CRITICAL: {
        IntelligenceTriggerAction.CRISIS_TEMPLATE,
    },
    IntelligenceTriggerPriority.P1_HIGH: {
        IntelligenceTriggerAction.CRISIS_TEMPLATE,
        IntelligenceTriggerAction.PROTOCOL_ALERT,
    },
    IntelligenceTriggerPriority.P2_MEDIUM: {
        IntelligenceTriggerAction.PROTOCOL_ALERT,
        IntelligenceTriggerAction.SMART_MONEY_INSIGHT,
        IntelligenceTriggerAction.PERFORMANCE_ALERT,
    },
    IntelligenceTriggerPriority.P3_INFO: {
        IntelligenceTriggerAction.SMART_MONEY_INSIGHT,
        IntelligenceTriggerAction.PERFORMANCE_ALERT,
        IntelligenceTriggerAction.INTERNAL_ONLY,
    },
}

# Required fields for trigger results
REQUIRED_TRIGGER_FIELDS = [
    "trigger_id",
    "fired",
    "priority",
    "category",
    "action",
    "affected_strategies",
]

# Strategies by type (for validation)
STABLE_STRATEGIES = {1, 3, 5, 7, 9}  # 0% crypto exposure
CRYPTO_STRATEGIES = {2, 4, 6, 8, 10}  # Have crypto exposure

# Strategy to protocol mapping (which protocols affect which strategies)
STRATEGY_PROTOCOL_MAP: Dict[str, Set[int]] = {
    "sky": {1, 3, 5, 7, 9},      # Sky affects strategies 1,3,5,7,9
    "sanctum": {2, 4, 6, 8, 10},  # Sanctum affects even strategies
    "jlp": {4, 6, 8, 10},        # JLP affects higher-risk strategies
    "aave": {1, 3, 5, 7, 9},     # Aave affects stable strategies
}


def get_valid_actions_for_priority(
    priority: IntelligenceTriggerPriority
) -> Set[IntelligenceTriggerAction]:
    """
    Get valid actions for a given priority level.

    Args:
        priority: The trigger priority level

    Returns:
        Set of valid actions for that priority
    """
    return VALID_PRIORITY_ACTIONS.get(priority, set())


def is_valid_strategy_id(strategy_id: int) -> bool:
    """
    Check if strategy ID is valid.

    Args:
        strategy_id: Strategy ID to check

    Returns:
        True if valid (1-10), False otherwise
    """
    return strategy_id in VALID_STRATEGY_IDS


def get_expected_strategies_for_protocol(protocol: str) -> Set[int]:
    """
    Get expected affected strategies for a protocol.

    Args:
        protocol: Protocol name (lowercase)

    Returns:
        Set of strategy IDs that should be affected
    """
    return STRATEGY_PROTOCOL_MAP.get(protocol.lower(), set())


def is_action_valid_for_priority(
    action: IntelligenceTriggerAction,
    priority: IntelligenceTriggerPriority
) -> bool:
    """
    Check if action is valid for the given priority.

    Args:
        action: The action to check
        priority: The priority level

    Returns:
        True if action is valid for priority, False otherwise
    """
    valid_actions = get_valid_actions_for_priority(priority)
    return action in valid_actions
