"""
Wallet monitoring triggers.

Monitor large wallet movements that may impact markets:
- Estate wallets (Mt. Gox, FTX, government seizures)
- Whale wallets (large holders with market-moving potential)
"""

from src.triggers.wallet.estate_wallet_triggers import (
    EstateMovementInfoTrigger,
    EstateMovementLevel2Trigger,
    EstateMovementLevel3Trigger,
)
from src.triggers.wallet.whale_wallet_triggers import (
    WhaleMovementLevel2Trigger,
    WhaleAccumulationTrigger,
    WhaleDistributionTrigger,
)

__all__ = [
    "EstateMovementInfoTrigger",
    "EstateMovementLevel2Trigger",
    "EstateMovementLevel3Trigger",
    "WhaleMovementLevel2Trigger",
    "WhaleAccumulationTrigger",
    "WhaleDistributionTrigger",
]
