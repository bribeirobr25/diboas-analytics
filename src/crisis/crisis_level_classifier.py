"""
Crisis level classifier.

Classifies content into crisis levels 0-5 based on:
- Keywords indicating severity
- Trigger priorities
- Market data indicators
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Dict, List, Optional


class CrisisLevel(IntEnum):
    """
    Crisis severity levels.

    Higher levels require more approvals and faster response.
    """
    LEVEL_0_NORMAL = 0       # Normal operations, auto-approve
    LEVEL_1_WATCH = 1        # Minor concern, auto-approve with flag
    LEVEL_2_CAUTION = 2      # Elevated concern, auto-approve with monitoring
    LEVEL_3_WARNING = 3      # Significant concern, CLO + CEO approval (60min SLA)
    LEVEL_4_ALERT = 4        # Major concern, CLO + CEO + Counsel (75min SLA)
    LEVEL_5_CRITICAL = 5     # Critical event, Full board + Counsel (90min SLA)


@dataclass
class CrisisClassification:
    """
    Result of crisis level classification.

    Contains level, reasons, and required approvers.
    """
    level: CrisisLevel
    reasons: List[str]
    requires_human_approval: bool
    approvers: List[str]
    sla_minutes: Optional[int]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "level": self.level.value,
            "level_name": self.level.name,
            "reasons": self.reasons,
            "requires_human_approval": self.requires_human_approval,
            "approvers": self.approvers,
            "sla_minutes": self.sla_minutes,
        }


# Keywords by crisis level
CRISIS_KEYWORDS = {
    CrisisLevel.LEVEL_5_CRITICAL: [
        "confirmed loss",
        "funds lost",
        "hack confirmed",
        "rug pull",
        "exploit confirmed",
        "total loss",
        "protocol failure",
    ],
    CrisisLevel.LEVEL_4_ALERT: [
        "potential loss",
        "security incident",
        "funds at risk",
        "suspected hack",
        "critical vulnerability",
        "unconfirmed exploit",
    ],
    CrisisLevel.LEVEL_3_WARNING: [
        "security concern",
        "elevated risk",
        "caution advised",
        "unusual activity",
        "potential vulnerability",
        "significant drawdown",
    ],
    CrisisLevel.LEVEL_2_CAUTION: [
        "volatility",
        "market decline",
        "apy dropped",
        "minor concern",
        "monitoring",
        "attention needed",
    ],
}

# Approvers by level
CRISIS_APPROVERS = {
    CrisisLevel.LEVEL_3_WARNING: ["clo_board", "ceo"],
    CrisisLevel.LEVEL_4_ALERT: ["clo_board", "ceo", "external_counsel"],
    CrisisLevel.LEVEL_5_CRITICAL: ["clo_board", "ceo", "board", "external_counsel"],
}

# SLA by level (minutes)
CRISIS_SLA = {
    CrisisLevel.LEVEL_3_WARNING: 60,
    CrisisLevel.LEVEL_4_ALERT: 75,
    CrisisLevel.LEVEL_5_CRITICAL: 90,
}


class CrisisLevelClassifier:
    """
    Classify content into crisis levels.

    Uses multiple signals:
    1. Keyword matching
    2. Trigger priority
    3. Market data indicators
    """

    def classify(
        self,
        content: str,
        trigger_priority: Optional[str] = None,
        market_data: Optional[Dict[str, Any]] = None,
    ) -> CrisisClassification:
        """
        Classify content into a crisis level.

        Args:
            content: Content to classify
            trigger_priority: Optional trigger priority (P0/P1/P2/P3)
            market_data: Optional market data for context

        Returns:
            CrisisClassification with level and requirements
        """
        content_lower = content.lower()
        reasons: List[str] = []
        level = CrisisLevel.LEVEL_0_NORMAL

        # 1. Check keywords (highest level wins)
        for crisis_level in [
            CrisisLevel.LEVEL_5_CRITICAL,
            CrisisLevel.LEVEL_4_ALERT,
            CrisisLevel.LEVEL_3_WARNING,
            CrisisLevel.LEVEL_2_CAUTION,
        ]:
            keywords = CRISIS_KEYWORDS.get(crisis_level, [])
            for keyword in keywords:
                if keyword in content_lower:
                    if crisis_level > level:
                        level = crisis_level
                        reasons.append(f"Keyword: '{keyword}'")
                    break  # Only need one match per level

        # 2. Check trigger priority
        if trigger_priority:
            trigger_level = self._priority_to_level(trigger_priority)
            if trigger_level > level:
                level = trigger_level
                reasons.append(f"Trigger priority: {trigger_priority}")

        # 3. Check market data
        if market_data:
            market_level, market_reason = self._check_market_data(market_data)
            if market_level > level:
                level = market_level
                reasons.append(market_reason)

        # Determine approval requirements
        requires_human = level >= CrisisLevel.LEVEL_3_WARNING
        approvers = CRISIS_APPROVERS.get(level, [])
        sla = CRISIS_SLA.get(level)

        return CrisisClassification(
            level=level,
            reasons=reasons if reasons else ["Normal operations"],
            requires_human_approval=requires_human,
            approvers=approvers,
            sla_minutes=sla,
        )

    def _priority_to_level(self, priority: str) -> CrisisLevel:
        """Convert trigger priority to crisis level."""
        priority_map = {
            "P0": CrisisLevel.LEVEL_4_ALERT,
            "P1": CrisisLevel.LEVEL_3_WARNING,
            "P2": CrisisLevel.LEVEL_2_CAUTION,
            "P3": CrisisLevel.LEVEL_1_WATCH,
        }
        return priority_map.get(priority, CrisisLevel.LEVEL_0_NORMAL)

    def _check_market_data(
        self, market_data: Dict[str, Any]
    ) -> tuple[CrisisLevel, str]:
        """Check market data for crisis indicators."""
        # BTC crash
        btc_change = market_data.get("btc_change_24h_pct", 0)
        if btc_change < -20:
            return CrisisLevel.LEVEL_4_ALERT, f"BTC crash: {btc_change:.1f}%"
        elif btc_change < -10:
            return CrisisLevel.LEVEL_3_WARNING, f"BTC significant drop: {btc_change:.1f}%"

        # VIX spike
        vix = market_data.get("vix", 0)
        if vix > 40:
            return CrisisLevel.LEVEL_3_WARNING, f"VIX elevated: {vix}"

        # Protocol TVL drop
        tvl_drop = market_data.get("max_tvl_drop_24h_pct", 0)
        if tvl_drop < -25:
            return CrisisLevel.LEVEL_4_ALERT, f"Protocol TVL crash: {tvl_drop:.1f}%"

        return CrisisLevel.LEVEL_0_NORMAL, ""
