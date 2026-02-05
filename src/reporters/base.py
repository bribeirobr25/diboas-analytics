"""
Base reporter functionality.

DRY Principle (Principle 4):
---------------------------
This module provides shared functionality for all reporters to avoid
duplicated export patterns across CSV, JSON, and Markdown reporters.

Usage:
    from src.reporters.base import BaseReporter

    class MyReporter(BaseReporter):
        def export_data(self, data, filename):
            output_path = self._prepare_output_path(filename)
            # ... transform and write data ...
            self._log_export(output_path, len(data))
            return output_path
"""

import logging
from abc import ABC
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from config.settings import OUTPUT_DIR
from src.utils.serialization import to_dict_safe, make_json_safe, round_floats

logger = logging.getLogger(__name__)


class BaseReporter(ABC):
    """
    Abstract base class for all reporters.

    Provides common functionality:
    - Output directory management
    - Path preparation
    - Export logging
    - Data transformation helpers
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize reporter with output directory.

        Args:
            output_dir: Directory for output files. Defaults to OUTPUT_DIR from settings.
        """
        self.output_dir = output_dir or OUTPUT_DIR
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Ensure output directory exists."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _prepare_output_path(
        self,
        filename: str,
        subdirectory: Optional[str] = None
    ) -> Path:
        """
        Prepare the full output path for a file.

        Args:
            filename: Name of the output file
            subdirectory: Optional subdirectory within output_dir

        Returns:
            Full path to the output file
        """
        if subdirectory:
            subdir = self.output_dir / subdirectory
            subdir.mkdir(parents=True, exist_ok=True)
            return subdir / filename
        return self.output_dir / filename

    def _log_export(
        self,
        output_path: Path,
        record_count: Optional[int] = None,
        export_type: str = "data"
    ) -> None:
        """
        Log successful export.

        Args:
            output_path: Path where file was written
            record_count: Number of records exported (if applicable)
            export_type: Type of data exported (for log message)
        """
        if record_count is not None:
            logger.info(f"Exported {record_count} {export_type} records to {output_path}")
        else:
            logger.info(f"Exported {export_type} to {output_path}")

    @staticmethod
    def _objects_to_dicts(
        objects: List[Any],
        round_precision: Optional[int] = 2
    ) -> List[Dict[str, Any]]:
        """
        Convert a list of objects to list of dictionaries.

        Handles objects with to_dict(), dataclasses, and dicts.

        Args:
            objects: List of objects to convert
            round_precision: Decimal places to round floats (None to skip)

        Returns:
            List of dictionaries
        """
        results = []
        for obj in objects:
            d = to_dict_safe(obj)
            if round_precision is not None:
                d = round_floats(d, round_precision)
            results.append(d)
        return results

    @staticmethod
    def _make_json_safe(data: Any) -> Any:
        """
        Convert data to JSON-safe format.

        Args:
            data: Any data structure

        Returns:
            JSON-serializable data
        """
        return make_json_safe(data)


class ReporterFactory:
    """
    Factory for creating reporters.

    Usage:
        factory = ReporterFactory(output_dir=Path("./outputs"))
        csv_reporter = factory.get_csv_reporter()
        json_reporter = factory.get_json_reporter()
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize factory with shared output directory.

        Args:
            output_dir: Directory for all reporters to use
        """
        self.output_dir = output_dir or OUTPUT_DIR

    def get_csv_reporter(self) -> 'CSVReporter':
        """Get CSV reporter instance."""
        from src.reporters.csv_reporter import CSVReporter
        return CSVReporter(self.output_dir)

    def get_json_reporter(self) -> 'JSONReporter':
        """Get JSON reporter instance."""
        from src.reporters.json_reporter import JSONReporter
        return JSONReporter(self.output_dir)

    def get_markdown_reporter(self) -> 'MarkdownReporter':
        """Get Markdown reporter instance."""
        from src.reporters.markdown_reporter import MarkdownReporter
        return MarkdownReporter(self.output_dir)
