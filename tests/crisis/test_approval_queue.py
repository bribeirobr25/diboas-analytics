"""Tests for crisis approval queue."""

import pytest
import tempfile
from pathlib import Path

from src.crisis.crisis_approval_queue import (
    CrisisFileBasedApprovalQueue,
    CrisisApprovalRequest,
)


class TestCrisisApprovalQueue:
    """Tests for CrisisFileBasedApprovalQueue."""

    @pytest.fixture
    def temp_queue_dir(self):
        """Create temporary queue directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def queue(self, temp_queue_dir):
        """Create queue with temp directory."""
        return CrisisFileBasedApprovalQueue(queue_dir=temp_queue_dir)

    def test_should_submit_request(self, queue):
        """Can submit a new request."""
        request_id = queue.submit(
            content="Test crisis content",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board", "ceo"],
            sla_minutes=60
        )
        assert request_id is not None
        assert len(request_id) == 8

    def test_should_get_submitted_request(self, queue):
        """Can get a submitted request."""
        request_id = queue.submit(
            content="Test crisis content",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board", "ceo"],
            sla_minutes=60
        )

        request = queue.get(request_id)
        assert request is not None
        assert request.request_id == request_id
        assert request.crisis_level == 3
        assert request.status == "pending"

    def test_should_return_none_for_nonexistent_request(self, queue):
        """Returns None for nonexistent request."""
        request = queue.get("nonexistent")
        assert request is None

    def test_should_approve_request(self, queue):
        """Can approve a request."""
        request_id = queue.submit(
            content="Test crisis content",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board", "ceo"],
            sla_minutes=60
        )

        result = queue.approve(request_id, approved_by="ceo@company.com")
        assert result is True

        request = queue.get(request_id)
        assert request.status == "approved"
        assert request.approved_by == "ceo@company.com"

    def test_should_reject_request(self, queue):
        """Can reject a request."""
        request_id = queue.submit(
            content="Test crisis content",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board", "ceo"],
            sla_minutes=60
        )

        result = queue.reject(request_id, rejected_by="ceo@company.com", reason="Not appropriate")
        assert result is True

        request = queue.get(request_id)
        assert request.status == "rejected"
        assert request.rejected_by == "ceo@company.com"
        assert request.rejection_reason == "Not appropriate"

    def test_should_return_false_for_approve_nonexistent(self, queue):
        """Returns False when approving nonexistent request."""
        result = queue.approve("nonexistent", approved_by="test")
        assert result is False

    def test_should_get_pending_requests(self, queue):
        """Can get all pending requests."""
        queue.submit(
            content="Content 1",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board"],
            sla_minutes=60
        )
        queue.submit(
            content="Content 2",
            crisis_level=4,
            queue="crisis_alert_review",
            approvers=["clo_board"],
            sla_minutes=75
        )

        pending = queue.get_pending()
        assert len(pending) == 2

    def test_should_filter_pending_by_queue(self, queue):
        """Can filter pending requests by queue."""
        queue.submit(
            content="Content 1",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board"],
            sla_minutes=60
        )
        queue.submit(
            content="Content 2",
            crisis_level=4,
            queue="crisis_alert_review",
            approvers=["clo_board"],
            sla_minutes=75
        )

        warning_pending = queue.get_pending(queue="crisis_warning_review")
        assert len(warning_pending) == 1
        assert warning_pending[0].queue == "crisis_warning_review"

    def test_should_exclude_approved_from_pending(self, queue):
        """Approved requests not in pending list."""
        request_id = queue.submit(
            content="Content 1",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board"],
            sla_minutes=60
        )
        queue.approve(request_id, approved_by="test")

        pending = queue.get_pending()
        assert len(pending) == 0

    def test_should_sort_pending_by_created_time(self, queue):
        """Pending requests sorted by creation time."""
        import time

        id1 = queue.submit(content="First", crisis_level=3, queue="q", approvers=[], sla_minutes=60)
        time.sleep(0.01)
        id2 = queue.submit(content="Second", crisis_level=3, queue="q", approvers=[], sla_minutes=60)

        pending = queue.get_pending()
        assert pending[0].request_id == id1
        assert pending[1].request_id == id2

    def test_should_persist_to_files(self, temp_queue_dir):
        """Requests persist to files."""
        queue1 = CrisisFileBasedApprovalQueue(queue_dir=temp_queue_dir)
        request_id = queue1.submit(
            content="Test content",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board"],
            sla_minutes=60
        )

        # Create new queue instance
        queue2 = CrisisFileBasedApprovalQueue(queue_dir=temp_queue_dir)
        request = queue2.get(request_id)
        assert request is not None
        assert request.request_id == request_id

    def test_should_store_metadata(self, queue):
        """Metadata is stored with request."""
        request_id = queue.submit(
            content="Test content",
            crisis_level=3,
            queue="crisis_warning_review",
            approvers=["clo_board"],
            sla_minutes=60,
            metadata={"trigger_id": "SKY-DEPEG-L4", "source": "trigger"}
        )

        request = queue.get(request_id)
        assert request.metadata["trigger_id"] == "SKY-DEPEG-L4"
        assert request.metadata["source"] == "trigger"
