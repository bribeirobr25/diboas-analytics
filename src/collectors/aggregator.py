"""
Aggregator Collector - Orchestrates all data collectors.

Provides unified interface to collect data from all sources:
- FRED (macro data)
- Yahoo Finance (equities, crypto, commodities)
- DeFiLlama (DeFi protocol APYs)
- CoinGecko (crypto prices backup)
- Alternative.me (sentiment)

Usage:
    collector = CollectorRegistry.get_instance().get("aggregator", {})
    data = collector.collect()  # Returns all data
    data = collector.collect(sources=['fred', 'yahoo_live'])  # Specific sources
"""

import logging
from datetime import date, datetime
from typing import Optional, Dict, List, Any
from pathlib import Path
import pandas as pd

from config.settings import DATA_DIR
from src.registries import CollectorRegistry, Collector
from src.utils.file_io import safe_write_csv

logger = logging.getLogger(__name__)

# Source to collector mapping
SOURCE_COLLECTORS = {
    'fred': 'fred',
    'yahoo_live': 'yahoo_live',
    'defillama_live': 'defillama_live',
    'coingecko': 'coingecko',
    'alternative': 'alternative',
    # File-based collectors
    'file_loader': 'file_loader',
    'defillama': 'defillama',
    'yahoo': 'yahoo',
    'jupiter': 'jupiter',
}


@CollectorRegistry.register("aggregator")
class AggregatorCollector(Collector):
    """
    Aggregator that orchestrates multiple data collectors.

    Provides a unified interface for collecting data from all sources
    with graceful degradation if individual sources fail.

    Usage:
        # Collect from all live sources
        aggregator = CollectorRegistry.get_instance().get("aggregator", {})
        data = aggregator.collect()

        # Collect from specific sources
        data = aggregator.collect(sources=['fred', 'alternative'])

        # Save all data to CSV
        paths = aggregator.save_all()
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize aggregator.

        Args:
            config: Configuration dict with optional keys:
                - sources: List of sources to use (default: all live)
                - start_date: Start date for data
                - end_date: End date for data
                - output_dir: Directory for saving files
        """
        self.config = config
        self._registry = CollectorRegistry.get_instance()

    def _get_collector(self, source: str) -> Optional[Collector]:
        """
        Get a collector instance for a source.

        Args:
            source: Source name

        Returns:
            Collector instance or None if not found
        """
        if source not in SOURCE_COLLECTORS:
            logger.warning(f"Unknown source: {source}")
            return None

        collector_name = SOURCE_COLLECTORS[source]

        try:
            return self._registry.get(collector_name, self.config)
        except KeyError:
            logger.warning(f"Collector not registered: {collector_name}")
            return None

    def collect(
        self,
        sources: List[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Collect data from specified sources.

        Args:
            sources: List of source names (default: all live API sources)
            start_date: Start date for data
            end_date: End date for data

        Returns:
            Dictionary mapping source to collected data
        """
        # Default to live API sources
        if sources is None:
            sources = ['fred', 'yahoo_live', 'defillama_live', 'alternative']

        # Use config dates if not specified
        if start_date is None:
            start_str = self.config.get('start_date')
            if start_str:
                start_date = datetime.strptime(start_str, '%Y-%m-%d').date()

        if end_date is None:
            end_str = self.config.get('end_date')
            if end_str:
                end_date = datetime.strptime(end_str, '%Y-%m-%d').date()

        logger.info(f"Collecting data from sources: {sources}")

        results = {}

        for source in sources:
            collector = self._get_collector(source)
            if collector is None:
                continue

            try:
                logger.info(f"Collecting from {source}...")
                data = collector.collect(start_date, end_date)
                results[source] = data
                logger.info(f"Successfully collected from {source}")

            except Exception as e:
                logger.error(f"Failed to collect from {source}: {e}")
                results[source] = {'error': str(e)}

        return results

    def collect_all_live(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Collect from all live API sources.

        Returns:
            Dictionary with all collected data
        """
        live_sources = ['fred', 'yahoo_live', 'defillama_live', 'alternative']
        return self.collect(sources=live_sources, start_date=start_date, end_date=end_date)

    def save_all(
        self,
        output_dir: str = None,
        sources: List[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Collect and save all data to CSV files.

        Args:
            output_dir: Output directory (default: data/)
            sources: List of sources (default: all live)
            start_date: Start date
            end_date: End date

        Returns:
            Dictionary mapping source to saved file paths
        """
        output_path = Path(output_dir) if output_dir else DATA_DIR

        if sources is None:
            sources = ['fred', 'yahoo_live', 'defillama_live', 'alternative']

        saved_files = {}

        for source in sources:
            collector = self._get_collector(source)
            if collector is None:
                continue

            try:
                logger.info(f"Saving data from {source}...")

                if hasattr(collector, 'save_to_csv'):
                    paths = collector.save_to_csv(str(output_path), start_date, end_date)
                    saved_files[source] = paths
                else:
                    # Fallback: collect and save manually
                    data = collector.collect(start_date, end_date)
                    if isinstance(data, pd.DataFrame):
                        filepath = output_path / f"{source}_data.csv"
                        if safe_write_csv(data, filepath):
                            saved_files[source] = str(filepath)
                    elif isinstance(data, dict):
                        saved_files[source] = {}
                        for key, df in data.items():
                            if isinstance(df, pd.DataFrame) and not df.empty:
                                filepath = output_path / f"{source}_{key}.csv"
                                if safe_write_csv(df, filepath):
                                    saved_files[source][key] = str(filepath)

            except Exception as e:
                logger.error(f"Failed to save data from {source}: {e}")
                saved_files[source] = {'error': str(e)}

        return saved_files

    def get_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status of all collectors.

        Returns:
            Dictionary with collector availability and health
        """
        status = {}

        for source, collector_name in SOURCE_COLLECTORS.items():
            collector = self._get_collector(source)

            status[source] = {
                'available': collector is not None,
                'collector': collector_name,
                'type': collector.source_type if collector else 'unknown'
            }

            # Check if collector has required configuration
            if source == 'fred':
                from config.settings import settings
                status[source]['configured'] = settings.has('FRED_API_KEY')
            elif source == 'coingecko':
                from config.settings import settings
                status[source]['configured'] = True  # Works without key
                status[source]['has_api_key'] = settings.has('COINGECKO_API_KEY')
            else:
                status[source]['configured'] = True

        return status

    def get_name(self) -> str:
        """Return collector name."""
        return "aggregator"

    @property
    def source_type(self) -> str:
        """Return source type."""
        return "hybrid"


def collect_and_save_all(
    output_dir: str = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Dict[str, Any]:
    """
    Convenience function to collect and save all data.

    Args:
        output_dir: Output directory
        start_date: Start date
        end_date: End date

    Returns:
        Dictionary of saved file paths
    """
    aggregator = CollectorRegistry.get_instance().get("aggregator", {})
    return aggregator.save_all(output_dir, start_date=start_date, end_date=end_date)
