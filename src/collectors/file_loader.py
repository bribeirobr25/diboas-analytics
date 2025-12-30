"""
File loader for bundled historical data.

Loads CSV files from the data/ directory.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
from datetime import date, datetime
import logging

from config.settings import DATA_DIR

logger = logging.getLogger(__name__)


class FileLoader:
    """Load bundled historical data from CSV files."""

    FILES = {
        'defillama': 'defillama_historical_apy.csv',
        'yahoo': 'yahoo_historical_prices.csv',
        'jupiter': 'jupiter_jlp_historical_apy.csv',
        'perps': 'perps_lp_combined_apy.csv'
    }

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or DATA_DIR

    def load(
        self,
        source: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Load data from bundled CSV file.

        Args:
            source: Data source identifier ('defillama', 'yahoo', 'jupiter', 'perps')
            start_date: Optional filter for start date
            end_date: Optional filter for end date

        Returns:
            DataFrame with loaded data
        """
        if source not in self.FILES:
            raise ValueError(f"Unknown source: {source}. Available: {list(self.FILES.keys())}")

        filepath = self.data_dir / self.FILES[source]

        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")

        logger.info(f"Loading {source} data from {filepath}")

        # Load CSV with date parsing
        df = pd.read_csv(filepath)

        # Parse date column
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

            # Filter by date range if specified
            if start_date:
                df = df[df['date'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['date'] <= pd.to_datetime(end_date)]

            # Sort by date
            df = df.sort_values('date').reset_index(drop=True)

        logger.info(f"Loaded {len(df)} rows from {source}")
        return df

    def load_all(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict[str, pd.DataFrame]:
        """
        Load all bundled data files.

        Returns:
            Dictionary mapping source name to DataFrame
        """
        data = {}
        for source in self.FILES.keys():
            try:
                data[source] = self.load(source, start_date, end_date)
            except FileNotFoundError as e:
                logger.warning(f"Could not load {source}: {e}")
                data[source] = pd.DataFrame()
        return data

    def get_date_range(self, source: str) -> tuple[date, date]:
        """Get the date range available in a data file."""
        df = self.load(source)
        if 'date' not in df.columns or df.empty:
            raise ValueError(f"No date data available for {source}")

        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        return min_date, max_date

    def get_available_protocols(self, source: str = 'defillama') -> list[str]:
        """Get list of protocols available in the data."""
        df = self.load(source)
        if 'project' in df.columns:
            return sorted(df['project'].unique().tolist())
        return []

    def get_available_symbols(self, source: str = 'yahoo') -> list[str]:
        """Get list of symbols available in price data."""
        df = self.load(source)
        if 'symbol' in df.columns:
            return sorted(df['symbol'].unique().tolist())
        return []


class DataAggregator:
    """
    Aggregate data from multiple sources for simulation.

    Combines APY data, price data, and JLP data into unified structures.
    """

    def __init__(self, file_loader: FileLoader = None):
        self.loader = file_loader or FileLoader()

    def get_protocol_apy_series(
        self,
        protocol: str,
        start_date: date,
        end_date: date
    ) -> pd.Series:
        """
        Get daily APY series for a protocol.

        Args:
            protocol: Protocol identifier (e.g., 'aave-v3', 'lido')
            start_date: Start date
            end_date: End date

        Returns:
            Series with date index and APY values
        """
        df = self.loader.load('defillama', start_date, end_date)

        # Filter to specific protocol
        protocol_df = df[df['project'] == protocol].copy()

        if protocol_df.empty:
            logger.warning(f"No data found for protocol: {protocol}")
            return pd.Series(dtype=float)

        # Create daily series with interpolation for missing dates
        protocol_df = protocol_df.set_index('date')

        # Take mean APY if multiple pools per day
        apy_series = protocol_df.groupby('date')['apy'].mean()

        # Reindex to full date range
        date_range = pd.date_range(start_date, end_date, freq='D')
        apy_series = apy_series.reindex(date_range)

        # Forward fill missing values
        apy_series = apy_series.ffill().bfill()

        return apy_series

    def get_price_series(
        self,
        symbol: str,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """
        Get daily price data for a crypto asset.

        Args:
            symbol: Asset symbol (BTC, ETH, SOL)
            start_date: Start date
            end_date: End date

        Returns:
            DataFrame with date index and OHLCV columns
        """
        df = self.loader.load('yahoo', start_date, end_date)

        # Filter to specific symbol
        symbol_df = df[df['symbol'] == symbol].copy()

        if symbol_df.empty:
            logger.warning(f"No price data found for symbol: {symbol}")
            return pd.DataFrame()

        symbol_df = symbol_df.set_index('date')

        # Reindex to full date range
        date_range = pd.date_range(start_date, end_date, freq='D')
        symbol_df = symbol_df.reindex(date_range)

        # Forward fill missing values
        symbol_df = symbol_df.ffill().bfill()

        return symbol_df

    def get_jlp_apy_series(
        self,
        start_date: date,
        end_date: date
    ) -> pd.Series:
        """
        Get daily JLP APY series.

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            Series with date index and APY values
        """
        df = self.loader.load('jupiter', start_date, end_date)

        if df.empty:
            logger.warning("No JLP data found")
            return pd.Series(dtype=float)

        df = df.set_index('date')
        apy_series = df['apy']

        # Reindex to full date range
        date_range = pd.date_range(start_date, end_date, freq='D')
        apy_series = apy_series.reindex(date_range)

        # Forward fill missing values
        apy_series = apy_series.ffill().bfill()

        return apy_series

    def calculate_daily_returns(
        self,
        symbol: str,
        start_date: date,
        end_date: date
    ) -> pd.Series:
        """
        Calculate daily returns for a crypto asset.

        Returns:
            Series with daily percentage returns
        """
        prices = self.get_price_series(symbol, start_date, end_date)

        if prices.empty or 'close' not in prices.columns:
            return pd.Series(dtype=float)

        returns = prices['close'].pct_change()
        returns = returns.fillna(0)  # First day has no return

        return returns
