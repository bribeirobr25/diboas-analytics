"""
CSV Reporter for exporting results.
"""

import csv
from pathlib import Path
from typing import Union
import pandas as pd
import logging

from src.domain.simulation import BattleTestResult, MonteCarloResult
from src.utils.file_io import safe_write_csv
from src.utils.audit import get_audit_trail
from config.settings import OUTPUT_DIR

logger = logging.getLogger(__name__)


class CSVReporter:
    """Export results to CSV format."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or OUTPUT_DIR

    def export_battle_test(
        self,
        results: list[BattleTestResult],
        filename: str = 'battle_test_results.csv'
    ) -> Path:
        """
        Export Battle Test results to CSV.

        Args:
            results: List of BattleTestResult
            filename: Output filename

        Returns:
            Path to output file
        """
        output_path = self.output_dir / filename

        rows = []
        for r in results:
            rows.append({
                'strategy_id': r.strategy_id,
                'strategy_name': r.strategy_name,
                'scenario': r.scenario,
                'period_start': str(r.period_start),
                'period_end': str(r.period_end),
                'days': r.days,
                'deposited': round(r.deposited, 2),
                'final_value': round(r.final_value, 2),
                'profit': round(r.profit, 2),
                'return_pct': round(r.return_pct, 2),
                'max_drawdown_pct': round(r.max_drawdown_pct, 2),
                'annualized_return': round(r.annualized_return, 2)
            })

        df = pd.DataFrame(rows)
        safe_write_csv(df, output_path)

        # Log output file to audit trail
        audit = get_audit_trail()
        if audit:
            audit.log_output_file(output_path)

        logger.info(f"Battle Test results exported to {output_path}")
        return output_path

    def export_monte_carlo(
        self,
        results: list[MonteCarloResult],
        filename: str = 'monte_carlo_results.csv'
    ) -> Path:
        """
        Export Monte Carlo results to CSV.

        Args:
            results: List of MonteCarloResult
            filename: Output filename

        Returns:
            Path to output file
        """
        output_path = self.output_dir / filename

        rows = []
        for r in results:
            rows.append({
                'strategy_id': r.strategy_id,
                'strategy_name': r.strategy_name,
                'simulations': r.simulations,
                'horizon_months': r.horizon_months,
                'total_deposited': round(r.total_deposited, 2),
                'mean_final': round(r.mean_final, 2),
                'median_final': round(r.median_final, 2),
                'std_final': round(r.std_final, 2),
                'mean_return': round(r.mean_return, 2),
                'median_return': round(r.median_return, 2),
                'prob_any_loss': round(r.prob_any_loss, 2),
                'prob_loss_10pct': round(r.prob_loss_10pct, 2),
                'prob_loss_20pct': round(r.prob_loss_20pct, 2),
                'prob_loss_50pct': round(r.prob_loss_50pct, 2),
                'var_95': round(r.var_95, 2),
                'cvar_95': round(r.cvar_95, 2),
                'p5_final': round(r.p5_final, 2),
                'p95_final': round(r.p95_final, 2),
                'mean_max_drawdown': round(r.mean_max_drawdown, 2),
                'p95_max_drawdown': round(r.p95_max_drawdown, 2)
            })

        df = pd.DataFrame(rows)
        safe_write_csv(df, output_path)

        # Log output file to audit trail
        audit = get_audit_trail()
        if audit:
            audit.log_output_file(output_path)

        logger.info(f"Monte Carlo results exported to {output_path}")
        return output_path

    def export_validation(
        self,
        validation_results: list[dict],
        filename: str = 'validation_results.csv'
    ) -> Path:
        """Export validation results to CSV."""
        output_path = self.output_dir / filename

        df = pd.DataFrame(validation_results)
        safe_write_csv(df, output_path, allow_empty=True)  # Allow empty for "no violations" case

        # Log output file to audit trail
        audit = get_audit_trail()
        if audit:
            audit.log_output_file(output_path)

        logger.info(f"Validation results exported to {output_path}")
        return output_path
