"""
Concurrency and performance utilities.

Principle 8 (Performance & Scalability):
----------------------------------------
Provides thread pool utilities for parallel processing and
caching decorators for expensive computations. Designed to
work with both sync and async code patterns.

Usage:
    from src.utils.concurrency import (
        ThreadPoolManager,
        parallel_map,
        cached,
        timed_lru_cache,
    )

    # Parallel processing
    results = parallel_map(process_item, items, max_workers=4)

    # Caching
    @cached(ttl_seconds=300)
    def expensive_computation(x):
        return x ** 2

    @timed_lru_cache(maxsize=128, ttl_seconds=60)
    def api_call(endpoint):
        return requests.get(endpoint).json()
"""

import logging
import time
import functools
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from threading import Lock, RLock
from typing import (
    Any, Callable, Dict, Generic, Iterable, List, Optional,
    TypeVar, Tuple, Union
)

logger = logging.getLogger(__name__)

T = TypeVar('T')
R = TypeVar('R')


@dataclass
class CacheStats:
    """Statistics for cache performance."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    size: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "size": self.size,
            "hit_rate": round(self.hit_rate * 100, 2),
        }


@dataclass
class CacheEntry(Generic[T]):
    """An entry in a cache with TTL."""
    value: T
    created_at: float = field(default_factory=time.time)
    ttl_seconds: Optional[float] = None

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.ttl_seconds is None:
            return False
        return time.time() - self.created_at > self.ttl_seconds


class SimpleCache(Generic[T]):
    """
    Thread-safe cache with TTL support.

    Features:
    - Time-to-live (TTL) per entry
    - Max size with LRU eviction
    - Thread-safe access
    - Statistics tracking

    Usage:
        cache = SimpleCache[str](maxsize=100, ttl_seconds=300)
        cache.set("key1", "value1")
        value = cache.get("key1")  # Returns "value1" or None
    """

    def __init__(
        self,
        maxsize: int = 128,
        ttl_seconds: Optional[float] = None,
    ):
        """
        Initialize cache.

        Args:
            maxsize: Maximum number of entries
            ttl_seconds: Default TTL for entries (None = no expiry)
        """
        self.maxsize = maxsize
        self.default_ttl = ttl_seconds
        self._cache: Dict[str, CacheEntry[T]] = {}
        self._access_order: List[str] = []  # For LRU
        self._lock = RLock()
        self._stats = CacheStats()

    def get(self, key: str) -> Optional[T]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            entry = self._cache.get(key)

            if entry is None:
                self._stats.misses += 1
                return None

            if entry.is_expired():
                self._remove(key)
                self._stats.misses += 1
                return None

            # Update access order for LRU
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)

            self._stats.hits += 1
            return entry.value

    def set(
        self,
        key: str,
        value: T,
        ttl_seconds: Optional[float] = None,
    ) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: TTL for this entry (overrides default)
        """
        with self._lock:
            # Evict if at capacity
            while len(self._cache) >= self.maxsize:
                self._evict_lru()

            ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
            self._cache[key] = CacheEntry(value=value, ttl_seconds=ttl)

            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)

            self._stats.size = len(self._cache)

    def _remove(self, key: str) -> None:
        """Remove key from cache (must hold lock)."""
        if key in self._cache:
            del self._cache[key]
        if key in self._access_order:
            self._access_order.remove(key)
        self._stats.size = len(self._cache)

    def _evict_lru(self) -> None:
        """Evict least recently used entry (must hold lock)."""
        if self._access_order:
            lru_key = self._access_order.pop(0)
            if lru_key in self._cache:
                del self._cache[lru_key]
                self._stats.evictions += 1
        self._stats.size = len(self._cache)

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._stats.size = 0

    def invalidate(self, key: str) -> bool:
        """
        Invalidate a specific cache entry.

        Args:
            key: Cache key to invalidate

        Returns:
            True if entry was found and removed
        """
        with self._lock:
            if key in self._cache:
                self._remove(key)
                return True
            return False

    @property
    def stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._stats


def make_cache_key(*args, **kwargs) -> str:
    """
    Create a cache key from function arguments.

    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Hash string as cache key
    """
    # Create string representation of args
    key_parts = [repr(arg) for arg in args]
    key_parts.extend(f"{k}={repr(v)}" for k, v in sorted(kwargs.items()))
    key_str = "|".join(key_parts)

    # Hash for consistent key length
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(
    ttl_seconds: Optional[float] = 300,
    maxsize: int = 128,
    key_func: Optional[Callable[..., str]] = None,
):
    """
    Caching decorator with TTL support.

    Args:
        ttl_seconds: Time-to-live for cached values (None = no expiry)
        maxsize: Maximum cache size
        key_func: Custom function to generate cache keys

    Returns:
        Decorator function

    Example:
        @cached(ttl_seconds=60)
        def get_user(user_id):
            return db.query(user_id)

        @cached(key_func=lambda x: f"user_{x}")
        def get_user_custom_key(user_id):
            return db.query(user_id)
    """
    cache = SimpleCache(maxsize=maxsize, ttl_seconds=ttl_seconds)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Generate cache key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = make_cache_key(*args, **kwargs)

            # Check cache
            result = cache.get(key)
            if result is not None:
                return result

            # Compute and cache
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result

        # Attach cache for introspection
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_stats = lambda: cache.stats.to_dict()

        return wrapper
    return decorator


def timed_lru_cache(
    maxsize: int = 128,
    ttl_seconds: float = 300,
):
    """
    LRU cache with time-based expiration.

    Like functools.lru_cache but entries expire after TTL.

    Args:
        maxsize: Maximum cache size
        ttl_seconds: Time-to-live for entries

    Example:
        @timed_lru_cache(maxsize=100, ttl_seconds=60)
        def api_call(endpoint):
            return requests.get(endpoint).json()
    """
    return cached(ttl_seconds=ttl_seconds, maxsize=maxsize)


class ThreadPoolManager:
    """
    Managed thread pool for parallel processing.

    Provides a reusable thread pool with context manager support
    and task tracking.

    Usage:
        with ThreadPoolManager(max_workers=4) as pool:
            futures = pool.submit_all(process_item, items)
            results = pool.wait_all(futures)

        # Or singleton pattern
        pool = ThreadPoolManager.get_instance()
        results = pool.map(process_item, items)
    """

    _instance: Optional['ThreadPoolManager'] = None
    _instance_lock = Lock()

    def __init__(
        self,
        max_workers: int = None,
        thread_name_prefix: str = "diboas-worker"
    ):
        """
        Initialize thread pool.

        Args:
            max_workers: Max threads (default: CPU count + 4)
            thread_name_prefix: Prefix for thread names
        """
        import os
        self.max_workers = max_workers or (os.cpu_count() or 1) + 4
        self.thread_name_prefix = thread_name_prefix
        self._executor: Optional[ThreadPoolExecutor] = None
        self._lock = Lock()

    @classmethod
    def get_instance(cls, max_workers: int = None) -> 'ThreadPoolManager':
        """
        Get singleton instance.

        Args:
            max_workers: Max workers (only used on first call)

        Returns:
            Singleton ThreadPoolManager
        """
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls(max_workers=max_workers)
            return cls._instance

    def __enter__(self) -> 'ThreadPoolManager':
        """Start the thread pool."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Shutdown the thread pool."""
        self.shutdown(wait=True)
        return False

    def start(self) -> None:
        """Start the thread pool if not already running."""
        with self._lock:
            if self._executor is None:
                self._executor = ThreadPoolExecutor(
                    max_workers=self.max_workers,
                    thread_name_prefix=self.thread_name_prefix
                )
                logger.debug(
                    f"Started thread pool with {self.max_workers} workers"
                )

    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown the thread pool.

        Args:
            wait: Whether to wait for pending tasks
        """
        with self._lock:
            if self._executor is not None:
                self._executor.shutdown(wait=wait)
                self._executor = None
                logger.debug("Thread pool shutdown")

    def submit(
        self,
        func: Callable[..., R],
        *args,
        **kwargs
    ):
        """
        Submit a single task.

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Future object
        """
        self.start()
        return self._executor.submit(func, *args, **kwargs)

    def map(
        self,
        func: Callable[[T], R],
        items: Iterable[T],
        timeout: Optional[float] = None,
    ) -> List[R]:
        """
        Apply function to items in parallel.

        Args:
            func: Function to apply
            items: Items to process
            timeout: Timeout in seconds

        Returns:
            List of results (preserves order)
        """
        self.start()
        return list(self._executor.map(func, items, timeout=timeout))

    def map_with_progress(
        self,
        func: Callable[[T], R],
        items: List[T],
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> List[R]:
        """
        Apply function with progress tracking.

        Args:
            func: Function to apply
            items: Items to process
            progress_callback: Called with (completed, total)

        Returns:
            List of results (preserves order)
        """
        self.start()

        # Submit all tasks
        futures = {
            self._executor.submit(func, item): i
            for i, item in enumerate(items)
        }

        # Collect results in order
        results = [None] * len(items)
        completed = 0

        for future in as_completed(futures):
            idx = futures[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                logger.error(f"Task {idx} failed: {e}")
                raise

            completed += 1
            if progress_callback:
                progress_callback(completed, len(items))

        return results


def parallel_map(
    func: Callable[[T], R],
    items: Iterable[T],
    max_workers: int = None,
    timeout: Optional[float] = None,
) -> List[R]:
    """
    Convenience function for parallel map.

    Args:
        func: Function to apply
        items: Items to process
        max_workers: Max parallel workers
        timeout: Timeout per task

    Returns:
        List of results

    Example:
        results = parallel_map(process_item, items, max_workers=4)
    """
    with ThreadPoolManager(max_workers=max_workers) as pool:
        return pool.map(func, items, timeout=timeout)


def batch_process(
    items: List[T],
    batch_size: int,
    process_func: Callable[[List[T]], R],
    parallel: bool = False,
    max_workers: int = None,
) -> List[R]:
    """
    Process items in batches.

    Args:
        items: Items to process
        batch_size: Size of each batch
        process_func: Function to process a batch
        parallel: Whether to process batches in parallel
        max_workers: Max workers for parallel processing

    Returns:
        List of results (one per batch)

    Example:
        def process_batch(batch):
            return [x * 2 for x in batch]

        results = batch_process(items, batch_size=100, process_func=process_batch)
    """
    # Create batches
    batches = [
        items[i:i + batch_size]
        for i in range(0, len(items), batch_size)
    ]

    if parallel:
        return parallel_map(process_func, batches, max_workers=max_workers)
    else:
        return [process_func(batch) for batch in batches]


class RateLimiter:
    """
    Simple rate limiter for controlling operation frequency.

    Usage:
        limiter = RateLimiter(max_calls=10, period_seconds=1.0)

        for item in items:
            limiter.wait()  # Blocks if rate exceeded
            process(item)
    """

    def __init__(self, max_calls: int, period_seconds: float):
        """
        Initialize rate limiter.

        Args:
            max_calls: Maximum calls allowed in period
            period_seconds: Time period in seconds
        """
        self.max_calls = max_calls
        self.period_seconds = period_seconds
        self._calls: List[float] = []
        self._lock = Lock()

    def wait(self) -> None:
        """
        Wait if rate limit would be exceeded.

        Blocks until a call is allowed under the rate limit.
        """
        with self._lock:
            now = time.time()
            cutoff = now - self.period_seconds

            # Remove old calls
            self._calls = [t for t in self._calls if t > cutoff]

            if len(self._calls) >= self.max_calls:
                # Need to wait
                oldest = self._calls[0]
                wait_time = oldest + self.period_seconds - now
                if wait_time > 0:
                    time.sleep(wait_time)

            self._calls.append(time.time())

    def try_acquire(self) -> bool:
        """
        Try to acquire a rate limit slot without blocking.

        Returns:
            True if acquired, False if rate limited
        """
        with self._lock:
            now = time.time()
            cutoff = now - self.period_seconds

            self._calls = [t for t in self._calls if t > cutoff]

            if len(self._calls) >= self.max_calls:
                return False

            self._calls.append(now)
            return True
