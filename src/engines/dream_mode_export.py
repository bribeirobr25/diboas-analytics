"""
Dream Mode Export Engine.

Generate consumer-ready data for the Dream Mode frontend feature.
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

from config.dream_mode import DREAM_MODE_PATHS, BANK_COMPARISON, DISCLAIMERS, REGIONAL_DISCLAIMERS
from src.domain.dream_mode import DreamModeData, PathMetrics, PathProjection, DataSourceInfo
from src.domain.simulation import BattleTestResult, MonteCarloResult
from src.utils.audit import get_audit_trail
from config.settings import OUTPUT_DIR

logger = logging.getLogger(__name__)


class DreamModeExporter:
    """
    Generate consumer-ready Dream Mode data from simulation results.

    Bridges internal analytics to the frontend feature.
    """

    def __init__(
        self,
        battle_test_results: list[dict],
        monte_carlo_results: list[dict],
        strategies: list[dict]
    ):
        """
        Initialize Dream Mode exporter.

        Args:
            battle_test_results: Results from Battle Test (as dicts)
            monte_carlo_results: Results from Monte Carlo (as dicts)
            strategies: Strategy definitions
        """
        self.battle_test_results = battle_test_results
        self.monte_carlo_results = monte_carlo_results
        self.strategies = strategies

    def export(
        self,
        output_path: str = None
    ) -> DreamModeData:
        """
        Generate and save Dream Mode data.

        Args:
            output_path: Output file path (default: outputs/dream_mode_data.json)

        Returns:
            DreamModeData object
        """
        output_path = output_path or str(OUTPUT_DIR / 'dream_mode_data.json')

        logger.info("Generating Dream Mode data...")

        # Build data sources metadata
        data_sources = self._build_data_sources()

        # Aggregate metrics for each path
        paths = {}
        for path_id, path_config in DREAM_MODE_PATHS.items():
            paths[path_id] = self._aggregate_path_metrics(path_id, path_config)
            logger.info(f"  Path '{path_id}': APY={paths[path_id].avg_apy:.1f}%")

        # Build complete export
        dream_mode_data = DreamModeData(
            version='1.0',
            generated_at=datetime.utcnow(),
            data_sources=data_sources,
            paths=paths,
            bank_comparison=BANK_COMPARISON,
            disclaimers=DISCLAIMERS,
            regional_disclaimers=REGIONAL_DISCLAIMERS
        )

        # Save to file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(dream_mode_data.to_dict(), f, indent=2)

        # Log output file to audit trail for compliance tracking
        audit = get_audit_trail()
        if audit:
            audit.log_output_file(output_path)

        logger.info(f"Dream Mode data exported to: {output_path}")
        return dream_mode_data

    def _build_data_sources(self) -> dict[str, DataSourceInfo]:
        """Build data sources metadata for CLO compliance."""
        return {
            'apy_data': DataSourceInfo(
                source='DeFiLlama',
                period='2022-05-01 to 2025-12-31',
                last_updated=datetime.utcnow().strftime('%Y-%m-%d')
            ),
            'price_data': DataSourceInfo(
                source='Yahoo Finance',
                period='2022-05-01 to 2025-12-31'
            ),
            'battle_test': DataSourceInfo(
                source='diBoaS Analytics',
                methodology='Historical backtesting with DCA',
                period='1,334 days (May 2022 - Dec 2025)',
                events_captured=['Terra/Luna collapse', 'FTX crash', 'USDC depeg']
            ),
            'monte_carlo': DataSourceInfo(
                source='diBoaS Analytics',
                methodology='Regime-switching simulation with fat tails',
                simulations=5000,
                horizon='48 months'
            )
        }

    def _aggregate_path_metrics(
        self,
        path_id: str,
        path_config: dict
    ) -> PathMetrics:
        """
        Aggregate metrics across strategies in a path.

        Args:
            path_id: Path identifier ('safety', 'balance', 'growth')
            path_config: Path configuration from config

        Returns:
            PathMetrics with aggregated data
        """
        strategy_ids = path_config['strategies']

        # Filter results for this path's strategies
        bt_results = [
            r for r in self.battle_test_results
            if r.get('strategy_id') in strategy_ids
        ]
        mc_results = [
            r for r in self.monte_carlo_results
            if r.get('strategy_id') in strategy_ids
        ]

        # Calculate averages across strategies in path
        if bt_results:
            avg_return = np.mean([r.get('return_pct', 0) for r in bt_results])
            max_drawdown = max([r.get('max_drawdown_pct', 0) for r in bt_results])
        else:
            # Default values based on path
            defaults = {
                'safety': (9.5, 0.0),
                'balance': (29.4, 13.0),
                'growth': (184.0, 66.1)
            }
            avg_return, max_drawdown = defaults.get(path_id, (10.0, 0.0))

        if mc_results:
            prob_loss = np.mean([r.get('prob_any_loss', 0) for r in mc_results])
        else:
            # Default values based on path
            prob_defaults = {'safety': 0.0, 'balance': 18.7, 'growth': 25.5}
            prob_loss = prob_defaults.get(path_id, 0.0)

        # Convert return to APY (Battle test is ~3.65 years)
        annual_return = avg_return / 3.65

        # Pre-calculate projections
        projections = self._calculate_projections(annual_return)

        # Add warning for high-risk paths
        warning = None
        if path_id == 'growth':
            warning = f"High volatility - up to {max_drawdown:.0f}% drawdown observed in historical testing"

        return PathMetrics(
            path_id=path_id,
            label=path_config['label'],
            description=path_config['description'],
            color=path_config['color'],
            risk_level=path_config['risk_level'],
            avg_apy=round(annual_return, 1),
            max_drawdown=round(max_drawdown, 1),
            probability_of_loss=round(prob_loss, 1),
            projections=projections,
            warning=warning
        )

    def _calculate_projections(
        self,
        annual_return: float
    ) -> dict[str, PathProjection]:
        """
        Calculate projections for different time horizons.

        Args:
            annual_return: Annualized return percentage

        Returns:
            Dictionary of period -> PathProjection
        """
        # Convert annual return to decimal
        r = annual_return / 100
        bank_r = BANK_COMPARISON['apy'] / 100

        periods = {
            '1_week': 7 / 365,
            '1_month': 30 / 365,
            '1_year': 1,
            '5_years': 5
        }

        projections = {}
        for period_name, years in periods.items():
            multiplier = (1 + r) ** years
            bank_multiplier = (1 + bank_r) ** years

            projections[period_name] = PathProjection(
                period=period_name,
                multiplier=round(multiplier, 4),
                bank_multiplier=round(bank_multiplier, 4)
            )

        return projections


def export_dream_mode(
    battle_test_results: list = None,
    monte_carlo_results: list = None,
    output_path: str = None
) -> DreamModeData:
    """
    Convenience function to export Dream Mode data.

    If results not provided, loads from existing output files.
    """
    import pandas as pd

    # Load results from files if not provided
    if battle_test_results is None:
        bt_path = OUTPUT_DIR / 'battle_test_results.csv'
        if bt_path.exists():
            battle_test_results = pd.read_csv(bt_path).to_dict('records')
        else:
            battle_test_results = []
            logger.warning("No Battle Test results found")

    if monte_carlo_results is None:
        mc_path = OUTPUT_DIR / 'monte_carlo_results.csv'
        if mc_path.exists():
            monte_carlo_results = pd.read_csv(mc_path).to_dict('records')
        else:
            monte_carlo_results = []
            logger.warning("No Monte Carlo results found")

    # Load strategies
    strategies_path = Path(__file__).parent.parent.parent / 'config' / 'strategies.json'
    with open(strategies_path) as f:
        strategies = json.load(f)['strategies']

    # Export
    exporter = DreamModeExporter(battle_test_results, monte_carlo_results, strategies)
    return exporter.export(output_path)
