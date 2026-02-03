"""
Validate CLO command handler - Run CLO Gate 4 compliance validation.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def run_validate_clo(args):
    """
    Run CLO Gate 4 compliance validation.

    Args:
        args: CLI arguments with:
            - content: Content to validate (or path to file)
            - jurisdiction: Target jurisdiction (US, EU, BR, UK)
            - crisis_level: Crisis level 0-5
    """
    from src.validators.clo import (
        CLOGate4Validator,
        CLOValidationInput,
        CLOJurisdiction,
        CLOValidationStatus,
    )

    print("Running CLO Gate 4 compliance validation...")
    print()

    # Get content
    content = args.content
    if content and Path(content).exists():
        content = Path(content).read_text()
        print(f"  Loaded content from file: {args.content}")
    elif not content:
        print("  Error: No content provided")
        print("  Usage: validate-clo --content 'Your content here'")
        print("         validate-clo --content ./path/to/file.txt")
        return

    # Parse jurisdiction
    jurisdiction_map = {
        "US": CLOJurisdiction.US,
        "EU": CLOJurisdiction.EU,
        "BR": CLOJurisdiction.BR,
        "UK": CLOJurisdiction.UK,
    }
    jurisdiction = jurisdiction_map.get(args.jurisdiction, CLOJurisdiction.US)

    print(f"  Jurisdiction: {args.jurisdiction}")
    print(f"  Crisis level: {args.crisis_level}")
    print(f"  Content length: {len(content)} characters")
    print()

    # Create validator
    validator = CLOGate4Validator(config={})

    # Create input
    input_data = CLOValidationInput(
        content=content,
        jurisdiction=jurisdiction,
        crisis_level=args.crisis_level,
    )

    # Run validation
    result = validator.validate(input_data)

    # Display results
    status_icons = {
        CLOValidationStatus.PASS: "PASS",
        CLOValidationStatus.WARN: "WARN",
        CLOValidationStatus.FAIL: "FAIL",
        CLOValidationStatus.HUMAN_REQUIRED: "HUMAN",
    }

    print("  Validation Result")
    print("  -----------------")
    print(f"  Status: {status_icons.get(result.status, 'UNKNOWN')}")
    print(f"  Routing: {result.routing_decision}")
    print(f"  Requires human: {result.requires_human}")

    if result.human_queue:
        print(f"  Human queue: {result.human_queue}")

    if result.issues:
        print()
        print(f"  Issues ({len(result.issues)}):")
        for issue in result.issues:
            severity = issue.get("severity", "info")
            message = issue.get("message", str(issue))
            print(f"    [{severity.upper()}] {message}")

    if result.warnings:
        print()
        print(f"  Warnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"    - {warning}")

    print()

    if result.status == CLOValidationStatus.PASS:
        print("  Content is compliant and ready for delivery.")
    elif result.status == CLOValidationStatus.WARN:
        print("  Content has warnings but can proceed.")
    elif result.status == CLOValidationStatus.FAIL:
        print("  Content failed compliance. Must be revised before delivery.")
    elif result.status == CLOValidationStatus.HUMAN_REQUIRED:
        print(f"  Content requires human review in queue: {result.human_queue}")
