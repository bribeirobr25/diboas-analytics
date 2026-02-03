"""
diBoaS Analytics Data Collectors.

Provides both file-based and live API collectors for market data.

File-based collectors (bundled data):
- file_loader: Load historical CSV files

Live API collectors:
- fred: FRED macro economic data
- yahoo_live: Yahoo Finance market data
- defillama_live: DeFiLlama DeFi protocol data
- coingecko: CoinGecko crypto prices
- alternative: Alternative.me Fear & Greed Index

Orchestration:
- aggregator: Combines all collectors

Usage:
    from src.registries import CollectorRegistry

    # Get a specific collector
    fred = CollectorRegistry.get_instance().get("fred", {})
    data = fred.collect()

    # Or use the aggregator
    agg = CollectorRegistry.get_instance().get("aggregator", {})
    all_data = agg.collect_all_live()
"""

# Import to trigger registration
from src.collectors.file_loader import FileLoader, DataAggregator
from src.collectors.http_client import RateLimitedClient, APIError, RateLimitError
from src.collectors.fred_collector import FREDCollector
from src.collectors.yahoo_collector import YahooCollector
from src.collectors.defillama_collector import DeFiLlamaCollector
from src.collectors.coingecko_collector import CoinGeckoCollector
from src.collectors.alternative_collector import AlternativeCollector
from src.collectors.aggregator import AggregatorCollector, collect_and_save_all

__all__ = [
    # File-based
    'FileLoader',
    'DataAggregator',
    # HTTP client
    'RateLimitedClient',
    'APIError',
    'RateLimitError',
    # Live collectors
    'FREDCollector',
    'YahooCollector',
    'DeFiLlamaCollector',
    'CoinGeckoCollector',
    'AlternativeCollector',
    # Orchestration
    'AggregatorCollector',
    'collect_and_save_all',
]
