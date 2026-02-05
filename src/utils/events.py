"""
Event-driven architecture utilities.

Principle 10 (Event-Driven Communication):
------------------------------------------
Provides a lightweight event bus for decoupled communication between
components. Events are published without knowledge of subscribers,
allowing loose coupling and extensibility.

Principle 11 (Audit & Compliance):
----------------------------------
All events are logged for audit trail purposes, enabling reconstruction
of system behavior and compliance verification.

Usage:
    from src.utils.events import (
        EventBus,
        Event,
        get_event_bus,
        subscribe,
        publish,
    )

    # Subscribe to events
    @subscribe("data.loaded")
    def on_data_loaded(event):
        print(f"Data loaded: {event.data}")

    # Publish events
    publish("data.loaded", {"source": "crypto_prices.csv", "rows": 1000})

    # Or use EventBus directly
    bus = get_event_bus()
    bus.subscribe("trigger.fired", handler_func)
    bus.publish("trigger.fired", {"trigger_id": "usdc_depeg_l2"})
"""

import logging
import functools
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set
from threading import Lock
from enum import Enum

logger = logging.getLogger(__name__)


class EventPriority(Enum):
    """Priority levels for event handlers."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Event:
    """
    Represents an event in the system.

    Attributes:
        name: Event name (e.g., "data.loaded", "trigger.fired")
        data: Event payload (arbitrary data)
        timestamp: When the event was created
        source: Optional source identifier
        correlation_id: Optional correlation ID for tracing
    """
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: Optional[str] = None
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "correlation_id": self.correlation_id,
        }


@dataclass
class EventSubscription:
    """Represents a subscription to an event."""
    handler: Callable[[Event], None]
    priority: EventPriority = EventPriority.NORMAL
    filter_func: Optional[Callable[[Event], bool]] = None


class EventBus:
    """
    Simple event bus for pub/sub communication.

    Supports:
    - Multiple subscribers per event
    - Wildcard subscriptions (e.g., "data.*")
    - Handler priorities
    - Event filtering
    - Audit logging

    Thread-safe for concurrent access.

    Usage:
        bus = EventBus()

        # Subscribe
        bus.subscribe("user.created", handle_user_created)
        bus.subscribe("user.*", log_all_user_events)  # Wildcard

        # Publish
        bus.publish("user.created", {"user_id": 123})
    """

    def __init__(self, name: str = "default"):
        """
        Initialize event bus.

        Args:
            name: Bus identifier for logging
        """
        self.name = name
        self._subscriptions: Dict[str, List[EventSubscription]] = {}
        self._lock = Lock()
        self._event_history: List[Event] = []
        self._max_history = 1000
        self._audit_enabled = True

    def subscribe(
        self,
        event_name: str,
        handler: Callable[[Event], None],
        priority: EventPriority = EventPriority.NORMAL,
        filter_func: Optional[Callable[[Event], bool]] = None,
    ) -> None:
        """
        Subscribe to an event.

        Args:
            event_name: Event name or pattern (supports * wildcard)
            handler: Function to call when event occurs
            priority: Handler priority (higher = called first)
            filter_func: Optional filter function (return True to receive)
        """
        with self._lock:
            if event_name not in self._subscriptions:
                self._subscriptions[event_name] = []

            subscription = EventSubscription(
                handler=handler,
                priority=priority,
                filter_func=filter_func,
            )
            self._subscriptions[event_name].append(subscription)

            # Sort by priority (highest first)
            self._subscriptions[event_name].sort(
                key=lambda s: s.priority.value,
                reverse=True
            )

            handler_name = getattr(handler, '__name__', repr(handler))
            logger.debug(
                f"EventBus[{self.name}]: Subscribed {handler_name} "
                f"to '{event_name}'"
            )

    def unsubscribe(
        self,
        event_name: str,
        handler: Callable[[Event], None]
    ) -> bool:
        """
        Unsubscribe from an event.

        Args:
            event_name: Event name
            handler: Handler to remove

        Returns:
            True if handler was removed
        """
        with self._lock:
            if event_name not in self._subscriptions:
                return False

            original_len = len(self._subscriptions[event_name])
            self._subscriptions[event_name] = [
                s for s in self._subscriptions[event_name]
                if s.handler != handler
            ]

            removed = len(self._subscriptions[event_name]) < original_len

            if removed:
                handler_name = getattr(handler, '__name__', repr(handler))
                logger.debug(
                    f"EventBus[{self.name}]: Unsubscribed {handler_name} "
                    f"from '{event_name}'"
                )

            return removed

    def publish(
        self,
        event_name: str,
        data: Dict[str, Any] = None,
        source: str = None,
        correlation_id: str = None,
    ) -> Event:
        """
        Publish an event.

        Args:
            event_name: Event name
            data: Event payload
            source: Optional source identifier
            correlation_id: Optional correlation ID

        Returns:
            The published Event object
        """
        # Get correlation ID from context if not provided
        if correlation_id is None:
            try:
                from src.utils.correlation import get_correlation_id
                correlation_id = get_correlation_id()
            except ImportError:
                pass

        event = Event(
            name=event_name,
            data=data or {},
            source=source,
            correlation_id=correlation_id,
        )

        # Audit log
        if self._audit_enabled:
            self._record_event(event)

        # Find matching handlers
        handlers = self._get_handlers(event_name)

        # Call handlers
        for subscription in handlers:
            try:
                # Apply filter if present
                if subscription.filter_func and not subscription.filter_func(event):
                    continue

                subscription.handler(event)

            except Exception as e:
                handler_name = getattr(subscription.handler, '__name__', repr(subscription.handler))
                logger.error(
                    f"EventBus[{self.name}]: Handler {handler_name} "
                    f"failed for event '{event_name}': {e}"
                )

        logger.debug(
            f"EventBus[{self.name}]: Published '{event_name}' "
            f"to {len(handlers)} handlers"
        )

        return event

    def _get_handlers(self, event_name: str) -> List[EventSubscription]:
        """
        Get all handlers matching an event name.

        Includes exact matches and wildcard patterns.
        """
        with self._lock:
            handlers = []

            for pattern, subscriptions in self._subscriptions.items():
                if self._matches_pattern(pattern, event_name):
                    handlers.extend(subscriptions)

            # Re-sort combined handlers by priority
            handlers.sort(key=lambda s: s.priority.value, reverse=True)

            return handlers

    def _matches_pattern(self, pattern: str, event_name: str) -> bool:
        """Check if event name matches pattern (supports * wildcard)."""
        if pattern == event_name:
            return True

        if "*" not in pattern:
            return False

        # Simple wildcard matching
        if pattern == "*":
            return True

        if pattern.endswith(".*"):
            prefix = pattern[:-2]
            return event_name.startswith(prefix + ".")

        if pattern.startswith("*."):
            suffix = pattern[2:]
            return event_name.endswith("." + suffix)

        return False

    def _record_event(self, event: Event) -> None:
        """Record event in history for audit."""
        with self._lock:
            self._event_history.append(event)

            # Trim history if too long
            if len(self._event_history) > self._max_history:
                self._event_history = self._event_history[-self._max_history:]

    def get_event_history(
        self,
        event_name: str = None,
        limit: int = 100
    ) -> List[Event]:
        """
        Get event history for audit purposes.

        Args:
            event_name: Filter by event name (optional)
            limit: Maximum events to return

        Returns:
            List of events (newest first)
        """
        with self._lock:
            events = list(reversed(self._event_history))

            if event_name:
                events = [e for e in events if e.name == event_name]

            return events[:limit]

    def clear_history(self) -> None:
        """Clear event history."""
        with self._lock:
            self._event_history.clear()

    def get_subscriptions(self) -> Dict[str, int]:
        """Get subscription counts by event name."""
        with self._lock:
            return {
                name: len(subs)
                for name, subs in self._subscriptions.items()
            }


# Global event bus instance
_global_bus: Optional[EventBus] = None
_global_bus_lock = Lock()


def get_event_bus() -> EventBus:
    """
    Get the global event bus instance.

    Returns:
        Global EventBus singleton
    """
    global _global_bus
    with _global_bus_lock:
        if _global_bus is None:
            _global_bus = EventBus(name="global")
        return _global_bus


def publish(
    event_name: str,
    data: Dict[str, Any] = None,
    source: str = None,
) -> Event:
    """
    Publish an event to the global event bus.

    Args:
        event_name: Event name
        data: Event payload
        source: Optional source identifier

    Returns:
        The published Event object
    """
    return get_event_bus().publish(event_name, data, source)


def subscribe(
    event_name: str,
    priority: EventPriority = EventPriority.NORMAL,
    filter_func: Optional[Callable[[Event], bool]] = None,
):
    """
    Decorator to subscribe a function to an event.

    Args:
        event_name: Event name or pattern
        priority: Handler priority
        filter_func: Optional filter function

    Example:
        @subscribe("data.loaded")
        def handle_data_loaded(event):
            print(f"Loaded: {event.data}")

        @subscribe("trigger.*", priority=EventPriority.HIGH)
        def log_all_triggers(event):
            logger.info(f"Trigger event: {event.name}")
    """
    def decorator(func: Callable[[Event], None]) -> Callable[[Event], None]:
        get_event_bus().subscribe(
            event_name,
            func,
            priority=priority,
            filter_func=filter_func,
        )
        return func
    return decorator


# Standard event names for the diBoaS system
class EventNames:
    """Standard event names used in the system."""

    # Data events
    DATA_LOADED = "data.loaded"
    DATA_REFRESH_STARTED = "data.refresh.started"
    DATA_REFRESH_COMPLETED = "data.refresh.completed"
    DATA_VALIDATION_FAILED = "data.validation.failed"

    # Trigger events
    TRIGGER_EVALUATED = "trigger.evaluated"
    TRIGGER_FIRED = "trigger.fired"
    TRIGGER_COOLED_DOWN = "trigger.cooled_down"

    # Validation events
    VALIDATION_STARTED = "validation.started"
    VALIDATION_COMPLETED = "validation.completed"
    VALIDATION_FAILED = "validation.failed"

    # Adelaide events
    ADELAIDE_GENERATION_STARTED = "adelaide.generation.started"
    ADELAIDE_GENERATION_COMPLETED = "adelaide.generation.completed"
    ADELAIDE_GENERATION_FAILED = "adelaide.generation.failed"

    # Crisis events
    CRISIS_DETECTED = "crisis.detected"
    CRISIS_ESCALATED = "crisis.escalated"
    CRISIS_RESOLVED = "crisis.resolved"

    # System events
    SYSTEM_HEALTH_CHANGED = "system.health.changed"
    CIRCUIT_OPENED = "circuit.opened"
    CIRCUIT_CLOSED = "circuit.closed"


def emit_data_loaded(source: str, rows: int, **extra) -> Event:
    """Emit a data.loaded event."""
    return publish(
        EventNames.DATA_LOADED,
        {"source": source, "rows": rows, **extra},
        source="data_collector"
    )


def emit_trigger_fired(
    trigger_id: str,
    trigger_name: str,
    priority: str,
    **extra
) -> Event:
    """Emit a trigger.fired event."""
    return publish(
        EventNames.TRIGGER_FIRED,
        {
            "trigger_id": trigger_id,
            "trigger_name": trigger_name,
            "priority": priority,
            **extra
        },
        source="trigger_engine"
    )


def emit_validation_completed(
    validator: str,
    status: str,
    issues_count: int,
    **extra
) -> Event:
    """Emit a validation.completed event."""
    return publish(
        EventNames.VALIDATION_COMPLETED,
        {
            "validator": validator,
            "status": status,
            "issues_count": issues_count,
            **extra
        },
        source="validator"
    )
