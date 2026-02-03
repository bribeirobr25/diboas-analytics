"""
CLO Gate 4 Compliance Validators.

Validates Adelaide newsletter content for legal compliance before delivery.
Ensures content meets regulatory requirements across jurisdictions.

Validators:
- CLOGate4Validator: Main orchestrator (composite pattern)
- CLODisclaimerValidator: Required disclaimers per jurisdiction
- CLOProhibitedTermsValidator: Blocked terms detection
- CLOInvestmentAdviceValidator: SEC/FINRA advice patterns
- CLOClaimsValidator: Claims vs QR-approved list
- CLOFeeDisclosureValidator: Fee structure validation
- CLOToneValidator: Crisis-appropriate tone

Usage:
    from src.validators.clo import CLOGate4Validator, CLOValidationInput

    validator = CLOGate4Validator()
    result = validator.validate(CLOValidationInput(
        content="newsletter content...",
        jurisdiction=CLOJurisdiction.US
    ))
"""

from src.validators.clo.clo_validation_types import (
    CLOValidationStatus,
    CLOValidationSeverity,
    CLOJurisdiction,
    CLOValidationIssue,
    CLOValidationResult,
    CLOValidationInput,
    CLOSubValidator,
)
from src.validators.clo.clo_gate4_validator import CLOGate4Validator

__all__ = [
    "CLOValidationStatus",
    "CLOValidationSeverity",
    "CLOJurisdiction",
    "CLOValidationIssue",
    "CLOValidationResult",
    "CLOValidationInput",
    "CLOSubValidator",
    "CLOGate4Validator",
]
