"""
Tests for event-driven architecture utilities.
"""

import pytest
from unittest.mock import Mock, call

from src.utils.events import (
    Event,
    EventBus,
    EventPriority,
    EventSubscription,
    EventNames,
    get_event_bus,
    publish,
    subscribe,
    emit_data_loaded,
    emit_trigger_fired,
    emit_validation_completed,
)


class TestEvent:
    """Tests for Event class."""

    def test_event_creation(self):
        """Event can be created with required fields."""
        event = Event(name="test.event", data={"key": "value"})

        assert event.name == "test.event"
        assert event.data == {"key": "value"}
        assert event.timestamp is not None

    def test_event_to_dict(self):
        """Event.to_dict() returns proper dict."""
        event = Event(
            name="test.event",
            data={"key": "value"},
            source="test",
            correlation_id="cid-123",
        )

        d = event.to_dict()

        assert d["name"] == "test.event"
        assert d["data"] == {"key": "value"}
        assert d["source"] == "test"
        assert d["correlation_id"] == "cid-123"
        assert "timestamp" in d


class TestEventBus:
    """Tests for EventBus class."""

    def test_subscribe_and_publish(self):
        """Basic subscribe and publish works."""
        bus = EventBus(name="test")
        handler = Mock()

        bus.subscribe("test.event", handler)
        bus.publish("test.event", {"key": "value"})

        handler.assert_called_once()
        event = handler.call_args[0][0]
        assert event.name == "test.event"
        assert event.data == {"key": "value"}

    def test_multiple_subscribers(self):
        """Multiple subscribers receive the same event."""
        bus = EventBus(name="test")
        handler1 = Mock()
        handler2 = Mock()

        bus.subscribe("test.event", handler1)
        bus.subscribe("test.event", handler2)
        bus.publish("test.event", {})

        handler1.assert_called_once()
        handler2.assert_called_once()

    def test_wildcard_subscription(self):
        """Wildcard subscriptions work."""
        bus = EventBus(name="test")
        handler = Mock()

        bus.subscribe("test.*", handler)

        bus.publish("test.event1", {})
        bus.publish("test.event2", {})
        bus.publish("other.event", {})  # Should not match

        assert handler.call_count == 2

    def test_star_wildcard_matches_all(self):
        """Star wildcard matches all events."""
        bus = EventBus(name="test")
        handler = Mock()

        bus.subscribe("*", handler)

        bus.publish("any.event", {})
        bus.publish("another.event", {})

        assert handler.call_count == 2

    def test_priority_ordering(self):
        """Handlers are called in priority order."""
        bus = EventBus(name="test")
        call_order = []

        def low_handler(e):
            call_order.append("low")

        def normal_handler(e):
            call_order.append("normal")

        def high_handler(e):
            call_order.append("high")

        bus.subscribe("test.event", low_handler, EventPriority.LOW)
        bus.subscribe("test.event", normal_handler, EventPriority.NORMAL)
        bus.subscribe("test.event", high_handler, EventPriority.HIGH)

        bus.publish("test.event", {})

        # High priority first
        assert call_order == ["high", "normal", "low"]

    def test_filter_function(self):
        """Filter function controls which events handler receives."""
        bus = EventBus(name="test")
        handler = Mock()

        # Only receive events where data["important"] is True
        bus.subscribe(
            "test.event",
            handler,
            filter_func=lambda e: e.data.get("important", False)
        )

        bus.publish("test.event", {"important": False})
        bus.publish("test.event", {"important": True})
        bus.publish("test.event", {})

        # Only the important one should be received
        assert handler.call_count == 1

    def test_unsubscribe(self):
        """Unsubscribe removes handler."""
        bus = EventBus(name="test")
        handler = Mock()

        bus.subscribe("test.event", handler)
        bus.publish("test.event", {})
        assert handler.call_count == 1

        result = bus.unsubscribe("test.event", handler)
        assert result is True

        bus.publish("test.event", {})
        assert handler.call_count == 1  # Not called again

    def test_unsubscribe_nonexistent_returns_false(self):
        """Unsubscribe returns False if handler not found."""
        bus = EventBus(name="test")
        handler = Mock()

        result = bus.unsubscribe("test.event", handler)

        assert result is False

    def test_handler_exception_does_not_stop_others(self):
        """Exception in one handler doesn't stop other handlers."""
        bus = EventBus(name="test")

        def failing_handler(e):
            raise RuntimeError("Handler failed")

        success_handler = Mock()

        bus.subscribe("test.event", failing_handler)
        bus.subscribe("test.event", success_handler)

        # Should not raise
        bus.publish("test.event", {})

        # Other handler still called
        success_handler.assert_called_once()

    def test_event_history(self):
        """Event history is recorded."""
        bus = EventBus(name="test")

        bus.publish("event1", {"a": 1})
        bus.publish("event2", {"b": 2})
        bus.publish("event3", {"c": 3})

        history = bus.get_event_history(limit=10)

        assert len(history) == 3
        # Newest first
        assert history[0].name == "event3"
        assert history[1].name == "event2"
        assert history[2].name == "event1"

    def test_event_history_filtered(self):
        """Event history can be filtered by event name."""
        bus = EventBus(name="test")

        bus.publish("event1", {})
        bus.publish("event2", {})
        bus.publish("event1", {})

        history = bus.get_event_history(event_name="event1")

        assert len(history) == 2
        assert all(e.name == "event1" for e in history)

    def test_clear_history(self):
        """Clear history removes all events."""
        bus = EventBus(name="test")

        bus.publish("event1", {})
        bus.publish("event2", {})
        bus.clear_history()

        history = bus.get_event_history()
        assert len(history) == 0

    def test_get_subscriptions(self):
        """Get subscriptions returns counts."""
        bus = EventBus(name="test")

        bus.subscribe("event1", Mock())
        bus.subscribe("event1", Mock())
        bus.subscribe("event2", Mock())

        subs = bus.get_subscriptions()

        assert subs["event1"] == 2
        assert subs["event2"] == 1

    def test_publish_returns_event(self):
        """Publish returns the created event."""
        bus = EventBus(name="test")

        event = bus.publish("test.event", {"key": "value"}, source="test")

        assert isinstance(event, Event)
        assert event.name == "test.event"
        assert event.data == {"key": "value"}
        assert event.source == "test"


class TestGlobalEventBus:
    """Tests for global event bus functions."""

    def test_get_event_bus_returns_singleton(self):
        """get_event_bus returns same instance."""
        bus1 = get_event_bus()
        bus2 = get_event_bus()

        assert bus1 is bus2

    def test_publish_uses_global_bus(self):
        """publish() uses the global event bus."""
        handler = Mock()
        get_event_bus().subscribe("global.test", handler)

        publish("global.test", {"test": True})

        handler.assert_called_once()

    def test_subscribe_decorator(self):
        """@subscribe decorator registers handler."""
        received = []

        @subscribe("decorator.test")
        def handler(event):
            received.append(event)

        publish("decorator.test", {"key": "value"})

        assert len(received) == 1
        assert received[0].data == {"key": "value"}


class TestEventHelpers:
    """Tests for event emission helpers."""

    def test_emit_data_loaded(self):
        """emit_data_loaded creates correct event."""
        handler = Mock()
        get_event_bus().subscribe(EventNames.DATA_LOADED, handler)

        event = emit_data_loaded("test.csv", 100, extra_field="value")

        handler.assert_called_once()
        received = handler.call_args[0][0]
        assert received.name == EventNames.DATA_LOADED
        assert received.data["source"] == "test.csv"
        assert received.data["rows"] == 100
        assert received.data["extra_field"] == "value"

    def test_emit_trigger_fired(self):
        """emit_trigger_fired creates correct event."""
        handler = Mock()
        get_event_bus().subscribe(EventNames.TRIGGER_FIRED, handler)

        event = emit_trigger_fired(
            trigger_id="t1",
            trigger_name="Test Trigger",
            priority="P1"
        )

        handler.assert_called_once()
        received = handler.call_args[0][0]
        assert received.data["trigger_id"] == "t1"
        assert received.data["trigger_name"] == "Test Trigger"
        assert received.data["priority"] == "P1"

    def test_emit_validation_completed(self):
        """emit_validation_completed creates correct event."""
        handler = Mock()
        get_event_bus().subscribe(EventNames.VALIDATION_COMPLETED, handler)

        event = emit_validation_completed(
            validator="gate1",
            status="pass",
            issues_count=0
        )

        handler.assert_called_once()
        received = handler.call_args[0][0]
        assert received.data["validator"] == "gate1"
        assert received.data["status"] == "pass"
        assert received.data["issues_count"] == 0


class TestEventNames:
    """Tests for EventNames constants."""

    def test_event_names_are_strings(self):
        """All event names are strings."""
        assert isinstance(EventNames.DATA_LOADED, str)
        assert isinstance(EventNames.TRIGGER_FIRED, str)
        assert isinstance(EventNames.VALIDATION_COMPLETED, str)

    def test_event_names_follow_convention(self):
        """Event names follow dot notation convention."""
        assert "." in EventNames.DATA_LOADED
        assert "." in EventNames.TRIGGER_FIRED
        assert "." in EventNames.SYSTEM_HEALTH_CHANGED
