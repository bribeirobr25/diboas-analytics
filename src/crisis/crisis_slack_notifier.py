"""
Slack webhook notifier.

Sends notifications via Slack webhooks ($0 cost).
Uses free incoming webhook feature.
"""

import json
import logging
import os
from typing import List, Optional
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)


class CrisisSlackNotifier:
    """
    Send crisis notifications via Slack webhook.

    Uses free Slack incoming webhooks.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize notifier with webhook URL.

        Args:
            webhook_url: Slack webhook URL (or use SLACK_ANALYTICS_WEBHOOK env var)
        """
        self.webhook_url = webhook_url or os.getenv("SLACK_ANALYTICS_WEBHOOK")

    def notify_approval_required(
        self,
        crisis_level: int,
        request_id: str,
        approvers: List[str],
        sla_minutes: int,
        preview: str,
    ) -> bool:
        """
        Send notification that approval is required.

        Args:
            crisis_level: Crisis level (0-5)
            request_id: Approval request ID
            approvers: Required approvers
            sla_minutes: SLA in minutes
            preview: Content preview

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.webhook_url:
            logger.warning("Slack webhook not configured")
            return False

        emoji = self._get_emoji(crisis_level)
        color = self._get_color(crisis_level)

        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Crisis L{crisis_level} - Approval Required",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Request ID:*\n{request_id}"},
                        {"type": "mrkdwn", "text": f"*SLA:*\n{sla_minutes} minutes"},
                        {
                            "type": "mrkdwn",
                            "text": f"*Approvers:*\n{', '.join(approvers)}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Level:*\n{self._get_level_name(crisis_level)}",
                        },
                    ],
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Preview:*\n```{preview[:200]}...```",
                    },
                },
            ],
            "attachments": [
                {
                    "color": color,
                    "text": f"Respond within {sla_minutes} minutes",
                }
            ],
        }

        return self._send_webhook(message)

    def notify_sla_breach(
        self,
        request_id: str,
        crisis_level: int,
        elapsed_minutes: int,
        sla_minutes: int,
    ) -> bool:
        """
        Send notification that SLA has been breached.

        Args:
            request_id: Approval request ID
            crisis_level: Crisis level
            elapsed_minutes: Time elapsed since request
            sla_minutes: Original SLA

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.webhook_url:
            logger.warning("Slack webhook not configured")
            return False

        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🚨 SLA BREACH - Request {request_id}",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*Crisis Level:* {crisis_level}\n"
                            f"*SLA:* {sla_minutes} minutes\n"
                            f"*Elapsed:* {elapsed_minutes} minutes\n"
                            f"*Overdue by:* {elapsed_minutes - sla_minutes} minutes"
                        ),
                    },
                },
            ],
            "attachments": [
                {
                    "color": "danger",
                    "text": "IMMEDIATE ACTION REQUIRED",
                }
            ],
        }

        return self._send_webhook(message)

    def _send_webhook(self, message: dict) -> bool:
        """Send message to Slack webhook."""
        try:
            data = json.dumps(message).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json"},
            )

            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200

        except urllib.error.URLError as e:
            logger.error(f"Slack webhook error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending to Slack: {e}")
            return False

    def _get_emoji(self, level: int) -> str:
        """Get emoji for crisis level."""
        emoji_map = {
            0: "ℹ️",
            1: "👀",
            2: "⚠️",
            3: "⚠️",
            4: "🚨",
            5: "🆘",
        }
        return emoji_map.get(level, "ℹ️")

    def _get_color(self, level: int) -> str:
        """Get color for crisis level."""
        color_map = {
            0: "good",
            1: "good",
            2: "warning",
            3: "warning",
            4: "danger",
            5: "danger",
        }
        return color_map.get(level, "good")

    def _get_level_name(self, level: int) -> str:
        """Get name for crisis level."""
        name_map = {
            0: "Normal",
            1: "Watch",
            2: "Caution",
            3: "Warning",
            4: "Alert",
            5: "Critical",
        }
        return name_map.get(level, "Unknown")
