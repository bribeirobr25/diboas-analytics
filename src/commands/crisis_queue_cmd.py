"""
Crisis queue command handler - Manage crisis approval queue.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def run_crisis_queue(args):
    """
    Manage crisis approval queue.

    Args:
        args: CLI arguments with:
            - crisis_action: 'list', 'approve', or 'reject'
            - queue: Queue filter (for list)
            - request_id: Request ID (for approve/reject)
            - approver: Approver name/email
            - reason: Rejection reason
    """
    from src.crisis import CrisisFileBasedApprovalQueue

    queue = CrisisFileBasedApprovalQueue()

    if args.crisis_action == 'list':
        _handle_list(queue, args)
    elif args.crisis_action == 'approve':
        _handle_approve(queue, args)
    elif args.crisis_action == 'reject':
        _handle_reject(queue, args)
    else:
        print("Crisis queue management")
        print()
        print("Commands:")
        print("  crisis-queue list [--queue NAME]     List pending requests")
        print("  crisis-queue approve ID --approver X  Approve a request")
        print("  crisis-queue reject ID --approver X   Reject a request")


def _handle_list(queue, args):
    """List pending requests."""
    print("Pending Crisis Approval Requests")
    print("=" * 50)
    print()

    pending = queue.get_pending(queue=getattr(args, 'queue', None))

    if not pending:
        print("  No pending requests.")
        return

    for request in pending:
        _print_request(request)
        print()


def _print_request(request):
    """Print a single request."""
    age_minutes = (datetime.utcnow() - request.created_at).total_seconds() / 60

    print(f"  Request ID: {request.request_id}")
    print(f"  Queue: {request.queue}")
    print(f"  Crisis Level: {request.crisis_level}")
    print(f"  Status: {request.status}")
    print(f"  Submitted: {request.created_at.strftime('%Y-%m-%d %H:%M UTC')} ({age_minutes:.0f}m ago)")
    print(f"  SLA: {request.sla_minutes}m")
    print(f"  Approvers: {', '.join(request.approvers)}")

    if request.metadata:
        print(f"  Metadata: {request.metadata}")

    # Preview first 100 chars of content
    preview = request.content[:100].replace('\n', ' ')
    if len(request.content) > 100:
        preview += "..."
    print(f"  Preview: {preview}")


def _handle_approve(queue, args):
    """Approve a request."""
    print(f"Approving request: {args.request_id}")
    print()

    # Get request first
    request = queue.get(args.request_id)
    if not request:
        print(f"  Error: Request {args.request_id} not found")
        return

    if request.status != "pending":
        print(f"  Error: Request is already {request.status}")
        return

    # Approve
    success = queue.approve(args.request_id, approved_by=args.approver)

    if success:
        print(f"  Request approved by: {args.approver}")
        print(f"  Status: approved")
        print()
        print("  Content can now be delivered.")
    else:
        print("  Error: Failed to approve request")


def _handle_reject(queue, args):
    """Reject a request."""
    print(f"Rejecting request: {args.request_id}")
    print()

    # Get request first
    request = queue.get(args.request_id)
    if not request:
        print(f"  Error: Request {args.request_id} not found")
        return

    if request.status != "pending":
        print(f"  Error: Request is already {request.status}")
        return

    # Reject
    reason = getattr(args, 'reason', None) or "No reason provided"
    success = queue.reject(args.request_id, rejected_by=args.approver, reason=reason)

    if success:
        print(f"  Request rejected by: {args.approver}")
        print(f"  Reason: {reason}")
        print(f"  Status: rejected")
        print()
        print("  Content will NOT be delivered.")
    else:
        print("  Error: Failed to reject request")
