"""
File loader for bundled historical data.

Loads CSV files from the data/ directory with error handling
and audit trail integration.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
from datetime import date, datetime
import logging

from config.settings import DATA_DIR
from src.utils.errors import DataNotFoundError, DataCorruptError, graceful_degradation
from src.utils.audit import get_audit_trail

logger = logging.getLogger(__name__)


class FileLoader:
    """Load bundled historical data from CSV files."""

    # V3 schema file mappings (from live collectors)
    FILES = {
        'defillama': 'defillama_historical_apy.csv',
        'yahoo': 'crypto_prices.csv',  # V3: wide format with btc_close, eth_close, sol_close
        'jupiter': 'jupiter_jlp_historical_apy.csv',
        'jito': 'jito_historical_apy.csv',  # P0-ADDENDUM-1: dedicated Jito APY file
        'perps': 'perps_lp_combined_apy.csv',
        # Additional v3 sources
        'crypto_prices': 'crypto_prices.csv',
        'treasury_yields': 'treasury_yields.csv',
        'sentiment': 'sentiment_indicators.csv',
        'tradfi': 'tradfi_benchmark_data.csv',
    }

    # Fallback for legacy file names (pre-v3)
    LEGACY_FILES = {
        'yahoo': 'yahoo_historical_prices.csv',  # Legacy: long format with symbol column
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

        Raises:
            DataNotFoundError: If file doesn't exist
            DataCorruptError: If file is malformed
        """
        if source not in self.FILES:
            available = ", ".join(self.FILES.keys())
            raise ValueError(
                f"Unknown source: '{source}'. Available sources: {available}"
            )

        filepath = self.data_dir / self.FILES[source]

        # Try legacy file if v3 file doesn't exist
        if not filepath.exists() and source in self.LEGACY_FILES:
            legacy_path = self.data_dir / self.LEGACY_FILES[source]
            if legacy_path.exists():
                logger.info(f"Using legacy file: {legacy_path}")
                filepath = legacy_path

        if not filepath.exists():
            raise DataNotFoundError(
                filepath=str(filepath),
                data_type=f'{source} historical data'
            )

        logger.info(f"Loading {source} data from {filepath}")

        # Log to audit trail if active
        audit = get_audit_trail()
        if audit:
            audit.log_input_file(filepath)

        # Load CSV with error handling
        try:
            df = pd.read_csv(filepath)
        except pd.errors.EmptyDataError:
            raise DataCorruptError(
                filepath=str(filepath),
                reason="File is empty"
            )
        except pd.errors.ParserError as e:
            raise DataCorruptError(
                filepath=str(filepath),
                reason=f"CSV parsing failed: {e}"
            )

        # Validate data has expected structure
        if df.empty:
            logger.warning(f"Data file {source} is empty")
            return df

        # Parse date column
        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'])
            except Exception as e:
                raise DataCorruptError(
                    filepath=str(filepath),
                    reason=f"Failed to parse date column: {e}"
                )

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
            except (FileNotFoundError, DataNotFoundError) as e:
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
        # V3 schema uses 'protocol', legacy uses 'project'
        if 'protocol' in df.columns:
            return sorted(df['protocol'].unique().tolist())
        elif 'project' in df.columns:
            return sorted(df['project'].unique().tolist())
        return []

    def get_available_symbols(self, source: str = 'yahoo') -> list[str]:
        """Get list of symbols available in price data."""
        df = self.load(source)
        # Legacy long format has 'symbol' column
        if 'symbol' in df.columns:
            return sorted(df['symbol'].unique().tolist())
        # V3 wide format has btc_close, eth_close, sol_close columns
        symbols = []
        for col in df.columns:
            if col.endswith('_close'):
                symbol = col.replace('_close', '').upper()
                symbols.append(symbol)
        return sorted(symbols) if symbols else []


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

        # Filter to specific protocol (V3 uses 'protocol', legacy uses 'project')
        protocol_col = 'protocol' if 'protocol' in df.columns else 'project'
        protocol_df = df[df[protocol_col] == protocol].copy()

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

        # Check if V3 wide format (btc_close, eth_close, sol_close)
        close_col = f'{symbol.lower()}_close'
        if close_col in df.columns:
            # V3 wide format - extract single symbol
            symbol_df = df[['date', close_col]].copy()
            symbol_df = symbol_df.rename(columns={close_col: 'close'})
            symbol_df = symbol_df.set_index('date')
        elif 'symbol' in df.columns:
            # Legacy long format - filter to specific symbol
            symbol_df = df[df['symbol'] == symbol].copy()
            if symbol_df.empty:
                logger.warning(f"No price data found for symbol: {symbol}")
                return pd.DataFrame()
            symbol_df = symbol_df.set_index('date')
        else:
            logger.warning(f"No price data found for symbol: {symbol}")
            return pd.DataFrame()

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
