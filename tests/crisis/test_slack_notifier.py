"""Tests for crisis Slack notifier."""

import pytest
from unittest.mock import patch, MagicMock

from src.crisis.crisis_slack_notifier import CrisisSlackNotifier


class TestCrisisSlackNotifier:
    """Tests for CrisisSlackNotifier."""

    @pytest.fixture
    def notifier(self):
        """Create notifier with test webhook."""
        return CrisisSlackNotifier(webhook_url="https://hooks.slack.com/test")

    def test_should_return_false_when_no_webhook(self):
        """Returns False when no webhook configured."""
        notifier = CrisisSlackNotifier(webhook_url=None)
        result = notifier.notify_approval_required(
            crisis_level=3,
            request_id="test-123",
            approvers=["clo_board"],
            sla_minutes=60,
            preview="Test content"
        )
        assert result is False

    @patch("urllib.request.urlopen")
    def test_should_send_approval_notification(self, mock_urlopen, notifier):
        """Sends approval required notification."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = notifier.notify_approval_required(
            crisis_level=3,
            request_id="test-123",
            approvers=["clo_board", "ceo"],
            sla_minutes=60,
            preview="Test crisis content"
        )
        assert result is True
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_should_send_sla_breach_notification(self, mock_urlopen, notifier):
        """Sends SLA breach notification."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = notifier.notify_sla_breach(
            request_id="test-123",
            crisis_level=4,
            elapsed_minutes=90,
            sla_minutes=75
        )
        assert result is True
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_should_return_false_on_network_error(self, mock_urlopen, notifier):
        """Returns False on network error."""
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

        result = notifier.notify_approval_required(
            crisis_level=3,
            request_id="test-123",
            approvers=["clo_board"],
            sla_minutes=60,
            preview="Test content"
        )
        assert result is False

    def test_should_get_correct_emoji_for_levels(self, notifier):
        """Returns correct emoji for each level."""
        assert notifier._get_emoji(0) == "ℹ️"
        assert notifier._get_emoji(3) == "⚠️"
        assert notifier._get_emoji(4) == "🚨"
        assert notifier._get_emoji(5) == "🆘"

    def test_should_get_correct_color_for_levels(self, notifier):
        """Returns correct color for each level."""
        assert notifier._get_color(0) == "good"
        assert notifier._get_color(2) == "warning"
        assert notifier._get_color(4) == "danger"

    def test_should_get_correct_level_name(self, notifier):
        """Returns correct level name."""
        assert notifier._get_level_name(0) == "Normal"
        assert notifier._get_level_name(3) == "Warning"
        assert notifier._get_level_name(5) == "Critical"

    def test_should_use_env_var_when_no_url_provided(self):
        """Uses environment variable when no URL provided."""
        with patch.dict("os.environ", {"SLACK_ANALYTICS_WEBHOOK": "https://hooks.slack.com/env-test"}):
            notifier = CrisisSlackNotifier()
            assert notifier.webhook_url == "https://hooks.slack.com/env-test"
