"""
Crisis router.

Routes content to appropriate queues based on crisis level.
Coordinates with approval queue and notifications.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.crisis.crisis_level_classifier import CrisisLevel, CrisisClassification

logger = logging.getLogger(__name__)


@dataclass
class CrisisRoutingDecision:
    """
    Decision from crisis routing.

    Contains action to take and queue assignment.
    """
    action: str  # "auto_approve", "queue", "block"
    queue: Optional[str]
    request_id: Optional[str]
    approvers: list
    sla_minutes: Optional[int]
    notification_sent: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "action": self.action,
            "queue": self.queue,
            "request_id": self.request_id,
            "approvers": self.approvers,
            "sla_minutes": self.sla_minutes,
            "notification_sent": self.notification_sent,
        }


class CrisisRouter:
    """
    Route content based on crisis classification.

    Routing logic:
    - Level 0-2: Auto-approve, no queue
    - Level 3+: Queue for human approval, send notifications
    """

    def __init__(
        self,
        approval_queue=None,
        notifier=None,
    ):
        """
        Initialize router with optional dependencies.

        Args:
            approval_queue: Approval queue instance
            notifier: Notification service instance
        """
        self.approval_queue = approval_queue
        self.notifier = notifier

    def route(
        self,
        content: str,
        classification: CrisisClassification,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CrisisRoutingDecision:
        """
        Route content based on classification.

        Args:
            content: Content to route
            classification: Crisis classification result
            metadata: Optional metadata

        Returns:
            CrisisRoutingDecision with action and queue
        """
        # Auto-approve for levels 0-2
        if classification.level < CrisisLevel.LEVEL_3_WARNING:
            return CrisisRoutingDecision(
                action="auto_approve",
                queue=None,
                request_id=None,
                approvers=[],
                sla_minutes=None,
                notification_sent=False,
            )

        # Levels 3+ require human approval
        request_id = None
        notification_sent = False

        # Submit to queue if available
        if self.approval_queue:
            try:
                request_id = self.approval_queue.submit(
                    content=content,
                    crisis_level=classification.level,
                    queue=self._get_queue_name(classification.level),
                    approvers=classification.approvers,
                    sla_minutes=classification.sla_minutes or 60,
                    metadata=metadata,
                )
                logger.info(f"Submitted to approval queue: {request_id}")
            except Exception as e:
                logger.error(f"Failed to submit to queue: {e}")

        # Send notification if available
        if self.notifier:
            try:
                notification_sent = self.notifier.notify_approval_required(
                    crisis_level=classification.level,
                    request_id=request_id or "unknown",
                    approvers=classification.approvers,
                    sla_minutes=classification.sla_minutes or 60,
                    preview=content[:500],
                )
                logger.info(f"Notification sent: {notification_sent}")
            except Exception as e:
                logger.error(f"Failed to send notification: {e}")

        return CrisisRoutingDecision(
            action="queue",
            queue=self._get_queue_name(classification.level),
            request_id=request_id,
            approvers=classification.approvers,
            sla_minutes=classification.sla_minutes,
            notification_sent=notification_sent,
        )

    def _get_queue_name(self, level: CrisisLevel) -> str:
        """Get queue name for crisis level."""
        queue_map = {
            CrisisLevel.LEVEL_3_WARNING: "crisis_warning_review",
            CrisisLevel.LEVEL_4_ALERT: "crisis_alert_review",
            CrisisLevel.LEVEL_5_CRITICAL: "crisis_critical_review",
        }
        return queue_map.get(level, "crisis_review")
