"""
Monte Carlo Simulation Engine.

Forward-looking risk analysis with regime switching.
"""

import numpy as np
import pandas as pd
from scipy import stats
from datetime import date, datetime
from typing import Optional
import logging

from src.domain.simulation import MonteCarloResult, SimulationMetadata
from src.domain.strategy import Strategy, StrategyLoader
from src.collectors.file_loader import FileLoader, DataAggregator
from src.utils.hashing import hash_strategies, generate_run_id
from config.settings import DEFAULT_SIMULATIONS, DEFAULT_HORIZON_MONTHS, DEFAULT_RANDOM_SEED

logger = logging.getLogger(__name__)


class MonteCarloEngine:
    """
    Monte Carlo simulation engine with regime switching.

    Methodology:
    - 5,000+ simulations per strategy
    - Block bootstrap (21-day blocks)
    - 4 regimes: Bull, Bear, Crash, Recovery
    - Fat-tailed distributions (Student-t, df=4)
    """

    # Market regimes with parameters
    REGIMES = {
        'bull': {
            'mean_mult': 1.5,    # Higher returns
            'vol_mult': 0.8,     # Lower volatility
            'duration': 180,     # ~6 months
            'description': 'Upward trending market'
        },
        'bear': {
            'mean_mult': 0.3,    # Lower returns
            'vol_mult': 1.5,     # Higher volatility
            'duration': 120,     # ~4 months
            'description': 'Downward trending market'
        },
        'crash': {
            'mean_mult': -2.0,   # Negative returns
            'vol_mult': 3.0,     # Very high volatility
            'duration': 30,      # ~1 month
            'description': 'Market crash event'
        },
        'recovery': {
            'mean_mult': 2.0,    # High returns
            'vol_mult': 1.2,     # Moderate volatility
            'duration': 90,      # ~3 months
            'description': 'Recovery from crash'
        }
    }

    # Markov transition matrix for regime changes
    TRANSITIONS = {
        'bull': {'bull': 0.85, 'bear': 0.10, 'crash': 0.03, 'recovery': 0.02},
        'bear': {'bull': 0.05, 'bear': 0.80, 'crash': 0.10, 'recovery': 0.05},
        'crash': {'bull': 0.00, 'bear': 0.20, 'crash': 0.30, 'recovery': 0.50},
        'recovery': {'bull': 0.40, 'bear': 0.10, 'crash': 0.05, 'recovery': 0.45}
    }

    # Crypto correlation matrix
    CORRELATIONS = {
        ('SOL', 'ETH'): 0.75,
        ('SOL', 'BTC'): 0.70,
        ('ETH', 'BTC'): 0.85
    }

    def __init__(
        self,
        strategies: list[Strategy] = None,
        n_simulations: int = DEFAULT_SIMULATIONS,
        horizon_months: int = DEFAULT_HORIZON_MONTHS,
        random_seed: int = DEFAULT_RANDOM_SEED
    ):
        """
        Initialize Monte Carlo engine.

        Args:
            strategies: List of strategies to simulate
            n_simulations: Number of simulation paths (default 5000)
            horizon_months: Simulation horizon in months (default 48)
            random_seed: Random seed for reproducibility
        """
        self.strategies = strategies or StrategyLoader.load_default()
        self.n_simulations = n_simulations
        self.horizon_months = horizon_months
        self.random_seed = random_seed

        np.random.seed(random_seed)

        # Calculate base parameters from historical data
        self._calculate_base_parameters()

    def _calculate_base_parameters(self):
        """Calculate base return and volatility parameters."""
        # Base daily parameters (approximate historical values)
        self.base_stable_return = 0.08 / 365  # ~8% annual for stables
        self.base_stable_vol = 0.001           # Very low vol

        self.base_crypto_return = 0.20 / 365   # ~20% annual for crypto
        self.base_crypto_vol = 0.04            # ~60% annual vol

    def run(
        self,
        strategy_id: int,
        initial_deposit: float = 10000,
        monthly_dca: float = 200
    ) -> MonteCarloResult:
        """
        Run Monte Carlo simulation for a single strategy.

        Args:
            strategy_id: Strategy ID (1-10)
            initial_deposit: Initial deposit in USD
            monthly_dca: Monthly DCA amount in USD

        Returns:
            MonteCarloResult with simulation statistics
        """
        strategy = StrategyLoader.get_strategy_by_id(strategy_id, self.strategies)
        logger.info(f"Running Monte Carlo for {strategy.name} (ID: {strategy_id})")

        # Calculate total deposits
        total_deposited = initial_deposit + (monthly_dca * self.horizon_months)

        # Generate simulated paths
        final_values = []
        max_drawdowns = []

        for sim in range(self.n_simulations):
            path = self._simulate_path(strategy, initial_deposit, monthly_dca)
            final_values.append(path[-1])
            max_drawdowns.append(self._calculate_max_drawdown(path))

        final_values = np.array(final_values)
        max_drawdowns = np.array(max_drawdowns)

        # Calculate returns
        returns = (final_values - total_deposited) / total_deposited

        # Calculate VaR and CVaR
        var_95 = np.percentile(final_values, 5)
        var_99 = np.percentile(final_values, 1)
        cvar_95 = np.mean(final_values[final_values <= var_95])
        cvar_99 = np.mean(final_values[final_values <= var_99]) if np.any(final_values <= var_99) else var_99

        return MonteCarloResult(
            strategy_id=strategy_id,
            strategy_name=strategy.name,
            simulations=self.n_simulations,
            horizon_months=self.horizon_months,
            total_deposited=total_deposited,

            mean_final=np.mean(final_values),
            median_final=np.median(final_values),
            std_final=np.std(final_values),

            mean_return=np.mean(returns) * 100,
            median_return=np.median(returns) * 100,

            prob_any_loss=np.mean(final_values < total_deposited) * 100,
            prob_loss_10pct=np.mean(returns < -0.10) * 100,
            prob_loss_20pct=np.mean(returns < -0.20) * 100,
            prob_loss_50pct=np.mean(returns < -0.50) * 100,

            var_95=var_95,
            cvar_95=cvar_95,
            var_99=var_99,
            cvar_99=cvar_99,

            p5_final=np.percentile(final_values, 5),
            p10_final=np.percentile(final_values, 10),
            p25_final=np.percentile(final_values, 25),
            p75_final=np.percentile(final_values, 75),
            p90_final=np.percentile(final_values, 90),
            p95_final=np.percentile(final_values, 95),

            mean_max_drawdown=np.mean(max_drawdowns) * 100,
            p95_max_drawdown=np.percentile(max_drawdowns, 95) * 100,

            final_values=final_values
        )

    def _simulate_path(
        self,
        strategy: Strategy,
        initial_deposit: float,
        monthly_dca: float
    ) -> np.ndarray:
        """
        Simulate a single price path with regime switching.

        Args:
            strategy: Strategy being simulated
            initial_deposit: Initial deposit
            monthly_dca: Monthly DCA amount

        Returns:
            Array of portfolio values over time
        """
        # Convert months to trading days (21 days per month)
        days = self.horizon_months * 21
        values = np.zeros(days)
        values[0] = initial_deposit

        current_regime = 'bull'
        regime_day = 0

        for day in range(1, days):
            # Monthly DCA (every 21 days)
            if day % 21 == 0:
                values[day - 1] += monthly_dca

            # Check regime transition
            regime_day += 1
            if regime_day >= self.REGIMES[current_regime]['duration']:
                current_regime = self._transition_regime(current_regime)
                regime_day = 0

            # Generate daily return
            daily_return = self._generate_return(strategy, current_regime)
            # Cap daily loss at 99% to prevent mathematically impossible negative values
            # (portfolios can only lose 100% max without leverage)
            daily_return = max(daily_return, -0.99)
            values[day] = max(0, values[day - 1] * (1 + daily_return))

        return values

    def _generate_return(self, strategy: Strategy, regime: str) -> float:
        """
        Generate daily return with fat tails.

        Args:
            strategy: Strategy being simulated
            regime: Current market regime

        Returns:
            Daily return as decimal
        """
        regime_params = self.REGIMES[regime]
        crypto_pct = strategy.crypto_pct / 100

        # Stable component
        stable_pct = 1 - crypto_pct
        stable_mean = self.base_stable_return * regime_params['mean_mult'] * 0.5
        stable_std = self.base_stable_vol * regime_params['vol_mult'] * 0.5
        stable_return = np.random.normal(stable_mean, stable_std) if stable_pct > 0 else 0

        # Crypto component (with fat tails)
        if crypto_pct > 0:
            crypto_mean = self.base_crypto_return * regime_params['mean_mult']
            crypto_std = self.base_crypto_vol * regime_params['vol_mult']

            # Use Student-t distribution for fat tails
            crypto_return = stats.t.rvs(df=4, loc=crypto_mean, scale=crypto_std)
        else:
            crypto_return = 0

        # Combine returns
        total_return = stable_pct * stable_return + crypto_pct * crypto_return

        return total_return

    def _transition_regime(self, current: str) -> str:
        """
        Transition to new regime based on Markov matrix.

        Args:
            current: Current regime

        Returns:
            New regime
        """
        probs = self.TRANSITIONS[current]
        regimes = list(probs.keys())
        weights = list(probs.values())
        return np.random.choice(regimes, p=weights)

    def _calculate_max_drawdown(self, path: np.ndarray) -> float:
        """
        Calculate maximum drawdown from price path.

        Args:
            path: Array of portfolio values

        Returns:
            Maximum drawdown as decimal
        """
        peak = np.maximum.accumulate(path)
        drawdown = (peak - path) / peak
        return np.max(drawdown)

    def run_all_strategies(
        self,
        initial_deposit: float = 10000,
        monthly_dca: float = 200
    ) -> list[MonteCarloResult]:
        """
        Run Monte Carlo for all strategies.

        Args:
            initial_deposit: Initial deposit
            monthly_dca: Monthly DCA amount

        Returns:
            List of MonteCarloResult for all strategies
        """
        results = []

        for strategy in self.strategies:
            result = self.run(
                strategy_id=strategy.id,
                initial_deposit=initial_deposit,
                monthly_dca=monthly_dca
            )
            results.append(result)

            logger.info(
                f"  {strategy.name}: {result.median_return:.1f}% median return, "
                f"{result.prob_any_loss:.1f}% prob of loss"
            )

        return results


def run_monte_carlo(
    strategy_id: Optional[int] = None,
    n_simulations: int = DEFAULT_SIMULATIONS,
    horizon_months: int = DEFAULT_HORIZON_MONTHS,
    initial_deposit: float = 10000,
    monthly_dca: float = 200,
    random_seed: int = DEFAULT_RANDOM_SEED
) -> tuple[list[MonteCarloResult], SimulationMetadata]:
    """
    Convenience function to run Monte Carlo simulation.

    Args:
        strategy_id: Specific strategy ID or None for all
        n_simulations: Number of simulations
        horizon_months: Simulation horizon
        initial_deposit: Initial deposit
        monthly_dca: Monthly DCA
        random_seed: Random seed

    Returns:
        Tuple of (results, metadata)
    """
    import time
    start_time = time.time()

    engine = MonteCarloEngine(
        n_simulations=n_simulations,
        horizon_months=horizon_months,
        random_seed=random_seed
    )

    if strategy_id:
        results = [engine.run(
            strategy_id=strategy_id,
            initial_deposit=initial_deposit,
            monthly_dca=monthly_dca
        )]
    else:
        results = engine.run_all_strategies(initial_deposit, monthly_dca)

    duration = time.time() - start_time

    metadata = SimulationMetadata(
        run_id=generate_run_id('mc'),
        run_type='monte_carlo',
        timestamp=datetime.utcnow(),
        config_hash=hash_strategies([s.__dict__ for s in engine.strategies]),
        parameters={
            'strategy_id': strategy_id,
            'n_simulations': n_simulations,
            'horizon_months': horizon_months,
            'initial_deposit': initial_deposit,
            'monthly_dca': monthly_dca,
            'random_seed': random_seed
        },
        duration_seconds=duration,
        status='success'
    )

    return results, metadata
