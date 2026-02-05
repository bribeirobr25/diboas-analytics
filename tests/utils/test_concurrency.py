"""
Tests for concurrency and performance utilities.
"""

import pytest
import time
from unittest.mock import Mock

from src.utils.concurrency import (
    SimpleCache,
    CacheEntry,
    CacheStats,
    cached,
    timed_lru_cache,
    make_cache_key,
    ThreadPoolManager,
    parallel_map,
    batch_process,
    RateLimiter,
)


class TestCacheEntry:
    """Tests for CacheEntry class."""

    def test_not_expired_without_ttl(self):
        """Entry without TTL never expires."""
        entry = CacheEntry(value="test", ttl_seconds=None)

        assert entry.is_expired() is False

    def test_not_expired_within_ttl(self):
        """Entry within TTL is not expired."""
        entry = CacheEntry(value="test", ttl_seconds=10)

        assert entry.is_expired() is False

    def test_expired_after_ttl(self):
        """Entry after TTL is expired."""
        entry = CacheEntry(value="test", ttl_seconds=0.01)
        time.sleep(0.02)

        assert entry.is_expired() is True


class TestCacheStats:
    """Tests for CacheStats class."""

    def test_hit_rate_calculation(self):
        """Hit rate is calculated correctly."""
        stats = CacheStats(hits=80, misses=20)

        assert stats.hit_rate == 0.8

    def test_hit_rate_zero_when_no_calls(self):
        """Hit rate is 0 when no calls made."""
        stats = CacheStats()

        assert stats.hit_rate == 0.0

    def test_to_dict(self):
        """to_dict returns expected structure."""
        stats = CacheStats(hits=10, misses=5, evictions=2, size=8)

        d = stats.to_dict()

        assert d["hits"] == 10
        assert d["misses"] == 5
        assert d["evictions"] == 2
        assert d["size"] == 8
        assert d["hit_rate"] == 66.67


class TestSimpleCache:
    """Tests for SimpleCache class."""

    def test_set_and_get(self):
        """Basic set and get works."""
        cache = SimpleCache[str]()

        cache.set("key1", "value1")
        result = cache.get("key1")

        assert result == "value1"

    def test_get_missing_returns_none(self):
        """Get on missing key returns None."""
        cache = SimpleCache[str]()

        result = cache.get("nonexistent")

        assert result is None

    def test_ttl_expiration(self):
        """Entry expires after TTL."""
        cache = SimpleCache[str](ttl_seconds=0.01)

        cache.set("key1", "value1")
        time.sleep(0.02)

        result = cache.get("key1")
        assert result is None

    def test_per_entry_ttl(self):
        """Per-entry TTL overrides default."""
        cache = SimpleCache[str](ttl_seconds=10)

        cache.set("key1", "value1", ttl_seconds=0.01)
        time.sleep(0.02)

        result = cache.get("key1")
        assert result is None

    def test_lru_eviction(self):
        """Least recently used entry is evicted at capacity."""
        cache = SimpleCache[str](maxsize=2)

        cache.set("key1", "value1")
        cache.set("key2", "value2")

        # Access key1 to make key2 the LRU
        cache.get("key1")

        # Add key3, should evict key2
        cache.set("key3", "value3")

        assert cache.get("key1") == "value1"
        assert cache.get("key2") is None  # Evicted
        assert cache.get("key3") == "value3"

    def test_stats_tracking(self):
        """Cache statistics are tracked."""
        cache = SimpleCache[str](maxsize=2)

        cache.set("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss

        assert cache.stats.hits == 1
        assert cache.stats.misses == 1

    def test_clear(self):
        """Clear removes all entries."""
        cache = SimpleCache[str]()

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()

        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_invalidate(self):
        """Invalidate removes specific entry."""
        cache = SimpleCache[str]()

        cache.set("key1", "value1")
        cache.set("key2", "value2")

        result = cache.invalidate("key1")

        assert result is True
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"

    def test_invalidate_nonexistent(self):
        """Invalidate returns False for nonexistent key."""
        cache = SimpleCache[str]()

        result = cache.invalidate("nonexistent")

        assert result is False


class TestCachedDecorator:
    """Tests for @cached decorator."""

    def test_caches_function_result(self):
        """Decorator caches function result."""
        call_count = 0

        @cached()
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = expensive_func(5)
        result2 = expensive_func(5)

        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # Only called once

    def test_different_args_cached_separately(self):
        """Different arguments have separate cache entries."""
        call_count = 0

        @cached()
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        func(1)
        func(2)
        func(1)

        assert call_count == 2  # Called for 1 and 2, not second 1

    def test_cache_expiration(self):
        """Cache entries expire after TTL."""
        call_count = 0

        @cached(ttl_seconds=0.01)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x

        func(1)
        time.sleep(0.02)
        func(1)

        assert call_count == 2  # Called twice due to expiration

    def test_cache_clear_method(self):
        """Decorated function has cache_clear method."""
        @cached()
        def func(x):
            return x

        func(1)
        func.cache_clear()
        func(1)  # Should call function again

        # Just verify method exists and works
        assert callable(func.cache_clear)

    def test_cache_stats_method(self):
        """Decorated function has cache_stats method."""
        @cached()
        def func(x):
            return x

        func(1)
        func(1)
        func(2)

        stats = func.cache_stats()

        assert stats["hits"] == 1
        assert stats["misses"] == 2


class TestTimedLruCache:
    """Tests for timed_lru_cache decorator."""

    def test_works_like_cached(self):
        """timed_lru_cache works like cached."""
        call_count = 0

        @timed_lru_cache(ttl_seconds=10)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = func(5)
        result2 = func(5)

        assert result1 == 10
        assert result2 == 10
        assert call_count == 1


class TestMakeCacheKey:
    """Tests for make_cache_key function."""

    def test_same_args_same_key(self):
        """Same arguments produce same key."""
        key1 = make_cache_key(1, 2, a="b")
        key2 = make_cache_key(1, 2, a="b")

        assert key1 == key2

    def test_different_args_different_key(self):
        """Different arguments produce different keys."""
        key1 = make_cache_key(1, 2)
        key2 = make_cache_key(1, 3)

        assert key1 != key2

    def test_kwarg_order_independent(self):
        """Keyword argument order doesn't affect key."""
        key1 = make_cache_key(a=1, b=2)
        key2 = make_cache_key(b=2, a=1)

        assert key1 == key2


class TestThreadPoolManager:
    """Tests for ThreadPoolManager class."""

    def test_context_manager(self):
        """Context manager starts and stops pool."""
        with ThreadPoolManager(max_workers=2) as pool:
            assert pool._executor is not None

        assert pool._executor is None

    def test_submit(self):
        """Submit executes task."""
        with ThreadPoolManager(max_workers=2) as pool:
            future = pool.submit(lambda x: x * 2, 5)
            result = future.result()

        assert result == 10

    def test_map(self):
        """Map processes items in parallel."""
        items = [1, 2, 3, 4, 5]

        with ThreadPoolManager(max_workers=2) as pool:
            results = pool.map(lambda x: x * 2, items)

        assert results == [2, 4, 6, 8, 10]

    def test_map_preserves_order(self):
        """Map preserves input order."""
        items = list(range(10))

        with ThreadPoolManager(max_workers=4) as pool:
            results = pool.map(lambda x: x, items)

        assert results == items

    def test_singleton_instance(self):
        """get_instance returns singleton."""
        # Reset singleton for test
        ThreadPoolManager._instance = None

        pool1 = ThreadPoolManager.get_instance()
        pool2 = ThreadPoolManager.get_instance()

        assert pool1 is pool2

        # Cleanup
        pool1.shutdown()
        ThreadPoolManager._instance = None


class TestParallelMap:
    """Tests for parallel_map function."""

    def test_processes_items(self):
        """parallel_map processes items correctly."""
        items = [1, 2, 3, 4, 5]

        results = parallel_map(lambda x: x ** 2, items, max_workers=2)

        assert results == [1, 4, 9, 16, 25]

    def test_preserves_order(self):
        """parallel_map preserves order."""
        items = list(range(20))

        results = parallel_map(lambda x: x, items, max_workers=4)

        assert results == items


class TestBatchProcess:
    """Tests for batch_process function."""

    def test_creates_batches(self):
        """batch_process creates correct batches."""
        items = list(range(10))
        batch_sizes = []

        def process(batch):
            batch_sizes.append(len(batch))
            return sum(batch)

        results = batch_process(items, batch_size=3, process_func=process)

        assert batch_sizes == [3, 3, 3, 1]  # 10 items in batches of 3
        assert results == [3, 12, 21, 9]  # Sum of each batch

    def test_parallel_processing(self):
        """batch_process supports parallel mode."""
        items = list(range(10))

        results = batch_process(
            items,
            batch_size=3,
            process_func=sum,
            parallel=True,
            max_workers=2
        )

        assert sum(results) == sum(items)


class TestRateLimiter:
    """Tests for RateLimiter class."""

    def test_allows_calls_under_limit(self):
        """Calls under limit are allowed immediately."""
        limiter = RateLimiter(max_calls=5, period_seconds=1.0)

        start = time.time()
        for _ in range(5):
            limiter.wait()
        elapsed = time.time() - start

        # Should be nearly instant
        assert elapsed < 0.1

    def test_blocks_when_over_limit(self):
        """Calls over limit block until period passes."""
        limiter = RateLimiter(max_calls=2, period_seconds=0.1)

        limiter.wait()
        limiter.wait()

        start = time.time()
        limiter.wait()  # Should block
        elapsed = time.time() - start

        # Should have waited roughly 0.1 seconds
        assert elapsed >= 0.05

    def test_try_acquire_non_blocking(self):
        """try_acquire doesn't block."""
        limiter = RateLimiter(max_calls=1, period_seconds=1.0)

        result1 = limiter.try_acquire()
        result2 = limiter.try_acquire()

        assert result1 is True
        assert result2 is False  # Limit reached, not acquired
