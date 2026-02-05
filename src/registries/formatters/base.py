"""
Base classes for output formatters.

Contains:
- OutputFormatter: Abstract base class for all formatters
- OutputRegistry: Registry for discovering and instantiating formatters
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar
from pathlib import Path
import logging

from src.registries.base import Registry

logger = logging.getLogger(__name__)


class OutputFormatter(ABC):
    """
    Abstract base class for all output formatters.

    All formatters must implement format() and declare their output_type.
    """

    @abstractmethod
    def format(self, data: Any, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Format data for output.

        Args:
            data: Data to format (type depends on formatter)
            config: Optional formatting configuration

        Returns:
            Formatted string output
        """
        pass

    @property
    @abstractmethod
    def output_type(self) -> str:
        """
        Return the type of output.

        Returns:
            One of: 'json', 'csv', 'markdown', 'newsletter', 'twitter', 'html', etc.
        """
        pass

    def get_name(self) -> str:
        """Get the formatter name for logging."""
        return self.__class__.__name__

    def export(self, data: Any, filepath: Path, config: Optional[Dict[str, Any]] = None) -> Path:
        """
        Format and export data to a file.

        Args:
            data: Data to format
            filepath: Output file path
            config: Optional formatting configuration

        Returns:
            Path to the output file
        """
        content = self.format(data, config)
        with open(filepath, 'w') as f:
            f.write(content)
        logger.info(f"Exported {self.output_type} to {filepath}")
        return filepath


class OutputRegistry(Registry[OutputFormatter]):
    """
    Registry for output formatters.

    Usage:
        formatter = OutputRegistry.get_instance().get("json", {})
        output = formatter.format(results)
    """
    pass
