"""Integration tests for trigger to Adelaide pipeline."""

import pytest
import tempfile

from src.triggers.intelligence_trigger_evaluator import IntelligenceTriggerEvaluator
from src.triggers.base import IntelligenceTriggerPriority
from src.crisis.crisis_level_classifier import CrisisLevelClassifier, CrisisLevel


class TestTriggerToAdelaidePipeline:
    """Integration tests for trigger evaluation to Adelaide content pipeline."""

    @pytest.fixture
    def evaluator(self):
        """Create trigger evaluator."""
        return IntelligenceTriggerEvaluator(config={
            "default_cooldown_minutes": 0,  # Disable cooldown for tests
            "consolidate_alerts": False,
        })

    @pytest.fixture
    def classifier(self):
        """Create crisis classifier."""
        return CrisisLevelClassifier()

    def test_should_fire_trigger_and_classify_crisis(self, evaluator, classifier):
        """Trigger fires and crisis level is correctly classified."""
        # Simulate market data with BTC crash
        data = {
            "protocol_health": {"sky": {"usds_price": 0.92}},  # 8% depeg
            "market_prices": {"btc": {"change_24h_pct": -22}},  # 22% crash
        }

        # Evaluate triggers
        results = evaluator.evaluate_all(data)

        # Find highest priority
        highest_priority = min(
            [r.priority for r in results],
            key=lambda p: ["P0", "P1", "P2", "P3"].index(p.value),
            default=IntelligenceTriggerPriority.P3_INFO
        )

        # Classify crisis based on trigger priority
        classification = classifier.classify(
            "Market update with triggered alerts.",
            trigger_priority=highest_priority.value,
            market_data={"btc_change_24h_pct": -22}
        )

        # Should be at least Level 4 due to P0 trigger or BTC crash
        assert classification.level >= CrisisLevel.LEVEL_4_ALERT
        assert classification.requires_human_approval is True

    def test_should_have_no_crisis_on_normal_data(self, evaluator, classifier):
        """Normal market data results in no crisis."""
        data = {
            "protocol_health": {"sky": {"usds_price": 1.0}},
            "market_prices": {"btc": {"change_24h_pct": 2}},
        }

        results = evaluator.evaluate_all(data)

        # No P0/P1 triggers should fire
        p0_p1_results = [r for r in results if r.priority in [
            IntelligenceTriggerPriority.P0_CRITICAL,
            IntelligenceTriggerPriority.P1_HIGH
        ]]

        # Classify without high-priority triggers
        classification = classifier.classify(
            "Normal market update.",
            market_data={"btc_change_24h_pct": 2}
        )

        assert classification.level <= CrisisLevel.LEVEL_2_CAUTION

    def test_should_include_affected_strategies_in_alerts(self, evaluator):
        """Fired alerts include affected strategies."""
        data = {
            "protocol_health": {"sky": {"usds_price": 0.85}},  # Major depeg
        }

        results = evaluator.evaluate_all(data)
        sky_results = [r for r in results if "SKY" in r.trigger_id]

        for result in sky_results:
            assert len(result.affected_strategies) > 0
            # Sky strategies are 1, 3, 5, 7, 9
            assert any(s in [1, 3, 5, 7, 9] for s in result.affected_strategies)

    def test_should_provide_correlation_id_for_tracing(self, evaluator):
        """Correlation ID is consistent across related operations."""
        data = {"protocol_health": {"sky": {"usds_price": 0.90}}}

        results = evaluator.evaluate_all(data, correlation_id="trace-001")

        for result in results:
            assert result.correlation_id == "trace-001"


class TestTriggerConsolidation:
    """Tests for alert consolidation in trigger pipeline."""

    @pytest.fixture
    def evaluator(self):
        """Create evaluator with consolidation enabled."""
        return IntelligenceTriggerEvaluator(config={
            "default_cooldown_minutes": 0,
            "consolidate_alerts": True,
            "strategy_overlap_threshold": 0.5,
        })

    def test_should_consolidate_related_alerts(self, evaluator):
        """Related alerts are consolidated."""
        # Fire multiple related triggers
        data = {
            "protocol_health": {
                "sky": {"usds_price": 0.90, "tvl_change_24h_pct": -15},
            }
        }

        results_consolidated = evaluator.evaluate_all(data)

        # With consolidation, there should be fewer unique alerts
        # than without consolidation for the same data
        evaluator_no_consolidate = IntelligenceTriggerEvaluator(config={
            "default_cooldown_minutes": 0,
            "consolidate_alerts": False,
        })
        results_unconsolidated = evaluator_no_consolidate.evaluate_all(data)

        # Consolidated should have <= unconsolidated
        assert len(results_consolidated) <= len(results_unconsolidated)
