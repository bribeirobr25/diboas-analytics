"""
DeFiLlama Collector for DeFi protocol data.

Collects:
- Protocol APYs (Aave, Compound, Sky, Jito, etc.)
- Pool historical data
- TVL data

API Documentation: https://defillama.com/docs/api
"""

import logging
from datetime import date, datetime
from typing import Optional, Dict, List, Any
import pandas as pd

from src.collectors.http_client import RateLimitedClient, get_defillama_client, APIError
from src.registries import CollectorRegistry, Collector
from src.utils.file_io import safe_write_csv

logger = logging.getLogger(__name__)

# DeFiLlama API endpoints
DEFILLAMA_YIELDS_URL = "https://yields.llama.fi"
DEFILLAMA_PROTOCOL_URL = "https://api.llama.fi"

# Pool IDs for tracked protocols
TRACKED_POOLS = {
    'sky-ssr': {
        'pool_id': 'd8c4eff5-c8a9-46fc-a888-057c4c668e72',
        'protocol': 'sky',
        'chain': 'ethereum',
        'pool': 'sUSDS'
    },
    'compound-v3-arb-usdc': {
        'pool_id': 'd9c395b9-00d0-4426-a6b3-572a6dd68e54',
        'protocol': 'compound-v3',
        'chain': 'arbitrum',
        'pool': 'USDC'
    },
    'jito': {
        'pool_id': '0e7d0722-9054-4907-8593-567b353c0900',
        'protocol': 'jito',
        'chain': 'solana',
        'pool': 'jitoSOL'
    },
    'aave-v3-eth-usdc': {
        'pool_id': '747c1d2a-c668-4682-b9f9-296708a3dd90',
        'protocol': 'aave-v3',
        'chain': 'ethereum',
        'pool': 'USDC'
    }
}


@CollectorRegistry.register("defillama_live")
class DeFiLlamaCollector(Collector):
    """
    Collector for DeFiLlama DeFi protocol data.

    Fetches historical APY and TVL data for tracked DeFi protocols
    used in diBoaS investment strategies.

    Usage:
        collector = CollectorRegistry.get_instance().get("defillama_live", {})
        df = collector.collect()
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize DeFiLlama collector.

        Args:
            config: Configuration dict with optional keys:
                - pools: List of pool keys to fetch (default: all tracked)
        """
        self.config = config
        self._client: Optional[RateLimitedClient] = None

    def _get_client(self) -> RateLimitedClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = get_defillama_client()
        return self._client

    def _fetch_pool_history(self, pool_id: str) -> List[Dict[str, Any]]:
        """
        Fetch historical data for a specific pool.

        Args:
            pool_id: DeFiLlama pool UUID

        Returns:
            List of historical data points
        """
        client = self._get_client()
        url = f"{DEFILLAMA_YIELDS_URL}/chart/{pool_id}"

        try:
            data = client.get(url)
            return data.get('data', [])
        except APIError as e:
            logger.error(f"Failed to fetch pool {pool_id}: {e}")
            return []

    def _fetch_all_pools(self) -> List[Dict[str, Any]]:
        """
        Fetch current data for all DeFi pools.

        Returns:
            List of all pool data
        """
        client = self._get_client()
        url = f"{DEFILLAMA_YIELDS_URL}/pools"

        try:
            data = client.get(url)
            return data.get('data', [])
        except APIError as e:
            logger.error(f"Failed to fetch pools: {e}")
            return []

    def collect_pool_history(
        self,
        pool_key: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect historical APY data for a specific pool.

        Args:
            pool_key: Key from TRACKED_POOLS (e.g., 'sky-ssr')
            start_date: Start date filter
            end_date: End date filter

        Returns:
            DataFrame with columns: date, protocol, chain, pool, apy, tvl_usd
        """
        if pool_key not in TRACKED_POOLS:
            logger.warning(f"Unknown pool key: {pool_key}")
            return pd.DataFrame()

        pool_info = TRACKED_POOLS[pool_key]
        pool_id = pool_info['pool_id']

        logger.info(f"Fetching history for {pool_key} ({pool_id})")

        history = self._fetch_pool_history(pool_id)

        if not history:
            return pd.DataFrame()

        records = []
        for item in history:
            timestamp = item.get('timestamp')
            if timestamp:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                records.append({
                    'date': dt.strftime('%Y-%m-%d'),
                    'protocol': pool_info['protocol'],
                    'chain': pool_info['chain'],
                    'pool': pool_info['pool'],
                    'apy': item.get('apy', 0),
                    'tvl_usd': item.get('tvlUsd', 0)
                })

        df = pd.DataFrame(records)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)

            # Filter by date range
            if start_date:
                df = df[df['date'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['date'] <= pd.to_datetime(end_date)]

        logger.info(f"Fetched {len(df)} records for {pool_key}")
        return df

    def collect(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect APY data for all tracked pools.

        Args:
            start_date: Start date filter
            end_date: End date filter

        Returns:
            DataFrame with columns: date, protocol, chain, pool, apy, tvl_usd
        """
        # Get pool keys to fetch
        pool_keys = self.config.get('pools', list(TRACKED_POOLS.keys()))

        all_data = []

        for pool_key in pool_keys:
            df = self.collect_pool_history(pool_key, start_date, end_date)
            if not df.empty:
                all_data.append(df)

        if not all_data:
            return pd.DataFrame(columns=['date', 'protocol', 'chain', 'pool', 'apy', 'tvl_usd'])

        result = pd.concat(all_data, ignore_index=True)
        result = result.sort_values(['date', 'protocol']).reset_index(drop=True)

        logger.info(f"Collected {len(result)} total APY records")
        return result

    def get_current_apys(self) -> Dict[str, Dict[str, Any]]:
        """
        Get current APY for all tracked pools.

        Returns:
            Dictionary mapping pool_key to current APY data
        """
        pools = self._fetch_all_pools()

        # Create lookup by pool ID
        pool_lookup = {p.get('pool'): p for p in pools}

        result = {}
        for pool_key, pool_info in TRACKED_POOLS.items():
            pool_id = pool_info['pool_id']
            if pool_id in pool_lookup:
                pool_data = pool_lookup[pool_id]
                result[pool_key] = {
                    'protocol': pool_info['protocol'],
                    'chain': pool_info['chain'],
                    'pool': pool_info['pool'],
                    'apy': pool_data.get('apy', 0),
                    'tvl_usd': pool_data.get('tvlUsd', 0),
                    'apy_base': pool_data.get('apyBase', 0),
                    'apy_reward': pool_data.get('apyReward', 0)
                }

        return result

    def get_name(self) -> str:
        """Return collector name."""
        return "defillama_live"

    @property
    def source_type(self) -> str:
        """Return source type."""
        return "api"

    def collect_jito_history(
        self,
        output_dir: str = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Collect Jito APY history from DeFiLlama and save to dedicated file.

        Jito requires a separate file because Battle Test loads it independently
        from the combined defillama_historical_apy.csv.

        Args:
            output_dir: Output directory (default: data/)
            start_date: Start date filter
            end_date: End date filter

        Returns:
            DataFrame with columns: date, apy, tvl_usd
        """
        from pathlib import Path
        from config.settings import DATA_DIR

        output_path = Path(output_dir) if output_dir else DATA_DIR

        # Fetch Jito pool history
        pool_info = TRACKED_POOLS['jito']
        pool_id = pool_info['pool_id']

        logger.info(f"Fetching Jito history from DeFiLlama (pool: {pool_id})")

        history = self._fetch_pool_history(pool_id)

        if not history:
            logger.warning("No Jito history data received from DeFiLlama")
            return pd.DataFrame()

        records = []
        for item in history:
            timestamp = item.get('timestamp')
            if timestamp:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                records.append({
                    'date': dt.strftime('%Y-%m-%d'),
                    'apy': item.get('apy', 0),
                    'tvl_usd': item.get('tvlUsd', 0)
                })

        df = pd.DataFrame(records)

        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)

            # Filter by date range
            if start_date:
                df = df[df['date'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['date'] <= pd.to_datetime(end_date)]

            # Save to dedicated file
            filepath = output_path / 'jito_historical_apy.csv'
            if safe_write_csv(df, filepath):
                logger.info(f"Saved {len(df)} Jito APY records to {filepath}")

        return df

    def collect_jupiter_jlp_apy(
        self,
        output_dir: str = None
    ) -> tuple:
        """
        Calculate Jupiter JLP APY from DeFiLlama fees and TVL data.

        Jupiter JLP APY is not available directly via DeFiLlama yields API.
        Instead, it must be calculated from:
        - TVL: api.llama.fi/tvl/jupiter-perpetual-exchange
        - Fees: api.llama.fi/overview/fees (daily fees)

        Formula: APY = (daily_fees × 365 × 0.75) / TVL × 100
        - JLP earns 75% of Jupiter Perps trading fees

        Args:
            output_dir: Output directory to append to historical file

        Returns:
            Tuple of (current_apy, metadata_dict) or (None, {}) on failure
        """
        from pathlib import Path
        from config.settings import DATA_DIR
        import requests

        output_path = Path(output_dir) if output_dir else DATA_DIR

        try:
            # Get TVL
            logger.info("Fetching Jupiter Perpetual Exchange TVL...")
            tvl_response = requests.get(
                "https://api.llama.fi/tvl/jupiter-perpetual-exchange",
                timeout=30
            )
            tvl_response.raise_for_status()
            tvl = tvl_response.json()  # Returns float

            # Get fees
            logger.info("Fetching DeFiLlama fees overview...")
            fees_response = requests.get(
                "https://api.llama.fi/overview/fees",
                timeout=30
            )
            fees_response.raise_for_status()
            fees_data = fees_response.json()

            # Find Jupiter Perps in protocols list
            jup_perps = next(
                (p for p in fees_data.get('protocols', [])
                 if p.get('name') == 'Jupiter Perpetual Exchange'),
                None
            )

            if jup_perps is None:
                logger.warning("Jupiter Perpetual Exchange not found in DeFiLlama fees")
                return None, {}

            daily_fees = jup_perps.get('total24h', 0) or 0

            # Calculate APY (JLP gets 75% of fees)
            if tvl and tvl > 0:
                apy = (daily_fees * 365 * 0.75) / tvl * 100
            else:
                apy = 0

            metadata = {
                'source': 'defillama_calculated',
                'tvl_usd': tvl,
                'daily_fees_usd': daily_fees,
                'fee_share': 0.75,
                'calculation': '(daily_fees × 365 × 0.75) / TVL × 100',
                'timestamp': datetime.utcnow().isoformat(),
            }

            logger.info(
                f"Jupiter JLP APY: {apy:.2f}% "
                f"(TVL: ${tvl:,.0f}, Daily Fees: ${daily_fees:,.0f})"
            )

            # Append to historical file if output_dir provided
            filepath = output_path / 'jupiter_jlp_historical_apy.csv'
            new_row = pd.DataFrame([{
                'date': date.today().isoformat(),
                'apy': round(apy, 2),
                'tvl_usd': tvl,
                'daily_fees': daily_fees,
            }])

            if filepath.exists():
                existing = pd.read_csv(filepath)
                # Ensure date column exists
                if 'date' in existing.columns:
                    combined = pd.concat([existing, new_row])
                    combined = combined.drop_duplicates(subset=['date'], keep='last')
                    combined = combined.sort_values('date').reset_index(drop=True)
                else:
                    combined = new_row
            else:
                combined = new_row

            if safe_write_csv(combined, filepath):
                logger.info(f"Updated Jupiter JLP historical data: {filepath}")

            return apy, metadata

        except requests.RequestException as e:
            logger.error(f"Failed to fetch Jupiter JLP data: {e}")
            return None, {}
        except Exception as e:
            logger.error(f"Error calculating Jupiter JLP APY: {e}")
            return None, {}

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
            filepath = output_path / 'defillama_historical_apy.csv'
            if safe_write_csv(df, filepath):
                logger.info(f"Saved DeFiLlama APY data to {filepath}")
                return str(filepath)

        return ""
