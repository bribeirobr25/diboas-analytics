"""
Claims validator.

Validates performance claims against QR (Quality Review) approved list.
Ensures all claims are backed by data and within approved parameters.
"""

import re
from typing import Any, Dict, List

from src.validators.clo.clo_validation_types import (
    CLOValidationInput,
    CLOValidationIssue,
    CLOValidationSeverity,
    CLOSubValidator,
)


# QR-approved claim patterns
QR_APPROVED_CLAIMS = {
    # APY claims must be within these ranges
    "apy_range": {"min": 0, "max": 50},
    # Return claims must specify timeframe
    "return_timeframes": ["daily", "weekly", "monthly", "annual", "ytd"],
    # Allowed comparison benchmarks
    "benchmarks": ["S&P 500", "BTC", "ETH", "SOL", "USDC", "Treasury"],
}

# Patterns to detect performance claims
CLAIM_PATTERNS = [
    (r"(\d+(?:\.\d+)?)\s*%\s*(?:apy|apr|return|yield)", "percentage_claim"),
    (r"(\d+(?:\.\d+)?)\s*x\s*(?:return|gain|growth)", "multiplier_claim"),
    (r"outperform(?:s|ed)?\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*%", "outperformance_claim"),
    (r"beat(?:s|ing)?\s+(?:the\s+)?market", "market_beat_claim"),
]


class CLOClaimsValidator(CLOSubValidator):
    """
    Validate performance claims against approved parameters.

    Ensures claims are:
    1. Within approved ranges
    2. Include required timeframe context
    3. Reference approved benchmarks
    """

    @property
    def validator_name(self) -> str:
        return "claims"

    def validate(self, input: CLOValidationInput) -> List[CLOValidationIssue]:
        """
        Check content for performance claims.

        Args:
            input: Validation input with content

        Returns:
            List of issues for problematic claims
        """
        issues: List[CLOValidationIssue] = []
        content_lower = input.content.lower()

        # Check for percentage claims
        issues.extend(self._validate_percentage_claims(content_lower))

        # Check for multiplier claims
        issues.extend(self._validate_multiplier_claims(content_lower))

        # Check for unsubstantiated comparisons
        issues.extend(self._validate_comparisons(content_lower))

        return issues

    def _validate_percentage_claims(self, content: str) -> List[CLOValidationIssue]:
        """Validate percentage-based performance claims."""
        issues: List[CLOValidationIssue] = []

        pattern = r"(\d+(?:\.\d+)?)\s*%\s*(apy|apr|return|yield)"
        matches = re.findall(pattern, content)

        for value_str, claim_type in matches:
            value = float(value_str)

            # Check if APY/APR is within approved range
            if claim_type in ["apy", "apr"]:
                max_apy = QR_APPROVED_CLAIMS["apy_range"]["max"]
                if value > max_apy:
                    issues.append(
                        CLOValidationIssue(
                            code="CLO-CLM-001",
                            severity=CLOValidationSeverity.WARNING,
                            message=f"APY claim {value}% exceeds approved maximum {max_apy}%",
                            actual_value=value,
                            remediation=f"Verify claim accuracy or reduce to <= {max_apy}%",
                        )
                    )

            # Check if return claim has timeframe
            if claim_type == "return":
                has_timeframe = any(
                    tf in content for tf in QR_APPROVED_CLAIMS["return_timeframes"]
                )
                if not has_timeframe:
                    issues.append(
                        CLOValidationIssue(
                            code="CLO-CLM-002",
                            severity=CLOValidationSeverity.WARNING,
                            message=f"Return claim {value}% missing timeframe context",
                            actual_value=value,
                            remediation="Add timeframe (e.g., 'annual return', 'YTD return')",
                        )
                    )

        return issues

    def _validate_multiplier_claims(self, content: str) -> List[CLOValidationIssue]:
        """Validate multiplier claims (e.g., '10x return')."""
        issues: List[CLOValidationIssue] = []

        pattern = r"(\d+(?:\.\d+)?)\s*x\s*(return|gain|growth)"
        matches = re.findall(pattern, content)

        for value_str, claim_type in matches:
            value = float(value_str)

            # Flag unrealistic multiplier claims
            if value > 10:
                issues.append(
                    CLOValidationIssue(
                        code="CLO-CLM-003",
                        severity=CLOValidationSeverity.ERROR,
                        message=f"Unrealistic multiplier claim: {value}x {claim_type}",
                        actual_value=value,
                        remediation="Remove or substantiate with verified data",
                    )
                )

        return issues

    def _validate_comparisons(self, content: str) -> List[CLOValidationIssue]:
        """Validate benchmark comparisons."""
        issues: List[CLOValidationIssue] = []

        # Check for 'beat market' claims without specifics
        if "beat" in content and "market" in content:
            has_benchmark = any(
                b.lower() in content for b in QR_APPROVED_CLAIMS["benchmarks"]
            )
            if not has_benchmark:
                issues.append(
                    CLOValidationIssue(
                        code="CLO-CLM-004",
                        severity=CLOValidationSeverity.WARNING,
                        message="'Beat market' claim without specific benchmark",
                        remediation="Specify benchmark (e.g., 'beat S&P 500')",
                    )
                )

        return issues
