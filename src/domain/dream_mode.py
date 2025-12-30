"""
Dream Mode domain models for diBoaS Analytics.

Represents the consumer-facing data structures for Dream Mode feature.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


@dataclass
class PathProjection:
    """Projection for a specific time period."""
    period: str  # '1_week', '1_month', '1_year', '5_years'
    multiplier: float  # e.g., 1.095 for +9.5%
    bank_multiplier: float  # e.g., 1.005 for +0.5%

    def projected_value(self, initial_amount: float) -> float:
        """Calculate projected value for an initial amount."""
        return initial_amount * self.multiplier

    def bank_value(self, initial_amount: float) -> float:
        """Calculate what a bank would give for the same amount."""
        return initial_amount * self.bank_multiplier

    def advantage_over_bank(self, initial_amount: float) -> float:
        """Calculate the advantage over traditional bank savings."""
        return self.projected_value(initial_amount) - self.bank_value(initial_amount)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'period': self.period,
            'multiplier': round(self.multiplier, 4),
            'bank_multiplier': round(self.bank_multiplier, 4)
        }


@dataclass
class PathMetrics:
    """Aggregated metrics for a Dream Mode path."""
    path_id: str  # 'safety', 'balance', 'growth'
    label: str
    description: str
    color: str
    risk_level: str

    # Aggregated from underlying strategies
    avg_apy: float
    max_drawdown: float
    probability_of_loss: float

    # Pre-calculated projections
    projections: dict[str, PathProjection] = field(default_factory=dict)

    # Warning for high-risk paths
    warning: Optional[str] = None

    def get_projection(self, period: str) -> PathProjection:
        """Get projection for a specific period."""
        if period not in self.projections:
            raise ValueError(f"Unknown period: {period}")
        return self.projections[period]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'path_id': self.path_id,
            'label': self.label,
            'description': self.description,
            'color': self.color,
            'risk_level': self.risk_level,
            'avg_apy': round(self.avg_apy, 1),
            'max_drawdown': round(self.max_drawdown, 1),
            'probability_of_loss': round(self.probability_of_loss, 1),
            'projections': {k: v.to_dict() for k, v in self.projections.items()},
            'warning': self.warning
        }


@dataclass
class DataSourceInfo:
    """Information about a data source for compliance."""
    source: str
    period: Optional[str] = None
    last_updated: Optional[str] = None
    methodology: Optional[str] = None
    simulations: Optional[int] = None
    horizon: Optional[str] = None
    events_captured: Optional[list[str]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values."""
        result = {'source': self.source}
        if self.period:
            result['period'] = self.period
        if self.last_updated:
            result['last_updated'] = self.last_updated
        if self.methodology:
            result['methodology'] = self.methodology
        if self.simulations:
            result['simulations'] = self.simulations
        if self.horizon:
            result['horizon'] = self.horizon
        if self.events_captured:
            result['events_captured'] = self.events_captured
        return result


@dataclass
class DreamModeData:
    """Complete export for Dream Mode frontend."""
    version: str
    generated_at: datetime

    # Data sources for CLO compliance
    data_sources: dict[str, DataSourceInfo]

    # The 3 paths
    paths: dict[str, PathMetrics]

    # Bank comparison
    bank_comparison: dict

    # CLO-mandated disclaimers
    disclaimers: dict
    regional_disclaimers: dict

    def get_path(self, path_id: str) -> PathMetrics:
        """Get a specific path by ID."""
        if path_id not in self.paths:
            raise ValueError(f"Unknown path: {path_id}")
        return self.paths[path_id]

    def calculate_projection(
        self,
        path_id: str,
        amount: float,
        period: str
    ) -> dict:
        """Calculate projection for a specific amount and period."""
        path = self.get_path(path_id)
        projection = path.get_projection(period)

        return {
            'path': path.label,
            'initial_amount': amount,
            'period': period,
            'projected_value': round(projection.projected_value(amount), 2),
            'bank_value': round(projection.bank_value(amount), 2),
            'advantage': round(projection.advantage_over_bank(amount), 2),
            'return_pct': round((projection.multiplier - 1) * 100, 2),
            'bank_return_pct': round((projection.bank_multiplier - 1) * 100, 2)
        }

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            'version': self.version,
            'generated_at': self.generated_at.isoformat(),
            'data_sources': {k: v.to_dict() for k, v in self.data_sources.items()},
            'paths': {k: v.to_dict() for k, v in self.paths.items()},
            'bank_comparison': self.bank_comparison,
            'disclaimers': self.disclaimers,
            'regional_disclaimers': self.regional_disclaimers
        }
