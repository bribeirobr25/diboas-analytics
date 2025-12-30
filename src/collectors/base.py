"""
Abstract base class for data providers.

All data collectors must implement this interface.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
import pandas as pd


class DataProvider(ABC):
    """
    Abstract base class for all data providers.

    Provides a consistent interface for fetching data from various sources.
    """

    @abstractmethod
    def fetch_historical(
        self,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """
        Fetch historical data for the given period.

        Args:
            start_date: Start of the period (inclusive)
            end_date: End of the period (inclusive)

        Returns:
            DataFrame with historical data
        """
        pass

    @abstractmethod
    def fetch_current(self) -> dict:
        """
        Fetch current/live data.

        Returns:
            Dictionary with current data points
        """
        pass

    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate data quality.

        Args:
            data: DataFrame to validate

        Returns:
            True if data is valid, False otherwise
        """
        pass

    def get_name(self) -> str:
        """Get provider name for logging."""
        return self.__class__.__name__

    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess data before returning.

        Override this method to add custom preprocessing.
        Default implementation returns data unchanged.
        """
        return data


class CachedDataProvider(DataProvider):
    """
    Data provider with caching support.

    Caches fetched data to avoid redundant API calls.
    """

    def __init__(self, cache_ttl_seconds: int = 900):  # 15 minutes default
        self._cache: dict[str, tuple[pd.DataFrame, float]] = {}
        self.cache_ttl = cache_ttl_seconds

    def _get_cache_key(self, start_date: date, end_date: date) -> str:
        """Generate cache key for a date range."""
        return f"{self.get_name()}_{start_date}_{end_date}"

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        import time
        if cache_key not in self._cache:
            return False
        _, timestamp = self._cache[cache_key]
        return (time.time() - timestamp) < self.cache_ttl

    def get_cached(
        self,
        start_date: date,
        end_date: date
    ) -> Optional[pd.DataFrame]:
        """Get data from cache if available and valid."""
        cache_key = self._get_cache_key(start_date, end_date)
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key][0].copy()
        return None

    def set_cached(
        self,
        start_date: date,
        end_date: date,
        data: pd.DataFrame
    ):
        """Store data in cache."""
        import time
        cache_key = self._get_cache_key(start_date, end_date)
        self._cache[cache_key] = (data.copy(), time.time())

    def clear_cache(self):
        """Clear all cached data."""
        self._cache.clear()
