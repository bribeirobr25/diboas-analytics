"""
Tone validator.

Ensures content tone is appropriate for the context.
Crisis-level content requires serious, measured tone.
"""

import re
from typing import Any, Dict, List

from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOValidationIssue,
    CLOValidationSeverity,
    CLOSubValidator,
)


# Inappropriate tone patterns for crisis content
INAPPROPRIATE_CRISIS_PATTERNS = [
    # Overly casual
    (r"\blol\b", "Casual acronym"),
    (r"\bhaha\b", "Casual expression"),
    (r"!{2,}", "Excessive exclamation marks"),
    # Emojis that minimize seriousness
    (r"[😂🤣😜😝🎉🥳]", "Inappropriate emoji"),
    # Dismissive language
    (r"\bno big deal\b", "Dismissive language"),
    (r"\bnothing to worry about\b", "Dismissive language"),
    (r"\bdon't panic\b", "Panic reference"),
]

# Expected serious tone markers for crisis content
CRISIS_TONE_MARKERS = [
    "we are monitoring",
    "we recommend",
    "please be aware",
    "important update",
    "market conditions",
    "we advise caution",
]


class CLOToneValidator(CLOSubValidator):
    """
    Validate content tone is appropriate for context.

    Crisis content requires measured, professional tone.
    """

    @property
    def validator_name(self) -> str:
        return "tone"

    def validate(self, input: CLOValidationInput) -> List[CLOValidationIssue]:
        """
        Check content tone appropriateness.

        Args:
            input: Validation input with content and crisis level

        Returns:
            List of issues for inappropriate tone
        """
        issues: List[CLOValidationIssue] = []

        # Only validate tone strictly for crisis content (level >= 2)
        if input.crisis_level < 2:
            return issues

        content_lower = input.content.lower()

        # Check for inappropriate patterns
        for pattern, description in INAPPROPRIATE_CRISIS_PATTERNS:
            if re.search(pattern, content_lower) or re.search(pattern, input.content):
                issues.append(
                    CLOValidationIssue(
                        code="CLO-TON-001",
                        severity=CLOValidationSeverity.WARNING,
                        message=f"Inappropriate tone for crisis content: {description}",
                        remediation="Use professional, measured language",
                    )
                )

        # For high crisis levels, check for serious tone markers
        if input.crisis_level >= 3:
            has_serious_tone = any(
                marker in content_lower for marker in CRISIS_TONE_MARKERS
            )
            if not has_serious_tone:
                issues.append(
                    CLOValidationIssue(
                        code="CLO-TON-002",
                        severity=CLOValidationSeverity.INFO,
                        message="Crisis content may benefit from more measured language",
                        remediation="Consider adding professional tone markers",
                    )
                )

        return issues
