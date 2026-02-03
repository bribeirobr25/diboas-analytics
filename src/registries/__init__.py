"""
diBoaS Analytics Registry Framework.

Provides pluggable architecture for B2B-ready multi-tenant support.

Registries:
- CollectorRegistry: Data source plugins (file, API, hybrid)
- ValidatorRegistry: Validation plugins (CV-01 to CV-07, data quality)
- EngineRegistry: Analytics plugins (Battle Test, Monte Carlo, etc.)
- TriggerRegistry: Alert triggers (protocol, estate, whale, regime)
- PersonaRegistry: Adelaide personas (Ana, Maria, Felipe)
- OutputRegistry: Output formatters (JSON, CSV, Markdown, newsletter, etc.)

Usage:
    from src.registries import EngineRegistry, CollectorRegistry

    # Get a registered implementation
    engine = EngineRegistry.get_instance().get("battle_test", config={})
    results = engine.run(data, {"scenario": "A"})

    # List available implementations
    engines = EngineRegistry.get_instance().list_available()
    # ['battle_test', 'monte_carlo', 'monitoring', 'anomaly']

    # Register a custom implementation
    @EngineRegistry.register("my_custom_engine")
    class MyCustomEngine(AnalyticsEngine):
        ...
"""

from src.registries.base import Registry, RegistryError, ImplementationNotFoundError, DuplicateRegistrationError
from src.registries.collector_registry import CollectorRegistry, Collector
from src.registries.validator_registry import ValidatorRegistry, Validator
from src.registries.engine_registry import EngineRegistry, AnalyticsEngine
from src.registries.trigger_registry import TriggerRegistry, Trigger, Alert, AlertSeverity
from src.registries.persona_registry import PersonaRegistry, Persona, EmojiLevel, get_persona_for_strategy
from src.registries.output_registry import OutputRegistry, OutputFormatter

__all__ = [
    # Base
    'Registry',
    'RegistryError',
    'ImplementationNotFoundError',
    'DuplicateRegistrationError',

    # Collectors
    'CollectorRegistry',
    'Collector',

    # Validators
    'ValidatorRegistry',
    'Validator',

    # Engines
    'EngineRegistry',
    'AnalyticsEngine',

    # Triggers
    'TriggerRegistry',
    'Trigger',
    'Alert',
    'AlertSeverity',

    # Personas
    'PersonaRegistry',
    'Persona',
    'EmojiLevel',
    'get_persona_for_strategy',

    # Outputs
    'OutputRegistry',
    'OutputFormatter',

    # Utilities
    'ensure_collectors_registered',
]


def list_all_registrations() -> dict:
    """
    List all registered implementations across all registries.

    Returns:
        Dict mapping registry name to list of registered implementations
    """
    return {
        'collectors': CollectorRegistry.get_instance().list_available(),
        'validators': ValidatorRegistry.get_instance().list_available(),
        'engines': EngineRegistry.get_instance().list_available(),
        'triggers': TriggerRegistry.get_instance().list_available(),
        'personas': PersonaRegistry.get_instance().list_available(),
        'outputs': OutputRegistry.get_instance().list_available(),
    }


def reset_all_registries() -> None:
    """
    Reset all registries to clean state.

    Primarily used for testing.
    """
    CollectorRegistry.reset_instance()
    ValidatorRegistry.reset_instance()
    EngineRegistry.reset_instance()
    TriggerRegistry.reset_instance()
    PersonaRegistry.reset_instance()
    OutputRegistry.reset_instance()


def ensure_collectors_registered() -> None:
    """
    Ensure all collectors are registered.

    Call this before using CollectorRegistry if you haven't
    imported src.collectors yet.
    """
    import src.collectors  # noqa: F401 - triggers registration
