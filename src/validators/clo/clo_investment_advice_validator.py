"""
Investment advice validator.

Detects patterns that could constitute investment advice under SEC/FINRA rules.
Distinguishes between educational content and personalized advice.
"""

import re
from typing import Any, Dict, List

from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOValidationIssue,
    CLOValidationSeverity,
    CLOSubValidator,
    CLOJurisdiction,
)


# Patterns that may constitute investment advice
ADVICE_PATTERNS = [
    # Direct recommendations
    (r"\byou should (buy|sell|invest|hold|avoid)\b", "Direct investment recommendation"),
    (r"\bwe (recommend|advise|suggest) (you )?(buy|sell|invest|hold)\b", "Investment recommendation"),
    (r"\bi (recommend|advise|suggest) (you )?(buy|sell|invest|hold)\b", "Investment recommendation"),
    # Personalized advice indicators
    (r"\bbased on your (situation|portfolio|risk|goals)\b", "Personalized advice"),
    (r"\bfor your specific (needs|situation|portfolio)\b", "Personalized advice"),
    # Imperative buy/sell
    (r"\b(buy|sell|invest in) (this|these|the) (strategy|strategies|asset)\b", "Imperative advice"),
    # Timing advice
    (r"\bnow is the (time|right time|best time) to (buy|sell|invest)\b", "Market timing advice"),
    (r"\bact (now|quickly|fast) (before|to)\b", "Urgency pressure"),
]

# Patterns allowed (educational context)
ALLOWED_PATTERNS = [
    r"\bgenerally\b",
    r"\bhistorically\b",
    r"\bin the past\b",
    r"\bmay\b",
    r"\bcould\b",
    r"\bmight\b",
    r"\bsome investors\b",
    r"\bconsider consulting\b",
]


class CLOInvestmentAdviceValidator(CLOSubValidator):
    """
    Validate content for investment advice patterns.

    Flags content that may cross the line from education to advice.
    """

    @property
    def validator_name(self) -> str:
        return "investment_advice"

    def validate(self, input: CLOValidationInput) -> List[CLOValidationIssue]:
        """
        Check content for investment advice patterns.

        Args:
            input: Validation input with content and jurisdiction

        Returns:
            List of issues for advice patterns found
        """
        issues: List[CLOValidationIssue] = []
        content_lower = input.content.lower()

        # Check each advice pattern
        for pattern, description in ADVICE_PATTERNS:
            matches = re.findall(pattern, content_lower)
            if matches:
                # Check if mitigated by allowed patterns nearby
                if self._is_mitigated(content_lower, matches[0] if isinstance(matches[0], str) else matches[0][0]):
                    continue

                # Determine severity based on jurisdiction
                severity = self._get_severity(input.jurisdiction)

                issues.append(
                    CLOValidationIssue(
                        code="CLO-ADV-001",
                        severity=severity,
                        message=f"Potential investment advice: {description}",
                        actual_value=str(matches[0]),
                        remediation="Rephrase using educational language or add appropriate disclaimers",
                        jurisdiction=input.jurisdiction.value,
                        regulatory_reference="SEC/FINRA Investment Advisers Act",
                    )
                )

        return issues

    def _is_mitigated(self, content: str, match: str) -> bool:
        """
        Check if advice pattern is mitigated by educational context.

        Looks for hedging language near the matched pattern.
        """
        # Find position of match
        match_pos = content.find(match.lower() if isinstance(match, str) else match)
        if match_pos == -1:
            return False

        # Check surrounding context (100 chars before)
        start = max(0, match_pos - 100)
        context = content[start:match_pos]

        for allowed in ALLOWED_PATTERNS:
            if re.search(allowed, context):
                return True

        return False

    def _get_severity(self, jurisdiction: CLOJurisdiction) -> CLOValidationSeverity:
        """
        Get severity based on jurisdiction.

        US has stricter requirements.
        """
        if jurisdiction == CLOJurisdiction.US:
            return CLOValidationSeverity.ERROR
        return CLOValidationSeverity.WARNING
