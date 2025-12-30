"""
JSON Reporter for exporting results.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any
import logging

from src.domain.simulation import BattleTestResult, MonteCarloResult, SimulationMetadata
from config.settings import OUTPUT_DIR

logger = logging.getLogger(__name__)


class JSONReporter:
    """Export results to JSON format."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or OUTPUT_DIR

    def export_battle_test(
        self,
        results: list[BattleTestResult],
        metadata: SimulationMetadata = None,
        filename: str = 'battle_test_results.json'
    ) -> Path:
        """
        Export Battle Test results to JSON.

        Args:
            results: List of BattleTestResult
            metadata: Simulation metadata
            filename: Output filename

        Returns:
            Path to output file
        """
        output_path = self.output_dir / filename

        output = {
            'generated_at': datetime.utcnow().isoformat(),
            'type': 'battle_test',
            'results': [r.to_dict() for r in results]
        }

        if metadata:
            output['metadata'] = metadata.to_dict()

        self._write_json(output_path, output)
        logger.info(f"Battle Test results exported to {output_path}")
        return output_path

    def export_monte_carlo(
        self,
        results: list[MonteCarloResult],
        metadata: SimulationMetadata = None,
        filename: str = 'monte_carlo_results.json'
    ) -> Path:
        """
        Export Monte Carlo results to JSON.

        Args:
            results: List of MonteCarloResult
            metadata: Simulation metadata
            filename: Output filename

        Returns:
            Path to output file
        """
        output_path = self.output_dir / filename

        output = {
            'generated_at': datetime.utcnow().isoformat(),
            'type': 'monte_carlo',
            'results': [r.to_dict() for r in results]
        }

        if metadata:
            output['metadata'] = metadata.to_dict()

        self._write_json(output_path, output)
        logger.info(f"Monte Carlo results exported to {output_path}")
        return output_path

    def export_validation(
        self,
        report: dict,
        filename: str = 'validation_report.json'
    ) -> Path:
        """Export validation report to JSON."""
        output_path = self.output_dir / filename

        output = {
            'generated_at': datetime.utcnow().isoformat(),
            'type': 'validation',
            **report
        }

        self._write_json(output_path, output)
        logger.info(f"Validation report exported to {output_path}")
        return output_path

    def export_protocol_health(
        self,
        health_data: list[dict],
        filename: str = 'protocol_health.json'
    ) -> Path:
        """Export protocol health data to JSON."""
        output_path = self.output_dir / filename

        output = {
            'generated_at': datetime.utcnow().isoformat(),
            'type': 'protocol_health',
            'protocols': health_data
        }

        self._write_json(output_path, output)
        logger.info(f"Protocol health exported to {output_path}")
        return output_path

    def export_anomalies(
        self,
        anomaly_report: dict,
        filename: str = 'anomaly_scores.json'
    ) -> Path:
        """Export anomaly detection results to JSON."""
        output_path = self.output_dir / filename

        output = {
            'generated_at': datetime.utcnow().isoformat(),
            'type': 'anomaly_detection',
            **anomaly_report
        }

        self._write_json(output_path, output)
        logger.info(f"Anomaly report exported to {output_path}")
        return output_path

    def export_metadata(
        self,
        metadata: SimulationMetadata,
        filename: str = 'execution_metadata.json'
    ) -> Path:
        """Export execution metadata to JSON."""
        output_path = self.output_dir / filename
        self._write_json(output_path, metadata.to_dict())
        logger.info(f"Metadata exported to {output_path}")
        return output_path

    def _write_json(self, path: Path, data: Any):
        """Write JSON to file with proper formatting."""
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
