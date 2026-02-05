"""
Legacy reporter wrappers.

Wraps existing reporters (JSON, CSV, Markdown) to make them registry-compatible.
"""

from typing import Any, Dict, Optional
from pathlib import Path
import logging

from src.registries.formatters.base import OutputFormatter, OutputRegistry

logger = logging.getLogger(__name__)


@OutputRegistry.register("json")
class JSONOutputFormatter(OutputFormatter):
    """
    Wrapper for JSONReporter.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.reporters.json_reporter import JSONReporter
        self.config = config
        output_dir = config.get('output_dir')
        self._reporter = JSONReporter(output_dir=Path(output_dir)) if output_dir else JSONReporter()

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format data as JSON.

        Args:
            data: Data to format (results, validation report, etc.)
            config: Optional config with:
                - indent: JSON indentation (default: 2)
                - include_metadata: Whether to include metadata

        Returns:
            JSON string
        """
        import json
        from datetime import datetime

        config = config or {}
        indent = config.get('indent', 2)

        # Build output structure
        output = {
            'generated_at': datetime.utcnow().isoformat()
        }

        # Handle different data types
        if isinstance(data, list):
            if data and hasattr(data[0], 'to_dict'):
                output['results'] = [item.to_dict() for item in data]
            else:
                output['results'] = data
        elif hasattr(data, 'to_dict'):
            output.update(data.to_dict())
        elif isinstance(data, dict):
            output.update(data)
        else:
            output['data'] = str(data)

        return json.dumps(output, indent=indent, default=str)

    @property
    def output_type(self) -> str:
        return "json"

    # ==========================================================================
    # Direct access to reporter methods
    # ==========================================================================

    def export_battle_test(self, results, metadata=None, filename='battle_test_results.json') -> Path:
        """Export Battle Test results."""
        return self._reporter.export_battle_test(results, metadata, filename)

    def export_monte_carlo(self, results, metadata=None, filename='monte_carlo_results.json') -> Path:
        """Export Monte Carlo results."""
        return self._reporter.export_monte_carlo(results, metadata, filename)

    def export_validation(self, report, filename='validation_report.json') -> Path:
        """Export validation report."""
        return self._reporter.export_validation(report, filename)


@OutputRegistry.register("csv")
class CSVOutputFormatter(OutputFormatter):
    """
    Wrapper for CSVReporter.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.reporters.csv_reporter import CSVReporter
        self.config = config
        output_dir = config.get('output_dir')
        self._reporter = CSVReporter(output_dir=Path(output_dir)) if output_dir else CSVReporter()

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format data as CSV.

        Args:
            data: Data to format (list of results with to_dict())
            config: Optional config

        Returns:
            CSV string
        """
        import io
        import csv

        if isinstance(data, list) and data:
            if hasattr(data[0], 'to_dict'):
                rows = [item.to_dict() for item in data]
            else:
                rows = data

            if rows:
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
                return output.getvalue()

        return ""

    @property
    def output_type(self) -> str:
        return "csv"

    # ==========================================================================
    # Direct access to reporter methods
    # ==========================================================================

    def export_battle_test(self, results, filename='battle_test_results.csv') -> Path:
        """Export Battle Test results."""
        return self._reporter.export_battle_test(results, filename)

    def export_monte_carlo(self, results, filename='monte_carlo_results.csv') -> Path:
        """Export Monte Carlo results."""
        return self._reporter.export_monte_carlo(results, filename)


@OutputRegistry.register("markdown")
class MarkdownOutputFormatter(OutputFormatter):
    """
    Wrapper for MarkdownReporter.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.reporters.markdown_reporter import MarkdownReporter
        self.config = config
        output_dir = config.get('output_dir')
        self._reporter = MarkdownReporter(output_dir=Path(output_dir)) if output_dir else MarkdownReporter()

    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format data as Markdown.

        Args:
            data: Data to format
            config: Optional config with:
                - title: Report title
                - include_summary: Whether to include summary section

        Returns:
            Markdown string
        """
        from datetime import datetime

        config = config or {}
        title = config.get('title', 'Results Report')

        lines = [
            f"# {title}",
            "",
            f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            "",
        ]

        # Handle different data types
        if isinstance(data, list) and data:
            if hasattr(data[0], 'to_dict'):
                rows = [item.to_dict() for item in data]
            else:
                rows = data

            if rows:
                # Create table
                headers = list(rows[0].keys())
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

                for row in rows:
                    values = [str(row.get(h, '')) for h in headers]
                    lines.append("| " + " | ".join(values) + " |")

        elif hasattr(data, 'to_dict'):
            for key, value in data.to_dict().items():
                lines.append(f"**{key}**: {value}")

        elif isinstance(data, dict):
            for key, value in data.items():
                lines.append(f"**{key}**: {value}")

        return "\n".join(lines)

    @property
    def output_type(self) -> str:
        return "markdown"

    # ==========================================================================
    # Direct access to reporter methods
    # ==========================================================================

    def export_battle_test(self, results, metadata=None, filename='battle_test_report.md') -> Path:
        """Export Battle Test report."""
        # MarkdownReporter uses generate_* methods
        # Extract scenario from metadata if available
        scenario = 'A'
        if metadata and hasattr(metadata, 'scenario'):
            scenario = metadata.scenario
        return self._reporter.generate_battle_test_report(results, scenario, filename)

    def export_monte_carlo(self, results, metadata=None, filename='monte_carlo_report.md') -> Path:
        """Export Monte Carlo report."""
        # MarkdownReporter uses generate_* methods
        return self._reporter.generate_monte_carlo_report(results, filename)
