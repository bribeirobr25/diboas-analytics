"""Tests for crisis level classifier."""

import pytest
from src.crisis.crisis_level_classifier import CrisisLevelClassifier, CrisisLevel


class TestCrisisLevelClassifier:
    """Tests for CrisisLevelClassifier."""

    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return CrisisLevelClassifier()

    def test_should_classify_normal_content_as_level_0(self, classifier):
        """Normal content is classified as level 0."""
        result = classifier.classify("The market is performing well today.")
        assert result.level == CrisisLevel.LEVEL_0_NORMAL
        assert result.requires_human_approval is False
        assert len(result.approvers) == 0

    def test_should_classify_caution_keywords_as_level_2(self, classifier):
        """Caution keywords are classified as level 2."""
        result = classifier.classify("There is increased volatility in the market.")
        assert result.level == CrisisLevel.LEVEL_2_CAUTION
        assert result.requires_human_approval is False

    def test_should_classify_warning_keywords_as_level_3(self, classifier):
        """Warning keywords are classified as level 3."""
        result = classifier.classify("We have a security concern regarding the protocol.")
        assert result.level == CrisisLevel.LEVEL_3_WARNING
        assert result.requires_human_approval is True
        assert "clo_board" in result.approvers
        assert "ceo" in result.approvers
        assert result.sla_minutes == 60

    def test_should_classify_alert_keywords_as_level_4(self, classifier):
        """Alert keywords are classified as level 4."""
        result = classifier.classify("There is a potential loss situation developing.")
        assert result.level == CrisisLevel.LEVEL_4_ALERT
        assert result.requires_human_approval is True
        assert "external_counsel" in result.approvers
        assert result.sla_minutes == 75

    def test_should_classify_critical_keywords_as_level_5(self, classifier):
        """Critical keywords are classified as level 5."""
        result = classifier.classify("Hack confirmed. Funds have been lost.")
        assert result.level == CrisisLevel.LEVEL_5_CRITICAL
        assert result.requires_human_approval is True
        assert "board" in result.approvers
        assert result.sla_minutes == 90

    def test_should_use_highest_level_when_multiple_keywords(self, classifier):
        """Uses highest level when multiple keywords present."""
        result = classifier.classify("There is volatility and funds at risk.")
        # "volatility" is L2, "funds at risk" is L4
        assert result.level == CrisisLevel.LEVEL_4_ALERT

    def test_should_consider_p0_trigger_priority(self, classifier):
        """P0 trigger priority elevates to level 4."""
        result = classifier.classify("Market update.", trigger_priority="P0")
        assert result.level >= CrisisLevel.LEVEL_4_ALERT
        assert "P0" in str(result.reasons)

    def test_should_consider_p1_trigger_priority(self, classifier):
        """P1 trigger priority elevates to level 3."""
        result = classifier.classify("Market update.", trigger_priority="P1")
        assert result.level >= CrisisLevel.LEVEL_3_WARNING
        assert "P1" in str(result.reasons)

    def test_should_consider_btc_crash_in_market_data(self, classifier):
        """BTC crash elevates crisis level."""
        result = classifier.classify(
            "Market update.",
            market_data={"btc_change_24h_pct": -25}
        )
        assert result.level >= CrisisLevel.LEVEL_4_ALERT
        assert "BTC" in str(result.reasons)

    def test_should_consider_vix_spike_in_market_data(self, classifier):
        """High VIX elevates crisis level."""
        result = classifier.classify(
            "Market update.",
            market_data={"vix": 45}
        )
        assert result.level >= CrisisLevel.LEVEL_3_WARNING
        assert "VIX" in str(result.reasons)

    def test_should_be_case_insensitive(self, classifier):
        """Keyword detection is case insensitive."""
        result1 = classifier.classify("HACK CONFIRMED")
        result2 = classifier.classify("hack confirmed")
        assert result1.level == result2.level == CrisisLevel.LEVEL_5_CRITICAL

    def test_should_convert_to_dict(self, classifier):
        """Result can be converted to dict."""
        result = classifier.classify("There is a security concern.")
        result_dict = result.to_dict()

        assert "level" in result_dict
        assert "level_name" in result_dict
        assert "reasons" in result_dict
        assert "requires_human_approval" in result_dict
        assert "approvers" in result_dict
        assert "sla_minutes" in result_dict
