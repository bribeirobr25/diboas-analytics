"""
Serialization utilities for consistent data conversion.

DRY Principle (Principle 4):
---------------------------
This module provides a shared interface for converting objects to dictionaries,
avoiding repeated implementations of to_dict() methods across the codebase.

Usage:
    from src.utils.serialization import Serializable, to_dict_safe

    @dataclass
    class MyData(Serializable):
        name: str
        value: float

        def to_dict(self) -> Dict[str, Any]:
            return {'name': self.name, 'value': round(self.value, 2)}

    # Or use the helper for external objects
    result = to_dict_safe(my_object)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, is_dataclass, asdict
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable
import numpy as np


@runtime_checkable
class HasToDict(Protocol):
    """Protocol for objects that have a to_dict() method."""
    def to_dict(self) -> Dict[str, Any]: ...


class Serializable(ABC):
    """
    Abstract base class for serializable objects.

    Subclasses must implement to_dict() to define their serialization format.
    This provides a consistent interface across the codebase.
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert object to dictionary for serialization.

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        pass

    def to_json_safe(self) -> Dict[str, Any]:
        """
        Convert to a JSON-safe dictionary.

        Handles special types like datetime, Enum, numpy arrays.

        Returns:
            Dictionary with JSON-serializable values.
        """
        return make_json_safe(self.to_dict())


def make_json_safe(obj: Any) -> Any:
    """
    Convert an object to a JSON-safe representation.

    Handles:
    - datetime/date -> ISO format string
    - Enum -> value
    - numpy arrays -> lists
    - numpy types -> Python native types
    - Objects with to_dict() -> dict
    - Dataclasses -> dict

    Args:
        obj: Any Python object

    Returns:
        JSON-serializable representation
    """
    if obj is None:
        return None

    # Handle datetime types
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return str(obj)

    # Handle Enum
    if isinstance(obj, Enum):
        return obj.value

    # Handle numpy types
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)

    # Handle objects with to_dict
    if isinstance(obj, HasToDict):
        return make_json_safe(obj.to_dict())

    # Handle dataclasses
    if is_dataclass(obj) and not isinstance(obj, type):
        return make_json_safe(asdict(obj))

    # Handle collections
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_json_safe(item) for item in obj]
    if isinstance(obj, set):
        return [make_json_safe(item) for item in sorted(obj)]

    # Handle basic types (str, int, float, bool)
    return obj


def to_dict_safe(obj: Any) -> Dict[str, Any]:
    """
    Safely convert an object to a dictionary.

    Handles objects with to_dict(), dataclasses, and plain dicts.

    Args:
        obj: Object to convert

    Returns:
        Dictionary representation

    Raises:
        TypeError: If object cannot be converted to dict
    """
    if isinstance(obj, dict):
        return make_json_safe(obj)

    if isinstance(obj, HasToDict):
        return make_json_safe(obj.to_dict())

    if is_dataclass(obj) and not isinstance(obj, type):
        return make_json_safe(asdict(obj))

    raise TypeError(f"Cannot convert {type(obj).__name__} to dict")


def round_floats(data: Dict[str, Any], precision: int = 2) -> Dict[str, Any]:
    """
    Round all float values in a dictionary to specified precision.

    Useful for financial data where exact precision is important.

    Args:
        data: Dictionary with potentially float values
        precision: Decimal places to round to

    Returns:
        Dictionary with rounded float values
    """
    result = {}
    for key, value in data.items():
        if isinstance(value, float):
            result[key] = round(value, precision)
        elif isinstance(value, dict):
            result[key] = round_floats(value, precision)
        elif isinstance(value, list):
            result[key] = [
                round(v, precision) if isinstance(v, float) else v
                for v in value
            ]
        else:
            result[key] = value
    return result


@dataclass
class SerializableDataclass:
    """
    Mixin providing automatic to_dict() for dataclasses.

    Usage:
        @dataclass
        class MyData(SerializableDataclass):
            name: str
            value: float

        # Automatically has to_dict()
        data = MyData("test", 3.14159)
        d = data.to_dict()  # {'name': 'test', 'value': 3.14159}
    """

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to JSON-safe dictionary."""
        return make_json_safe(asdict(self))


# Type alias for serializable objects
SerializableType = Union[Dict[str, Any], HasToDict, 'Serializable']
