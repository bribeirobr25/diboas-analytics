"""
APY proxy calculations for protocols without historical data.

QR Board validated formulas for estimating yields.
"""

import pandas as pd
from datetime import date
from typing import Optional


def get_sanctum_apy(lido_apy: float) -> float:
    """
    Sanctum INF proxy: SOL staking is approximately 2x ETH staking + basket premium.

    Formula: Lido_ETH_APY * 2.0 + 0.5%

    Args:
        lido_apy: Lido stETH APY in percentage

    Returns:
        Estimated Sanctum INF APY in percentage
    """
    return lido_apy * 2.0 + 0.5


def get_jito_apy(lido_apy: float) -> float:
    """
    Jito proxy: SOL staking + MEV premium.

    Formula: Lido_ETH_APY * 2.0 + 1.0%

    Args:
        lido_apy: Lido stETH APY in percentage

    Returns:
        Estimated Jito APY in percentage
    """
    return lido_apy * 2.0 + 1.0


def get_jlp_apy(default: float = 25.0) -> float:
    """
    JLP proxy for periods before January 2024.

    Based on GMX GLP historical average performance.

    Args:
        default: Default APY to return (25% based on GMX GLP)

    Returns:
        Fixed JLP APY estimate in percentage
    """
    return default


def get_compound_apy(aave_apy: float) -> float:
    """
    Compound V3 proxy for periods before October 2022.

    Compound V3 typically yields ~10% higher than Aave.

    Formula: Aave_APY * 1.1

    Args:
        aave_apy: Aave V3 APY in percentage

    Returns:
        Estimated Compound V3 APY in percentage
    """
    return aave_apy * 1.1


def get_sky_apy(aave_apy: float) -> float:
    """
    Sky SSR proxy for periods before October 2022.

    Sky SSR typically yields ~10% lower than Aave.

    Formula: Aave_APY * 0.9

    Args:
        aave_apy: Aave V3 APY in percentage

    Returns:
        Estimated Sky SSR APY in percentage
    """
    return aave_apy * 0.9


class ProxyCalculator:
    """
    Calculate proxy APYs for protocols without historical data.

    Uses QR Board validated formulas based on available reference data.
    """

    # Date thresholds for when to apply proxies
    THRESHOLDS = {
        'sanctum': date(2025, 3, 1),  # No historical data
        'jito': date(2025, 3, 1),     # Before March 2025
        'jlp': date(2024, 1, 1),      # Before January 2024
        'compound': date(2022, 10, 1), # Before October 2022
        'sky': date(2022, 10, 1),      # Before October 2022
    }

    def __init__(self, lido_apy_series: pd.Series = None, aave_apy_series: pd.Series = None):
        """
        Initialize proxy calculator.

        Args:
            lido_apy_series: Series of Lido APYs indexed by date
            aave_apy_series: Series of Aave APYs indexed by date
        """
        self.lido_apy = lido_apy_series
        self.aave_apy = aave_apy_series

    def needs_proxy(self, protocol: str, current_date: date) -> bool:
        """Check if a protocol needs proxy calculation for a given date."""
        if protocol not in self.THRESHOLDS:
            return False
        return current_date < self.THRESHOLDS[protocol]

    def get_protocol_apy(
        self,
        protocol: str,
        current_date: date,
        actual_apy: Optional[float] = None
    ) -> float:
        """
        Get APY for a protocol, using proxy if needed.

        Args:
            protocol: Protocol identifier
            current_date: Date for which to get APY
            actual_apy: Actual APY if available

        Returns:
            APY in percentage
        """
        # If actual data is available and we don't need proxy, use it
        if actual_apy is not None and not self.needs_proxy(protocol, current_date):
            return actual_apy

        # Get reference APYs
        lido_apy = self._get_lido_apy(current_date)
        aave_apy = self._get_aave_apy(current_date)

        # Calculate proxy based on protocol
        if protocol == 'sanctum':
            return get_sanctum_apy(lido_apy)
        elif protocol == 'jito':
            return get_jito_apy(lido_apy)
        elif protocol == 'jlp':
            return get_jlp_apy()
        elif protocol == 'compound':
            if actual_apy is not None:
                return actual_apy
            return get_compound_apy(aave_apy)
        elif protocol == 'sky':
            if actual_apy is not None:
                return actual_apy
            return get_sky_apy(aave_apy)
        else:
            # Return actual APY or default
            return actual_apy if actual_apy is not None else 5.0

    def _get_lido_apy(self, current_date: date) -> float:
        """Get Lido APY for a given date."""
        if self.lido_apy is None or self.lido_apy.empty:
            return 4.0  # Default Lido APY

        try:
            # Convert date to datetime for pandas lookup
            dt = pd.Timestamp(current_date)
            if dt in self.lido_apy.index:
                return self.lido_apy.loc[dt]
            # Find nearest date
            nearest_idx = self.lido_apy.index.get_indexer([dt], method='nearest')[0]
            return self.lido_apy.iloc[nearest_idx]
        except Exception:
            return 4.0

    def _get_aave_apy(self, current_date: date) -> float:
        """Get Aave APY for a given date."""
        if self.aave_apy is None or self.aave_apy.empty:
            return 5.0  # Default Aave APY

        try:
            dt = pd.Timestamp(current_date)
            if dt in self.aave_apy.index:
                return self.aave_apy.loc[dt]
            nearest_idx = self.aave_apy.index.get_indexer([dt], method='nearest')[0]
            return self.aave_apy.iloc[nearest_idx]
        except Exception:
            return 5.0


def calculate_jlp_daily_return(
    sol_return: float,
    eth_return: float,
    btc_return: float,
    jlp_apy: float
) -> float:
    """
    Calculate JLP daily return.

    JLP return = weighted basket price change + daily fee income

    Basket weights: 45% SOL, 27% ETH, 27% BTC

    Args:
        sol_return: SOL daily return (decimal, e.g., 0.02 for 2%)
        eth_return: ETH daily return
        btc_return: BTC daily return
        jlp_apy: JLP APY in percentage

    Returns:
        Total daily return (decimal)
    """
    price_return = (
        0.45 * sol_return +
        0.27 * eth_return +
        0.27 * btc_return
    )
    fee_return = jlp_apy / 365 / 100  # Daily APY as decimal
    return price_return + fee_return
