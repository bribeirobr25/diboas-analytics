"""Tests for metrics collection utilities."""

import pytest
import tempfile
import json
from pathlib import Path

from src.utils.metrics import (
    ExecutionMetrics,
    MetricsSummary,
    MetricsCollector,
    get_metrics_collector,
    record_metric,
)


class TestExecutionMetrics:
    """Tests for ExecutionMetrics dataclass."""

    def test_default_values(self):
        """ExecutionMetrics has sensible defaults."""
        metrics = ExecutionMetrics()

        assert metrics.command == ""
        assert metrics.success is True
        assert metrics.errors == []
        assert metrics.duration_ms == 0

    def test_to_dict(self):
        """ExecutionMetrics.to_dict() returns proper dict."""
        metrics = ExecutionMetrics(
            command="battle-test",
            strategies_tested=10,
            success=True,
        )

        d = metrics.to_dict()

        assert d["command"] == "battle-test"
        assert d["strategies_tested"] == 10
        assert d["success"] is True
        assert "timestamp" in d

    def test_calculate_duration(self):
        """calculate_duration computes from start/end times."""
        metrics = ExecutionMetrics()
        metrics.start_time = 1000.0
        metrics.end_time = 1001.5

        metrics.calculate_duration()

        assert metrics.duration_ms == 1500


class TestMetricsSummary:
    """Tests for MetricsSummary dataclass."""

    def test_default_values(self):
        """MetricsSummary has sensible defaults."""
        summary = MetricsSummary()

        assert summary.total_runs == 0
        assert summary.success_rate == 0.0
        assert summary.first_run is None

    def test_to_dict(self):
        """MetricsSummary.to_dict() returns proper dict."""
        summary = MetricsSummary(
            total_runs=10,
            successful_runs=9,
            success_rate=90.0,
        )

        d = summary.to_dict()

        assert d["total_runs"] == 10
        assert d["success_rate"] == 90.0


class TestMetricsCollector:
    """Tests for MetricsCollector class."""

    @pytest.fixture
    def collector(self):
        """Create collector with temp file."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            # Reset singleton for testing
            MetricsCollector._instance = None
            collector = MetricsCollector(metrics_file=Path(f.name))
            yield collector
            # Cleanup
            MetricsCollector._instance = None

    def test_start_and_end_execution(self, collector):
        """Can start and end execution tracking."""
        metrics = collector.start_execution("test-command")

        assert metrics.command == "test-command"
        assert metrics.start_time > 0

        collector.end_execution(
            success=True,
            strategies_tested=5,
        )

        # Verify recorded
        runs = collector.get_recent_runs(limit=1)
        assert len(runs) == 1
        assert runs[0]["command"] == "test-command"
        assert runs[0]["strategies_tested"] == 5

    def test_record_incremental_metrics(self, collector):
        """Can record incremental metrics during execution."""
        collector.start_execution("test-command")

        collector.record(triggers_evaluated=10)
        collector.record(triggers_evaluated=5)  # Should add

        collector.end_execution(success=True)

        runs = collector.get_recent_runs(limit=1)
        assert runs[0]["triggers_evaluated"] == 15

    def test_get_summary(self, collector):
        """get_summary aggregates metrics correctly."""
        # Record some executions
        for i in range(5):
            collector.start_execution("test")
            collector.end_execution(success=(i < 4))  # 4 success, 1 failure

        summary = collector.get_summary(last_n_runs=5)

        assert summary.total_runs == 5
        assert summary.successful_runs == 4
        assert summary.failed_runs == 1
        assert summary.success_rate == 80.0

    def test_persistence(self, collector):
        """Metrics are persisted to file."""
        collector.start_execution("test")
        collector.end_execution(success=True)

        # Read file directly
        with open(collector.metrics_file, "r") as f:
            data = json.load(f)

        assert len(data["runs"]) == 1
        assert data["runs"][0]["command"] == "test"

    def test_export_to_json(self, collector):
        """Can export all metrics to JSON file."""
        collector.start_execution("test")
        collector.end_execution(success=True)

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            export_path = Path(f.name)

        collector.export_to_json(export_path)

        with open(export_path, "r") as f:
            data = json.load(f)

        assert "summary" in data
        assert "runs" in data
        assert len(data["runs"]) == 1


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    def test_record_metric(self):
        """record_metric works without active execution."""
        # Should not raise when no active execution
        record_metric(triggers_evaluated=10)
