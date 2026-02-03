"""
Protocol health triggers.

Monitor DeFi protocol metrics for TVL drops, depegs, APY changes,
and utilization spikes.

Protocols:
- Sky (USDS): Stablecoin depeg, TVL monitoring
- Sanctum (LST): APY changes, LST health
- JLP: Utilization rates, pool health
- Aave/Compound: Lending protocol health
- USDC/USDT: Stablecoin depeg monitoring (affects Aave/Compound strategies)
"""

from src.triggers.protocol.sky_protocol_triggers import (
    SkyUSDSDepegLevel2Trigger,
    SkyUSDSDepegLevel3Trigger,
    SkyUSDSDepegLevel4Trigger,
    SkyTVLDropLevel2Trigger,
    SkyTVLDropLevel3Trigger,
)
from src.triggers.protocol.sanctum_protocol_triggers import (
    SanctumAPYDropLevel2Trigger,
    SanctumLSTHealthTrigger,
)
from src.triggers.protocol.jlp_protocol_triggers import (
    JLPUtilizationLevel2Trigger,
    JLPUtilizationLevel3Trigger,
)
from src.triggers.protocol.aave_protocol_triggers import (
    AaveUtilizationLevel2Trigger,
    AaveLiquidationRiskTrigger,
)
from src.triggers.protocol.stablecoin_depeg_triggers import (
    USDCDepegLevel2Trigger,
    USDCDepegLevel3Trigger,
    USDCDepegLevel4Trigger,
    USDTDepegLevel2Trigger,
    USDTDepegLevel3Trigger,
    USDTDepegLevel4Trigger,
)

__all__ = [
    "SkyUSDSDepegLevel2Trigger",
    "SkyUSDSDepegLevel3Trigger",
    "SkyUSDSDepegLevel4Trigger",
    "SkyTVLDropLevel2Trigger",
    "SkyTVLDropLevel3Trigger",
    "SanctumAPYDropLevel2Trigger",
    "SanctumLSTHealthTrigger",
    "JLPUtilizationLevel2Trigger",
    "JLPUtilizationLevel3Trigger",
    "AaveUtilizationLevel2Trigger",
    "AaveLiquidationRiskTrigger",
    # Stablecoin depeg triggers (P0-5b)
    "USDCDepegLevel2Trigger",
    "USDCDepegLevel3Trigger",
    "USDCDepegLevel4Trigger",
    "USDTDepegLevel2Trigger",
    "USDTDepegLevel3Trigger",
    "USDTDepegLevel4Trigger",
]
