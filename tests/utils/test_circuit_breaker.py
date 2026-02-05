"""
Tests for circuit breaker implementation.
"""

import pytest
import time
from unittest.mock import Mock

from src.utils.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
    CircuitOpenError,
    CircuitBreakerStats,
    get_circuit_breaker,
    get_all_circuit_health,
    reset_all_circuits,
)


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_initial_state_is_closed(self):
        """Circuit starts in CLOSED state."""
        breaker = CircuitBreaker(name="test")
        assert breaker.state == CircuitState.CLOSED

    def test_success_keeps_circuit_closed(self):
        """Successful calls keep circuit closed."""
        breaker = CircuitBreaker(name="test", failure_threshold=3)

        # Simulate successful calls
        for _ in range(5):
            breaker._record_success()

        assert breaker.state == CircuitState.CLOSED
        assert breaker.stats.successful_calls == 5

    def test_failures_trip_circuit(self):
        """Failures above threshold trip circuit to OPEN."""
        breaker = CircuitBreaker(name="test", failure_threshold=3)

        # Simulate failures
        for i in range(3):
            breaker._record_failure(Exception(f"Error {i}"))

        assert breaker.state == CircuitState.OPEN
        assert breaker.stats.failed_calls == 3

    def test_open_circuit_rejects_requests(self):
        """Open circuit raises CircuitOpenError."""
        breaker = CircuitBreaker(
            name="test",
            failure_threshold=2,
            recovery_timeout=60.0
        )

        # Trip the circuit
        breaker._record_failure(Exception("Error 1"))
        breaker._record_failure(Exception("Error 2"))

        # Should be open now
        assert breaker.state == CircuitState.OPEN

        # Request should be rejected
        with pytest.raises(CircuitOpenError) as exc_info:
            breaker._check_state()

        assert "test" in str(exc_info.value)
        assert breaker.stats.rejected_calls == 1

    def test_circuit_transitions_to_half_open(self):
        """Circuit transitions to HALF_OPEN after recovery timeout."""
        breaker = CircuitBreaker(
            name="test",
            failure_threshold=2,
            recovery_timeout=0.1  # 100ms for fast test
        )

        # Trip the circuit
        breaker._record_failure(Exception("Error 1"))
        breaker._record_failure(Exception("Error 2"))
        assert breaker.state == CircuitState.OPEN

        # Wait for recovery timeout
        time.sleep(0.15)

        # Should transition to HALF_OPEN
        assert breaker.state == CircuitState.HALF_OPEN

    def test_half_open_success_closes_circuit(self):
        """Successful call in HALF_OPEN closes circuit."""
        breaker = CircuitBreaker(
            name="test",
            failure_threshold=2,
            recovery_timeout=0.1
        )

        # Trip and wait
        breaker._record_failure(Exception("Error 1"))
        breaker._record_failure(Exception("Error 2"))
        time.sleep(0.15)

        # Should be HALF_OPEN
        assert breaker.state == CircuitState.HALF_OPEN

        # Record success
        breaker._record_success()

        # Should be CLOSED now
        assert breaker.state == CircuitState.CLOSED

    def test_half_open_failure_reopens_circuit(self):
        """Failure in HALF_OPEN reopens circuit."""
        breaker = CircuitBreaker(
            name="test",
            failure_threshold=2,
            recovery_timeout=0.1
        )

        # Trip and wait
        breaker._record_failure(Exception("Error 1"))
        breaker._record_failure(Exception("Error 2"))
        time.sleep(0.15)

        # Should be HALF_OPEN
        assert breaker.state == CircuitState.HALF_OPEN

        # Record failure
        breaker._record_failure(Exception("Error 3"))

        # Should be OPEN again
        assert breaker.state == CircuitState.OPEN

    def test_decorator_usage(self):
        """Circuit breaker works as decorator."""
        breaker = CircuitBreaker(name="test", failure_threshold=2)

        call_count = 0

        @breaker
        def risky_function():
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise ValueError("Simulated error")
            return "success"

        # First two calls fail
        with pytest.raises(ValueError):
            risky_function()
        with pytest.raises(ValueError):
            risky_function()

        # Circuit should be open
        assert breaker.state == CircuitState.OPEN

        # Third call rejected by circuit
        with pytest.raises(CircuitOpenError):
            risky_function()

    def test_context_manager_usage(self):
        """Circuit breaker works as context manager."""
        breaker = CircuitBreaker(name="test", failure_threshold=2)

        # Successful call
        with breaker:
            result = 1 + 1
        assert breaker.stats.successful_calls == 1

        # Failed call
        with pytest.raises(ValueError):
            with breaker:
                raise ValueError("Test error")
        assert breaker.stats.failed_calls == 1

    def test_reset_closes_circuit(self):
        """Reset returns circuit to CLOSED state."""
        breaker = CircuitBreaker(name="test", failure_threshold=2)

        # Trip the circuit
        breaker._record_failure(Exception("Error 1"))
        breaker._record_failure(Exception("Error 2"))
        assert breaker.state == CircuitState.OPEN

        # Reset
        breaker.reset()

        # Should be CLOSED
        assert breaker.state == CircuitState.CLOSED

    def test_callbacks_are_called(self):
        """State transition callbacks are invoked."""
        on_open = Mock()
        on_close = Mock()
        on_half_open = Mock()

        breaker = CircuitBreaker(
            name="test",
            failure_threshold=2,
            recovery_timeout=0.1,
            on_open=on_open,
            on_close=on_close,
            on_half_open=on_half_open,
        )

        # Trip circuit
        breaker._record_failure(Exception("Error 1"))
        breaker._record_failure(Exception("Error 2"))
        on_open.assert_called_once_with("test")

        # Wait for half-open
        time.sleep(0.15)
        _ = breaker.state  # Trigger state check
        on_half_open.assert_called_once_with("test")

        # Close circuit
        breaker._record_success()
        on_close.assert_called_once_with("test")

    def test_get_health_returns_status(self):
        """get_health() returns current circuit status."""
        breaker = CircuitBreaker(name="test", failure_threshold=3)

        health = breaker.get_health()

        assert health["name"] == "test"
        assert health["state"] == "closed"
        assert health["healthy"] is True
        assert "stats" in health

    def test_stats_to_dict(self):
        """CircuitBreakerStats.to_dict() returns proper dict."""
        stats = CircuitBreakerStats(
            total_calls=10,
            successful_calls=8,
            failed_calls=2,
        )

        d = stats.to_dict()

        assert d["total_calls"] == 10
        assert d["successful_calls"] == 8
        assert d["failed_calls"] == 2
        assert d["success_rate"] == 80.0


class TestCircuitBreakerRegistry:
    """Tests for circuit breaker registry functions."""

    def test_get_circuit_breaker_creates_new(self):
        """get_circuit_breaker creates new breaker if not exists."""
        reset_all_circuits()

        breaker = get_circuit_breaker("new_circuit")

        assert breaker is not None
        assert breaker.name == "new_circuit"

    def test_get_circuit_breaker_returns_same(self):
        """get_circuit_breaker returns same breaker for same name."""
        reset_all_circuits()

        breaker1 = get_circuit_breaker("shared_circuit")
        breaker2 = get_circuit_breaker("shared_circuit")

        assert breaker1 is breaker2

    def test_get_all_circuit_health(self):
        """get_all_circuit_health returns all breakers' health."""
        reset_all_circuits()

        get_circuit_breaker("circuit_a")
        get_circuit_breaker("circuit_b")

        health = get_all_circuit_health()

        assert "circuit_a" in health
        assert "circuit_b" in health

    def test_reset_all_circuits(self):
        """reset_all_circuits resets all breakers."""
        reset_all_circuits()

        breaker = get_circuit_breaker("test_reset", failure_threshold=1)
        breaker._record_failure(Exception("Error"))
        assert breaker.state == CircuitState.OPEN

        reset_all_circuits()

        assert breaker.state == CircuitState.CLOSED
