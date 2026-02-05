"""
Correlation ID support for request tracing.

Principle 12 (Monitoring & Observability):
------------------------------------------
Implements correlation IDs using Python's contextvars for
thread-safe request tracing across async and sync code.

Correlation IDs allow tracing a request through multiple
components and services, making debugging and log analysis
much easier.

Usage:
    from src.utils.correlation import (
        get_correlation_id,
        set_correlation_id,
        new_correlation_id,
        correlation_context,
        with_correlation_id,
    )

    # Set ID at request start
    set_correlation_id("req-12345")

    # Or generate a new one
    cid = new_correlation_id()

    # Get current ID anywhere in the call stack
    current_id = get_correlation_id()

    # Use context manager for automatic management
    with correlation_context("operation-name"):
        do_something()  # All logs include correlation ID

    # Or decorator
    @with_correlation_id
    def handle_request():
        logger.info("Processing")  # Includes correlation ID
"""

import uuid
import logging
import functools
from contextvars import ContextVar
from typing import Optional, Callable, Any
from contextlib import contextmanager
from datetime import datetime

# Context variable for correlation ID
# This is thread-safe and async-safe
_correlation_id: ContextVar[Optional[str]] = ContextVar(
    'correlation_id',
    default=None
)

# Context variable for operation name
_operation_name: ContextVar[Optional[str]] = ContextVar(
    'operation_name',
    default=None
)

# Context variable for operation start time
_operation_start: ContextVar[Optional[float]] = ContextVar(
    'operation_start',
    default=None
)


def generate_correlation_id(prefix: str = "cid") -> str:
    """
    Generate a new correlation ID.

    Format: {prefix}-{timestamp}-{uuid4_short}
    Example: cid-20260204-abc123de

    Args:
        prefix: Optional prefix for the ID

    Returns:
        New correlation ID string
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique = uuid.uuid4().hex[:8]
    return f"{prefix}-{timestamp}-{unique}"


def get_correlation_id() -> Optional[str]:
    """
    Get current correlation ID from context.

    Returns:
        Current correlation ID or None if not set
    """
    return _correlation_id.get()


def set_correlation_id(correlation_id: str) -> None:
    """
    Set correlation ID in current context.

    Args:
        correlation_id: ID to set
    """
    _correlation_id.set(correlation_id)


def new_correlation_id(prefix: str = "cid") -> str:
    """
    Generate and set a new correlation ID.

    Args:
        prefix: Optional prefix for the ID

    Returns:
        The newly generated correlation ID
    """
    cid = generate_correlation_id(prefix)
    set_correlation_id(cid)
    return cid


def get_operation_name() -> Optional[str]:
    """Get current operation name from context."""
    return _operation_name.get()


def clear_correlation_context() -> None:
    """Clear all correlation context variables."""
    _correlation_id.set(None)
    _operation_name.set(None)
    _operation_start.set(None)


@contextmanager
def correlation_context(
    operation_name: str = None,
    correlation_id: str = None,
    prefix: str = "cid"
):
    """
    Context manager for correlation ID scope.

    Automatically generates ID if not provided and cleans up on exit.

    Args:
        operation_name: Name of the operation (for logging)
        correlation_id: Existing ID to use, or None to generate
        prefix: Prefix for generated ID

    Yields:
        The correlation ID being used

    Example:
        with correlation_context("process_order", prefix="order"):
            process_order(order_id)
    """
    import time

    # Store previous values
    prev_cid = _correlation_id.get()
    prev_op = _operation_name.get()
    prev_start = _operation_start.get()

    try:
        # Set new values
        cid = correlation_id or generate_correlation_id(prefix)
        _correlation_id.set(cid)
        _operation_name.set(operation_name)
        _operation_start.set(time.time())

        yield cid

    finally:
        # Restore previous values
        _correlation_id.set(prev_cid)
        _operation_name.set(prev_op)
        _operation_start.set(prev_start)


def with_correlation_id(func: Callable = None, prefix: str = "cid"):
    """
    Decorator to automatically manage correlation ID.

    Generates new correlation ID for each function call
    if one isn't already set.

    Args:
        func: Function to decorate
        prefix: Prefix for generated IDs

    Example:
        @with_correlation_id
        def handle_request():
            logger.info("Processing")

        @with_correlation_id(prefix="api")
        def api_call():
            pass
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            # Only generate new ID if one isn't already set
            existing = get_correlation_id()
            if existing:
                return fn(*args, **kwargs)

            with correlation_context(fn.__name__, prefix=prefix):
                return fn(*args, **kwargs)

        return wrapper

    # Allow both @with_correlation_id and @with_correlation_id()
    if func is not None:
        return decorator(func)
    return decorator


class CorrelatedLogger:
    """
    Logger wrapper that automatically includes correlation ID.

    Wraps a standard logger and adds correlation ID to all log messages.

    Usage:
        logger = CorrelatedLogger(logging.getLogger(__name__))
        logger.info("Processing request")
        # Output: [cid-20260204-abc123de] Processing request
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize with underlying logger.

        Args:
            logger: Standard Python logger to wrap
        """
        self._logger = logger

    def _format_message(self, message: str) -> str:
        """Add correlation context to message."""
        parts = []

        cid = get_correlation_id()
        if cid:
            parts.append(f"[{cid}]")

        op = get_operation_name()
        if op:
            parts.append(f"[{op}]")

        parts.append(message)
        return " ".join(parts)

    def debug(self, message: str, *args, **kwargs):
        """Log debug message with correlation ID."""
        self._logger.debug(self._format_message(message), *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message with correlation ID."""
        self._logger.info(self._format_message(message), *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message with correlation ID."""
        self._logger.warning(self._format_message(message), *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message with correlation ID."""
        self._logger.error(self._format_message(message), *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message with correlation ID."""
        self._logger.critical(self._format_message(message), *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """Log exception with correlation ID."""
        self._logger.exception(self._format_message(message), *args, **kwargs)


def get_correlated_logger(name: str) -> CorrelatedLogger:
    """
    Get a correlated logger for a module.

    Args:
        name: Module name (usually __name__)

    Returns:
        CorrelatedLogger instance
    """
    return CorrelatedLogger(logging.getLogger(name))


class CorrelationIDFilter(logging.Filter):
    """
    Logging filter that adds correlation ID to log records.

    Use this with standard logging to add correlation_id field
    to all log records.

    Usage:
        handler = logging.StreamHandler()
        handler.addFilter(CorrelationIDFilter())

        formatter = logging.Formatter(
            '%(asctime)s [%(correlation_id)s] %(message)s'
        )
        handler.setFormatter(formatter)
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Add correlation_id to log record."""
        record.correlation_id = get_correlation_id() or "no-cid"
        record.operation_name = get_operation_name() or ""
        return True


def setup_correlated_logging(
    logger: logging.Logger = None,
    log_format: str = None
) -> logging.Logger:
    """
    Setup logging with correlation ID support.

    Adds CorrelationIDFilter to logger and configures formatter
    to include correlation_id field.

    Args:
        logger: Logger to configure (default: root logger)
        log_format: Custom format string (must include %(correlation_id)s)

    Returns:
        Configured logger
    """
    if logger is None:
        logger = logging.getLogger()

    # Default format with correlation ID
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "[%(correlation_id)s] %(message)s"
        )

    # Add filter to all handlers
    cid_filter = CorrelationIDFilter()
    for handler in logger.handlers:
        handler.addFilter(cid_filter)
        handler.setFormatter(logging.Formatter(log_format))

    # If no handlers, add one
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.addFilter(cid_filter)
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)

    return logger
