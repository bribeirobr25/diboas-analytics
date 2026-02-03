"""
Battle Test Engine for historical backtesting.

Simulates DCA investing through historical market conditions.
"""

import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from typing import Optional
import logging

from src.domain.simulation import BattleTestResult, SimulationMetadata
from src.domain.strategy import Strategy, StrategyLoader
from src.collectors.file_loader import FileLoader, DataAggregator
from src.utils.proxies import ProxyCalculator, calculate_jlp_daily_return
from src.utils.hashing import hash_strategies, generate_run_id
from config.settings import BATTLE_TEST_START_DATE, BATTLE_TEST_END_DATE

logger = logging.getLogger(__name__)


# Test scenarios
SCENARIOS = {
    'A': {
        'name': 'Felipe (Sophisticated)',
        'initial_deposit': 10000,
        'monthly_dca': 200
    },
    'B': {
        'name': 'Ana (Minimum)',
        'initial_deposit': 5,
        'monthly_dca': 5
    },
    'C': {
        'name': 'Per-Strategy Minimum',
        'minimums': {
            1: {'initial': 50, 'monthly': 10},
            2: {'initial': 20, 'monthly': 5},
            3: {'initial': 50, 'monthly': 10},
            4: {'initial': 20, 'monthly': 5},
            5: {'initial': 50, 'monthly': 10},
            6: {'initial': 30, 'monthly': 5},
            7: {'initial': 50, 'monthly': 10},
            8: {'initial': 100, 'monthly': 20},
            9: {'initial': 50, 'monthly': 10},
            10: {'initial': 200, 'monthly': 40}
        }
    }
}


class BattleTestEngine:
    """
    Historical backtesting engine.

    Simulates DCA investing through historical market conditions
    from May 2022 to December 2025.
    """

    def __init__(
        self,
        strategies: list[Strategy] = None,
        file_loader: FileLoader = None
    ):
        """
        Initialize Battle Test engine.

        Args:
            strategies: List of strategies to test (loads default if None)
            file_loader: File loader for historical data
        """
        self.strategies = strategies or StrategyLoader.load_default()
        self.loader = file_loader or FileLoader()
        self.aggregator = DataAggregator(self.loader)

        # Load data
        self._load_data()

    def _load_data(self):
        """Load and prepare historical data."""
        logger.info("Loading historical data for Battle Test...")

        # Load APY data
        self.apy_data = self.loader.load('defillama')

        # Load price data
        self.price_data = self.loader.load('yahoo')

        # Load JLP data
        self.jlp_data = self.loader.load('jupiter')

        # Determine protocol column name (v3 uses 'protocol', legacy uses 'project')
        protocol_col = 'protocol' if 'protocol' in self.apy_data.columns else 'project'

        # Prepare Lido APY series for proxies (use jito as proxy for lido if not available)
        lido_df = self.apy_data[self.apy_data[protocol_col] == 'lido'].copy()
        if lido_df.empty:
            # Try jito as staking proxy
            lido_df = self.apy_data[self.apy_data[protocol_col] == 'jito'].copy()
        if not lido_df.empty:
            lido_df = lido_df.set_index('date')
            self.lido_apy_series = lido_df.groupby('date')['apy'].mean()
        else:
            self.lido_apy_series = pd.Series(dtype=float)

        # Prepare Aave APY series for proxies
        aave_df = self.apy_data[self.apy_data[protocol_col] == 'aave-v3'].copy()
        if not aave_df.empty:
            aave_df = aave_df.set_index('date')
            self.aave_apy_series = aave_df.groupby('date')['apy'].mean()
        else:
            self.aave_apy_series = pd.Series(dtype=float)

        # Initialize proxy calculator
        self.proxy_calc = ProxyCalculator(self.lido_apy_series, self.aave_apy_series)

        # Prepare price return series (handles both v3 wide format and legacy long format)
        self.price_returns = {}
        for symbol in ['BTC', 'ETH', 'SOL']:
            close_col = f'{symbol.lower()}_close'
            if close_col in self.price_data.columns:
                # V3 wide format (btc_close, eth_close, sol_close)
                price_df = self.price_data[['date', close_col]].copy()
                price_df = price_df.set_index('date').sort_index()
                self.price_returns[symbol] = price_df[close_col].pct_change().fillna(0)
            elif 'symbol' in self.price_data.columns:
                # Legacy long format
                symbol_df = self.price_data[self.price_data['symbol'] == symbol].copy()
                if not symbol_df.empty:
                    symbol_df = symbol_df.set_index('date').sort_index()
                    self.price_returns[symbol] = symbol_df['close'].pct_change().fillna(0)

        # Prepare JLP APY series
        if not self.jlp_data.empty:
            jlp_df = self.jlp_data.set_index('date')
            self.jlp_apy_series = jlp_df['apy']
        else:
            self.jlp_apy_series = pd.Series(dtype=float)

        logger.info(f"Loaded {len(self.apy_data)} APY records, {len(self.price_data)} price records")

    def run(
        self,
        strategy_id: int,
        initial_deposit: float,
        monthly_dca: float,
        start_date: date = None,
        end_date: date = None
    ) -> BattleTestResult:
        """
        Run battle test for a single strategy.

        Args:
            strategy_id: Strategy ID (1-10)
            initial_deposit: Initial deposit amount in USD
            monthly_dca: Monthly DCA amount in USD
            start_date: Start date (default: 2022-05-01)
            end_date: End date (default: 2025-12-31)

        Returns:
            BattleTestResult with simulation results
        """
        start_date = start_date or pd.to_datetime(BATTLE_TEST_START_DATE).date()
        end_date = end_date or pd.to_datetime(BATTLE_TEST_END_DATE).date()

        strategy = StrategyLoader.get_strategy_by_id(strategy_id, self.strategies)
        logger.info(f"Running Battle Test for {strategy.name} (ID: {strategy_id})")

        # Generate date range
        dates = pd.date_range(start_date, end_date, freq='D')

        # Initialize tracking
        portfolio_value = initial_deposit
        peak_value = initial_deposit
        max_drawdown = 0.0
        total_deposited = initial_deposit
        last_dca_month = start_date.month

        # Track daily values
        daily_values = [initial_deposit]

        # Daily simulation
        for i, current_date in enumerate(dates[1:], 1):
            current_dt = current_date.date() if hasattr(current_date, 'date') else current_date

            # Monthly DCA (on first day of each new month)
            if current_date.month != last_dca_month:
                portfolio_value += monthly_dca
                total_deposited += monthly_dca
                last_dca_month = current_date.month

            # Calculate daily return
            daily_return = self._calculate_daily_return(strategy, current_date)

            # Apply return
            portfolio_value *= (1 + daily_return)

            # Track drawdown
            if portfolio_value > peak_value:
                peak_value = portfolio_value

            if peak_value > 0:
                drawdown = (peak_value - portfolio_value) / peak_value
                max_drawdown = max(max_drawdown, drawdown)

            daily_values.append(portfolio_value)

        # Calculate final metrics
        profit = portfolio_value - total_deposited
        return_pct = (profit / total_deposited) * 100 if total_deposited > 0 else 0

        return BattleTestResult(
            strategy_id=strategy_id,
            strategy_name=strategy.name,
            scenario=f"${initial_deposit:,.0f} + ${monthly_dca}/mo",
            period_start=start_date,
            period_end=end_date,
            days=len(dates),
            deposited=total_deposited,
            final_value=portfolio_value,
            profit=profit,
            return_pct=return_pct,
            max_drawdown_pct=max_drawdown * 100,
            daily_values=daily_values
        )

    def _calculate_daily_return(
        self,
        strategy: Strategy,
        current_date: pd.Timestamp
    ) -> float:
        """
        Calculate weighted daily return based on strategy allocations.

        Args:
            strategy: Strategy to calculate return for
            current_date: Current simulation date

        Returns:
            Daily return as decimal (e.g., 0.001 for 0.1%)
        """
        total_return = 0.0
        current_dt = current_date.date() if hasattr(current_date, 'date') else current_date

        # Stable allocations (no price exposure)
        for protocol, weight in strategy.stable_allocations.items():
            apy = self._get_protocol_apy(protocol, current_date)
            daily_return = apy / 365 / 100
            total_return += weight * daily_return

        # Crypto allocations (with price exposure)
        for protocol, weight in strategy.crypto_allocations.items():
            if protocol == 'jlp':
                # JLP = basket return + fee APY
                daily_return = self._get_jlp_return(current_date)
            else:
                # Sanctum/Jito = SOL return + staking APY
                sol_return = self._get_price_return('SOL', current_date)
                staking_apy = self._get_protocol_apy(protocol, current_date)
                daily_return = sol_return + (staking_apy / 365 / 100)

            total_return += weight * daily_return

        return total_return

    def _get_protocol_apy(self, protocol: str, current_date: pd.Timestamp) -> float:
        """Get APY for protocol on given date, with proxy fallback."""
        current_dt = current_date.date() if hasattr(current_date, 'date') else current_date

        # Map protocol names to DeFiLlama project names
        project_map = {
            'sky': 'sky-lending',
            'aave': 'aave-v3',
            'compound': 'compound-v3',
            'lido': 'lido',
            'sanctum': None,  # Use proxy
            'jito': None,     # Use proxy
            'jlp': None       # Use JLP data
        }

        project_name = project_map.get(protocol)

        # Try to get actual APY
        actual_apy = None
        if project_name:
            try:
                if current_date in self.apy_data.set_index('date').index:
                    day_data = self.apy_data[
                        (self.apy_data['date'] == current_date) &
                        (self.apy_data['project'] == project_name)
                    ]
                    if not day_data.empty:
                        actual_apy = day_data['apy'].mean()
            except Exception:
                pass

        # Use proxy calculator for final APY
        return self.proxy_calc.get_protocol_apy(protocol, current_dt, actual_apy)

    def _get_price_return(self, symbol: str, current_date: pd.Timestamp) -> float:
        """Get daily price return for crypto asset."""
        if symbol not in self.price_returns:
            return 0.0

        try:
            if current_date in self.price_returns[symbol].index:
                return self.price_returns[symbol].loc[current_date]
        except Exception:
            pass

        return 0.0

    def _get_jlp_return(self, current_date: pd.Timestamp) -> float:
        """Get JLP daily return (basket + fees)."""
        sol_return = self._get_price_return('SOL', current_date)
        eth_return = self._get_price_return('ETH', current_date)
        btc_return = self._get_price_return('BTC', current_date)

        # Get JLP APY
        current_dt = current_date.date() if hasattr(current_date, 'date') else current_date
        try:
            if current_date in self.jlp_apy_series.index:
                jlp_apy = self.jlp_apy_series.loc[current_date]
            else:
                # Use proxy (25% default)
                jlp_apy = self.proxy_calc.get_protocol_apy('jlp', current_dt)
        except Exception:
            jlp_apy = 25.0  # Default

        return calculate_jlp_daily_return(sol_return, eth_return, btc_return, jlp_apy)

    def run_all_strategies(
        self,
        scenario: str = 'A',
        start_date: date = None,
        end_date: date = None
    ) -> list[BattleTestResult]:
        """
        Run battle test for all strategies.

        Args:
            scenario: Scenario ID ('A', 'B', or 'C')
            start_date: Start date
            end_date: End date

        Returns:
            List of BattleTestResult for all strategies
        """
        results = []
        scenario_config = SCENARIOS[scenario]

        for strategy in self.strategies:
            if scenario == 'C':
                # Per-strategy minimums
                minimums = scenario_config['minimums'][strategy.id]
                initial = minimums['initial']
                monthly = minimums['monthly']
            else:
                initial = scenario_config['initial_deposit']
                monthly = scenario_config['monthly_dca']

            result = self.run(
                strategy_id=strategy.id,
                initial_deposit=initial,
                monthly_dca=monthly,
                start_date=start_date,
                end_date=end_date
            )
            results.append(result)

            logger.info(
                f"  {strategy.name}: {result.return_pct:.1f}% return, "
                f"{result.max_drawdown_pct:.1f}% max drawdown"
            )

        return results

    def run_all_scenarios(
        self,
        start_date: date = None,
        end_date: date = None
    ) -> dict[str, list[BattleTestResult]]:
        """
        Run all scenarios for all strategies.

        Returns:
            Dictionary mapping scenario ID to list of results
        """
        all_results = {}

        for scenario_id in SCENARIOS.keys():
            logger.info(f"Running Scenario {scenario_id}: {SCENARIOS[scenario_id]['name']}")
            results = self.run_all_strategies(scenario_id, start_date, end_date)
            all_results[scenario_id] = results

        return all_results


def run_battle_test(
    strategy_id: Optional[int] = None,
    scenario: str = 'A',
    start_date: date = None,
    end_date: date = None
) -> tuple[list[BattleTestResult], SimulationMetadata]:
    """
    Convenience function to run battle test.

    Args:
        strategy_id: Specific strategy ID or None for all
        scenario: Scenario ID
        start_date: Start date
        end_date: End date

    Returns:
        Tuple of (results, metadata)
    """
    import time
    start_time = time.time()

    engine = BattleTestEngine()

    if strategy_id:
        scenario_config = SCENARIOS[scenario]
        if scenario == 'C':
            minimums = scenario_config['minimums'][strategy_id]
            initial = minimums['initial']
            monthly = minimums['monthly']
        else:
            initial = scenario_config['initial_deposit']
            monthly = scenario_config['monthly_dca']

        results = [engine.run(
            strategy_id=strategy_id,
            initial_deposit=initial,
            monthly_dca=monthly,
            start_date=start_date,
            end_date=end_date
        )]
    else:
        results = engine.run_all_strategies(scenario, start_date, end_date)

    duration = time.time() - start_time

    metadata = SimulationMetadata(
        run_id=generate_run_id('bt'),
        run_type='battle_test',
        timestamp=datetime.utcnow(),
        config_hash=hash_strategies([s.__dict__ for s in engine.strategies]),
        parameters={
            'scenario': scenario,
            'strategy_id': strategy_id,
            'start_date': str(start_date),
            'end_date': str(end_date)
        },
        duration_seconds=duration,
        status='success'
    )

    return results, metadata
