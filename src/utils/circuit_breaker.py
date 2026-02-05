"""
Circuit breaker pattern implementation.

Principle 7 (Error Handling & System Recovery):
----------------------------------------------
Implements circuit breaker pattern to prevent cascading failures
when external services are unavailable. The circuit trips open
after a threshold of failures, allowing the system to fail fast
rather than blocking on unavailable services.

States:
    CLOSED: Normal operation, requests flow through
    OPEN: Circuit tripped, requests fail immediately
    HALF_OPEN: Testing if service recovered

Usage:
    from src.utils.circuit_breaker import CircuitBreaker, CircuitOpenError

    breaker = CircuitBreaker(
        failure_threshold=5,
        recovery_timeout=30.0,
        name="fred_api"
    )

    @breaker
    def call_fred_api():
        return requests.get("https://api.fred.com/...")

    # Or use as context manager
    with breaker:
        response = requests.get(url)
"""

import time
import logging
import functools
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional, Any, Dict, Type, Tuple
from threading import Lock

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Failing fast
    HALF_OPEN = "half_open" # Testing recovery


class CircuitOpenError(Exception):
    """Raised when circuit is open and request is rejected."""

    def __init__(self, name: str, retry_after: float):
        self.name = name
        self.retry_after = retry_after
        super().__init__(
            f"Circuit '{name}' is OPEN. Retry after {retry_after:.1f}s"
        )


@dataclass
class CircuitBreakerStats:
    """Statistics for a circuit breaker."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0  # Calls rejected due to open circuit
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    current_failure_streak: int = 0
    state_changes: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "rejected_calls": self.rejected_calls,
            "success_rate": (
                self.successful_calls / self.total_calls * 100
                if self.total_calls > 0 else 0.0
            ),
            "last_failure_time": (
                self.last_failure_time.isoformat()
                if self.last_failure_time else None
            ),
            "last_success_time": (
                self.last_success_time.isoformat()
                if self.last_success_time else None
            ),
            "current_failure_streak": self.current_failure_streak,
            "state_changes": self.state_changes,
        }


class CircuitBreaker:
    """
    Circuit breaker implementation.

    Monitors failures and opens circuit when threshold is reached,
    preventing further requests until recovery timeout expires.

    Attributes:
        name: Identifier for this circuit (for logging)
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before testing recovery
        expected_exceptions: Exception types that count as failures
    """

    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exceptions: Tuple[Type[Exception], ...] = (Exception,),
        on_open: Optional[Callable[[str], None]] = None,
        on_close: Optional[Callable[[str], None]] = None,
        on_half_open: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialize circuit breaker.

        Args:
            name: Identifier for logging and monitoring
            failure_threshold: Failures needed to trip circuit
            recovery_timeout: Seconds before testing recovery
            expected_exceptions: Exceptions that count as failures
            on_open: Callback when circuit opens
            on_close: Callback when circuit closes
            on_half_open: Callback when circuit enters half-open
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: Optional[float] = None
        self._lock = Lock()

        self._on_open = on_open
        self._on_close = on_close
        self._on_half_open = on_half_open

        self._stats = CircuitBreakerStats()

    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        with self._lock:
            return self._get_state()

    def _get_state(self) -> CircuitState:
        """
        Get state, checking if recovery timeout expired.

        Must be called with lock held.
        """
        if self._state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self._transition_to(CircuitState.HALF_OPEN)
        return self._state

    def _should_attempt_recovery(self) -> bool:
        """Check if enough time passed to attempt recovery."""
        if self._last_failure_time is None:
            return True
        elapsed = time.time() - self._last_failure_time
        return elapsed >= self.recovery_timeout

    def _transition_to(self, new_state: CircuitState) -> None:
        """
        Transition to a new state.

        Must be called with lock held.
        """
        old_state = self._state
        if old_state == new_state:
            return

        self._state = new_state
        self._stats.state_changes += 1

        logger.info(
            f"Circuit '{self.name}' state: {old_state.value} -> {new_state.value}"
        )

        # Fire callbacks
        if new_state == CircuitState.OPEN and self._on_open:
            self._on_open(self.name)
        elif new_state == CircuitState.CLOSED and self._on_close:
            self._on_close(self.name)
        elif new_state == CircuitState.HALF_OPEN and self._on_half_open:
            self._on_half_open(self.name)

    def _record_success(self) -> None:
        """Record a successful call."""
        with self._lock:
            self._stats.total_calls += 1
            self._stats.successful_calls += 1
            self._stats.last_success_time = datetime.utcnow()
            self._stats.current_failure_streak = 0
            self._failure_count = 0

            if self._state == CircuitState.HALF_OPEN:
                # Recovery successful, close circuit
                self._transition_to(CircuitState.CLOSED)

    def _record_failure(self, exception: Exception) -> None:
        """Record a failed call."""
        with self._lock:
            self._stats.total_calls += 1
            self._stats.failed_calls += 1
            self._stats.last_failure_time = datetime.utcnow()
            self._stats.current_failure_streak += 1
            self._failure_count += 1
            self._last_failure_time = time.time()

            logger.warning(
                f"Circuit '{self.name}' failure {self._failure_count}/{self.failure_threshold}: "
                f"{type(exception).__name__}: {exception}"
            )

            if self._state == CircuitState.HALF_OPEN:
                # Recovery failed, reopen circuit
                self._transition_to(CircuitState.OPEN)
            elif self._failure_count >= self.failure_threshold:
                # Threshold reached, open circuit
                self._transition_to(CircuitState.OPEN)

    def _check_state(self) -> None:
        """
        Check if circuit allows request.

        Raises CircuitOpenError if circuit is open.
        """
        with self._lock:
            state = self._get_state()

            if state == CircuitState.OPEN:
                self._stats.rejected_calls += 1
                retry_after = self.recovery_timeout
                if self._last_failure_time:
                    elapsed = time.time() - self._last_failure_time
                    retry_after = max(0, self.recovery_timeout - elapsed)
                raise CircuitOpenError(self.name, retry_after)

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker.

        Args:
            func: Function to execute
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            Function result

        Raises:
            CircuitOpenError: If circuit is open
            Exception: If function raises non-circuit exception
        """
        self._check_state()

        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except self.expected_exceptions as e:
            self._record_failure(e)
            raise

    def __call__(self, func: Callable) -> Callable:
        """
        Decorator usage.

        Example:
            @circuit_breaker
            def call_api():
                return requests.get(url)
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper

    def __enter__(self) -> 'CircuitBreaker':
        """Context manager entry."""
        self._check_state()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Context manager exit."""
        if exc_val is None:
            self._record_success()
        elif isinstance(exc_val, self.expected_exceptions):
            self._record_failure(exc_val)
        return False  # Don't suppress exceptions

    def reset(self) -> None:
        """Reset circuit breaker to initial state."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None
            logger.info(f"Circuit '{self.name}' reset to CLOSED")

    @property
    def stats(self) -> CircuitBreakerStats:
        """Get circuit breaker statistics."""
        return self._stats

    def get_health(self) -> Dict[str, Any]:
        """
        Get health information for monitoring.

        Returns dict with state, stats, and whether circuit is healthy.
        """
        with self._lock:
            state = self._get_state()
            return {
                "name": self.name,
                "state": state.value,
                "healthy": state == CircuitState.CLOSED,
                "failure_count": self._failure_count,
                "failure_threshold": self.failure_threshold,
                "stats": self._stats.to_dict(),
            }


# Registry of circuit breakers for monitoring
_circuit_registry: Dict[str, CircuitBreaker] = {}
_registry_lock = Lock()


def get_circuit_breaker(
    name: str,
    failure_threshold: int = 5,
    recovery_timeout: float = 30.0,
    **kwargs
) -> CircuitBreaker:
    """
    Get or create a circuit breaker by name.

    Circuit breakers are cached by name, so multiple calls
    with the same name return the same instance.

    Args:
        name: Unique identifier for this circuit
        failure_threshold: Failures needed to trip circuit
        recovery_timeout: Seconds before testing recovery
        **kwargs: Additional CircuitBreaker arguments

    Returns:
        CircuitBreaker instance
    """
    with _registry_lock:
        if name not in _circuit_registry:
            _circuit_registry[name] = CircuitBreaker(
                name=name,
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                **kwargs
            )
        return _circuit_registry[name]


def get_all_circuit_health() -> Dict[str, Dict[str, Any]]:
    """
    Get health of all registered circuit breakers.

    Returns:
        Dict mapping circuit name to health info
    """
    with _registry_lock:
        return {
            name: breaker.get_health()
            for name, breaker in _circuit_registry.items()
        }


def reset_all_circuits() -> None:
    """Reset all registered circuit breakers."""
    with _registry_lock:
        for breaker in _circuit_registry.values():
            breaker.reset()
