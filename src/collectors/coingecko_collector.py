"""
CoinGecko Collector for crypto market data.

Collects:
- Current prices for BTC, ETH, SOL
- Market caps and 24h volumes
- Historical price data (backup to Yahoo)
- Market dominance ratios

API Documentation: https://www.coingecko.com/en/api/documentation
"""

import logging
from datetime import date, datetime, timedelta
from typing import Optional, Dict, List, Any
import pandas as pd

from config.settings import settings
from src.collectors.http_client import RateLimitedClient, get_coingecko_client, APIError
from src.registries import CollectorRegistry, Collector
from src.utils.file_io import safe_write_csv

logger = logging.getLogger(__name__)

# CoinGecko API endpoints
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Coin ID mapping
COIN_IDS = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'sol': 'solana',
}


@CollectorRegistry.register("coingecko")
class CoinGeckoCollector(Collector):
    """
    Collector for CoinGecko crypto market data.

    Provides current and historical crypto price data,
    market caps, and dominance metrics.

    Usage:
        collector = CollectorRegistry.get_instance().get("coingecko", {})
        data = collector.collect()
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize CoinGecko collector.

        Args:
            config: Configuration dict with optional keys:
                - coins: List of coin IDs to fetch (default: btc, eth, sol)
        """
        self.config = config
        self._client: Optional[RateLimitedClient] = None
        self._api_key: Optional[str] = None

    def _get_client(self) -> RateLimitedClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = get_coingecko_client()
        return self._client

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers including API key if available."""
        headers = {}
        if self._api_key is None:
            self._api_key = settings.get('COINGECKO_API_KEY')

        if self._api_key:
            headers['x-cg-demo-api-key'] = self._api_key

        return headers

    def get_current_prices(
        self,
        coins: List[str] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get current prices for specified coins.

        Args:
            coins: List of coin IDs (default: btc, eth, sol)

        Returns:
            Dictionary mapping coin to price data
        """
        client = self._get_client()
        headers = self._get_headers()

        if coins is None:
            coins = list(COIN_IDS.values())

        coin_ids = ','.join(coins)

        url = f"{COINGECKO_BASE_URL}/simple/price"
        params = {
            'ids': coin_ids,
            'vs_currencies': 'usd',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true'
        }

        logger.info(f"Fetching current prices for {coins}")

        try:
            data = client.get(url, params=params, headers=headers)
            return data
        except APIError as e:
            logger.error(f"Failed to get current prices: {e}")
            return {}

    def get_market_chart(
        self,
        coin_id: str,
        days: int = 365,
        vs_currency: str = 'usd'
    ) -> pd.DataFrame:
        """
        Get historical market data for a coin.

        Args:
            coin_id: CoinGecko coin ID
            days: Number of days of history
            vs_currency: Currency for prices

        Returns:
            DataFrame with date, price, market_cap, volume
        """
        client = self._get_client()
        headers = self._get_headers()

        url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': vs_currency,
            'days': days
        }

        logger.info(f"Fetching {days} days of history for {coin_id}")

        try:
            data = client.get(url, params=params, headers=headers)

            prices = data.get('prices', [])
            market_caps = data.get('market_caps', [])
            volumes = data.get('total_volumes', [])

            records = []
            for i, (ts, price) in enumerate(prices):
                dt = datetime.fromtimestamp(ts / 1000)
                record = {
                    'date': dt.strftime('%Y-%m-%d'),
                    'price': price,
                }
                if i < len(market_caps):
                    record['market_cap'] = market_caps[i][1]
                if i < len(volumes):
                    record['volume'] = volumes[i][1]
                records.append(record)

            df = pd.DataFrame(records)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                # Group by date and take last value (API may return multiple per day)
                df = df.groupby('date').last().reset_index()
                df = df.sort_values('date').reset_index(drop=True)

            return df

        except APIError as e:
            logger.error(f"Failed to get market chart for {coin_id}: {e}")
            return pd.DataFrame()

    def get_global_data(self) -> Dict[str, Any]:
        """
        Get global crypto market data.

        Returns:
            Dictionary with total market cap, BTC dominance, etc.
        """
        client = self._get_client()
        headers = self._get_headers()

        url = f"{COINGECKO_BASE_URL}/global"

        try:
            data = client.get(url, headers=headers)
            return data.get('data', {})
        except APIError as e:
            logger.error(f"Failed to get global data: {e}")
            return {}

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect crypto price data for all tracked coins.

        Args:
            start_date: Start date (used to calculate days)
            end_date: End date (not directly used)

        Returns:
            DataFrame with columns: date, btc_close, eth_close, sol_close
        """
        # Calculate days to fetch
        if start_date:
            days = (date.today() - start_date).days
        else:
            days = 365

        # Fetch data for each coin
        coin_data = {}
        for short_name, coin_id in COIN_IDS.items():
            df = self.get_market_chart(coin_id, days=days)
            if not df.empty:
                coin_data[short_name] = df[['date', 'price']].rename(
                    columns={'price': f'{short_name}_close'}
                )

        if not coin_data:
            return pd.DataFrame(columns=['date', 'btc_close', 'eth_close', 'sol_close'])

        # Merge all coin data
        result = None
        for short_name, df in coin_data.items():
            if result is None:
                result = df
            else:
                result = result.merge(df, on='date', how='outer')

        if result is not None:
            result = result.sort_values('date').reset_index(drop=True)

            # Filter by date range
            if start_date:
                result = result[result['date'] >= pd.to_datetime(start_date)]
            if end_date:
                result = result[result['date'] <= pd.to_datetime(end_date)]

        logger.info(f"Collected {len(result) if result is not None else 0} days of crypto data")
        return result if result is not None else pd.DataFrame()

    def get_name(self) -> str:
        """Return collector name."""
        return "coingecko"

    @property
    def source_type(self) -> str:
        """Return source type."""
        return "api"

    def save_to_csv(
        self,
        output_dir: str = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> str:
        """
        Collect data and save to CSV file.

        Args:
            output_dir: Output directory (default: data/)
            start_date: Start date for data
            end_date: End date for data

        Returns:
            Path to saved file
        """
        from pathlib import Path
        from config.settings import DATA_DIR

        output_path = Path(output_dir) if output_dir else DATA_DIR

        df = self.collect(start_date, end_date)

        if not df.empty:
            filepath = output_path / 'crypto_prices_coingecko.csv'
            if safe_write_csv(df, filepath):
                logger.info(f"Saved CoinGecko crypto data to {filepath}")
                return str(filepath)

        return ""
