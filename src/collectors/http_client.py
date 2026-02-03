"""
Rate-limited HTTP client for API collectors.

Provides:
- Rate limiting (requests per minute)
- Retry logic with exponential backoff
- Error handling and logging
- Request/response logging for debugging
"""

import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class RateLimitError(Exception):
    """Raised when rate limit is exceeded."""
    pass


class APIError(Exception):
    """Raised when API returns an error."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class RateLimitedClient:
    """
    HTTP client with rate limiting and retry logic.

    Features:
    - Configurable requests per minute
    - Automatic retry with exponential backoff
    - Request logging
    - Graceful error handling

    Usage:
        client = RateLimitedClient(requests_per_minute=30)
        data = client.get("https://api.example.com/data")
    """

    def __init__(
        self,
        requests_per_minute: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        timeout: int = 30
    ):
        """
        Initialize the rate-limited client.

        Args:
            requests_per_minute: Maximum requests per minute (default: 30)
            max_retries: Maximum retry attempts (default: 3)
            backoff_factor: Multiplier for exponential backoff (default: 1.0)
            timeout: Request timeout in seconds (default: 30)
        """
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout

        self._last_request_time: Optional[datetime] = None
        self._request_count = 0

        # Configure session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _wait_for_rate_limit(self):
        """Wait if necessary to respect rate limit."""
        if self._last_request_time is None:
            return

        elapsed = (datetime.now() - self._last_request_time).total_seconds()
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
            time.sleep(wait_time)

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a GET request with rate limiting and retry.

        Args:
            url: Request URL
            params: Query parameters
            headers: Request headers

        Returns:
            JSON response as dictionary

        Raises:
            APIError: If request fails after retries
            RateLimitError: If rate limit exceeded and cannot recover
        """
        self._wait_for_rate_limit()

        try:
            logger.debug(f"GET {url} params={params}")

            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            self._last_request_time = datetime.now()
            self._request_count += 1

            # Check for rate limit response
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited. Waiting {retry_after}s")
                time.sleep(retry_after)
                return self.get(url, params, headers)  # Retry

            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            logger.error(f"Request timeout: {url}")
            raise APIError(f"Request timed out: {url}")

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise APIError(
                f"HTTP error: {e}",
                status_code=e.response.status_code if e.response else None
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise APIError(f"Request failed: {e}")

        except ValueError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise APIError(f"Invalid JSON response from {url}")

    def get_raw(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Make a GET request and return raw response.

        Useful when response is not JSON.
        """
        self._wait_for_rate_limit()

        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout
        )

        self._last_request_time = datetime.now()
        self._request_count += 1

        response.raise_for_status()
        return response

    @property
    def request_count(self) -> int:
        """Get total request count for this session."""
        return self._request_count

    def reset_count(self):
        """Reset the request counter."""
        self._request_count = 0


# Pre-configured clients for common APIs
def get_fred_client() -> RateLimitedClient:
    """Get client configured for FRED API (120 requests/minute)."""
    return RateLimitedClient(requests_per_minute=120)


def get_coingecko_client() -> RateLimitedClient:
    """Get client configured for CoinGecko API (30 requests/minute free tier)."""
    return RateLimitedClient(requests_per_minute=30)


def get_defillama_client() -> RateLimitedClient:
    """Get client configured for DeFiLlama API (no strict limit, but be nice)."""
    return RateLimitedClient(requests_per_minute=60)


def get_alternative_client() -> RateLimitedClient:
    """Get client configured for Alternative.me API."""
    return RateLimitedClient(requests_per_minute=30)
