"""
Crisis Communication Routing.

Handles crisis-level content classification, routing, and approval workflows.

Components:
- CrisisLevelClassifier: Classify content into crisis levels 0-5
- CrisisRouter: Route content based on level
- CrisisFileBasedApprovalQueue: File-based approval queue ($0 budget)
- CrisisSlackNotifier: Slack webhook notifications
- CrisisEscalationChecker: SLA enforcement

Usage:
    from src.crisis import CrisisLevelClassifier, CrisisRouter

    classifier = CrisisLevelClassifier()
    classification = classifier.classify(content)

    router = CrisisRouter()
    decision = router.route(content, classification)
"""

from src.crisis.crisis_level_classifier import (
    CrisisLevel,
    CrisisClassification,
    CrisisLevelClassifier,
)
from src.crisis.crisis_router import CrisisRouter, CrisisRoutingDecision
from src.crisis.crisis_approval_queue import (
    CrisisApprovalRequest,
    CrisisFileBasedApprovalQueue,
)
from src.crisis.crisis_slack_notifier import CrisisSlackNotifier
from src.crisis.crisis_escalation_checker import CrisisEscalationChecker

__all__ = [
    "CrisisLevel",
    "CrisisClassification",
    "CrisisLevelClassifier",
    "CrisisRouter",
    "CrisisRoutingDecision",
    "CrisisApprovalRequest",
    "CrisisFileBasedApprovalQueue",
    "CrisisSlackNotifier",
    "CrisisEscalationChecker",
]
