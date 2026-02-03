"""
Fee disclosure validator.

Ensures fee-related content includes required disclosures.
Validates that fee structures are clearly communicated.
"""

import re
from typing import Any, Dict, List

from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOValidationIssue,
    CLOValidationSeverity,
    CLOSubValidator,
)


# Patterns that indicate fee discussion
FEE_PATTERNS = [
    r"\bfee(?:s)?\b",
    r"\bcost(?:s)?\b",
    r"\bcharge(?:s)?\b",
    r"\bcommission\b",
    r"\bexpense(?:s)?\b",
]

# Required disclosure when fees are mentioned
REQUIRED_FEE_DISCLOSURES = [
    "fee schedule",
    "full fee details",
    "additional fees may apply",
    "see fee schedule",
    "consult fee schedule",
]


class CLOFeeDisclosureValidator(CLOSubValidator):
    """
    Validate fee-related content for required disclosures.

    When fees are mentioned, ensures proper disclosure language is present.
    """

    @property
    def validator_name(self) -> str:
        return "fee_disclosure"

    def validate(self, input: CLOValidationInput) -> List[CLOValidationIssue]:
        """
        Check content for fee disclosure requirements.

        Args:
            input: Validation input with content

        Returns:
            List of issues for missing fee disclosures
        """
        issues: List[CLOValidationIssue] = []
        content_lower = input.content.lower()

        # Check if fees are mentioned
        mentions_fees = any(
            re.search(pattern, content_lower) for pattern in FEE_PATTERNS
        )

        if not mentions_fees:
            return issues

        # If fees are mentioned, check for required disclosure
        has_disclosure = any(
            disclosure in content_lower for disclosure in REQUIRED_FEE_DISCLOSURES
        )

        if not has_disclosure:
            issues.append(
                CLOValidationIssue(
                    code="CLO-FEE-001",
                    severity=CLOValidationSeverity.WARNING,
                    message="Fee content without disclosure reference",
                    remediation="Add reference to full fee schedule",
                )
            )

        return issues
