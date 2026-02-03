"""
Engine Registry for analytics engines.

Wraps existing BattleTestEngine, MonteCarloEngine, MonitoringEngine,
and AnomalyEngine in a registry pattern for pluggable architecture.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import date
import logging

from src.registries.base import Registry

logger = logging.getLogger(__name__)


class AnalyticsEngine(ABC):
    """
    Abstract base class for all analytics engines.

    All engines must implement the run() method and declare their engine_type.
    """

    @abstractmethod
    def run(self, data: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run the analytics engine.

        Args:
            data: Input data (optional, some engines load their own)
            config: Runtime configuration

        Returns:
            Engine-specific results
        """
        pass

    @property
    @abstractmethod
    def engine_type(self) -> str:
        """
        Return the type of engine.

        Returns:
            One of: 'battle_test', 'monte_carlo', 'monitoring', 'anomaly'
        """
        pass

    def get_name(self) -> str:
        """Get the engine name for logging."""
        return self.__class__.__name__


class EngineRegistry(Registry[AnalyticsEngine]):
    """
    Registry for analytics engines.

    Usage:
        engine = EngineRegistry.get_instance().get("battle_test", config={})
        results = engine.run(data, {"scenario": "A"})
    """
    pass


# =============================================================================
# Wrapped Implementations
# =============================================================================

@EngineRegistry.register("battle_test")
class BattleTestEnginePlugin(AnalyticsEngine):
    """
    Wrapper for BattleTestEngine.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        from src.engines.battle_test import BattleTestEngine
        self.config = config
        self._engine = None  # Lazy initialization

    def _get_engine(self):
        """Lazy initialization of the underlying engine."""
        if self._engine is None:
            from src.engines.battle_test import BattleTestEngine
            self._engine = BattleTestEngine()
        return self._engine

    def run(self, data: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run Battle Test simulation.

        Args:
            data: Optional - engine loads its own data
            config: Runtime config with keys:
                - scenario: 'A', 'B', or 'C' (default: 'A')
                - strategy_id: Optional specific strategy ID
                - start_date: Optional start date
                - end_date: Optional end date

        Returns:
            list[BattleTestResult] or dict[str, list[BattleTestResult]]
        """
        config = config or {}
        engine = self._get_engine()

        scenario = config.get('scenario', 'A')
        strategy_id = config.get('strategy_id')
        start_date = config.get('start_date')
        end_date = config.get('end_date')

        # Parse dates if provided as strings
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)

        logger.info(f"Running Battle Test - scenario={scenario}, strategy={strategy_id}")

        if strategy_id is not None:
            # Run single strategy
            from src.engines.battle_test import SCENARIOS
            scenario_config = SCENARIOS[scenario]

            if scenario == 'C':
                minimums = scenario_config['minimums'][strategy_id]
                initial = minimums['initial']
                monthly = minimums['monthly']
            else:
                initial = scenario_config['initial_deposit']
                monthly = scenario_config['monthly_dca']

            result = engine.run(
                strategy_id=strategy_id,
                initial_deposit=initial,
                monthly_dca=monthly,
                start_date=start_date,
                end_date=end_date
            )
            return [result]
        else:
            # Run all strategies for scenario
            return engine.run_all_strategies(
                scenario=scenario,
                start_date=start_date,
                end_date=end_date
            )

    @property
    def engine_type(self) -> str:
        return 'battle_test'

    # Expose underlying engine methods for direct access if needed
    def run_single(self, strategy_id: int, initial_deposit: float, monthly_dca: float,
                   start_date: date = None, end_date: date = None):
        """Direct access to single strategy run."""
        return self._get_engine().run(
            strategy_id=strategy_id,
            initial_deposit=initial_deposit,
            monthly_dca=monthly_dca,
            start_date=start_date,
            end_date=end_date
        )

    def run_all_strategies(self, scenario: str = 'A', start_date: date = None, end_date: date = None):
        """Direct access to run all strategies."""
        return self._get_engine().run_all_strategies(
            scenario=scenario,
            start_date=start_date,
            end_date=end_date
        )

    def run_all_scenarios(self, start_date: date = None, end_date: date = None):
        """Direct access to run all scenarios."""
        return self._get_engine().run_all_scenarios(
            start_date=start_date,
            end_date=end_date
        )


@EngineRegistry.register("monte_carlo")
class MonteCarloEnginePlugin(AnalyticsEngine):
    """
    Wrapper for MonteCarloEngine.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._engine = None  # Lazy initialization
        self._engine_config = {
            'n_simulations': config.get('simulations', 5000),
            'horizon_months': config.get('horizon_months', 48),
            'random_seed': config.get('seed', 42)
        }

    def _get_engine(self):
        """Lazy initialization of the underlying engine."""
        if self._engine is None:
            from src.engines.monte_carlo import MonteCarloEngine
            self._engine = MonteCarloEngine(
                n_simulations=self._engine_config['n_simulations'],
                horizon_months=self._engine_config['horizon_months'],
                random_seed=self._engine_config['random_seed']
            )
        return self._engine

    def run(self, data: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run Monte Carlo simulation.

        Args:
            data: Optional - engine uses its own parameters
            config: Runtime config with keys:
                - strategy_id: Optional specific strategy ID
                - initial_deposit: Initial deposit (default: 10000)
                - monthly_dca: Monthly DCA (default: 200)

        Returns:
            list[MonteCarloResult]
        """
        config = config or {}
        engine = self._get_engine()

        strategy_id = config.get('strategy_id')
        initial_deposit = config.get('initial_deposit', 10000)
        monthly_dca = config.get('monthly_dca', 200)

        logger.info(f"Running Monte Carlo - strategy={strategy_id}, simulations={self._engine_config['n_simulations']}")

        if strategy_id is not None:
            result = engine.run(
                strategy_id=strategy_id,
                initial_deposit=initial_deposit,
                monthly_dca=monthly_dca
            )
            return [result]
        else:
            return engine.run_all_strategies(
                initial_deposit=initial_deposit,
                monthly_dca=monthly_dca
            )

    @property
    def engine_type(self) -> str:
        return 'monte_carlo'

    # Expose underlying engine methods for direct access
    def run_single(self, strategy_id: int, initial_deposit: float = 10000, monthly_dca: float = 200):
        """Direct access to single strategy simulation."""
        return self._get_engine().run(
            strategy_id=strategy_id,
            initial_deposit=initial_deposit,
            monthly_dca=monthly_dca
        )

    def run_all_strategies(self, initial_deposit: float = 10000, monthly_dca: float = 200):
        """Direct access to run all strategies."""
        return self._get_engine().run_all_strategies(
            initial_deposit=initial_deposit,
            monthly_dca=monthly_dca
        )


@EngineRegistry.register("monitoring")
class MonitoringEnginePlugin(AnalyticsEngine):
    """
    Wrapper for MonitoringEngine.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._engine = None

    def _get_engine(self):
        """Lazy initialization of the underlying engine."""
        if self._engine is None:
            from src.engines.monitoring import MonitoringEngine
            self._engine = MonitoringEngine()
        return self._engine

    def run(self, data: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run protocol health monitoring.

        Args:
            data: Dict with 'current' and 'previous' metrics per protocol
            config: Runtime config with keys:
                - protocol: Optional specific protocol to check

        Returns:
            list[ProtocolHealth]
        """
        config = config or {}
        data = data or {}
        engine = self._get_engine()

        protocol = config.get('protocol')
        logger.info(f"Running Monitoring - protocol={protocol}")

        results = []
        protocols_to_check = [protocol] if protocol else data.keys()

        for proto in protocols_to_check:
            if proto in data:
                proto_data = data[proto]
                result = engine.check_protocol(
                    protocol=proto,
                    current=proto_data.get('current', {}),
                    previous=proto_data.get('previous', {})
                )
                results.append(result)

        return results

    @property
    def engine_type(self) -> str:
        return 'monitoring'


@EngineRegistry.register("anomaly")
class AnomalyEnginePlugin(AnalyticsEngine):
    """
    Wrapper for anomaly detection engines.

    Preserves all existing functionality while making it registry-compatible.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._detectors = {}

    def _get_detector(self, model: str):
        """Get or create a detector by model name."""
        if model not in self._detectors:
            if model == 'zscore':
                from src.engines.anomaly import ZScoreDetector
                self._detectors[model] = ZScoreDetector(
                    window=self.config.get('window', 30),
                    threshold=self.config.get('threshold')
                )
            else:
                raise ValueError(f"Unknown anomaly model: {model}")
        return self._detectors[model]

    def run(self, data: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run anomaly detection.

        Args:
            data: Dict with time series data per protocol
            config: Runtime config with keys:
                - model: 'zscore', 'isolation', 'correlation' (default: 'zscore')
                - protocol: Optional specific protocol to analyze

        Returns:
            list[AnomalyResult]
        """
        import pandas as pd

        config = config or {}
        data = data or {}

        model = config.get('model', 'zscore')
        protocol = config.get('protocol')

        logger.info(f"Running Anomaly Detection - model={model}, protocol={protocol}")

        detector = self._get_detector(model)
        results = []

        protocols_to_check = [protocol] if protocol else data.keys()

        for proto in protocols_to_check:
            if proto in data:
                series = data[proto]
                if isinstance(series, dict):
                    series = pd.Series(series)
                proto_results = detector.detect(series, protocol=proto)
                results.extend(proto_results)

        return results

    @property
    def engine_type(self) -> str:
        return 'anomaly'
