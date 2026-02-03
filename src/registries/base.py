"""
Base Registry class for plugin architecture.

Provides a generic registry pattern that all specific registries inherit from.
Enables B2B multi-tenant support with pluggable implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar, Generic, Any, Optional, Callable
import logging
import threading

T = TypeVar('T')

logger = logging.getLogger(__name__)


class Registry(Generic[T], ABC):
    """
    Base class for all registries.

    Provides thread-safe registration and retrieval of implementations.
    Each registry subclass maintains its own singleton instance.

    Usage:
        @MyRegistry.register("my_impl")
        class MyImplementation(MyInterface):
            pass

        impl = MyRegistry.get_instance().get("my_impl", config={})
    """

    _instances: Dict[str, 'Registry'] = {}
    _lock = threading.Lock()

    def __init__(self):
        self._registry: Dict[str, Type[T]] = {}
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @classmethod
    def get_instance(cls) -> 'Registry[T]':
        """
        Get the singleton instance of this registry.

        Thread-safe singleton pattern.
        """
        with cls._lock:
            class_name = cls.__name__
            if class_name not in cls._instances:
                cls._instances[class_name] = cls()
                logger.debug(f"Created singleton instance of {class_name}")
            return cls._instances[class_name]

    @classmethod
    def register(cls, name: str) -> Callable[[Type[T]], Type[T]]:
        """
        Decorator to register an implementation.

        Args:
            name: Unique identifier for this implementation

        Returns:
            Decorator function

        Usage:
            @MyRegistry.register("my_impl")
            class MyImplementation(MyInterface):
                pass
        """
        def decorator(impl_class: Type[T]) -> Type[T]:
            instance = cls.get_instance()
            with cls._lock:
                if name in instance._registry:
                    logger.warning(
                        f"Overwriting existing registration '{name}' in {cls.__name__}"
                    )
                instance._registry[name] = impl_class
                logger.info(f"Registered '{name}' -> {impl_class.__name__} in {cls.__name__}")
            return impl_class
        return decorator

    def get(self, name: str, config: Optional[Dict[str, Any]] = None) -> T:
        """
        Get an implementation instance by name.

        Args:
            name: Registered implementation name
            config: Configuration dict passed to implementation constructor

        Returns:
            Instance of the registered implementation

        Raises:
            KeyError: If name is not registered
        """
        if name not in self._registry:
            available = ", ".join(sorted(self._registry.keys()))
            raise KeyError(
                f"Unknown implementation '{name}' in {self.__class__.__name__}. "
                f"Available: [{available}]"
            )

        impl_class = self._registry[name]
        config = config or {}

        self._logger.debug(f"Creating instance of '{name}' with config: {config}")
        return impl_class(config)

    def list_available(self) -> list[str]:
        """
        List all registered implementation names.

        Returns:
            Sorted list of registered names
        """
        return sorted(self._registry.keys())

    def is_registered(self, name: str) -> bool:
        """
        Check if an implementation is registered.

        Args:
            name: Implementation name to check

        Returns:
            True if registered, False otherwise
        """
        return name in self._registry

    def get_class(self, name: str) -> Type[T]:
        """
        Get the implementation class (not an instance).

        Args:
            name: Registered implementation name

        Returns:
            The registered class

        Raises:
            KeyError: If name is not registered
        """
        if name not in self._registry:
            available = ", ".join(sorted(self._registry.keys()))
            raise KeyError(
                f"Unknown implementation '{name}' in {self.__class__.__name__}. "
                f"Available: [{available}]"
            )
        return self._registry[name]

    def unregister(self, name: str) -> bool:
        """
        Remove a registered implementation.

        Primarily used for testing.

        Args:
            name: Implementation name to remove

        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if name in self._registry:
                del self._registry[name]
                self._logger.info(f"Unregistered '{name}' from {self.__class__.__name__}")
                return True
            return False

    def clear(self) -> None:
        """
        Remove all registered implementations.

        Primarily used for testing.
        """
        with self._lock:
            count = len(self._registry)
            self._registry.clear()
            self._logger.info(f"Cleared {count} registrations from {self.__class__.__name__}")

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset the singleton instance.

        Primarily used for testing to ensure clean state.
        """
        with cls._lock:
            class_name = cls.__name__
            if class_name in cls._instances:
                del cls._instances[class_name]
                logger.debug(f"Reset singleton instance of {class_name}")


class RegistryError(Exception):
    """Base exception for registry errors."""
    pass


class ImplementationNotFoundError(RegistryError, KeyError):
    """Raised when a requested implementation is not found."""

    def __init__(self, name: str, registry_name: str, available: list[str]):
        self.name = name
        self.registry_name = registry_name
        self.available = available
        super().__init__(
            f"Implementation '{name}' not found in {registry_name}. "
            f"Available: {available}"
        )


class DuplicateRegistrationError(RegistryError):
    """Raised when attempting to register a duplicate name."""

    def __init__(self, name: str, registry_name: str):
        self.name = name
        self.registry_name = registry_name
        super().__init__(
            f"Implementation '{name}' is already registered in {registry_name}"
        )
