"""
Simulation result models for diBoaS Analytics.

Represents outputs from Battle Test and Monte Carlo simulations.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import date, datetime
import numpy as np


@dataclass
class BattleTestResult:
    """
    Result from a single Battle Test run.

    Represents historical backtesting output for one strategy/scenario.
    """
    strategy_id: int
    strategy_name: str
    scenario: str
    period_start: date
    period_end: date
    days: int
    deposited: float
    final_value: float
    profit: float
    return_pct: float
    max_drawdown_pct: float

    # Optional detailed tracking
    daily_values: Optional[list[float]] = None
    monthly_deposits: Optional[list[float]] = None

    @property
    def is_profitable(self) -> bool:
        """Check if strategy was profitable."""
        return self.profit > 0

    @property
    def annualized_return(self) -> float:
        """Calculate annualized return."""
        years = self.days / 365
        if years <= 0:
            return 0.0
        return ((self.final_value / self.deposited) ** (1 / years) - 1) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'strategy_id': self.strategy_id,
            'strategy_name': self.strategy_name,
            'scenario': self.scenario,
            'period_start': str(self.period_start),
            'period_end': str(self.period_end),
            'days': self.days,
            'deposited': round(self.deposited, 2),
            'final_value': round(self.final_value, 2),
            'profit': round(self.profit, 2),
            'return_pct': round(self.return_pct, 2),
            'max_drawdown_pct': round(self.max_drawdown_pct, 2),
            'annualized_return': round(self.annualized_return, 2)
        }


@dataclass
class MonteCarloResult:
    """
    Result from Monte Carlo simulation.

    Contains distribution statistics and risk metrics.
    """
    strategy_id: int
    strategy_name: str
    simulations: int
    horizon_months: int
    total_deposited: float

    # Distribution metrics
    mean_final: float
    median_final: float
    std_final: float

    # Return metrics
    mean_return: float
    median_return: float

    # Risk metrics
    prob_any_loss: float
    prob_loss_10pct: float
    prob_loss_20pct: float
    prob_loss_50pct: float

    # Value at Risk
    var_95: float
    cvar_95: float
    var_99: float
    cvar_99: float

    # Percentiles
    p5_final: float
    p10_final: float = 0.0
    p25_final: float = 0.0
    p75_final: float = 0.0
    p90_final: float = 0.0
    p95_final: float = 0.0

    # Drawdown metrics
    mean_max_drawdown: float = 0.0
    p95_max_drawdown: float = 0.0

    # Raw distribution (optional)
    final_values: Optional[np.ndarray] = field(default=None, repr=False)

    @property
    def confidence_interval_90(self) -> tuple[float, float]:
        """Get 90% confidence interval for final value."""
        return (self.p5_final, self.p95_final)

    @property
    def sharpe_ratio(self) -> float:
        """Estimate Sharpe ratio (assuming 0% risk-free rate)."""
        if self.std_final <= 0:
            return 0.0
        # Annualize: assume 48 months = 4 years
        annual_return = self.mean_return / 4
        annual_vol = (self.std_final / self.total_deposited) * 100 / 2  # Rough annualization
        return annual_return / annual_vol if annual_vol > 0 else 0

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'strategy_id': self.strategy_id,
            'strategy_name': self.strategy_name,
            'simulations': self.simulations,
            'horizon_months': self.horizon_months,
            'total_deposited': round(self.total_deposited, 2),
            'mean_final': round(self.mean_final, 2),
            'median_final': round(self.median_final, 2),
            'std_final': round(self.std_final, 2),
            'mean_return': round(self.mean_return, 2),
            'median_return': round(self.median_return, 2),
            'prob_any_loss': round(self.prob_any_loss, 2),
            'prob_loss_10pct': round(self.prob_loss_10pct, 2),
            'prob_loss_20pct': round(self.prob_loss_20pct, 2),
            'prob_loss_50pct': round(self.prob_loss_50pct, 2),
            'var_95': round(self.var_95, 2),
            'cvar_95': round(self.cvar_95, 2),
            'var_99': round(self.var_99, 2),
            'cvar_99': round(self.cvar_99, 2),
            'p5_final': round(self.p5_final, 2),
            'p95_final': round(self.p95_final, 2),
            'mean_max_drawdown': round(self.mean_max_drawdown, 2),
            'p95_max_drawdown': round(self.p95_max_drawdown, 2),
            'sharpe_ratio': round(self.sharpe_ratio, 3)
        }


@dataclass
class SimulationMetadata:
    """
    Metadata about a simulation run.

    Used for audit trail and reproducibility.
    """
    run_id: str
    run_type: str  # 'battle_test' or 'monte_carlo'
    timestamp: datetime
    config_hash: str
    parameters: dict
    duration_seconds: float
    status: str  # 'success', 'failed', 'warning'
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'run_id': self.run_id,
            'run_type': self.run_type,
            'timestamp': self.timestamp.isoformat(),
            'config_hash': self.config_hash,
            'parameters': self.parameters,
            'duration_seconds': round(self.duration_seconds, 2),
            'status': self.status,
            'errors': self.errors,
            'warnings': self.warnings
        }
