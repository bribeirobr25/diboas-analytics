"""
Retry utilities with exponential backoff.

Provides decorators and context managers for reliable API calls
and external service interactions.
"""

import time
import logging
import functools
from typing import Callable, Type, Tuple, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_retries: int = 3
    base_delay: float = 1.0  # seconds
    max_delay: float = 30.0  # seconds
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_exceptions: Tuple[Type[Exception], ...] = (
        ConnectionError,
        TimeoutError,
        OSError,
    )


# Default configuration
DEFAULT_RETRY_CONFIG = RetryConfig()


def calculate_delay(
    attempt: int,
    base_delay: float,
    max_delay: float,
    exponential_base: float,
    jitter: bool
) -> float:
    """
    Calculate delay for next retry attempt.

    Uses exponential backoff with optional jitter.

    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay cap
        exponential_base: Base for exponential calculation
        jitter: Whether to add random jitter

    Returns:
        Delay in seconds
    """
    delay = base_delay * (exponential_base ** attempt)
    delay = min(delay, max_delay)

    if jitter:
        import random
        delay = delay * (0.5 + random.random())

    return delay


def retry(
    max_retries: int = None,
    base_delay: float = None,
    max_delay: float = None,
    retryable_exceptions: Tuple[Type[Exception], ...] = None,
    on_retry: Optional[Callable[[Exception, int], None]] = None,
    config: RetryConfig = None
):
    """
    Decorator that retries a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay cap (seconds)
        retryable_exceptions: Tuple of exception types to retry on
        on_retry: Callback function called on each retry (exception, attempt)
        config: RetryConfig object (overrides individual params)

    Returns:
        Decorated function

    Example:
        @retry(max_retries=3, base_delay=1.0)
        def fetch_data():
            return requests.get(url)

        @retry(retryable_exceptions=(requests.RequestException,))
        def fetch_with_custom_exceptions():
            return requests.get(url)
    """
    cfg = config or DEFAULT_RETRY_CONFIG

    _max_retries = max_retries if max_retries is not None else cfg.max_retries
    _base_delay = base_delay if base_delay is not None else cfg.base_delay
    _max_delay = max_delay if max_delay is not None else cfg.max_delay
    _retryable = retryable_exceptions or cfg.retryable_exceptions

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(_max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except _retryable as e:
                    last_exception = e

                    if attempt < _max_retries:
                        delay = calculate_delay(
                            attempt,
                            _base_delay,
                            _max_delay,
                            cfg.exponential_base,
                            cfg.jitter
                        )

                        logger.warning(
                            f"Retry {attempt + 1}/{_max_retries} for {func.__name__} "
                            f"after {delay:.2f}s due to: {e}"
                        )

                        if on_retry:
                            on_retry(e, attempt + 1)

                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {_max_retries} retries exhausted for {func.__name__}: {e}"
                        )
                except Exception as e:
                    # Non-retryable exception, raise immediately
                    logger.error(f"Non-retryable error in {func.__name__}: {e}")
                    raise

            # All retries exhausted
            raise last_exception

        return wrapper
    return decorator


def retry_on_network_error(func: Callable) -> Callable:
    """
    Convenience decorator for network-related retries.

    Retries on common network exceptions:
    - ConnectionError
    - TimeoutError
    - OSError (includes socket errors)

    Example:
        @retry_on_network_error
        def fetch_api_data():
            return requests.get(url)
    """
    return retry(
        max_retries=3,
        base_delay=1.0,
        max_delay=30.0,
        retryable_exceptions=(
            ConnectionError,
            TimeoutError,
            OSError,
        )
    )(func)


class RetryContext:
    """
    Context manager for retry logic.

    Useful when you need more control over the retry flow.

    Example:
        with RetryContext(max_retries=3) as ctx:
            for attempt in ctx:
                try:
                    result = risky_operation()
                    break
                except ConnectionError as e:
                    ctx.record_failure(e)
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.attempt = 0
        self.last_exception = None
        self.success = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False  # Don't suppress exceptions

    def __iter__(self):
        return self

    def __next__(self):
        if self.success:
            raise StopIteration

        if self.attempt > self.max_retries:
            if self.last_exception:
                raise self.last_exception
            raise StopIteration

        if self.attempt > 0 and self.last_exception:
            delay = calculate_delay(
                self.attempt - 1,
                self.base_delay,
                self.max_delay,
                2.0,
                True
            )
            logger.info(f"Retry attempt {self.attempt}/{self.max_retries}, waiting {delay:.2f}s")
            time.sleep(delay)

        current = self.attempt
        self.attempt += 1
        return current

    def record_failure(self, exception: Exception):
        """Record a failed attempt."""
        self.last_exception = exception
        logger.warning(f"Attempt {self.attempt} failed: {exception}")

    def mark_success(self):
        """Mark operation as successful to stop retrying."""
        self.success = True


def with_fallback(
    fallback_value: Any = None,
    fallback_func: Callable = None,
    log_error: bool = True
):
    """
    Decorator that provides a fallback value on failure.

    Args:
        fallback_value: Value to return on failure
        fallback_func: Function to call for fallback value
        log_error: Whether to log the error

    Example:
        @with_fallback(fallback_value=[])
        def get_items():
            return api.fetch_items()

        @with_fallback(fallback_func=lambda: load_from_cache())
        def get_data():
            return api.fetch_data()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.warning(
                        f"{func.__name__} failed with {type(e).__name__}: {e}. "
                        f"Using fallback."
                    )

                if fallback_func:
                    return fallback_func()
                return fallback_value

        return wrapper
    return decorator
