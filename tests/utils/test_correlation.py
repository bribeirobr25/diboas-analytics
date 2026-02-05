"""
Tests for correlation ID utilities.
"""

import pytest
import logging
from unittest.mock import Mock, patch

from src.utils.correlation import (
    generate_correlation_id,
    get_correlation_id,
    set_correlation_id,
    new_correlation_id,
    get_operation_name,
    clear_correlation_context,
    correlation_context,
    with_correlation_id,
    CorrelatedLogger,
    get_correlated_logger,
    CorrelationIDFilter,
    setup_correlated_logging,
)


class TestCorrelationIDBasics:
    """Tests for basic correlation ID functions."""

    def setup_method(self):
        """Clear context before each test."""
        clear_correlation_context()

    def test_generate_correlation_id_format(self):
        """Generated ID has expected format."""
        cid = generate_correlation_id()

        # Format: cid-YYYYMMDDHHMMSS-xxxxxxxx
        parts = cid.split("-")
        assert len(parts) == 3
        assert parts[0] == "cid"
        assert len(parts[1]) == 14  # YYYYMMDDHHMMSS
        assert len(parts[2]) == 8   # UUID short

    def test_generate_correlation_id_with_prefix(self):
        """Generated ID uses custom prefix."""
        cid = generate_correlation_id(prefix="order")

        assert cid.startswith("order-")

    def test_generate_correlation_id_unique(self):
        """Generated IDs are unique."""
        ids = [generate_correlation_id() for _ in range(100)]
        assert len(set(ids)) == 100

    def test_get_correlation_id_returns_none_initially(self):
        """get_correlation_id returns None when not set."""
        assert get_correlation_id() is None

    def test_set_and_get_correlation_id(self):
        """set_correlation_id and get_correlation_id work together."""
        set_correlation_id("test-123")

        assert get_correlation_id() == "test-123"

    def test_new_correlation_id_sets_and_returns(self):
        """new_correlation_id generates, sets, and returns ID."""
        cid = new_correlation_id()

        assert cid is not None
        assert get_correlation_id() == cid

    def test_clear_correlation_context(self):
        """clear_correlation_context removes all context."""
        set_correlation_id("test-123")
        clear_correlation_context()

        assert get_correlation_id() is None


class TestCorrelationContext:
    """Tests for correlation_context context manager."""

    def setup_method(self):
        """Clear context before each test."""
        clear_correlation_context()

    def test_correlation_context_sets_id(self):
        """Context manager sets correlation ID."""
        with correlation_context("test_op") as cid:
            assert get_correlation_id() == cid
            assert cid is not None

    def test_correlation_context_sets_operation_name(self):
        """Context manager sets operation name."""
        with correlation_context("my_operation"):
            assert get_operation_name() == "my_operation"

    def test_correlation_context_clears_on_exit(self):
        """Context manager restores previous context on exit."""
        set_correlation_id("outer-cid")

        with correlation_context("inner_op"):
            assert get_correlation_id() != "outer-cid"

        assert get_correlation_id() == "outer-cid"

    def test_correlation_context_uses_provided_id(self):
        """Context manager uses provided correlation ID."""
        with correlation_context("op", correlation_id="my-custom-id"):
            assert get_correlation_id() == "my-custom-id"

    def test_correlation_context_uses_custom_prefix(self):
        """Context manager uses custom prefix for generated ID."""
        with correlation_context("op", prefix="api") as cid:
            assert cid.startswith("api-")

    def test_nested_correlation_contexts(self):
        """Nested contexts work correctly."""
        with correlation_context("outer") as outer_cid:
            assert get_correlation_id() == outer_cid
            assert get_operation_name() == "outer"

            with correlation_context("inner") as inner_cid:
                assert get_correlation_id() == inner_cid
                assert get_operation_name() == "inner"

            # Back to outer
            assert get_correlation_id() == outer_cid
            assert get_operation_name() == "outer"


class TestWithCorrelationIdDecorator:
    """Tests for with_correlation_id decorator."""

    def setup_method(self):
        """Clear context before each test."""
        clear_correlation_context()

    def test_decorator_sets_correlation_id(self):
        """Decorator sets correlation ID for function."""
        @with_correlation_id
        def my_function():
            return get_correlation_id()

        result = my_function()

        assert result is not None

    def test_decorator_clears_after_function(self):
        """Decorator clears context after function completes."""
        @with_correlation_id
        def my_function():
            pass

        my_function()

        assert get_correlation_id() is None

    def test_decorator_with_custom_prefix(self):
        """Decorator accepts custom prefix."""
        @with_correlation_id(prefix="handler")
        def my_function():
            return get_correlation_id()

        result = my_function()

        assert result.startswith("handler-")

    def test_decorator_preserves_existing_id(self):
        """Decorator doesn't override existing correlation ID."""
        set_correlation_id("existing-id")

        @with_correlation_id
        def my_function():
            return get_correlation_id()

        result = my_function()

        assert result == "existing-id"

    def test_decorator_preserves_function_metadata(self):
        """Decorator preserves function name and docstring."""
        @with_correlation_id
        def my_function():
            """My docstring."""
            pass

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."


class TestCorrelatedLogger:
    """Tests for CorrelatedLogger class."""

    def setup_method(self):
        """Clear context before each test."""
        clear_correlation_context()

    def test_correlated_logger_adds_cid_to_message(self):
        """Logger adds correlation ID to messages."""
        mock_logger = Mock()
        logger = CorrelatedLogger(mock_logger)

        set_correlation_id("test-cid")
        logger.info("Test message")

        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "[test-cid]" in call_args
        assert "Test message" in call_args

    def test_correlated_logger_adds_operation_name(self):
        """Logger adds operation name to messages."""
        mock_logger = Mock()
        logger = CorrelatedLogger(mock_logger)

        with correlation_context("my_op"):
            logger.info("Test message")

        call_args = mock_logger.info.call_args[0][0]
        assert "[my_op]" in call_args

    def test_correlated_logger_without_context(self):
        """Logger works without correlation context."""
        mock_logger = Mock()
        logger = CorrelatedLogger(mock_logger)

        logger.info("Test message")

        mock_logger.info.assert_called_once_with("Test message")

    def test_correlated_logger_all_levels(self):
        """Logger supports all log levels."""
        mock_logger = Mock()
        logger = CorrelatedLogger(mock_logger)

        set_correlation_id("test-cid")

        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")

        assert mock_logger.debug.called
        assert mock_logger.info.called
        assert mock_logger.warning.called
        assert mock_logger.error.called
        assert mock_logger.critical.called

    def test_get_correlated_logger(self):
        """get_correlated_logger returns CorrelatedLogger."""
        logger = get_correlated_logger("test.module")

        assert isinstance(logger, CorrelatedLogger)


class TestCorrelationIDFilter:
    """Tests for CorrelationIDFilter logging filter."""

    def setup_method(self):
        """Clear context before each test."""
        clear_correlation_context()

    def test_filter_adds_correlation_id_to_record(self):
        """Filter adds correlation_id attribute to log record."""
        filter_ = CorrelationIDFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test",
            args=(),
            exc_info=None,
        )

        set_correlation_id("filter-test-id")
        filter_.filter(record)

        assert record.correlation_id == "filter-test-id"

    def test_filter_uses_no_cid_when_not_set(self):
        """Filter uses 'no-cid' when correlation ID not set."""
        filter_ = CorrelationIDFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test",
            args=(),
            exc_info=None,
        )

        filter_.filter(record)

        assert record.correlation_id == "no-cid"

    def test_filter_always_returns_true(self):
        """Filter always returns True (doesn't filter out records)."""
        filter_ = CorrelationIDFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test",
            args=(),
            exc_info=None,
        )

        result = filter_.filter(record)

        assert result is True


class TestSetupCorrelatedLogging:
    """Tests for setup_correlated_logging function."""

    def test_setup_adds_filter_to_existing_handlers(self):
        """setup_correlated_logging adds filter to existing handlers."""
        logger = logging.getLogger("test.setup")
        handler = logging.StreamHandler()
        logger.addHandler(handler)

        setup_correlated_logging(logger)

        # Check filter was added
        assert any(
            isinstance(f, CorrelationIDFilter)
            for f in handler.filters
        )

        # Cleanup
        logger.removeHandler(handler)

    def test_setup_creates_handler_if_none(self):
        """setup_correlated_logging creates handler if none exist."""
        logger = logging.getLogger("test.setup.empty")
        logger.handlers.clear()

        setup_correlated_logging(logger)

        assert len(logger.handlers) >= 1
