"""
FRED (Federal Reserve Economic Data) Collector.

Collects macro economic data:
- Treasury yields (DGS2, DGS5, DGS10, DGS30)
- Real yields (DFII10 - 10Y TIPS)
- Credit spreads (BAMLH0A0HYM2 - High Yield OAS)
- M2 money supply (M2SL)

API Documentation: https://fred.stlouisfed.org/docs/api/fred/
"""

import logging
from datetime import date, datetime
from typing import Optional, Dict, List, Any
import pandas as pd

from config.settings import settings
from src.collectors.http_client import RateLimitedClient, get_fred_client, APIError
from src.registries import CollectorRegistry, Collector
from src.utils.file_io import safe_write_csv

logger = logging.getLogger(__name__)

# FRED API base URL
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# Series definitions
FRED_SERIES = {
    'treasury_yields': {
        'DGS2': 'yield_2y',
        'DGS5': 'yield_5y',
        'DGS10': 'yield_10y',
        'DGS30': 'yield_30y',
    },
    'real_yields': {
        'DFII10': 'real_yield_10y',
    },
    'credit_spreads': {
        'BAMLH0A0HYM2': 'hy_spread',
        'BAMLC0A4CBBB': 'ig_spread',
    },
    'global_liquidity': {
        'M2SL': 'us_m2_bn',
    }
}


@CollectorRegistry.register("fred")
class FREDCollector(Collector):
    """
    Collector for FRED (Federal Reserve Economic Data).

    Fetches macro economic indicators including treasury yields,
    real yields, credit spreads, and money supply data.

    Usage:
        collector = CollectorRegistry.get_instance().get("fred", {})
        data = collector.collect()  # Returns dict of DataFrames
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize FRED collector.

        Args:
            config: Configuration dict with optional keys:
                - start_date: Start date for data (default: 2020-01-01)
                - end_date: End date for data (default: today)
        """
        self.config = config
        self._client: Optional[RateLimitedClient] = None
        self._api_key: Optional[str] = None

    def _get_client(self) -> RateLimitedClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = get_fred_client()
        return self._client

    def _get_api_key(self) -> str:
        """Get FRED API key."""
        if self._api_key is None:
            self._api_key = settings.require('FRED_API_KEY')
        return self._api_key

    def _fetch_series(
        self,
        series_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Fetch a single FRED series.

        Args:
            series_id: FRED series ID (e.g., 'DGS10')
            start_date: Start date for observations
            end_date: End date for observations

        Returns:
            DataFrame with date and value columns
        """
        client = self._get_client()
        api_key = self._get_api_key()

        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
        }

        if start_date:
            params['observation_start'] = start_date.isoformat()
        if end_date:
            params['observation_end'] = end_date.isoformat()

        logger.info(f"Fetching FRED series: {series_id}")

        try:
            data = client.get(FRED_BASE_URL, params=params)
            observations = data.get('observations', [])

            if not observations:
                logger.warning(f"No data returned for series {series_id}")
                return pd.DataFrame(columns=['date', 'value'])

            # Convert to DataFrame
            df = pd.DataFrame(observations)
            df['date'] = pd.to_datetime(df['date'])

            # Handle missing values (FRED uses '.' for missing)
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.dropna(subset=['value'])

            df = df[['date', 'value']].sort_values('date').reset_index(drop=True)

            logger.info(f"Fetched {len(df)} observations for {series_id}")
            return df

        except APIError as e:
            logger.error(f"Failed to fetch {series_id}: {e}")
            return pd.DataFrame(columns=['date', 'value'])

    def collect_treasury_yields(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect treasury yields (2Y, 5Y, 10Y, 30Y).

        Returns:
            DataFrame with columns: date, yield_2y, yield_5y, yield_10y, yield_30y
        """
        series_map = FRED_SERIES['treasury_yields']
        result_df = None

        for series_id, column_name in series_map.items():
            df = self._fetch_series(series_id, start_date, end_date)
            df = df.rename(columns={'value': column_name})

            if result_df is None:
                result_df = df
            else:
                result_df = result_df.merge(df, on='date', how='outer')

        if result_df is not None:
            result_df = result_df.sort_values('date').reset_index(drop=True)
            # Forward fill missing values
            result_df = result_df.ffill()

        return result_df if result_df is not None else pd.DataFrame()

    def collect_real_yields(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect real yields (10Y TIPS).

        Returns:
            DataFrame with columns: date, real_yield_10y
        """
        series_map = FRED_SERIES['real_yields']
        result_df = None

        for series_id, column_name in series_map.items():
            df = self._fetch_series(series_id, start_date, end_date)
            df = df.rename(columns={'value': column_name})

            if result_df is None:
                result_df = df
            else:
                result_df = result_df.merge(df, on='date', how='outer')

        if result_df is not None:
            result_df = result_df.sort_values('date').reset_index(drop=True)

        return result_df if result_df is not None else pd.DataFrame()

    def collect_credit_spreads(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect credit spreads (High Yield and Investment Grade).

        Returns:
            DataFrame with columns: date, hy_spread, ig_spread
        """
        series_map = FRED_SERIES['credit_spreads']
        result_df = None

        for series_id, column_name in series_map.items():
            df = self._fetch_series(series_id, start_date, end_date)
            df = df.rename(columns={'value': column_name})

            if result_df is None:
                result_df = df
            else:
                result_df = result_df.merge(df, on='date', how='outer')

        if result_df is not None:
            result_df = result_df.sort_values('date').reset_index(drop=True)

        return result_df if result_df is not None else pd.DataFrame()

    def collect_global_liquidity(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect M2 money supply data.

        Returns:
            DataFrame with columns: date, us_m2_bn, us_m2_yoy
        """
        df = self._fetch_series('M2SL', start_date, end_date)
        df = df.rename(columns={'value': 'us_m2_bn'})

        if not df.empty:
            # Calculate year-over-year change
            df = df.sort_values('date').reset_index(drop=True)
            df['us_m2_yoy'] = df['us_m2_bn'].pct_change(periods=12) * 100

        return df

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Collect all FRED data.

        Args:
            start_date: Start date (default from config or 2020-01-01)
            end_date: End date (default from config or today)

        Returns:
            Dictionary with keys:
                - treasury_yields
                - real_yields
                - credit_spreads
                - global_liquidity
        """
        # Use config defaults if not specified
        if start_date is None:
            start_str = self.config.get('start_date', '2020-01-01')
            start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        if end_date is None:
            end_str = self.config.get('end_date')
            end_date = datetime.strptime(end_str, '%Y-%m-%d').date() if end_str else date.today()

        logger.info(f"Collecting FRED data from {start_date} to {end_date}")

        return {
            'treasury_yields': self.collect_treasury_yields(start_date, end_date),
            'real_yields': self.collect_real_yields(start_date, end_date),
            'credit_spreads': self.collect_credit_spreads(start_date, end_date),
            'global_liquidity': self.collect_global_liquidity(start_date, end_date),
        }

    def get_name(self) -> str:
        """Return collector name."""
        return "fred"

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
            'treasury_yields': 'treasury_yields.csv',
            'real_yields': 'real_yields.csv',
            'credit_spreads': 'credit_spreads.csv',
            'global_liquidity': 'global_liquidity.csv',
        }

        for key, filename in file_map.items():
            if key in data and not data[key].empty:
                filepath = output_path / filename
                if safe_write_csv(data[key], filepath):
                    paths[key] = str(filepath)
                    logger.info(f"Saved {key} to {filepath}")

        return paths
