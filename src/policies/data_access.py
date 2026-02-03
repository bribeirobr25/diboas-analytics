"""
DataAccessPolicy - Ethical guardrails for B2B data access.

From Innovation Board Session 003:
- Estate wallet data is BLOCKED for B2B API clients
- This prevents institutional clients from front-running retail users
- diBoaS users always get full data access

The Grandmother Test:
"Would this help my grandmother build wealth, or help sophisticated
players extract value from her?"
"""

from enum import Enum
from typing import Dict, Any, Set, FrozenSet, Optional, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class ClientTier(Enum):
    """Client access tiers for data access control."""
    DIBOAS_USER = "diboas_user"      # Full access (our users)
    B2B_STANDARD = "b2b_standard"    # Limited access
    B2B_PREMIUM = "b2b_premium"      # More access, but still restricted
    INTERNAL = "internal"            # Full access (internal tools)


@dataclass
class DataAccessPolicy:
    """
    Ethical guardrails for B2B data access.

    The Grandmother Test: "Would this help my grandmother build wealth,
    or help sophisticated players extract value from her?"

    Usage:
        policy = DataAccessPolicy()

        # Check if client can access data
        if policy.can_access(ClientTier.B2B_STANDARD, "estate_wallet_addresses"):
            # Will return False - B2B cannot access estate data

        # Filter response for client
        filtered = policy.filter_response(ClientTier.B2B_STANDARD, full_data)
    """

    # Data categories that are ALWAYS blocked for B2B clients
    # These protect retail users from institutional front-running
    BLOCKED_FOR_B2B: FrozenSet[str] = frozenset({
        "estate_wallet_addresses",      # No front-running Mt. Gox/FTX distributions
        "estate_wallet_balances",       # No front-running liquidations
        "estate_wallet_transactions",   # No tracking specific estate movements
        "whale_wallet_addresses",       # No copying whale trades
        "whale_real_time_movements",    # No HFT on whale activity
        "whale_transaction_history",    # No reconstructing whale strategies
        "individual_wallet_data",       # No tracking specific wallets
    })

    # Data that B2B gets in aggregated form only
    # Provides useful info without enabling front-running
    AGGREGATED_FOR_B2B: FrozenSet[str] = frozenset({
        "whale_activity_summary",       # "Large wallets moved X" not "Wallet 0x123 moved"
        "estate_risk_score",            # Aggregate risk score, not specific wallets
        "whale_sentiment",              # Net accumulation/distribution, not individual
        "large_holder_metrics",         # Aggregated stats only
    })

    # Data categories that are fully available to all tiers
    PUBLIC_DATA: FrozenSet[str] = frozenset({
        "market_prices",                # BTC, ETH, etc. prices
        "fear_greed_index",             # Public sentiment data
        "vix",                          # Public volatility index
        "credit_spreads",               # Public bond spreads
        "protocol_tvl",                 # Public DeFi metrics
        "strategy_performance",         # Anonymized strategy returns
        "historical_backtest",          # Backtest results
        "monte_carlo_results",          # Simulation results
    })

    @classmethod
    def can_access(cls, client_tier: ClientTier, data_type: str) -> bool:
        """
        Check if client tier can access specific data type.

        Args:
            client_tier: The client's access tier
            data_type: The type of data being requested

        Returns:
            True if access is allowed, False otherwise
        """
        # diBoaS users and internal tools get everything
        if client_tier in (ClientTier.DIBOAS_USER, ClientTier.INTERNAL):
            logger.debug(f"Full access granted to {client_tier.value} for {data_type}")
            return True

        # B2B clients cannot access blocked data
        if data_type in cls.BLOCKED_FOR_B2B:
            logger.info(
                f"Access DENIED: {client_tier.value} blocked from {data_type} "
                "(Grandmother Test protection)"
            )
            return False

        # All other data is accessible
        return True

    @classmethod
    def get_access_level(cls, client_tier: ClientTier, data_type: str) -> str:
        """
        Get the access level for a specific data type.

        Args:
            client_tier: The client's access tier
            data_type: The type of data being requested

        Returns:
            One of: "full", "aggregated", "blocked"
        """
        if client_tier in (ClientTier.DIBOAS_USER, ClientTier.INTERNAL):
            return "full"

        if data_type in cls.BLOCKED_FOR_B2B:
            return "blocked"

        if data_type in cls.AGGREGATED_FOR_B2B:
            return "aggregated"

        return "full"

    @classmethod
    def filter_response(
        cls,
        client_tier: ClientTier,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Filter response data based on client tier.

        Removes blocked fields and aggregates sensitive data.

        Args:
            client_tier: The client's access tier
            data: Full data dictionary to filter

        Returns:
            Filtered data dictionary appropriate for client tier
        """
        # diBoaS users and internal tools get full data
        if client_tier in (ClientTier.DIBOAS_USER, ClientTier.INTERNAL):
            return data

        filtered = {}
        blocked_keys = []
        aggregated_keys = []

        for key, value in data.items():
            if key in cls.BLOCKED_FOR_B2B:
                blocked_keys.append(key)
                continue  # Remove blocked fields entirely

            elif key in cls.AGGREGATED_FOR_B2B:
                aggregated_keys.append(key)
                filtered[key] = cls._aggregate(key, value)

            else:
                filtered[key] = value

        if blocked_keys:
            logger.info(
                f"Filtered {len(blocked_keys)} blocked fields for {client_tier.value}: "
                f"{blocked_keys}"
            )

        if aggregated_keys:
            logger.debug(
                f"Aggregated {len(aggregated_keys)} fields for {client_tier.value}: "
                f"{aggregated_keys}"
            )

        return filtered

    @classmethod
    def _aggregate(cls, key: str, value: Any) -> Any:
        """
        Convert detailed data to aggregated form for B2B clients.

        Args:
            key: The data field key
            value: The original value

        Returns:
            Aggregated/anonymized value
        """
        if key == "whale_activity_summary":
            # Return summary counts, not individual transactions
            if isinstance(value, list):
                total_in = sum(1 for v in value if v.get('direction') == 'in')
                total_out = sum(1 for v in value if v.get('direction') == 'out')
                return {
                    "total_movements": len(value),
                    "net_direction": "accumulation" if total_in > total_out else "distribution",
                    "period": "24h",
                    "note": "Aggregated data - individual wallets not disclosed"
                }
            return {"total_movements": 0, "note": "No activity"}

        elif key == "estate_risk_score":
            # Return risk category, not specific values
            if isinstance(value, (int, float)):
                if value < 30:
                    return {"risk_level": "low", "note": "Aggregated risk assessment"}
                elif value < 70:
                    return {"risk_level": "medium", "note": "Aggregated risk assessment"}
                else:
                    return {"risk_level": "high", "note": "Aggregated risk assessment"}
            return {"risk_level": "unknown", "note": "Aggregated risk assessment"}

        elif key == "whale_sentiment":
            # Return sentiment direction only
            if isinstance(value, dict):
                return {
                    "sentiment": value.get('direction', 'neutral'),
                    "confidence": "aggregated",
                    "note": "Based on large holder activity patterns"
                }
            return {"sentiment": "neutral", "note": "Aggregated sentiment"}

        elif key == "large_holder_metrics":
            # Return high-level metrics only
            if isinstance(value, dict):
                return {
                    "concentration": value.get('concentration_category', 'normal'),
                    "trend": value.get('trend', 'stable'),
                    "note": "Aggregated metrics - no individual holder data"
                }
            return {"note": "Aggregated metrics available"}

        # Default: return a placeholder
        return {"aggregated": True, "note": "Data aggregated for privacy"}

    @classmethod
    def get_blocked_fields(cls) -> List[str]:
        """Return list of fields blocked for B2B clients."""
        return sorted(list(cls.BLOCKED_FOR_B2B))

    @classmethod
    def get_aggregated_fields(cls) -> List[str]:
        """Return list of fields that are aggregated for B2B clients."""
        return sorted(list(cls.AGGREGATED_FOR_B2B))

    @classmethod
    def explain_policy(cls, client_tier: ClientTier) -> Dict[str, Any]:
        """
        Get human-readable explanation of data access policy for a tier.

        Args:
            client_tier: The client tier to explain

        Returns:
            Dictionary with policy explanation
        """
        if client_tier in (ClientTier.DIBOAS_USER, ClientTier.INTERNAL):
            return {
                "tier": client_tier.value,
                "access_level": "full",
                "description": "Full access to all data including estate and whale wallet details",
                "blocked_fields": [],
                "aggregated_fields": [],
            }

        return {
            "tier": client_tier.value,
            "access_level": "restricted",
            "description": (
                "Limited access to protect retail users from front-running. "
                "Estate and whale wallet data is blocked or aggregated."
            ),
            "blocked_fields": cls.get_blocked_fields(),
            "aggregated_fields": cls.get_aggregated_fields(),
            "reason": (
                "The Grandmother Test: This policy ensures that sophisticated "
                "institutional players cannot use our data to extract value from "
                "retail investors."
            ),
        }


def validate_access(
    client_tier: ClientTier,
    requested_fields: List[str]
) -> Dict[str, str]:
    """
    Validate access to multiple fields at once.

    Args:
        client_tier: The client's access tier
        requested_fields: List of data fields to validate

    Returns:
        Dictionary mapping field names to access levels
    """
    return {
        field: DataAccessPolicy.get_access_level(client_tier, field)
        for field in requested_fields
    }
