"""
File-based approval queue.

$0 budget constraint - uses JSON files instead of database.
Can be replaced with PostgreSQL/Redis in Phase 2+.
"""

import json
import logging
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class CrisisApprovalRequest:
    """
    An approval request in the queue.

    Contains all context needed for reviewers.
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
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class CrisisFileBasedApprovalQueue:
    """
    File-based approval queue.

    Each request is stored as a JSON file.
    Replace with database in Phase 2+.
    """

    def __init__(self, queue_dir: str = "data/crisis_approval_queue"):
        """
        Initialize queue with storage directory.

        Args:
            queue_dir: Directory to store queue files
        """
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def submit(
        self,
        content: str,
        crisis_level: int,
        queue: str,
        approvers: List[str],
        sla_minutes: int,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Submit a new request to the queue.

        Args:
            content: Content to review
            crisis_level: Crisis level (0-5)
            queue: Queue name
            approvers: List of required approvers
            sla_minutes: SLA in minutes
            metadata: Optional metadata

        Returns:
            Request ID
        """
        request_id = str(uuid.uuid4())[:8]
        now = datetime.utcnow()

        request = CrisisApprovalRequest(
            request_id=request_id,
            content_preview=content[:500],
            crisis_level=crisis_level,
            queue=queue,
            approvers=approvers,
            sla_minutes=sla_minutes,
            created_at=now.isoformat(),
            expires_at=(now + timedelta(minutes=sla_minutes)).isoformat(),
            metadata=metadata or {},
        )

        file_path = self.queue_dir / f"{request_id}.json"
        with open(file_path, "w") as f:
            json.dump(request.to_dict(), f, indent=2)

        logger.info(f"Created approval request: {request_id}")
        return request_id

    def approve(self, request_id: str, approved_by: str) -> bool:
        """
        Approve a request.

        Args:
            request_id: Request ID to approve
            approved_by: Approver identifier

        Returns:
            True if approved, False if not found
        """
        file_path = self.queue_dir / f"{request_id}.json"
        if not file_path.exists():
            logger.warning(f"Request not found: {request_id}")
            return False

        with open(file_path) as f:
            data = json.load(f)

        data["status"] = "approved"
        data["approved_by"] = approved_by

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Approved request: {request_id} by {approved_by}")
        return True

    def reject(
        self, request_id: str, rejected_by: str, reason: str = ""
    ) -> bool:
        """
        Reject a request.

        Args:
            request_id: Request ID to reject
            rejected_by: Rejector identifier
            reason: Rejection reason

        Returns:
            True if rejected, False if not found
        """
        file_path = self.queue_dir / f"{request_id}.json"
        if not file_path.exists():
            logger.warning(f"Request not found: {request_id}")
            return False

        with open(file_path) as f:
            data = json.load(f)

        data["status"] = "rejected"
        data["rejected_by"] = rejected_by
        data["rejection_reason"] = reason

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Rejected request: {request_id} by {rejected_by}")
        return True

    def get(self, request_id: str) -> Optional[CrisisApprovalRequest]:
        """
        Get a request by ID.

        Args:
            request_id: Request ID

        Returns:
            CrisisApprovalRequest or None if not found
        """
        file_path = self.queue_dir / f"{request_id}.json"
        if not file_path.exists():
            return None

        with open(file_path) as f:
            data = json.load(f)

        return CrisisApprovalRequest(**data)

    def get_pending(self, queue: Optional[str] = None) -> List[CrisisApprovalRequest]:
        """
        Get all pending requests.

        Args:
            queue: Optional queue filter

        Returns:
            List of pending requests
        """
        requests: List[CrisisApprovalRequest] = []

        for file_path in self.queue_dir.glob("*.json"):
            try:
                with open(file_path) as f:
                    data = json.load(f)

                if data.get("status") == "pending":
                    if queue is None or data.get("queue") == queue:
                        requests.append(CrisisApprovalRequest(**data))
            except (json.JSONDecodeError, TypeError) as e:
                logger.warning(f"Invalid queue file {file_path}: {e}")

        # Sort by created_at (oldest first)
        requests.sort(key=lambda r: r.created_at)
        return requests

    def get_expired(self) -> List[CrisisApprovalRequest]:
        """
        Get all expired pending requests.

        Returns:
            List of expired requests
        """
        now = datetime.utcnow()
        expired: List[CrisisApprovalRequest] = []

        for request in self.get_pending():
            try:
                expires_at = datetime.fromisoformat(request.expires_at)
                if now > expires_at:
                    expired.append(request)
            except (ValueError, TypeError):
                pass

        return expired
