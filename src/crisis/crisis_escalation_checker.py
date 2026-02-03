"""
Crisis escalation checker.

Monitors SLA compliance and triggers escalations when needed.
"""

import logging
from datetime import datetime
from typing import List, Optional

from src.crisis.crisis_approval_queue import (
    CrisisApprovalRequest,
    CrisisFileBasedApprovalQueue,
)
from src.crisis.crisis_slack_notifier import CrisisSlackNotifier

logger = logging.getLogger(__name__)


class CrisisEscalationChecker:
    """
    Check for SLA breaches and escalate as needed.

    Should be run periodically (e.g., every 5 minutes via cron).
    """

    def __init__(
        self,
        queue: Optional[CrisisFileBasedApprovalQueue] = None,
        notifier: Optional[CrisisSlackNotifier] = None,
    ):
        """
        Initialize checker with dependencies.

        Args:
            queue: Approval queue to check
            notifier: Notifier for escalations
        """
        self.queue = queue or CrisisFileBasedApprovalQueue()
        self.notifier = notifier or CrisisSlackNotifier()

    def check_all(self) -> List[CrisisApprovalRequest]:
        """
        Check all pending requests for SLA breaches.

        Returns:
            List of breached requests
        """
        breached: List[CrisisApprovalRequest] = []
        now = datetime.utcnow()

        for request in self.queue.get_pending():
            elapsed = self._get_elapsed_minutes(request, now)
            if elapsed > request.sla_minutes:
                breached.append(request)
                self._handle_breach(request, elapsed)

        if breached:
            logger.warning(f"Found {len(breached)} SLA breaches")

        return breached

    def _get_elapsed_minutes(
        self, request: CrisisApprovalRequest, now: datetime
    ) -> int:
        """Calculate elapsed minutes since request creation."""
        try:
            created_at = datetime.fromisoformat(request.created_at)
            elapsed = now - created_at
            return int(elapsed.total_seconds() / 60)
        except (ValueError, TypeError):
            return 0

    def _handle_breach(
        self, request: CrisisApprovalRequest, elapsed_minutes: int
    ) -> None:
        """Handle an SLA breach."""
        logger.warning(
            f"SLA breach: {request.request_id} "
            f"(L{request.crisis_level}, {elapsed_minutes}m elapsed, "
            f"{request.sla_minutes}m SLA)"
        )

        # Send notification
        if self.notifier:
            try:
                self.notifier.notify_sla_breach(
                    request_id=request.request_id,
                    crisis_level=request.crisis_level,
                    elapsed_minutes=elapsed_minutes,
                    sla_minutes=request.sla_minutes,
                )
            except Exception as e:
                logger.error(f"Failed to notify SLA breach: {e}")

    def get_status_report(self) -> dict:
        """
        Get status report of all pending requests.

        Returns:
            Dict with queue status information
        """
        now = datetime.utcnow()
        pending = self.queue.get_pending()

        by_level = {}
        breached_count = 0
        near_breach_count = 0

        for request in pending:
            # Count by level
            level = request.crisis_level
            by_level[level] = by_level.get(level, 0) + 1

            # Check for breaches
            elapsed = self._get_elapsed_minutes(request, now)
            if elapsed > request.sla_minutes:
                breached_count += 1
            elif elapsed > request.sla_minutes * 0.8:
                near_breach_count += 1

        return {
            "total_pending": len(pending),
            "by_level": by_level,
            "breached": breached_count,
            "near_breach": near_breach_count,
            "checked_at": now.isoformat(),
        }
