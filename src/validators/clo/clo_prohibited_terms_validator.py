"""
Prohibited terms validator.

Detects terms that are banned in financial communications.
Checks both universal terms and jurisdiction-specific terms.
"""

from typing import Any, Dict, List

from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOValidationIssue,
    CLOValidationSeverity,
    CLOSubValidator,
    CLOJurisdiction,
)


# Universal prohibited terms (all jurisdictions)
PROHIBITED_TERMS_UNIVERSAL = [
    ("guaranteed", "No return is guaranteed"),
    ("risk-free", "All investments carry risk"),
    ("risk free", "All investments carry risk"),
    ("cannot lose", "Losses are possible"),
    ("100% safe", "No investment is 100% safe"),
    ("assured profit", "Profits are not assured"),
    ("get rich quick", "Misleading claims"),
    ("no risk", "All investments carry risk"),
    ("zero risk", "All investments carry risk"),
    ("sure thing", "No investment is a sure thing"),
    ("can't fail", "All investments can fail"),
    ("failproof", "No investment is failproof"),
    ("foolproof", "No investment is foolproof"),
]

# US-specific prohibited terms (SEC/FINRA)
PROHIBITED_TERMS_US = [
    ("you should invest", "Constitutes investment advice"),
    ("i recommend", "Constitutes investment advice"),
    ("we advise", "Constitutes investment advice"),
    ("buy now", "Market timing advice"),
    ("sell now", "Market timing advice"),
    ("this is financial advice", "We do not provide financial advice"),
]

# Brazil-specific prohibited terms (CVM)
PROHIBITED_TERMS_BR = [
    ("lucro garantido", "Guaranteed profit"),
    ("sem risco", "Without risk"),
    ("rentabilidade certa", "Certain return"),
    ("ganho garantido", "Guaranteed gain"),
]

# EU-specific prohibited terms (MiFID II)
PROHIBITED_TERMS_EU = [
    ("guaranteed returns", "No return is guaranteed"),
    ("capital protection guarantee", "Capital protection not guaranteed"),
]


class CLOProhibitedTermsValidator(CLOSubValidator):
    """
    Validate content for prohibited terms.

    Checks both universal and jurisdiction-specific prohibited terms.
    """

    @property
    def validator_name(self) -> str:
        return "prohibited_terms"

    def validate(self, input: CLOValidationInput) -> List[CLOValidationIssue]:
        """
        Check content for prohibited terms.

        Args:
            input: Validation input with content and jurisdiction

        Returns:
            List of issues for any prohibited terms found
        """
        issues: List[CLOValidationIssue] = []
        content_lower = input.content.lower()

        # Check universal terms
        for term, reason in PROHIBITED_TERMS_UNIVERSAL:
            if term in content_lower:
                issues.append(
                    CLOValidationIssue(
                        code="CLO-PRO-001",
                        severity=CLOValidationSeverity.ERROR,
                        message=f"Prohibited term: '{term}'",
                        actual_value=term,
                        remediation=reason,
                    )
                )

        # Check jurisdiction-specific terms
        jurisdiction_terms = self._get_jurisdiction_terms(input.jurisdiction)
        for term, reason in jurisdiction_terms:
            if term in content_lower:
                issues.append(
                    CLOValidationIssue(
                        code="CLO-PRO-002",
                        severity=CLOValidationSeverity.ERROR,
                        message=f"{input.jurisdiction.value} prohibited: '{term}'",
                        actual_value=term,
                        remediation=reason,
                        jurisdiction=input.jurisdiction.value,
                    )
                )

        return issues

    def _get_jurisdiction_terms(
        self, jurisdiction: CLOJurisdiction
    ) -> List[tuple[str, str]]:
        """Get jurisdiction-specific prohibited terms."""
        terms_map = {
            CLOJurisdiction.US: PROHIBITED_TERMS_US,
            CLOJurisdiction.BR: PROHIBITED_TERMS_BR,
            CLOJurisdiction.EU: PROHIBITED_TERMS_EU,
        }
        return terms_map.get(jurisdiction, [])
