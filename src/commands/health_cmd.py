"""
Health check CLI command.

Runs system health checks and reports status.

Usage:
    python main.py health
    python main.py health --connectivity
    python main.py health --json
"""

import json
import logging
from datetime import datetime

from src.utils.health import get_system_health, HealthStatus
from src.utils.circuit_breaker import get_all_circuit_health
from src.utils.correlation import with_correlation_id

logger = logging.getLogger(__name__)


def add_health_parser(subparsers):
    """Add health command to CLI argument parser."""
    parser = subparsers.add_parser(
        "health",
        help="Check system health status",
    )
    parser.add_argument(
        "--connectivity",
        action="store_true",
        help="Include network connectivity checks (slower)",
    )
    parser.add_argument(
        "--json",
        dest="output_json",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include detailed check information",
    )
    parser.set_defaults(func=run_health)


@with_correlation_id(prefix="health")
def run_health(args) -> int:
    """
    Run health checks and display results.

    Args:
        args: Parsed command arguments

    Returns:
        Exit code (0 for healthy, 1 for degraded, 2 for unhealthy)
    """
    include_connectivity = getattr(args, "connectivity", False)
    output_json = getattr(args, "output_json", False)
    verbose = getattr(args, "verbose", False)

    logger.info("Running system health checks...")

    # Get health status
    health = get_system_health(include_connectivity=include_connectivity)

    # Get circuit breaker health
    circuit_health = get_all_circuit_health()
    health["circuit_breakers"] = circuit_health

    if output_json:
        print(json.dumps(health, indent=2))
    else:
        _print_health_report(health, verbose)

    # Determine exit code
    status = health.get("status", "unknown")
    if status == "healthy":
        return 0
    elif status == "degraded":
        return 1
    else:
        return 2


def _print_health_report(health: dict, verbose: bool = False) -> None:
    """
    Print human-readable health report.

    Args:
        health: Health check results
        verbose: Include detailed information
    """
    # Header
    status = health.get("status", "unknown")
    status_emoji = _get_status_emoji(status)
    timestamp = health.get("timestamp", datetime.utcnow().isoformat())

    print(f"\n{status_emoji} System Health: {status.upper()}")
    print(f"   Timestamp: {timestamp}")
    print("-" * 50)

    # Individual checks
    checks = health.get("checks", [])
    for check in checks:
        check_emoji = _get_status_emoji(check.get("status", "unknown"))
        name = check.get("name", "unknown")
        message = check.get("message", "")
        duration = check.get("duration_ms", 0)

        print(f"{check_emoji} {name}")
        print(f"   {message}")

        if verbose and "details" in check:
            details = check["details"]
            for key, value in details.items():
                print(f"     {key}: {value}")

        if duration > 0:
            print(f"     (completed in {duration}ms)")
        print()

    # Circuit breakers
    circuit_health = health.get("circuit_breakers", {})
    if circuit_health:
        print("\nCircuit Breakers:")
        print("-" * 50)
        for name, info in circuit_health.items():
            state = info.get("state", "unknown")
            state_emoji = "🟢" if state == "CLOSED" else "🔴" if state == "OPEN" else "🟡"
            failure_count = info.get("failure_count", 0)
            print(f"  {state_emoji} {name}: {state} (failures: {failure_count})")

    # Summary
    healthy_count = sum(1 for c in checks if c.get("status") == "healthy")
    total_count = len(checks)
    print(f"\nSummary: {healthy_count}/{total_count} checks healthy")


def _get_status_emoji(status: str) -> str:
    """Get emoji for status."""
    emoji_map = {
        "healthy": "✅",
        "degraded": "⚠️",
        "unhealthy": "❌",
        "unknown": "❓",
    }
    return emoji_map.get(status.lower(), "❓")
