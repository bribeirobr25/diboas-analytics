"""
Execution metrics collection and aggregation.

Principle 12 (Monitoring & Observability):
-----------------------------------------
Tracks execution metrics for each CLI invocation, enabling
performance monitoring and trend analysis over time.

Zero Budget Approach:
- JSON file storage (no database required)
- Simple aggregation functions
- Human-readable reports

Usage:
    from src.utils.metrics import MetricsCollector, get_metrics_collector

    # Record execution
    collector = get_metrics_collector()
    collector.start_execution("battle-test")
    # ... run command ...
    collector.end_execution(success=True, strategies_tested=10)

    # Generate report
    summary = collector.get_summary(last_n_runs=10)
"""

import json
import logging
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional

from src.utils.correlation import get_correlation_id

logger = logging.getLogger(__name__)


@dataclass
class ExecutionMetrics:
    """Metrics for a single CLI execution."""

    # Identification
    correlation_id: Optional[str] = None
    command: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # Timing
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_ms: int = 0

    # Status
    success: bool = True
    errors: List[str] = field(default_factory=list)

    # Business metrics
    strategies_tested: int = 0
    simulations_run: int = 0
    triggers_evaluated: int = 0
    triggers_fired: int = 0
    validations_passed: int = 0
    validations_failed: int = 0
    outputs_generated: int = 0

    # Resource usage
    data_rows_processed: int = 0
    files_read: int = 0
    files_written: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def calculate_duration(self) -> None:
        """Calculate duration from start/end times."""
        if self.end_time and self.start_time:
            self.duration_ms = int((self.end_time - self.start_time) * 1000)


@dataclass
class MetricsSummary:
    """Aggregated summary of execution metrics."""

    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    success_rate: float = 0.0
    avg_duration_ms: float = 0.0
    max_duration_ms: int = 0
    min_duration_ms: int = 0
    total_strategies_tested: int = 0
    total_triggers_fired: int = 0
    total_validations: int = 0

    # Time range
    first_run: Optional[str] = None
    last_run: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class MetricsCollector:
    """
    Collects and aggregates execution metrics.

    Thread-safe singleton with JSON file persistence.
    """

    _instance: Optional["MetricsCollector"] = None
    _lock = Lock()

    def __new__(cls, metrics_file: Path = None) -> "MetricsCollector":
        """Singleton pattern."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, metrics_file: Path = None):
        """
        Initialize metrics collector.

        Args:
            metrics_file: Path to JSON metrics file (default: outputs/metrics.json)
        """
        if self._initialized:
            return

        self.metrics_file = metrics_file or Path("outputs/metrics.json")
        self._current_metrics: Optional[ExecutionMetrics] = None
        self._metrics_history: List[Dict[str, Any]] = []
        self._max_history = 1000

        # Load existing metrics
        self._load_metrics()
        self._initialized = True

    def _load_metrics(self) -> None:
        """Load metrics from file."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, "r") as f:
                    data = json.load(f)
                    self._metrics_history = data.get("runs", [])
                logger.debug(f"Loaded {len(self._metrics_history)} historical runs")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load metrics file: {e}")
                self._metrics_history = []

    def _save_metrics(self) -> None:
        """Save metrics to file."""
        try:
            self.metrics_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "version": "1.0",
                "updated": datetime.utcnow().isoformat(),
                "runs": self._metrics_history[-self._max_history:],
            }

            with open(self.metrics_file, "w") as f:
                json.dump(data, f, indent=2)

            logger.debug(f"Saved metrics to {self.metrics_file}")
        except IOError as e:
            logger.error(f"Could not save metrics: {e}")

    def start_execution(self, command: str) -> ExecutionMetrics:
        """
        Start tracking a new execution.

        Args:
            command: CLI command being executed

        Returns:
            New ExecutionMetrics instance
        """
        self._current_metrics = ExecutionMetrics(
            command=command,
            correlation_id=get_correlation_id(),
        )
        logger.debug(f"Started metrics tracking for command: {command}")
        return self._current_metrics

    def end_execution(
        self,
        success: bool = True,
        error: str = None,
        **kwargs,
    ) -> None:
        """
        End execution tracking and record metrics.

        Args:
            success: Whether execution was successful
            error: Error message if failed
            **kwargs: Additional metrics to record
        """
        if not self._current_metrics:
            logger.warning("No active execution to end")
            return

        self._current_metrics.end_time = time.time()
        self._current_metrics.calculate_duration()
        self._current_metrics.success = success

        if error:
            self._current_metrics.errors.append(error)

        # Update with any additional metrics
        for key, value in kwargs.items():
            if hasattr(self._current_metrics, key):
                setattr(self._current_metrics, key, value)

        # Record to history
        self._metrics_history.append(self._current_metrics.to_dict())
        self._save_metrics()

        logger.debug(
            f"Ended metrics tracking: {self._current_metrics.command} "
            f"({self._current_metrics.duration_ms}ms, success={success})"
        )

        self._current_metrics = None

    def record(self, **kwargs) -> None:
        """
        Record additional metrics during execution.

        Args:
            **kwargs: Metrics to update
        """
        if not self._current_metrics:
            return

        for key, value in kwargs.items():
            if hasattr(self._current_metrics, key):
                current = getattr(self._current_metrics, key)
                if isinstance(current, int) and isinstance(value, int):
                    setattr(self._current_metrics, key, current + value)
                else:
                    setattr(self._current_metrics, key, value)

    def get_summary(self, last_n_runs: int = 10) -> MetricsSummary:
        """
        Get summary of recent executions.

        Args:
            last_n_runs: Number of recent runs to summarize

        Returns:
            MetricsSummary with aggregated metrics
        """
        runs = self._metrics_history[-last_n_runs:] if last_n_runs > 0 else self._metrics_history

        if not runs:
            return MetricsSummary()

        # Calculate aggregates
        total = len(runs)
        successful = sum(1 for r in runs if r.get("success", True))
        durations = [r.get("duration_ms", 0) for r in runs]

        return MetricsSummary(
            total_runs=total,
            successful_runs=successful,
            failed_runs=total - successful,
            success_rate=round(successful / total * 100, 2) if total > 0 else 0.0,
            avg_duration_ms=round(sum(durations) / len(durations), 2) if durations else 0.0,
            max_duration_ms=max(durations) if durations else 0,
            min_duration_ms=min(durations) if durations else 0,
            total_strategies_tested=sum(r.get("strategies_tested", 0) for r in runs),
            total_triggers_fired=sum(r.get("triggers_fired", 0) for r in runs),
            total_validations=sum(
                r.get("validations_passed", 0) + r.get("validations_failed", 0)
                for r in runs
            ),
            first_run=runs[0].get("timestamp") if runs else None,
            last_run=runs[-1].get("timestamp") if runs else None,
        )

    def get_recent_runs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent execution details.

        Args:
            limit: Maximum number of runs to return

        Returns:
            List of execution metrics dictionaries
        """
        return list(reversed(self._metrics_history[-limit:]))

    def export_to_json(self, filepath: Path) -> None:
        """
        Export all metrics to a JSON file.

        Args:
            filepath: Output file path
        """
        data = {
            "version": "1.0",
            "exported": datetime.utcnow().isoformat(),
            "summary": self.get_summary(last_n_runs=0).to_dict(),
            "runs": self._metrics_history,
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Exported {len(self._metrics_history)} runs to {filepath}")


# Global singleton accessor
def get_metrics_collector(metrics_file: Path = None) -> MetricsCollector:
    """
    Get the global metrics collector instance.

    Args:
        metrics_file: Optional custom metrics file path

    Returns:
        MetricsCollector singleton instance
    """
    return MetricsCollector(metrics_file)


def record_metric(**kwargs) -> None:
    """
    Convenience function to record metrics.

    Args:
        **kwargs: Metrics to record
    """
    get_metrics_collector().record(**kwargs)
