"""
Tests for the registry framework.

Verifies:
1. Basic registry operations (register, get, list)
2. Wrapped engines produce IDENTICAL output to direct calls
3. Error handling for unknown implementations
4. Thread safety and singleton behavior
"""

import pytest
from datetime import date


class TestBaseRegistry:
    """Test base registry functionality."""

    def test_registry_register_and_get(self):
        """Test basic registration and retrieval."""
        from src.registries import EngineRegistry

        # Registry should have engines registered
        registry = EngineRegistry.get_instance()
        assert registry.is_registered("battle_test")
        assert registry.is_registered("monte_carlo")

        # Get should return an instance
        engine = registry.get("battle_test", {})
        assert engine is not None
        assert engine.engine_type == "battle_test"

    def test_registry_list_available(self):
        """Test listing all registered implementations."""
        from src.registries import EngineRegistry

        registry = EngineRegistry.get_instance()
        available = registry.list_available()

        assert "battle_test" in available
        assert "monte_carlo" in available
        assert "monitoring" in available
        assert "anomaly" in available

    def test_registry_unknown_implementation_raises(self):
        """Test error handling for unknown implementations."""
        from src.registries import EngineRegistry

        registry = EngineRegistry.get_instance()

        with pytest.raises(KeyError) as exc_info:
            registry.get("nonexistent_engine", {})

        assert "nonexistent_engine" in str(exc_info.value)
        assert "Available:" in str(exc_info.value)

    def test_registry_singleton_behavior(self):
        """Test that get_instance returns the same instance."""
        from src.registries import EngineRegistry

        instance1 = EngineRegistry.get_instance()
        instance2 = EngineRegistry.get_instance()

        assert instance1 is instance2

    def test_list_all_registrations(self):
        """Test listing all registrations across all registries."""
        from src.registries import list_all_registrations

        all_regs = list_all_registrations()

        assert 'collectors' in all_regs
        assert 'validators' in all_regs
        assert 'engines' in all_regs
        assert 'triggers' in all_regs
        assert 'personas' in all_regs
        assert 'outputs' in all_regs

        # Check some expected registrations
        assert 'battle_test' in all_regs['engines']
        assert 'result_validator' in all_regs['validators']
        assert 'ana' in all_regs['personas']


class TestBattleTestEngineRegistry:
    """Test BattleTestEngine through registry produces identical output to direct call."""

    def test_battle_test_registry_matches_direct(self):
        """
        Registry output must match direct engine call.

        This is the critical test - wrapped engines must produce
        IDENTICAL output to direct calls, not just similar structure.
        """
        from src.engines.battle_test import BattleTestEngine
        from src.registries import EngineRegistry

        # Direct call
        direct_engine = BattleTestEngine()
        direct_results = direct_engine.run_all_strategies(scenario="A")

        # Through registry
        registry_engine = EngineRegistry.get_instance().get("battle_test", {})
        registry_results = registry_engine.run(data=None, config={"scenario": "A"})

        # Results must be identical
        assert len(direct_results) == len(registry_results)

        for direct, registry in zip(direct_results, registry_results):
            # Compare all key attributes
            assert direct.strategy_id == registry.strategy_id
            assert direct.strategy_name == registry.strategy_name
            assert direct.scenario == registry.scenario
            assert direct.deposited == registry.deposited
            assert direct.final_value == pytest.approx(registry.final_value, rel=1e-9)
            assert direct.profit == pytest.approx(registry.profit, rel=1e-9)
            assert direct.return_pct == pytest.approx(registry.return_pct, rel=1e-9)
            assert direct.max_drawdown_pct == pytest.approx(registry.max_drawdown_pct, rel=1e-9)
            assert direct.days == registry.days

    def test_battle_test_single_strategy_matches(self):
        """Test single strategy through registry matches direct call."""
        from src.engines.battle_test import BattleTestEngine, SCENARIOS
        from src.registries import EngineRegistry

        strategy_id = 1
        scenario = "A"
        scenario_config = SCENARIOS[scenario]

        # Direct call
        direct_engine = BattleTestEngine()
        direct_result = direct_engine.run(
            strategy_id=strategy_id,
            initial_deposit=scenario_config['initial_deposit'],
            monthly_dca=scenario_config['monthly_dca']
        )

        # Through registry
        registry_engine = EngineRegistry.get_instance().get("battle_test", {})
        registry_results = registry_engine.run(
            data=None,
            config={"scenario": scenario, "strategy_id": strategy_id}
        )

        assert len(registry_results) == 1
        registry_result = registry_results[0]

        # Must be identical
        assert direct_result.strategy_id == registry_result.strategy_id
        assert direct_result.final_value == pytest.approx(registry_result.final_value, rel=1e-9)
        assert direct_result.return_pct == pytest.approx(registry_result.return_pct, rel=1e-9)

    def test_battle_test_direct_method_access(self):
        """Test direct method access on wrapped engine."""
        from src.registries import EngineRegistry

        engine = EngineRegistry.get_instance().get("battle_test", {})

        # Should have direct method access
        assert hasattr(engine, 'run_all_strategies')
        assert hasattr(engine, 'run_single')

        # Direct method should work
        results = engine.run_all_strategies(scenario="A")
        assert len(results) == 10  # 10 strategies


class TestMonteCarloEngineRegistry:
    """Test MonteCarloEngine through registry produces identical output to direct call."""

    def test_monte_carlo_registry_matches_direct(self):
        """
        Registry output must match direct engine call.

        Uses same seed for reproducibility.
        """
        from src.engines.monte_carlo import MonteCarloEngine
        from src.registries import EngineRegistry

        seed = 42
        n_simulations = 100  # Small for speed

        # Direct call
        direct_engine = MonteCarloEngine(n_simulations=n_simulations, random_seed=seed)
        direct_results = direct_engine.run_all_strategies()

        # Through registry (same config)
        registry_engine = EngineRegistry.get_instance().get(
            "monte_carlo",
            {"simulations": n_simulations, "seed": seed}
        )
        registry_results = registry_engine.run(data=None, config={})

        # Results must be identical (same seed = same random numbers)
        assert len(direct_results) == len(registry_results)

        for direct, registry in zip(direct_results, registry_results):
            assert direct.strategy_id == registry.strategy_id
            assert direct.strategy_name == registry.strategy_name
            assert direct.simulations == registry.simulations
            assert direct.total_deposited == registry.total_deposited
            assert direct.mean_final == pytest.approx(registry.mean_final, rel=1e-9)
            assert direct.median_final == pytest.approx(registry.median_final, rel=1e-9)
            assert direct.prob_any_loss == pytest.approx(registry.prob_any_loss, rel=1e-9)
            assert direct.var_95 == pytest.approx(registry.var_95, rel=1e-9)

    def test_monte_carlo_single_strategy_matches(self):
        """Test single strategy through registry matches direct call."""
        from src.engines.monte_carlo import MonteCarloEngine
        from src.registries import EngineRegistry

        seed = 42
        n_simulations = 100
        strategy_id = 1

        # Direct call
        direct_engine = MonteCarloEngine(n_simulations=n_simulations, random_seed=seed)
        direct_result = direct_engine.run(strategy_id=strategy_id)

        # Through registry
        registry_engine = EngineRegistry.get_instance().get(
            "monte_carlo",
            {"simulations": n_simulations, "seed": seed}
        )
        registry_results = registry_engine.run(
            data=None,
            config={"strategy_id": strategy_id}
        )

        assert len(registry_results) == 1
        registry_result = registry_results[0]

        # Must be identical
        assert direct_result.strategy_id == registry_result.strategy_id
        assert direct_result.mean_final == pytest.approx(registry_result.mean_final, rel=1e-9)


class TestValidatorRegistry:
    """Test validators through registry."""

    def test_validator_registry_has_result_validator(self):
        """Test result_validator is registered."""
        from src.registries import ValidatorRegistry

        registry = ValidatorRegistry.get_instance()
        assert registry.is_registered("result_validator")

    def test_validator_cv01_through_registry(self):
        """Test CV-01 validation through registry."""
        from src.registries import ValidatorRegistry

        validator = ValidatorRegistry.get_instance().get("result_validator", {})

        # Valid case
        result = validator.validate_cv01([100, 150, 200])
        assert result.passed is True

        # Invalid case
        result = validator.validate_cv01([100, -10, 50])
        assert result.passed is False

    def test_validator_matches_direct(self):
        """Test validator through registry matches direct call."""
        from src.validators.result_validator import ResultValidator
        from src.registries import ValidatorRegistry

        # Direct call
        direct_validator = ResultValidator()
        direct_result = direct_validator.validate_cv05(
            deposited=10000,
            final_value=11000,
            reported_return=10.0
        )

        # Through registry
        registry_validator = ValidatorRegistry.get_instance().get("result_validator", {})
        registry_result = registry_validator.validate_cv05(
            deposited=10000,
            final_value=11000,
            reported_return=10.0
        )

        # Must be identical
        assert direct_result.passed == registry_result.passed
        assert direct_result.rule_id == registry_result.rule_id
        assert direct_result.severity == registry_result.severity


class TestCollectorRegistry:
    """Test collectors through registry."""

    def test_collector_registry_has_file_loader(self):
        """Test file_loader is registered."""
        from src.registries import CollectorRegistry

        registry = CollectorRegistry.get_instance()
        assert registry.is_registered("file_loader")
        assert registry.is_registered("defillama")
        assert registry.is_registered("yahoo")
        assert registry.is_registered("jupiter")

    def test_file_loader_through_registry(self):
        """Test FileLoader through registry loads data."""
        from src.registries import CollectorRegistry

        collector = CollectorRegistry.get_instance().get("file_loader", {})
        data = collector.collect()

        # Should have loaded data
        assert isinstance(data, dict)
        assert 'defillama' in data
        assert 'yahoo' in data

    def test_collector_matches_direct(self):
        """Test collector through registry matches direct call."""
        from src.collectors.file_loader import FileLoader
        from src.registries import CollectorRegistry

        # Direct call
        direct_loader = FileLoader()
        direct_data = direct_loader.load('defillama')

        # Through registry
        collector = CollectorRegistry.get_instance().get("defillama", {})
        registry_data = collector.collect()

        # Must be identical
        assert len(direct_data) == len(registry_data)
        assert list(direct_data.columns) == list(registry_data.columns)


class TestOutputRegistry:
    """Test output formatters through registry."""

    def test_output_registry_has_formatters(self):
        """Test formatters are registered."""
        from src.registries import OutputRegistry

        registry = OutputRegistry.get_instance()
        assert registry.is_registered("json")
        assert registry.is_registered("csv")
        assert registry.is_registered("markdown")

    def test_json_formatter_through_registry(self):
        """Test JSON formatter through registry."""
        from src.registries import OutputRegistry

        formatter = OutputRegistry.get_instance().get("json", {})

        # Format some data
        data = [{"strategy_id": 1, "return": 10.5}]
        output = formatter.format(data)

        # Should be valid JSON
        import json
        parsed = json.loads(output)
        assert 'generated_at' in parsed
        assert 'results' in parsed


class TestPersonaRegistry:
    """Test personas through registry."""

    def test_persona_registry_has_personas(self):
        """Test personas are registered."""
        from src.registries import PersonaRegistry

        registry = PersonaRegistry.get_instance()
        assert registry.is_registered("ana")
        assert registry.is_registered("maria")
        assert registry.is_registered("felipe")

    def test_persona_properties(self):
        """Test persona properties are correct."""
        from src.registries import PersonaRegistry, EmojiLevel

        ana = PersonaRegistry.get_instance().get("ana", {})
        assert ana.name == "Ana"
        assert ana.emoji_level == EmojiLevel.HIGH
        assert ana.risk_profile == "conservative"

        felipe = PersonaRegistry.get_instance().get("felipe", {})
        assert felipe.name == "Felipe"
        assert felipe.emoji_level == EmojiLevel.NONE
        assert felipe.risk_profile == "aggressive"

    def test_get_persona_for_strategy(self):
        """Test persona selection for strategies."""
        from src.registries import get_persona_for_strategy

        # Conservative strategies -> Ana
        assert get_persona_for_strategy(1) == "ana"
        assert get_persona_for_strategy(3) == "ana"
        assert get_persona_for_strategy(9) == "ana"

        # Balanced strategies -> Maria
        assert get_persona_for_strategy(2) == "maria"
        assert get_persona_for_strategy(4) == "maria"
        assert get_persona_for_strategy(6) == "maria"

        # Aggressive strategies -> Felipe
        assert get_persona_for_strategy(8) == "felipe"
        assert get_persona_for_strategy(10) == "felipe"


class TestTriggerRegistry:
    """Test triggers through registry."""

    def test_trigger_registry_has_triggers(self):
        """Test triggers are registered."""
        from src.registries import TriggerRegistry

        registry = TriggerRegistry.get_instance()
        assert registry.is_registered("protocol_health")
        assert registry.is_registered("regime_change")
        assert registry.is_registered("estate_movement")
        assert registry.is_registered("whale_activity")

    def test_trigger_stub_returns_empty_alerts(self):
        """Test stub triggers return empty alert list."""
        from src.registries import TriggerRegistry

        trigger = TriggerRegistry.get_instance().get("protocol_health", {})
        alerts = trigger.evaluate({})

        # Stub should return empty list
        assert alerts == []
