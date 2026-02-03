"""
Alternative.me Collector for Fear & Greed Index.

Collects crypto market sentiment data:
- Fear & Greed Index (0-100 scale)
- Sentiment classification (Extreme Fear, Fear, Neutral, Greed, Extreme Greed)

API Documentation: https://alternative.me/crypto/fear-and-greed-index/
"""

import logging
from datetime import date, datetime
from typing import Optional, Dict, Any
import pandas as pd

from src.collectors.http_client import RateLimitedClient, get_alternative_client, APIError
from src.registries import CollectorRegistry, Collector
from src.utils.file_io import safe_write_csv

logger = logging.getLogger(__name__)

# API endpoint
ALTERNATIVE_FNG_URL = "https://api.alternative.me/fng/"


@CollectorRegistry.register("alternative")
class AlternativeCollector(Collector):
    """
    Collector for Alternative.me Fear & Greed Index.

    The Fear & Greed Index ranges from 0 (Extreme Fear) to 100 (Extreme Greed).

    Classification:
    - 0-24: Extreme Fear
    - 25-44: Fear
    - 45-55: Neutral
    - 56-74: Greed
    - 75-100: Extreme Greed

    Usage:
        collector = CollectorRegistry.get_instance().get("alternative", {})
        df = collector.collect()
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Alternative.me collector.

        Args:
            config: Configuration dict with optional keys:
                - limit: Number of days to fetch (default: 365)
        """
        self.config = config
        self._client: Optional[RateLimitedClient] = None

    def _get_client(self) -> RateLimitedClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = get_alternative_client()
        return self._client

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect Fear & Greed Index data.

        Args:
            start_date: Start date (used to calculate limit)
            end_date: End date (not used, API returns from today backwards)

        Returns:
            DataFrame with columns: date, fear_greed_index, fear_greed_label
        """
        client = self._get_client()

        # Calculate limit based on date range
        if start_date:
            days_back = (date.today() - start_date).days
            limit = min(days_back + 1, 2000)  # API max is ~2000
        else:
            limit = self.config.get('limit', 365)

        params = {
            'limit': limit,
            'format': 'json'
        }

        logger.info(f"Fetching Fear & Greed Index (limit={limit} days)")

        try:
            data = client.get(ALTERNATIVE_FNG_URL, params=params)
            fng_data = data.get('data', [])

            if not fng_data:
                logger.warning("No Fear & Greed data returned")
                return pd.DataFrame(columns=['date', 'fear_greed_index', 'fear_greed_label'])

            # Convert to DataFrame
            records = []
            for item in fng_data:
                timestamp = int(item.get('timestamp', 0))
                dt = datetime.fromtimestamp(timestamp)

                records.append({
                    'date': dt.strftime('%Y-%m-%d'),
                    'fear_greed_index': int(item.get('value', 0)),
                    'fear_greed_label': item.get('value_classification', 'Unknown')
                })

            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)

            # Filter by date range if specified
            if start_date:
                df = df[df['date'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['date'] <= pd.to_datetime(end_date)]

            logger.info(f"Fetched {len(df)} Fear & Greed observations")
            return df

        except APIError as e:
            logger.error(f"Failed to fetch Fear & Greed Index: {e}")
            return pd.DataFrame(columns=['date', 'fear_greed_index', 'fear_greed_label'])

    def get_current(self) -> Dict[str, Any]:
        """
        Get current Fear & Greed Index value.

        Returns:
            Dictionary with current index value and classification
        """
        client = self._get_client()

        try:
            data = client.get(ALTERNATIVE_FNG_URL, params={'limit': 1})
            fng_data = data.get('data', [])

            if fng_data:
                current = fng_data[0]
                return {
                    'value': int(current.get('value', 0)),
                    'classification': current.get('value_classification', 'Unknown'),
                    'timestamp': datetime.fromtimestamp(int(current.get('timestamp', 0)))
                }

        except APIError as e:
            logger.error(f"Failed to get current Fear & Greed: {e}")

        return {'value': None, 'classification': 'Unknown', 'timestamp': None}

    def get_name(self) -> str:
        """Return collector name."""
        return "alternative"

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
            filepath = output_path / 'sentiment_indicators.csv'
            if safe_write_csv(df, filepath):
                logger.info(f"Saved sentiment indicators to {filepath}")
                return str(filepath)

        return ""
