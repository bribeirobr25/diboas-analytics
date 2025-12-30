"""
Protocol domain model for diBoaS Analytics.

Represents a DeFi protocol with its characteristics and metrics.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum


class ProtocolType(Enum):
    """Types of DeFi protocols."""
    STABLECOIN_YIELD = 'stablecoin_yield'
    LENDING = 'lending'
    LIQUID_STAKING = 'liquid_staking'
    LIQUID_STAKING_MEV = 'liquid_staking_mev'
    PERPS_LP = 'perps_lp'


class Chain(Enum):
    """Supported blockchain networks."""
    ARBITRUM = 'arbitrum'
    SOLANA = 'solana'
    ETHEREUM = 'ethereum'


@dataclass
class Protocol:
    """
    DeFi protocol definition.

    Represents a protocol that can be used in investment strategies.
    """
    id: str
    name: str
    chain: Chain
    asset: str
    protocol_type: ProtocolType
    crypto_exposure: bool
    defillama_project: Optional[str] = None
    price_exposure: Optional[str] = None  # e.g., 'SOL', 'ETH'
    basket_composition: Optional[dict[str, float]] = None
    enabled: bool = True
    notes: Optional[str] = None

    @property
    def is_stable(self) -> bool:
        """Check if protocol has no crypto price exposure."""
        return not self.crypto_exposure

    def get_gas_cost(self) -> float:
        """Get gas cost for this protocol's chain."""
        from config.settings import GAS_COSTS
        return GAS_COSTS.get(self.chain.value, 0.30)


@dataclass
class ProtocolMetrics:
    """
    Real-time metrics for a protocol.

    Used for monitoring and health checks.
    """
    protocol_id: str
    timestamp: datetime
    tvl_usd: float
    apy: float
    apy_base: Optional[float] = None
    apy_reward: Optional[float] = None
    utilization: Optional[float] = None
    volume_24h: Optional[float] = None

    @property
    def total_apy(self) -> float:
        """Get total APY (base + rewards)."""
        base = self.apy_base or 0
        reward = self.apy_reward or 0
        return base + reward if self.apy_base else self.apy


@dataclass
class ProtocolHistoricalData:
    """
    Historical data point for a protocol.

    Used in Battle Test calculations.
    """
    protocol_id: str
    date: datetime
    apy: float
    tvl_usd: Optional[float] = None

    def daily_return(self) -> float:
        """Convert APY to daily return."""
        return self.apy / 365 / 100


@dataclass
class PriceData:
    """
    Crypto price data point.

    Used for calculating returns on crypto-exposed protocols.
    """
    symbol: str  # BTC, ETH, SOL
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None

    def daily_return(self, previous_close: float) -> float:
        """Calculate daily return from previous close."""
        if previous_close <= 0:
            return 0.0
        return (self.close - previous_close) / previous_close
