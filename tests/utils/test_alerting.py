"""Tests for alerting utilities."""

import pytest
import os
from unittest.mock import patch, MagicMock

from src.utils.alerting import (
    send_alert,
    AlertSeverity,
    alert_crisis_detected,
    alert_circuit_opened,
    alert_validation_failure,
    alert_execution_failed,
)


class TestSendAlert:
    """Tests for send_alert function."""

    def test_logs_when_no_webhook(self):
        """Falls back to logging when no webhook configured."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("src.utils.alerting.logger") as mock_logger:
                result = send_alert("Test message", AlertSeverity.INFO)

                assert result is True
                mock_logger.log.assert_called_once()

    def test_disabled_when_env_var_false(self):
        """Does not send when ALERT_ENABLED=false."""
        with patch.dict(os.environ, {"ALERT_ENABLED": "false"}):
            result = send_alert("Test message", AlertSeverity.INFO)

            assert result is False

    def test_accepts_string_severity(self):
        """Accepts string severity."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("src.utils.alerting.logger"):
                result = send_alert("Test", severity="warning")
                assert result is True

    def test_accepts_enum_severity(self):
        """Accepts enum severity."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("src.utils.alerting.logger"):
                result = send_alert("Test", severity=AlertSeverity.ERROR)
                assert result is True

    def test_includes_context(self):
        """Context is included in message."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("src.utils.alerting.logger") as mock_logger:
                send_alert(
                    "Test message",
                    AlertSeverity.INFO,
                    context={"key": "value"},
                )

                call_args = mock_logger.log.call_args[0][1]
                assert "key" in call_args
                assert "value" in call_args


class TestAlertConvenienceFunctions:
    """Tests for convenience alert functions."""

    def test_alert_crisis_detected(self):
        """alert_crisis_detected sends critical alert for level 4+."""
        with patch("src.utils.alerting.send_alert") as mock_send:
            mock_send.return_value = True

            result = alert_crisis_detected(
                crisis_level=4,
                trigger_id="TEST-001",
                message="Test crisis",
                affected_strategies=[1, 3, 5],
            )

            assert result is True
            mock_send.assert_called_once()
            call_args = mock_send.call_args
            assert call_args[1]["severity"] == AlertSeverity.CRITICAL

    def test_alert_circuit_opened(self):
        """alert_circuit_opened includes circuit name."""
        with patch("src.utils.alerting.send_alert") as mock_send:
            mock_send.return_value = True

            result = alert_circuit_opened(
                circuit_name="api_client",
                failure_count=5,
                last_error="Connection refused",
            )

            assert result is True
            call_args = mock_send.call_args
            assert "api_client" in call_args[0][0]

    def test_alert_validation_failure(self):
        """alert_validation_failure sends warning."""
        with patch("src.utils.alerting.send_alert") as mock_send:
            mock_send.return_value = True

            result = alert_validation_failure(
                gate="Gate4",
                error_count=3,
                issues=["Issue 1", "Issue 2"],
            )

            assert result is True
            call_args = mock_send.call_args
            assert call_args[1]["severity"] == AlertSeverity.WARNING

    def test_alert_execution_failed(self):
        """alert_execution_failed includes command and error."""
        with patch("src.utils.alerting.send_alert") as mock_send:
            mock_send.return_value = True

            result = alert_execution_failed(
                command="battle-test",
                error="Data not found",
                correlation_id="test-123",
            )

            assert result is True
            call_args = mock_send.call_args
            assert call_args[1]["severity"] == AlertSeverity.ERROR


class TestSlackIntegration:
    """Tests for Slack webhook integration."""

    def test_sends_to_slack_when_configured(self):
        """Sends to Slack when webhook URL is set."""
        with patch.dict(os.environ, {"SLACK_WEBHOOK_URL": "https://hooks.slack.com/test"}):
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_response = MagicMock()
                mock_response.status = 200
                mock_response.__enter__ = MagicMock(return_value=mock_response)
                mock_response.__exit__ = MagicMock(return_value=False)
                mock_urlopen.return_value = mock_response

                result = send_alert("Test", AlertSeverity.INFO)

                assert result is True
                mock_urlopen.assert_called_once()

    def test_handles_slack_failure(self):
        """Handles Slack webhook failure gracefully."""
        with patch.dict(os.environ, {"SLACK_WEBHOOK_URL": "https://hooks.slack.com/test"}):
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_urlopen.side_effect = Exception("Network error")

                result = send_alert("Test", AlertSeverity.INFO)

                assert result is False
