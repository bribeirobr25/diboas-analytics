"""
Disclaimer validator.

Ensures required disclaimers are present based on jurisdiction.
Each jurisdiction has specific regulatory requirements for disclosures.
"""

import re
import unicodedata
from typing import Any, Dict, List

from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOValidationIssue,
    CLOValidationSeverity,
    CLOSubValidator,
    CLOJurisdiction,
)


# Required disclaimer phrases by jurisdiction
REQUIRED_DISCLAIMERS = {
    CLOJurisdiction.US: [
        {
            "id": "US-001",
            "pattern": "not investment advice",
            "alternatives": ["not financial advice", "for informational purposes only"],
            "regulatory_ref": "SEC/FINRA Guidelines",
        },
        {
            "id": "US-002",
            "pattern": "past performance",
            "alternatives": ["historical performance", "prior results"],
            "regulatory_ref": "SEC Rule 206(4)-1",
        },
    ],
    CLOJurisdiction.EU: [
        {
            "id": "EU-001",
            "pattern": "not investment advice",
            "alternatives": ["not financial advice", "for informational purposes only"],
            "regulatory_ref": "MiFID II",
        },
        {
            "id": "EU-002",
            "pattern": "capital at risk",
            "alternatives": ["your capital is at risk", "investment risk", "may lose value"],
            "regulatory_ref": "MiFID II Article 24",
        },
    ],
    CLOJurisdiction.BR: [
        {
            "id": "BR-001",
            "pattern": "investimentos envolvem riscos",
            "alternatives": ["risco de perda", "pode perder valor"],
            "regulatory_ref": "CVM Instruction 555",
        },
    ],
}


# CVM 3-part structure requirements for Brazil
# These are validated using regex patterns after content normalization
CVM_THREE_PARTS = [
    {
        "id": "BR-CVM-001",
        "part": "investor_protection",
        # Pattern matches normalized content (accents stripped, lowercase)
        # Matches: "não são protegidos" after normalization becomes "nao sao protegid"
        "pattern": r"\bnao\s+(sao|e)\s+protegid",
        "description": "Not protected by investor schemes",
        "regulatory_ref": "CVM Instruction 555",
    },
    {
        "id": "BR-CVM-002",
        "part": "loss_warning",
        # Matches variations of "pode perder capital/valor/investido"
        "pattern": r"(perder|perda).{0,30}(capital|investido|valor)",
        "description": "Risk of capital loss",
        "regulatory_ref": "CVM Instruction 555",
    },
    {
        "id": "BR-CVM-003",
        "part": "professional_advice",
        # Matches "profissional habilitado" or "assessor financeiro" or "consultar"
        "pattern": r"(profissional\s+habilitado|assessor\s+financeiro|cvm.*orienta|consultar.*assessor)",
        "description": "Consult qualified professional",
        "regulatory_ref": "CVM Instruction 555",
    },
]


class CLODisclaimerValidator(CLOSubValidator):
    """
    Validate that required disclaimers are present.

    Checks for jurisdiction-specific mandatory disclaimers.
    For Brazil (BR), validates the CVM 3-part structure requirement.
    """

    @property
    def validator_name(self) -> str:
        return "disclaimer"

    def _normalize_for_validation(self, content: str) -> str:
        """
        Normalize content for validation.

        Removes markdown formatting, lowercases, and strips accented characters
        to allow consistent regex matching regardless of formatting variations.

        Args:
            content: Raw content string

        Returns:
            Normalized string for pattern matching
        """
        # Remove markdown formatting
        content = re.sub(r'\*+', '', content)
        content = re.sub(r'#+\s*', '', content)
        # Lowercase
        content = content.lower()
        # Normalize unicode AND strip combining marks (accents)
        # NFKD decomposes accented chars: "ã" -> "a" + combining tilde
        # Then we filter out combining characters
        content = unicodedata.normalize('NFKD', content)
        content = "".join(ch for ch in content if not unicodedata.combining(ch))
        return content

    def _validate_cvm_structure(self, content: str) -> List[CLOValidationIssue]:
        """
        Validate all 3 CVM required parts are present for Brazil.

        The CVM (Comissão de Valores Mobiliários) requires 3 specific disclosures:
        1. Investor protection notice (not protected by guarantee schemes)
        2. Loss warning (may lose capital)
        3. Professional advice recommendation

        Args:
            content: Content to validate

        Returns:
            List of validation issues for missing CVM parts
        """
        issues = []
        normalized = self._normalize_for_validation(content)

        for part in CVM_THREE_PARTS:
            if not re.search(part["pattern"], normalized, re.IGNORECASE):
                issues.append(
                    CLOValidationIssue(
                        code=f"CLO-DIS-{part['id']}",
                        severity=CLOValidationSeverity.ERROR,
                        message=f"Missing CVM required part: {part['description']}",
                        field="disclaimer",
                        remediation=f"Add content matching CVM requirement for: {part['part']}",
                        jurisdiction="BR",
                        regulatory_reference=part["regulatory_ref"],
                    )
                )

        return issues

    def validate(self, input: CLOValidationInput) -> List[CLOValidationIssue]:
        """
        Check content for required disclaimers.

        Args:
            input: Validation input with content and jurisdiction

        Returns:
            List of issues for missing disclaimers
        """
        issues: List[CLOValidationIssue] = []
        content_lower = input.content.lower()

        required = REQUIRED_DISCLAIMERS.get(input.jurisdiction, [])

        for disclaimer in required:
            found = self._check_disclaimer_present(content_lower, disclaimer)
            if not found:
                issues.append(
                    CLOValidationIssue(
                        code=f"CLO-DIS-{disclaimer['id']}",
                        severity=CLOValidationSeverity.ERROR,
                        message=f"Missing required disclaimer: '{disclaimer['pattern']}'",
                        field="disclaimer",
                        remediation=f"Add disclaimer containing '{disclaimer['pattern']}' or equivalent",
                        jurisdiction=input.jurisdiction.value,
                        regulatory_reference=disclaimer.get("regulatory_ref"),
                    )
                )

        # For Brazil, also validate CVM 3-part structure
        if input.jurisdiction == CLOJurisdiction.BR:
            cvm_issues = self._validate_cvm_structure(input.content)
            issues.extend(cvm_issues)

        return issues

    def _check_disclaimer_present(
        self, content_lower: str, disclaimer: Dict[str, Any]
    ) -> bool:
        """
        Check if a disclaimer or its alternatives are present.

        Args:
            content_lower: Lowercase content to check
            disclaimer: Disclaimer definition with pattern and alternatives

        Returns:
            True if disclaimer found, False otherwise
        """
        # Check primary pattern
        if disclaimer["pattern"] in content_lower:
            return True

        # Check alternatives
        for alt in disclaimer.get("alternatives", []):
            if alt in content_lower:
                return True

        return False
