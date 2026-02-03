"""
CLO Gate 4 Validator - Main orchestrator.

Uses composite pattern to run all sub-validators and determine
final validation status and routing decision.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOValidationResult,
    CLOValidationStatus,
    CLOValidationIssue,
    CLOValidationSeverity,
    CLOSubValidator,
    CLOJurisdiction,
)
from src.validators.clo.clo_disclaimer_validator import CLODisclaimerValidator
from src.validators.clo.clo_prohibited_terms_validator import CLOProhibitedTermsValidator
from src.validators.clo.clo_investment_advice_validator import CLOInvestmentAdviceValidator
from src.validators.clo.clo_claims_validator import CLOClaimsValidator
from src.validators.clo.clo_fee_disclosure_validator import CLOFeeDisclosureValidator
from src.validators.clo.clo_tone_validator import CLOToneValidator

logger = logging.getLogger(__name__)

# Configuration constants
CLO_FIRST_N_SPOT_CHECK = 20
CLO_SLA_MINUTES = {
    "level_3": 60,
    "level_4": 75,
    "level_5": 90,
    "spot_check": 480,  # 8 hours
}


class CLOGate4Validator:
    """
    Main CLO Gate 4 compliance validator.

    Orchestrates all sub-validators using composite pattern.
    Determines final status and routing decision based on issues.

    Workflow:
    1. Check if human review required (crisis level, spot-check)
    2. Check jurisdiction (UK geo-blocked)
    3. Run all sub-validators
    4. Aggregate issues and determine status
    5. Return routing decision
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize with optional configuration.

        Args:
            config: Configuration dict with validator settings
        """
        self.config = config or {}
        self.sub_validators: List[CLOSubValidator] = self._init_validators()

    def _init_validators(self) -> List[CLOSubValidator]:
        """Initialize all sub-validators."""
        return [
            CLODisclaimerValidator(self.config),
            CLOProhibitedTermsValidator(self.config),
            CLOInvestmentAdviceValidator(self.config),
            CLOClaimsValidator(self.config),
            CLOFeeDisclosureValidator(self.config),
            CLOToneValidator(self.config),
        ]

    def validate(self, input: CLOValidationInput) -> CLOValidationResult:
        """
        Validate content through all compliance checks.

        Args:
            input: CLOValidationInput with content and context

        Returns:
            CLOValidationResult with status, issues, and routing
        """
        start_time = time.time()
        all_issues: List[CLOValidationIssue] = []

        # 1. Check if human review required (before other checks)
        human_check = self._check_human_required(input)
        if human_check:
            human_check.metadata["gate_duration_ms"] = int((time.time() - start_time) * 1000)
            return human_check

        # 2. Check jurisdiction (UK geo-block)
        if input.jurisdiction == CLOJurisdiction.UK:
            return CLOValidationResult(
                status=CLOValidationStatus.FAIL,
                issues=[
                    CLOValidationIssue(
                        code="CLO-JUR-001",
                        severity=CLOValidationSeverity.ERROR,
                        message="UK users are geo-blocked per FSMA Section 21",
                        regulatory_reference="FSMA Section 21",
                    )
                ],
                routing_decision="block",
                metadata={"gate_duration_ms": int((time.time() - start_time) * 1000)},
            )

        # 3. Run all sub-validators
        for validator in self.sub_validators:
            try:
                issues = validator.validate(input)
                all_issues.extend(issues)
            except Exception as e:
                logger.error(f"Validator {validator.validator_name} error: {e}")
                all_issues.append(
                    CLOValidationIssue(
                        code=f"CLO-ERR-{validator.validator_name.upper()[:8]}",
                        severity=CLOValidationSeverity.WARNING,
                        message=f"Validator error: {e}",
                        remediation="Manual review recommended",
                    )
                )

        # 4. Determine status based on issues
        status, routing = self._determine_status(all_issues)

        return CLOValidationResult(
            status=status,
            issues=all_issues,
            routing_decision=routing,
            metadata={"gate_duration_ms": int((time.time() - start_time) * 1000)},
        )

    def _check_human_required(self, input: CLOValidationInput) -> Optional[CLOValidationResult]:
        """
        Check if human review is required before automated checks.

        Conditions requiring human review:
        1. Crisis Level 3+ content
        2. First N editions (spot-check requirement)
        """
        # Crisis Level 3+ requires human approval
        if input.crisis_level >= 3:
            return CLOValidationResult(
                status=CLOValidationStatus.HUMAN_REQUIRED,
                issues=[
                    CLOValidationIssue(
                        code="CLO-HUM-001",
                        severity=CLOValidationSeverity.INFO,
                        message=f"Crisis Level {input.crisis_level} requires human approval",
                    )
                ],
                routing_decision="human_queue",
                human_queue="urgent_crisis_review",
                sla_minutes=CLO_SLA_MINUTES.get(f"level_{input.crisis_level}", 60),
            )

        # First N editions require spot-check
        first_n = self.config.get("first_n_spot_check", CLO_FIRST_N_SPOT_CHECK)
        if input.adelaide_edition_number and input.adelaide_edition_number <= first_n:
            return CLOValidationResult(
                status=CLOValidationStatus.HUMAN_REQUIRED,
                issues=[
                    CLOValidationIssue(
                        code="CLO-HUM-002",
                        severity=CLOValidationSeverity.INFO,
                        message=f"Edition {input.adelaide_edition_number} requires spot-check",
                    )
                ],
                routing_decision="human_queue",
                human_queue="adelaide_spot_check",
                sla_minutes=CLO_SLA_MINUTES["spot_check"],
            )

        return None

    def _determine_status(
        self, issues: List[CLOValidationIssue]
    ) -> tuple[CLOValidationStatus, str]:
        """
        Determine validation status based on issues.

        Returns:
            Tuple of (status, routing_decision)
        """
        errors = [i for i in issues if i.severity == CLOValidationSeverity.ERROR]
        warnings = [i for i in issues if i.severity == CLOValidationSeverity.WARNING]

        if errors:
            return CLOValidationStatus.FAIL, "block"
        elif warnings:
            return CLOValidationStatus.WARN, "flag_deliver"
        else:
            return CLOValidationStatus.PASS, "auto_deliver"
