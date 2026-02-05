"""
Abstract interfaces for crisis management.

DDD Principle 1: This module provides abstract interfaces that allow
the CrisisEscalationChecker to accept any implementation of the queue
and notifier, enabling dependency injection and easier testing.

Usage:
    # Using interfaces instead of concrete implementations
    from src.crisis.interfaces import ApprovalQueueInterface, NotifierInterface

    class CrisisEscalationChecker:
        def __init__(
            self,
            queue: ApprovalQueueInterface,
            notifier: NotifierInterface,
        ):
            ...
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol


@dataclass
class ApprovalRequestInterface:
    """
    Interface for an approval request.

    Defines the expected structure for approval requests that the
    escalation checker needs to work with.
    """
    request_id: str
    content_preview: str
    crisis_level: int
    queue: str
    approvers: List[str]
    sla_minutes: int
    created_at: str
    expires_at: str
    status: str = "pending"
    approved_by: Optional[str] = None
    rejected_by: Optional[str] = None
    rejection_reason: Optional[str] = None
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'request_id': self.request_id,
            'content_preview': self.content_preview,
            'crisis_level': self.crisis_level,
            'queue': self.queue,
            'approvers': self.approvers,
            'sla_minutes': self.sla_minutes,
            'created_at': self.created_at,
            'expires_at': self.expires_at,
            'status': self.status,
            'approved_by': self.approved_by,
            'rejected_by': self.rejected_by,
            'rejection_reason': self.rejection_reason,
            'metadata': self.metadata or {},
        }


class ApprovalQueueInterface(Protocol):
    """
    Protocol for approval queue implementations.

    Any class with these methods can be used as an approval queue,
    enabling easy substitution of implementations (file-based, database, etc.)
    """

    def submit(
        self,
        content: str,
        crisis_level: int,
        queue: str,
        approvers: List[str],
        sla_minutes: int,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Submit a new request to the queue. Returns request ID."""
        ...

    def approve(self, request_id: str, approved_by: str) -> bool:
        """Approve a request. Returns True if successful."""
        ...

    def reject(self, request_id: str, rejected_by: str, reason: str = "") -> bool:
        """Reject a request. Returns True if successful."""
        ...

    def get(self, request_id: str) -> Optional[ApprovalRequestInterface]:
        """Get a request by ID. Returns None if not found."""
        ...

    def get_pending(self, queue: Optional[str] = None) -> List[ApprovalRequestInterface]:
        """Get all pending requests, optionally filtered by queue."""
        ...

    def get_expired(self) -> List[ApprovalRequestInterface]:
        """Get all expired pending requests."""
        ...


class NotifierInterface(Protocol):
    """
    Protocol for notification backends.

    Service-agnostic interface allows swapping implementations
    (e.g., Slack webhook, email, PagerDuty) without code changes.
    """

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

        Returns True if sent successfully.
        """
        ...

    def notify_sla_breach(
        self,
        request_id: str,
        crisis_level: int,
        elapsed_minutes: int,
        sla_minutes: int,
    ) -> bool:
        """
        Send notification that SLA has been breached.

        Returns True if sent successfully.
        """
        ...


class NullNotifier:
    """
    Null implementation of NotifierInterface.

    Useful for testing or when notifications are disabled.
    """

    def notify_approval_required(
        self,
        crisis_level: int,
        request_id: str,
        approvers: List[str],
        sla_minutes: int,
        preview: str,
    ) -> bool:
        """No-op notification."""
        return True

    def notify_sla_breach(
        self,
        request_id: str,
        crisis_level: int,
        elapsed_minutes: int,
        sla_minutes: int,
    ) -> bool:
        """No-op notification."""
        return True
