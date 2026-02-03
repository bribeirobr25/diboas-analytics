"""
Macro indicator triggers.

Monitor broader economic indicators:
- Yield curve movements (recession indicators)
- Liquidity conditions (credit spreads, Fed balance sheet)
"""

from src.triggers.macro.yield_curve_triggers import (
    YieldCurveInversionTrigger,
    YieldCurveSteepTrigger,
)
from src.triggers.macro.liquidity_triggers import (
    CreditSpreadWideTrigger,
    FedLiquidityTrigger,
)

__all__ = [
    "YieldCurveInversionTrigger",
    "YieldCurveSteepTrigger",
    "CreditSpreadWideTrigger",
    "FedLiquidityTrigger",
]
