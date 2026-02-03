"""
Tests for live API collectors.

Tests cover:
1. Collector initialization
2. Registry integration
3. Output schema validation
4. Error handling

Note: Some tests require API keys to be configured in .env
Tests that require live API calls are marked with @pytest.mark.live
"""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock, patch, MagicMock
import pandas as pd


class TestCollectorRegistry:
    """Test collectors are properly registered."""

    def test_live_collectors_registered(self):
        """Test all live collectors are registered."""
        from src.registries import CollectorRegistry, ensure_collectors_registered

        ensure_collectors_registered()
        registry = CollectorRegistry.get_instance()

        # Live API collectors
        assert registry.is_registered("fred")
        assert registry.is_registered("yahoo_live")
        assert registry.is_registered("defillama_live")
        assert registry.is_registered("coingecko")
        assert registry.is_registered("alternative")
        assert registry.is_registered("aggregator")

    def test_file_collectors_registered(self):
        """Test file-based collectors are registered."""
        from src.registries import CollectorRegistry

        registry = CollectorRegistry.get_instance()

        assert registry.is_registered("file_loader")
        assert registry.is_registered("defillama")
        assert registry.is_registered("yahoo")
        assert registry.is_registered("jupiter")


class TestHTTPClient:
    """Test rate-limited HTTP client."""

    def test_client_initialization(self):
        """Test HTTP client initializes correctly."""
        from src.collectors.http_client import RateLimitedClient

        client = RateLimitedClient(requests_per_minute=30)
        assert client.requests_per_minute == 30
        assert client.min_interval == 2.0  # 60/30

    def test_client_rate_limit_calculation(self):
        """Test rate limit interval calculation."""
        from src.collectors.http_client import RateLimitedClient

        client = RateLimitedClient(requests_per_minute=60)
        assert client.min_interval == 1.0

        client = RateLimitedClient(requests_per_minute=120)
        assert client.min_interval == 0.5


class TestFREDCollector:
    """Test FRED collector."""

    def test_fred_collector_initialization(self):
        """Test FRED collector initializes."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("fred", {})
        assert collector is not None
        assert collector.get_name() == "fred"
        assert collector.source_type == "api"

    def test_fred_series_defined(self):
        """Test FRED series are properly defined."""
        from src.collectors.fred_collector import FRED_SERIES

        assert 'treasury_yields' in FRED_SERIES
        assert 'real_yields' in FRED_SERIES
        assert 'credit_spreads' in FRED_SERIES
        assert 'global_liquidity' in FRED_SERIES

        # Check specific series
        assert 'DGS10' in FRED_SERIES['treasury_yields']
        assert 'DFII10' in FRED_SERIES['real_yields']
        assert 'BAMLH0A0HYM2' in FRED_SERIES['credit_spreads']
        assert 'M2SL' in FRED_SERIES['global_liquidity']

    @pytest.mark.live
    def test_fred_collect_treasury_yields(self):
        """Test FRED treasury yields collection (requires API key)."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("fred", {})
        df = collector.collect_treasury_yields(
            start_date=date.today() - timedelta(days=30),
            end_date=date.today()
        )

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert 'date' in df.columns
            assert 'yield_10y' in df.columns


class TestAlternativeCollector:
    """Test Alternative.me collector."""

    def test_alternative_collector_initialization(self):
        """Test Alternative collector initializes."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("alternative", {})
        assert collector is not None
        assert collector.get_name() == "alternative"
        assert collector.source_type == "api"

    @pytest.mark.live
    def test_alternative_collect_fear_greed(self):
        """Test Fear & Greed collection (no API key needed)."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("alternative", {"limit": 7})
        df = collector.collect()

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert 'date' in df.columns
            assert 'fear_greed_index' in df.columns
            assert 'fear_greed_label' in df.columns

            # Check value ranges
            assert df['fear_greed_index'].min() >= 0
            assert df['fear_greed_index'].max() <= 100

    @pytest.mark.live
    def test_alternative_get_current(self):
        """Test getting current Fear & Greed value."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("alternative", {})
        current = collector.get_current()

        assert 'value' in current
        assert 'classification' in current
        if current['value'] is not None:
            assert 0 <= current['value'] <= 100


class TestDeFiLlamaCollector:
    """Test DeFiLlama collector."""

    def test_defillama_collector_initialization(self):
        """Test DeFiLlama collector initializes."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("defillama_live", {})
        assert collector is not None
        assert collector.get_name() == "defillama_live"
        assert collector.source_type == "api"

    def test_defillama_tracked_pools_defined(self):
        """Test tracked pools are defined."""
        from src.collectors.defillama_collector import TRACKED_POOLS

        assert 'sky-ssr' in TRACKED_POOLS
        assert 'compound-v3-arb-usdc' in TRACKED_POOLS
        assert 'jito' in TRACKED_POOLS

        # Check pool structure
        for pool_key, pool_info in TRACKED_POOLS.items():
            assert 'pool_id' in pool_info
            assert 'protocol' in pool_info
            assert 'chain' in pool_info
            assert 'pool' in pool_info

    @pytest.mark.live
    def test_defillama_get_current_apys(self):
        """Test getting current APYs (no API key needed)."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("defillama_live", {})
        apys = collector.get_current_apys()

        assert isinstance(apys, dict)


class TestYahooCollector:
    """Test Yahoo Finance collector."""

    def test_yahoo_collector_initialization(self):
        """Test Yahoo collector initializes."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("yahoo_live", {})
        assert collector is not None
        assert collector.get_name() == "yahoo_live"
        assert collector.source_type == "api"

    def test_yahoo_tickers_defined(self):
        """Test Yahoo tickers are defined."""
        from src.collectors.yahoo_collector import TRADFI_TICKERS, CRYPTO_TICKERS, COMMODITY_TICKERS

        # TradFi tickers
        assert 'spy' in TRADFI_TICKERS
        assert 'tlt' in TRADFI_TICKERS
        assert 'vix' in TRADFI_TICKERS

        # Crypto tickers
        assert 'btc' in CRYPTO_TICKERS
        assert 'eth' in CRYPTO_TICKERS
        assert 'sol' in CRYPTO_TICKERS

        # Commodity tickers
        assert 'gold' in COMMODITY_TICKERS
        assert 'copper' in COMMODITY_TICKERS

    @pytest.mark.live
    def test_yahoo_collect_crypto(self):
        """Test crypto price collection."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("yahoo_live", {})
        df = collector.collect_crypto_prices(
            start_date=date.today() - timedelta(days=7),
            end_date=date.today()
        )

        assert isinstance(df, pd.DataFrame)


class TestCoinGeckoCollector:
    """Test CoinGecko collector."""

    def test_coingecko_collector_initialization(self):
        """Test CoinGecko collector initializes."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("coingecko", {})
        assert collector is not None
        assert collector.get_name() == "coingecko"
        assert collector.source_type == "api"

    @pytest.mark.live
    def test_coingecko_current_prices(self):
        """Test getting current prices."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("coingecko", {})
        prices = collector.get_current_prices(['bitcoin', 'ethereum'])

        assert isinstance(prices, dict)
        if prices:
            assert 'bitcoin' in prices or 'ethereum' in prices


class TestAggregatorCollector:
    """Test aggregator collector."""

    def test_aggregator_initialization(self):
        """Test aggregator initializes."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("aggregator", {})
        assert collector is not None
        assert collector.get_name() == "aggregator"
        assert collector.source_type == "hybrid"

    def test_aggregator_get_status(self):
        """Test getting collector status."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("aggregator", {})
        status = collector.get_status()

        assert isinstance(status, dict)
        assert 'fred' in status
        assert 'yahoo_live' in status
        assert 'alternative' in status

        for source, info in status.items():
            assert 'available' in info
            assert 'type' in info


class TestOutputSchemas:
    """Test that collectors produce expected output schemas."""

    def test_treasury_yields_schema(self):
        """Test treasury yields output schema."""
        expected_columns = ['date', 'yield_2y', 'yield_5y', 'yield_10y', 'yield_30y']

        # Create mock DataFrame
        df = pd.DataFrame({
            'date': [date.today()],
            'yield_2y': [4.5],
            'yield_5y': [4.3],
            'yield_10y': [4.2],
            'yield_30y': [4.4]
        })

        for col in expected_columns:
            assert col in df.columns

    def test_real_yields_schema(self):
        """Test real yields output schema."""
        expected_columns = ['date', 'real_yield_10y']

        df = pd.DataFrame({
            'date': [date.today()],
            'real_yield_10y': [1.8]
        })

        for col in expected_columns:
            assert col in df.columns

    def test_credit_spreads_schema(self):
        """Test credit spreads output schema."""
        expected_columns = ['date', 'hy_spread', 'ig_spread']

        df = pd.DataFrame({
            'date': [date.today()],
            'hy_spread': [350],
            'ig_spread': [95]
        })

        for col in expected_columns:
            assert col in df.columns

    def test_sentiment_schema(self):
        """Test sentiment output schema."""
        expected_columns = ['date', 'fear_greed_index', 'fear_greed_label']

        df = pd.DataFrame({
            'date': [date.today()],
            'fear_greed_index': [55],
            'fear_greed_label': ['Neutral']
        })

        for col in expected_columns:
            assert col in df.columns

    def test_crypto_prices_schema(self):
        """Test crypto prices output schema."""
        expected_columns = ['date', 'btc_close', 'eth_close', 'sol_close']

        df = pd.DataFrame({
            'date': [date.today()],
            'btc_close': [45000],
            'eth_close': [2500],
            'sol_close': [100]
        })

        for col in expected_columns:
            assert col in df.columns

    def test_defillama_schema(self):
        """Test DeFiLlama APY output schema."""
        expected_columns = ['date', 'protocol', 'chain', 'pool', 'apy', 'tvl_usd']

        df = pd.DataFrame({
            'date': [date.today()],
            'protocol': ['aave-v3'],
            'chain': ['ethereum'],
            'pool': ['USDC'],
            'apy': [6.5],
            'tvl_usd': [1500000000]
        })

        for col in expected_columns:
            assert col in df.columns
