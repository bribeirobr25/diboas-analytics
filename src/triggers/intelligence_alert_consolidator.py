"""
Consolidate related alerts to reduce noise.

Groups related triggers into consolidated alerts for cleaner output.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.triggers.base import (
    IntelligenceTriggerResult,
    IntelligenceTriggerPriority,
    IntelligenceTriggerCategory,
)

logger = logging.getLogger(__name__)


class IntelligenceAlertConsolidator:
    """
    Consolidate multiple related alerts.

    Groups alerts by:
    - Category (protocol_health, market_condition, etc.)
    - Affected strategies overlap
    - Time proximity

    Selects highest priority from grouped alerts.
    """

    def __init__(self, strategy_overlap_threshold: float = 0.5):
        """
        Initialize consolidator.

        Args:
            strategy_overlap_threshold: Min overlap ratio to group (0.0-1.0)
        """
        self.strategy_overlap_threshold = strategy_overlap_threshold

    def consolidate(
        self,
        results: List[IntelligenceTriggerResult],
    ) -> List[IntelligenceTriggerResult]:
        """
        Consolidate related trigger results.

        Args:
            results: List of fired trigger results

        Returns:
            Consolidated list with grouped alerts
        """
        if not results:
            return []

        # Group by category
        by_category: Dict[IntelligenceTriggerCategory, List[IntelligenceTriggerResult]] = {}
        for result in results:
            if result.category not in by_category:
                by_category[result.category] = []
            by_category[result.category].append(result)

        consolidated = []
        for category, category_results in by_category.items():
            grouped = self._group_by_strategy_overlap(category_results)
            consolidated.extend(grouped)

        # Sort by priority (P0 first)
        priority_order = {
            IntelligenceTriggerPriority.P0_CRITICAL: 0,
            IntelligenceTriggerPriority.P1_HIGH: 1,
            IntelligenceTriggerPriority.P2_MEDIUM: 2,
            IntelligenceTriggerPriority.P3_INFO: 3,
        }
        consolidated.sort(key=lambda r: priority_order.get(r.priority, 99))

        return consolidated

    def _group_by_strategy_overlap(
        self,
        results: List[IntelligenceTriggerResult],
    ) -> List[IntelligenceTriggerResult]:
        """
        Group alerts with overlapping affected strategies.

        Returns representative alert for each group with merged metadata.
        """
        if len(results) <= 1:
            return results

        # For simplicity, group consecutive alerts with high overlap
        groups: List[List[IntelligenceTriggerResult]] = []
        current_group: List[IntelligenceTriggerResult] = [results[0]]

        for result in results[1:]:
            overlap = self._calculate_strategy_overlap(
                current_group[0].affected_strategies,
                result.affected_strategies,
            )
            if overlap >= self.strategy_overlap_threshold:
                current_group.append(result)
            else:
                groups.append(current_group)
                current_group = [result]

        groups.append(current_group)

        # Create representative for each group
        representatives = []
        for group in groups:
            rep = self._create_group_representative(group)
            representatives.append(rep)

        return representatives

    def _calculate_strategy_overlap(
        self,
        strategies_a: List[int],
        strategies_b: List[int],
    ) -> float:
        """Calculate Jaccard similarity between strategy sets."""
        if not strategies_a or not strategies_b:
            return 0.0

        set_a = set(strategies_a)
        set_b = set(strategies_b)

        intersection = len(set_a & set_b)
        union = len(set_a | set_b)

        return intersection / union if union > 0 else 0.0

    def _create_group_representative(
        self,
        group: List[IntelligenceTriggerResult],
    ) -> IntelligenceTriggerResult:
        """
        Create representative alert for a group.

        Uses highest priority, merges strategies and metadata.
        """
        if len(group) == 1:
            return group[0]

        # Sort by priority to get highest
        priority_order = {
            IntelligenceTriggerPriority.P0_CRITICAL: 0,
            IntelligenceTriggerPriority.P1_HIGH: 1,
            IntelligenceTriggerPriority.P2_MEDIUM: 2,
            IntelligenceTriggerPriority.P3_INFO: 3,
        }
        group.sort(key=lambda r: priority_order.get(r.priority, 99))
        primary = group[0]

        # Merge strategies
        all_strategies = set()
        for result in group:
            all_strategies.update(result.affected_strategies)

        # Merge metadata
        merged_metadata = {"consolidated_from": [r.trigger_id for r in group]}
        for result in group:
            merged_metadata.update(result.metadata)

        return IntelligenceTriggerResult(
            trigger_id=primary.trigger_id,
            trigger_name=f"{primary.trigger_name} (+{len(group)-1} related)",
            fired=True,
            priority=primary.priority,
            category=primary.category,
            action=primary.action,
            affected_strategies=sorted(list(all_strategies)),
            condition_description=primary.condition_description,
            threshold=primary.threshold,
            actual_value=primary.actual_value,
            timestamp=primary.timestamp,
            metadata=merged_metadata,
            correlation_id=primary.correlation_id,
        )

    def get_summary(
        self,
        results: List[IntelligenceTriggerResult],
    ) -> Dict[str, Any]:
        """
        Generate summary statistics for alerts.

        Args:
            results: List of trigger results

        Returns:
            Summary dict with counts by priority/category
        """
        by_priority = {}
        by_category = {}

        for result in results:
            p_key = result.priority.value
            c_key = result.category.value

            by_priority[p_key] = by_priority.get(p_key, 0) + 1
            by_category[c_key] = by_category.get(c_key, 0) + 1

        return {
            "total_alerts": len(results),
            "by_priority": by_priority,
            "by_category": by_category,
            "highest_priority": results[0].priority.value if results else None,
            "affected_strategies": sorted(
                list(set(s for r in results for s in r.affected_strategies))
            ),
        }
