"""
Depeg threshold configuration with time-window requirements.

Per CTO Board specification:
- L2/L3 triggers require 5 minutes (300 seconds) sustained depeg
- L4 (crisis) triggers require 1 minute (60 seconds) sustained depeg

This prevents instantaneous price spikes from triggering false alerts.
Time-window checking requires depeg to be sustained for the specified
duration before the trigger fires.

Data source: CoinGecko collector for USDC and USDT prices.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class DepegLevel(Enum):
    """Depeg severity levels."""
    L2_CAUTION = "L2"   # >1% depeg
    L3_WARNING = "L3"   # >2% depeg
    L4_CRISIS = "L4"    # >5% depeg


@dataclass(frozen=True)
class DepegThreshold:
    """
    Configuration for a depeg threshold level.

    Attributes:
        level: The severity level (L2, L3, or L4)
        threshold_pct: Percentage deviation from $1.00 to trigger
        time_window_seconds: Duration the depeg must be sustained
        description: Human-readable description of the threshold
    """
    level: DepegLevel
    threshold_pct: float
    time_window_seconds: int
    description: str


# =============================================================================
# Time-Window Configuration
# =============================================================================

# L2/L3 triggers: 5 minutes sustained to prevent false positives
L2_L3_TIME_WINDOW_SECONDS = 300  # 5 minutes

# L4 crisis triggers: 1 minute sustained (faster response for critical events)
L4_TIME_WINDOW_SECONDS = 60  # 1 minute


# =============================================================================
# USDC Depeg Thresholds
# =============================================================================

USDC_THRESHOLDS: Dict[str, DepegThreshold] = {
    "L2": DepegThreshold(
        level=DepegLevel.L2_CAUTION,
        threshold_pct=1.0,
        time_window_seconds=L2_L3_TIME_WINDOW_SECONDS,
        description="USDC >1% depeg sustained for 5 minutes",
    ),
    "L3": DepegThreshold(
        level=DepegLevel.L3_WARNING,
        threshold_pct=2.0,
        time_window_seconds=L2_L3_TIME_WINDOW_SECONDS,
        description="USDC >2% depeg sustained for 5 minutes",
    ),
    "L4": DepegThreshold(
        level=DepegLevel.L4_CRISIS,
        threshold_pct=5.0,
        time_window_seconds=L4_TIME_WINDOW_SECONDS,
        description="USDC >5% depeg sustained for 1 minute",
    ),
}


# =============================================================================
# USDT Depeg Thresholds
# =============================================================================

USDT_THRESHOLDS: Dict[str, DepegThreshold] = {
    "L2": DepegThreshold(
        level=DepegLevel.L2_CAUTION,
        threshold_pct=1.0,
        time_window_seconds=L2_L3_TIME_WINDOW_SECONDS,
        description="USDT >1% depeg sustained for 5 minutes",
    ),
    "L3": DepegThreshold(
        level=DepegLevel.L3_WARNING,
        threshold_pct=2.0,
        time_window_seconds=L2_L3_TIME_WINDOW_SECONDS,
        description="USDT >2% depeg sustained for 5 minutes",
    ),
    "L4": DepegThreshold(
        level=DepegLevel.L4_CRISIS,
        threshold_pct=5.0,
        time_window_seconds=L4_TIME_WINDOW_SECONDS,
        description="USDT >5% depeg sustained for 1 minute",
    ),
}


# =============================================================================
# Helper Functions
# =============================================================================

def get_usdc_threshold(level: str) -> DepegThreshold:
    """
    Get USDC depeg threshold configuration.

    Args:
        level: "L2", "L3", or "L4"

    Returns:
        DepegThreshold configuration for the specified level

    Raises:
        KeyError: If level is not valid
    """
    return USDC_THRESHOLDS[level.upper()]


def get_usdt_threshold(level: str) -> DepegThreshold:
    """
    Get USDT depeg threshold configuration.

    Args:
        level: "L2", "L3", or "L4"

    Returns:
        DepegThreshold configuration for the specified level

    Raises:
        KeyError: If level is not valid
    """
    return USDT_THRESHOLDS[level.upper()]


def get_time_window_for_level(level: str) -> int:
    """
    Get time-window duration in seconds for a given level.

    Args:
        level: "L2", "L3", or "L4"

    Returns:
        Time-window in seconds (300 for L2/L3, 60 for L4)
    """
    level_upper = level.upper()
    if level_upper == "L4":
        return L4_TIME_WINDOW_SECONDS
    return L2_L3_TIME_WINDOW_SECONDS
