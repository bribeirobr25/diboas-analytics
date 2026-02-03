"""
Market condition triggers.

Monitor market-wide events that affect strategy performance:
- Price movements (BTC, ETH, SOL drops)
- Volatility spikes (VIX, crypto implied volatility)
"""

from src.triggers.market.price_movement_triggers import (
    BTCDropLevel3Trigger,
    BTCDropLevel4Trigger,
    ETHDropLevel3Trigger,
    SOLDropLevel3Trigger,
    SOLDropLevel4Trigger,
)
from src.triggers.market.volatility_triggers import (
    VIXSpikeLevel2Trigger,
    VIXSpikeLevel3Trigger,
    CryptoVolatilityTrigger,
)

__all__ = [
    "BTCDropLevel3Trigger",
    "BTCDropLevel4Trigger",
    "ETHDropLevel3Trigger",
    "SOLDropLevel3Trigger",
    "SOLDropLevel4Trigger",
    "VIXSpikeLevel2Trigger",
    "VIXSpikeLevel3Trigger",
    "CryptoVolatilityTrigger",
]
