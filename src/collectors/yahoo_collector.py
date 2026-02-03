"""
Yahoo Finance Collector for market data.

Collects:
- Equity indices (S&P 500, NASDAQ, VIX)
- ETFs (SPY, TLT, IWM, XLF, XLU)
- Crypto prices (BTC, ETH, SOL)
- Commodities (Gold, Copper)
- Calculates rotation indicators

Uses yfinance library for data access.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Optional, Dict, List, Any
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    yf = None
    logging.warning("yfinance not installed. Install with: pip install yfinance")

from src.registries import CollectorRegistry, Collector
from src.utils.file_io import safe_write_csv

logger = logging.getLogger(__name__)

# Ticker definitions
TRADFI_TICKERS = {
    'sp500': '^GSPC',
    'nasdaq': '^IXIC',
    'vix': '^VIX',
    'spy': 'SPY',
    'tlt': 'TLT',
    'iwm': 'IWM',
    'xlf': 'XLF',
    'xlu': 'XLU',
}

CRYPTO_TICKERS = {
    'btc': 'BTC-USD',
    'eth': 'ETH-USD',
    'sol': 'SOL-USD',
}

COMMODITY_TICKERS = {
    'gold': 'GC=F',
    'copper': 'HG=F',
}


@CollectorRegistry.register("yahoo_live")
class YahooCollector(Collector):
    """
    Collector for Yahoo Finance market data.

    Fetches equity indices, ETFs, crypto prices, and commodities.
    Also calculates rotation indicators (SPY/TLT, XLF/XLU, IWM/SPY, Copper/Gold).

    Usage:
        collector = CollectorRegistry.get_instance().get("yahoo_live", {})
        data = collector.collect()  # Returns dict of DataFrames
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Yahoo Finance collector.

        Args:
            config: Configuration dict with optional keys:
                - start_date: Start date for data (default: 1 year ago)
                - end_date: End date for data (default: today)
        """
        self.config = config

        if yf is None:
            raise ImportError("yfinance is required. Install with: pip install yfinance")

    def _download_tickers(
        self,
        tickers: List[str],
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """
        Download data for multiple tickers.

        Args:
            tickers: List of Yahoo Finance ticker symbols
            start_date: Start date
            end_date: End date

        Returns:
            DataFrame with OHLCV data for all tickers
        """
        logger.info(f"Downloading {len(tickers)} tickers from Yahoo Finance")

        try:
            # yfinance expects string dates
            start_str = start_date.isoformat()
            end_str = (end_date + timedelta(days=1)).isoformat()  # end is exclusive

            data = yf.download(
                tickers,
                start=start_str,
                end=end_str,
                progress=False,
                auto_adjust=True
            )

            return data

        except Exception as e:
            logger.error(f"Failed to download from Yahoo Finance: {e}")
            return pd.DataFrame()

    def collect_tradfi_benchmark(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect TradFi benchmark data.

        Returns:
            DataFrame with columns:
            date, sp500_close, nasdaq_close, vix_close, iwm_close,
            spy_close, tlt_close, xlf_close, xlu_close
        """
        if start_date is None:
            start_date = date.today() - timedelta(days=365)
        if end_date is None:
            end_date = date.today()

        tickers = list(TRADFI_TICKERS.values())
        data = self._download_tickers(tickers, start_date, end_date)

        if data.empty:
            return pd.DataFrame()

        # Extract closing prices
        result = pd.DataFrame()
        result['date'] = data.index

        # Handle both single and multi-ticker DataFrame structures
        if len(tickers) == 1:
            result[f'{list(TRADFI_TICKERS.keys())[0]}_close'] = data['Close'].values
        else:
            for name, ticker in TRADFI_TICKERS.items():
                if ('Close', ticker) in data.columns:
                    result[f'{name}_close'] = data['Close'][ticker].values
                elif ticker in data.columns:
                    result[f'{name}_close'] = data[ticker]['Close'].values if hasattr(data[ticker], 'Close') else None

        result = result.reset_index(drop=True)

        # Rename columns to match expected schema
        column_map = {
            'sp500_close': 'sp500_close',
            'nasdaq_close': 'nasdaq_close',
            'vix_close': 'vix_close',
            'spy_close': 'spy_close',
            'tlt_close': 'tlt_close',
            'iwm_close': 'iwm_close',
            'xlf_close': 'xlf_close',
            'xlu_close': 'xlu_close',
        }

        logger.info(f"Collected {len(result)} days of TradFi benchmark data")
        return result

    def collect_crypto_prices(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect crypto price data.

        Returns:
            DataFrame with columns: date, btc_close, eth_close, sol_close
        """
        if start_date is None:
            start_date = date.today() - timedelta(days=365)
        if end_date is None:
            end_date = date.today()

        tickers = list(CRYPTO_TICKERS.values())
        data = self._download_tickers(tickers, start_date, end_date)

        if data.empty:
            return pd.DataFrame()

        result = pd.DataFrame()
        result['date'] = data.index

        for name, ticker in CRYPTO_TICKERS.items():
            try:
                if ('Close', ticker) in data.columns:
                    result[f'{name}_close'] = data['Close'][ticker].values
            except Exception as e:
                logger.warning(f"Could not extract {name}: {e}")

        result = result.reset_index(drop=True)

        logger.info(f"Collected {len(result)} days of crypto price data")
        return result

    def collect_commodities(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect commodity price data.

        Returns:
            DataFrame with columns: date, gold_close, copper_close
        """
        if start_date is None:
            start_date = date.today() - timedelta(days=365)
        if end_date is None:
            end_date = date.today()

        tickers = list(COMMODITY_TICKERS.values())
        data = self._download_tickers(tickers, start_date, end_date)

        if data.empty:
            return pd.DataFrame()

        result = pd.DataFrame()
        result['date'] = data.index

        for name, ticker in COMMODITY_TICKERS.items():
            try:
                if ('Close', ticker) in data.columns:
                    result[f'{name}_close'] = data['Close'][ticker].values
            except Exception as e:
                logger.warning(f"Could not extract {name}: {e}")

        result = result.reset_index(drop=True)

        logger.info(f"Collected {len(result)} days of commodity data")
        return result

    def calculate_rotation_indicators(
        self,
        tradfi_df: pd.DataFrame,
        commodities_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate rotation indicators from price data.

        Ratios calculated:
        - SPY/TLT: Risk-on vs risk-off
        - XLF/XLU: Cyclical vs defensive
        - IWM/SPY: Small cap vs large cap
        - Copper/Gold: Economic optimism

        Returns:
            DataFrame with rotation ratios and signals
        """
        if tradfi_df.empty:
            return pd.DataFrame()

        result = pd.DataFrame()
        result['date'] = tradfi_df['date']

        # SPY/TLT ratio
        if 'spy_close' in tradfi_df.columns and 'tlt_close' in tradfi_df.columns:
            result['spy_tlt_ratio'] = tradfi_df['spy_close'] / tradfi_df['tlt_close']
            result['spy_tlt_ma50'] = result['spy_tlt_ratio'].rolling(50).mean()
            result['spy_tlt_signal'] = (result['spy_tlt_ratio'] > result['spy_tlt_ma50']).map(
                {True: 'Risk-On', False: 'Risk-Off'}
            )

        # XLF/XLU ratio
        if 'xlf_close' in tradfi_df.columns and 'xlu_close' in tradfi_df.columns:
            result['xlf_xlu_ratio'] = tradfi_df['xlf_close'] / tradfi_df['xlu_close']

        # IWM/SPY ratio
        if 'iwm_close' in tradfi_df.columns and 'spy_close' in tradfi_df.columns:
            result['iwm_spy_ratio'] = tradfi_df['iwm_close'] / tradfi_df['spy_close']

        # Copper/Gold ratio
        if not commodities_df.empty:
            # Merge on date
            merged = result.merge(
                commodities_df[['date', 'gold_close', 'copper_close']],
                on='date',
                how='left'
            )
            if 'gold_close' in merged.columns and 'copper_close' in merged.columns:
                # Note: Copper is in cents/lb, Gold in $/oz - ratio will be small
                result['copper_gold_ratio'] = merged['copper_close'] / merged['gold_close']

        logger.info(f"Calculated rotation indicators for {len(result)} days")
        return result

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Collect all Yahoo Finance data.

        Args:
            start_date: Start date (default from config or 1 year ago)
            end_date: End date (default from config or today)

        Returns:
            Dictionary with keys:
                - tradfi_benchmark
                - crypto_prices
                - commodities
                - rotation_indicators
        """
        # Use config defaults if not specified
        if start_date is None:
            start_str = self.config.get('start_date')
            if start_str:
                start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
            else:
                start_date = date.today() - timedelta(days=365)

        if end_date is None:
            end_str = self.config.get('end_date')
            if end_str:
                end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
            else:
                end_date = date.today()

        logger.info(f"Collecting Yahoo Finance data from {start_date} to {end_date}")

        tradfi = self.collect_tradfi_benchmark(start_date, end_date)
        crypto = self.collect_crypto_prices(start_date, end_date)
        commodities = self.collect_commodities(start_date, end_date)
        rotation = self.calculate_rotation_indicators(tradfi, commodities)

        return {
            'tradfi_benchmark': tradfi,
            'crypto_prices': crypto,
            'commodities': commodities,
            'rotation_indicators': rotation,
        }

    def get_name(self) -> str:
        """Return collector name."""
        return "yahoo_live"

    @property
    def source_type(self) -> str:
        """Return source type."""
        return "api"

    def save_to_csv(
        self,
        output_dir: str = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, str]:
        """
        Collect data and save to CSV files.

        Args:
            output_dir: Output directory (default: data/)
            start_date: Start date for data
            end_date: End date for data

        Returns:
            Dictionary mapping data type to file path
        """
        from pathlib import Path
        from config.settings import DATA_DIR

        output_path = Path(output_dir) if output_dir else DATA_DIR

        data = self.collect(start_date, end_date)
        paths = {}

        file_map = {
            'tradfi_benchmark': 'tradfi_benchmark_data.csv',
            'crypto_prices': 'crypto_prices.csv',
            'commodities': 'commodities.csv',
            'rotation_indicators': 'rotation_indicators.csv',
        }

        for key, filename in file_map.items():
            if key in data and not data[key].empty:
                filepath = output_path / filename
                if safe_write_csv(data[key], filepath):
                    paths[key] = str(filepath)
                    logger.info(f"Saved {key} to {filepath}")

        return paths
