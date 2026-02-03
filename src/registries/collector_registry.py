"""
Collector Registry for data sources.

Wraps existing FileLoader and provides interface for future live API collectors.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import date
import pandas as pd
import logging

from src.registries.base import Registry

logger = logging.getLogger(__name__)


class Collector(ABC):
    """
    Abstract base class for all data collectors.

    All collectors must implement collect() and declare their source_type.
    """

    @abstractmethod
    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect data from the source.

        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            DataFrame with collected data
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the collector name for logging."""
        pass

    @property
    @abstractmethod
    def source_type(self) -> str:
        """
        Return the type of data source.

        Returns:
            One of: 'file', 'api', 'hybrid'
        """
        pass

    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate collected data.

        Override in subclasses for custom validation.
        Default implementation checks for non-empty DataFrame.

        Args:
            data: Collected DataFrame

        Returns:
            True if valid, False otherwise
        """
        return not data.empty


class CollectorRegistry(Registry[Collector]):
    """
    Registry for data collectors.

    Usage:
        collector = CollectorRegistry.get_instance().get("file_loader", {})
        data = collector.collect(start_date, end_date)
    """
    pass


# =============================================================================
# Wrapped Implementations
# =============================================================================

@CollectorRegistry.register("file_loader")
class FileLoaderCollector(Collector):
    """
    Wrapper for FileLoader (bundled CSV files).

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.collectors.file_loader import FileLoader
        self.config = config
        data_dir = config.get('data_dir')
        self._loader = FileLoader(data_dir=data_dir) if data_dir else FileLoader()

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect all bundled data.

        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            Dict of DataFrames keyed by source name
        """
        logger.info(f"Collecting from file_loader: {start_date} to {end_date}")
        return self._loader.load_all(start_date, end_date)

    def get_name(self) -> str:
        return "file_loader"

    @property
    def source_type(self) -> str:
        return "file"

    # ==========================================================================
    # Direct access to underlying FileLoader methods
    # ==========================================================================

    def load(self, source: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> pd.DataFrame:
        """Load a specific data source."""
        return self._loader.load(source, start_date, end_date)

    def load_all(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict[str, pd.DataFrame]:
        """Load all data sources."""
        return self._loader.load_all(start_date, end_date)

    def get_date_range(self, source: str) -> tuple[date, date]:
        """Get date range for a source."""
        return self._loader.get_date_range(source)

    def get_available_protocols(self, source: str = 'defillama') -> list[str]:
        """Get available protocols in the data."""
        return self._loader.get_available_protocols(source)

    def get_available_symbols(self, source: str = 'yahoo') -> list[str]:
        """Get available symbols in price data."""
        return self._loader.get_available_symbols(source)


@CollectorRegistry.register("defillama")
class DeFiLlamaCollector(Collector):
    """
    Collector for DeFiLlama data.

    Currently uses bundled CSV. Will be extended in Week 2 for live API.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.collectors.file_loader import FileLoader
        self.config = config
        self._loader = FileLoader()

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect DeFiLlama APY data.

        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            DataFrame with APY data
        """
        logger.info(f"Collecting DeFiLlama data: {start_date} to {end_date}")
        return self._loader.load('defillama', start_date, end_date)

    def get_name(self) -> str:
        return "defillama"

    @property
    def source_type(self) -> str:
        return "file"  # Will change to "api" in Week 2


@CollectorRegistry.register("yahoo")
class YahooCollector(Collector):
    """
    Collector for Yahoo Finance price data.

    Currently uses bundled CSV. Will be extended in Week 2 for live API.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.collectors.file_loader import FileLoader
        self.config = config
        self._loader = FileLoader()

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect Yahoo Finance price data.

        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            DataFrame with price data
        """
        logger.info(f"Collecting Yahoo data: {start_date} to {end_date}")
        return self._loader.load('yahoo', start_date, end_date)

    def get_name(self) -> str:
        return "yahoo"

    @property
    def source_type(self) -> str:
        return "file"  # Will change to "api" in Week 2


@CollectorRegistry.register("jupiter")
class JupiterCollector(Collector):
    """
    Collector for Jupiter JLP data.

    Currently uses bundled CSV.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.collectors.file_loader import FileLoader
        self.config = config
        self._loader = FileLoader()

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect Jupiter JLP APY data.

        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            DataFrame with JLP APY data
        """
        logger.info(f"Collecting Jupiter data: {start_date} to {end_date}")
        return self._loader.load('jupiter', start_date, end_date)

    def get_name(self) -> str:
        return "jupiter"

    @property
    def source_type(self) -> str:
        return "file"


@CollectorRegistry.register("data_aggregator")
class DataAggregatorCollector(Collector):
    """
    Wrapper for DataAggregator functionality (file-based).

    Provides higher-level data aggregation methods for bundled CSV data.
    Note: For live API aggregation, use 'aggregator' instead.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.collectors.file_loader import FileLoader, DataAggregator
        self.config = config
        loader = FileLoader()
        self._aggregator = DataAggregator(loader)

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect aggregated data.

        For specific series, use the direct methods below.
        """
        # Return empty DataFrame - use specific methods instead
        return pd.DataFrame()

    def get_name(self) -> str:
        return "data_aggregator"

    @property
    def source_type(self) -> str:
        return "file"

    # ==========================================================================
    # Direct access to aggregation methods
    # ==========================================================================

    def get_protocol_apy_series(self, protocol: str, start_date: date, end_date: date) -> pd.Series:
        """Get daily APY series for a protocol."""
        return self._aggregator.get_protocol_apy_series(protocol, start_date, end_date)

    def get_price_series(self, symbol: str, start_date: date, end_date: date) -> pd.DataFrame:
        """Get daily price data for a crypto asset."""
        return self._aggregator.get_price_series(symbol, start_date, end_date)

    def get_jlp_apy_series(self, start_date: date, end_date: date) -> pd.Series:
        """Get daily JLP APY series."""
        return self._aggregator.get_jlp_apy_series(start_date, end_date)

    def calculate_daily_returns(self, symbol: str, start_date: date, end_date: date) -> pd.Series:
        """Calculate daily returns for a crypto asset."""
        return self._aggregator.calculate_daily_returns(symbol, start_date, end_date)
