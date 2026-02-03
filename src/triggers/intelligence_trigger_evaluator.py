"""
Main engine for evaluating all registered intelligence triggers.

Orchestrates trigger evaluation with cooldown management and alert consolidation.
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

from src.registries.trigger_registry import TriggerRegistry
from src.triggers.base import IntelligenceTriggerBase, IntelligenceTriggerResult
from src.triggers.intelligence_cooldown_manager import IntelligenceCooldownManager
from src.triggers.intelligence_alert_consolidator import IntelligenceAlertConsolidator

logger = logging.getLogger(__name__)


class IntelligenceTriggerEvaluator:
    """
    Evaluate all registered triggers against market data.

    Features:
    - Iterates through all registered triggers
    - Applies cooldown to prevent spam
    - Consolidates related alerts
    - Calls future hooks (emit_event, verify)
    - Never crashes - catches exceptions and continues
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize evaluator with optional configuration.

        Args:
            config: Configuration dict with:
                - default_cooldown_minutes: Cooldown period (default: 60)
                - consolidate_alerts: Whether to consolidate (default: True)
        """
        self.config = config or {}
        self.cooldown_manager = IntelligenceCooldownManager(
            default_cooldown_minutes=self.config.get("default_cooldown_minutes", 60)
        )
        self.consolidator = IntelligenceAlertConsolidator(
            strategy_overlap_threshold=self.config.get("strategy_overlap_threshold", 0.5)
        )
        self.consolidate_alerts = self.config.get("consolidate_alerts", True)

    def evaluate_all(
        self,
        data: Dict[str, Any],
        correlation_id: Optional[str] = None,
    ) -> List[IntelligenceTriggerResult]:
        """
        Evaluate all registered triggers against data.

        Args:
            data: Market/protocol data containing:
                - protocol_health: Dict of protocol metrics
                - market_prices: Dict of price data
                - wallet_activity: Dict of wallet movements
                - macro_indicators: Dict of macro data
            correlation_id: Optional ID to trace related operations

        Returns:
            List of FIRED trigger results (passed triggers are excluded)
        """
        correlation_id = correlation_id or str(uuid.uuid4())[:8]
        results: List[IntelligenceTriggerResult] = []

        # Get all registered trigger names
        registry = TriggerRegistry.get_instance()
        trigger_names = registry.list_available()

        logger.debug(f"[{correlation_id}] Evaluating {len(trigger_names)} triggers")

        for trigger_name in trigger_names:
            try:
                result = self._evaluate_single_trigger(
                    trigger_name, data, correlation_id
                )
                if result and result.fired:
                    results.append(result)

            except Exception as e:
                # Never crash - log and continue
                logger.error(
                    f"[{correlation_id}] Error evaluating {trigger_name}: {e}",
                    exc_info=True,
                )

        logger.info(
            f"[{correlation_id}] Evaluation complete: {len(results)} alerts from "
            f"{len(trigger_names)} triggers"
        )

        # Optionally consolidate related alerts
        if self.consolidate_alerts and len(results) > 1:
            results = self.consolidator.consolidate(results)
            logger.debug(f"[{correlation_id}] Consolidated to {len(results)} alerts")

        return results

    def _evaluate_single_trigger(
        self,
        trigger_name: str,
        data: Dict[str, Any],
        correlation_id: str,
    ) -> Optional[IntelligenceTriggerResult]:
        """
        Evaluate a single trigger.

        Handles:
        - Getting trigger instance
        - Checking enabled status
        - Checking cooldown
        - Calling evaluate()
        - Setting cooldown if fired
        - Calling future hooks

        Returns:
            IntelligenceTriggerResult if fired, None otherwise
        """
        registry = TriggerRegistry.get_instance()
        trigger = registry.get(trigger_name, config={})

        # Check if this is an IntelligenceTriggerBase (new style)
        if not isinstance(trigger, IntelligenceTriggerBase):
            # Old-style trigger from registry stubs - evaluate differently
            return self._evaluate_legacy_trigger(trigger, data, correlation_id)

        # Check enabled
        if not trigger.enabled:
            logger.debug(f"[{correlation_id}] {trigger.trigger_id} disabled, skipping")
            return None

        # Evaluate
        result = trigger.evaluate(data)
        result.correlation_id = correlation_id

        if not result.fired:
            return None

        # Check cooldown
        if self.cooldown_manager.is_on_cooldown(result.trigger_id):
            remaining = self.cooldown_manager.get_remaining_minutes(result.trigger_id)
            logger.debug(
                f"[{correlation_id}] {result.trigger_id} on cooldown ({remaining}m remaining)"
            )
            return None

        # Set cooldown
        self.cooldown_manager.set_cooldown(result.trigger_id)

        # Call future hooks
        trigger.emit_event(result)
        trigger.verify(result)

        logger.info(
            f"[{correlation_id}] FIRED: {result.trigger_id} "
            f"priority={result.priority.value} value={result.actual_value}"
        )

        return result

    def _evaluate_legacy_trigger(
        self,
        trigger,
        data: Dict[str, Any],
        correlation_id: str,
    ) -> Optional[IntelligenceTriggerResult]:
        """
        Evaluate legacy trigger from existing TriggerRegistry stubs.

        Legacy triggers return List[Alert], not IntelligenceTriggerResult.
        This adapter converts for compatibility.
        """
        try:
            alerts = trigger.evaluate(data)
            if not alerts:
                return None

            # Convert first alert to IntelligenceTriggerResult
            from src.triggers.base import (
                IntelligenceTriggerCategory,
                IntelligenceTriggerPriority,
                IntelligenceTriggerAction,
            )

            alert = alerts[0]

            # Map legacy severity to priority
            severity_map = {
                "emergency": IntelligenceTriggerPriority.P0_CRITICAL,
                "critical": IntelligenceTriggerPriority.P1_HIGH,
                "warning": IntelligenceTriggerPriority.P2_MEDIUM,
                "info": IntelligenceTriggerPriority.P3_INFO,
            }

            # Map legacy trigger_type to category
            type_map = {
                "protocol": IntelligenceTriggerCategory.PROTOCOL_HEALTH,
                "regime": IntelligenceTriggerCategory.MARKET_CONDITION,
                "estate": IntelligenceTriggerCategory.ESTATE_WALLET,
                "whale": IntelligenceTriggerCategory.WHALE_ACTIVITY,
                "correlation": IntelligenceTriggerCategory.MACRO_INDICATOR,
            }

            return IntelligenceTriggerResult(
                trigger_id=alert.trigger_id,
                trigger_name=alert.title,
                fired=True,
                priority=severity_map.get(
                    alert.severity.value, IntelligenceTriggerPriority.P2_MEDIUM
                ),
                category=type_map.get(
                    trigger.trigger_type, IntelligenceTriggerCategory.PROTOCOL_HEALTH
                ),
                action=IntelligenceTriggerAction.PROTOCOL_ALERT,
                affected_strategies=list(range(1, 11)),  # All strategies
                condition_description=alert.message,
                threshold=None,
                actual_value=alert.data,
                correlation_id=correlation_id,
            )

        except Exception as e:
            logger.debug(f"[{correlation_id}] Legacy trigger eval failed: {e}")
            return None

    def evaluate_category(
        self,
        category: str,
        data: Dict[str, Any],
        correlation_id: Optional[str] = None,
    ) -> List[IntelligenceTriggerResult]:
        """
        Evaluate only triggers in a specific category.

        Args:
            category: Category to filter (protocol_health, market_condition, etc.)
            data: Market/protocol data
            correlation_id: Optional correlation ID

        Returns:
            List of fired trigger results for that category
        """
        all_results = self.evaluate_all(data, correlation_id)
        return [r for r in all_results if r.category.value == category]

    def get_alert_summary(
        self,
        results: List[IntelligenceTriggerResult],
    ) -> Dict[str, Any]:
        """
        Get summary statistics for alert results.

        Args:
            results: List of trigger results

        Returns:
            Summary dict from consolidator
        """
        return self.consolidator.get_summary(results)
