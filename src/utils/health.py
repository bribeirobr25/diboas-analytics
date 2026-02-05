"""
Health check utilities for monitoring system status.

Principle 12 (Monitoring & Observability):
------------------------------------------
Provides health checks for data freshness, protocol connectivity,
and overall system status. These checks enable proactive monitoring
and early detection of issues.

Usage:
    from src.utils.health import (
        HealthChecker,
        HealthStatus,
        check_data_freshness,
        check_protocol_connectivity,
        get_system_health,
    )

    # Quick check
    health = get_system_health()
    print(f"Status: {health['status']}")

    # Detailed check
    checker = HealthChecker()
    result = checker.run_all_checks()
    for check in result['checks']:
        print(f"{check['name']}: {check['status']}")
"""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from config.settings import DATA_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health check status values."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheckResult:
    """Result of a single health check."""
    name: str
    status: HealthStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class SystemHealthReport:
    """Overall system health report."""
    status: HealthStatus
    checks: List[HealthCheckResult]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "status": self.status.value,
            "healthy": self.status == HealthStatus.HEALTHY,
            "checks": [c.to_dict() for c in self.checks],
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


def check_data_freshness(
    data_dir: Path = None,
    max_age_hours: int = 24,
    is_offline: bool = False
) -> HealthCheckResult:
    """
    Check if data files are fresh enough.

    Args:
        data_dir: Directory containing data files
        max_age_hours: Maximum acceptable age in hours
        is_offline: Indicate using bundled offline data

    Returns:
        HealthCheckResult with freshness status
    """
    start = time.time()
    data_dir = data_dir or DATA_DIR

    try:
        # Critical files to check
        critical_files = [
            "crypto_prices.csv",
            "sentiment_indicators.csv",
            "defillama_historical_apy.csv",
        ]

        stale_files = []
        missing_files = []
        file_ages = {}

        now = datetime.now()
        max_age = timedelta(hours=max_age_hours)

        for filename in critical_files:
            filepath = data_dir / filename
            if not filepath.exists():
                missing_files.append(filename)
                continue

            mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
            age = now - mtime
            file_ages[filename] = {
                "last_modified": mtime.isoformat(),
                "age_hours": round(age.total_seconds() / 3600, 1),
            }

            if age > max_age:
                stale_files.append(filename)

        duration_ms = int((time.time() - start) * 1000)

        if missing_files:
            return HealthCheckResult(
                name="data_freshness",
                status=HealthStatus.UNHEALTHY,
                message=f"Missing critical files: {', '.join(missing_files)}",
                details={
                    "missing_files": missing_files,
                    "file_ages": file_ages,
                },
                duration_ms=duration_ms,
            )

        if stale_files:
            msg = f"Stale files (>{max_age_hours}h): {', '.join(stale_files)}"
            if is_offline:
                msg += "\n   (Expected when using bundled data in offline mode)"
            return HealthCheckResult(
                name="data_freshness",
                status=HealthStatus.DEGRADED,
                message=msg,
                details={
                    "stale_files": stale_files,
                    "file_ages": file_ages,
                    "max_age_hours": max_age_hours,
                    "is_offline": is_offline,
                },
                duration_ms=duration_ms,
            )

        return HealthCheckResult(
            name="data_freshness",
            status=HealthStatus.HEALTHY,
            message="All critical data files are fresh",
            details={
                "file_ages": file_ages,
                "max_age_hours": max_age_hours,
            },
            duration_ms=duration_ms,
        )

    except Exception as e:
        return HealthCheckResult(
            name="data_freshness",
            status=HealthStatus.UNKNOWN,
            message=f"Error checking freshness: {e}",
            details={"error": str(e)},
            duration_ms=int((time.time() - start) * 1000),
        )


def check_protocol_connectivity(timeout: int = 5) -> HealthCheckResult:
    """
    Check connectivity to external protocol APIs.

    Note: This is a lightweight check that verifies basic connectivity
    without making expensive API calls.

    Args:
        timeout: Request timeout in seconds

    Returns:
        HealthCheckResult with connectivity status
    """
    start = time.time()

    # Protocol endpoints to check (just base URLs)
    protocols = {
        "defillama": "https://api.llama.fi/protocols",
        "coingecko": "https://api.coingecko.com/api/v3/ping",
        "fred": "https://api.stlouisfed.org/fred/",
    }

    try:
        import requests

        results = {}
        failures = []

        for name, url in protocols.items():
            try:
                response = requests.head(url, timeout=timeout)
                results[name] = {
                    "status_code": response.status_code,
                    "reachable": response.status_code < 500,
                    "latency_ms": int(response.elapsed.total_seconds() * 1000),
                }
                if response.status_code >= 500:
                    failures.append(name)
            except requests.RequestException as e:
                results[name] = {
                    "status_code": None,
                    "reachable": False,
                    "error": str(e),
                }
                failures.append(name)

        duration_ms = int((time.time() - start) * 1000)

        if failures:
            status = (
                HealthStatus.UNHEALTHY
                if len(failures) == len(protocols)
                else HealthStatus.DEGRADED
            )
            return HealthCheckResult(
                name="protocol_connectivity",
                status=status,
                message=f"Unreachable protocols: {', '.join(failures)}",
                details=results,
                duration_ms=duration_ms,
            )

        return HealthCheckResult(
            name="protocol_connectivity",
            status=HealthStatus.HEALTHY,
            message="All protocol APIs reachable",
            details=results,
            duration_ms=duration_ms,
        )

    except ImportError:
        return HealthCheckResult(
            name="protocol_connectivity",
            status=HealthStatus.UNKNOWN,
            message="requests library not available",
            details={},
            duration_ms=int((time.time() - start) * 1000),
        )
    except Exception as e:
        return HealthCheckResult(
            name="protocol_connectivity",
            status=HealthStatus.UNKNOWN,
            message=f"Error checking connectivity: {e}",
            details={"error": str(e)},
            duration_ms=int((time.time() - start) * 1000),
        )


def check_disk_space(
    min_free_gb: float = 1.0,
    paths: List[Path] = None
) -> HealthCheckResult:
    """
    Check available disk space.

    Args:
        min_free_gb: Minimum required free space in GB
        paths: Paths to check (default: DATA_DIR and OUTPUT_DIR)

    Returns:
        HealthCheckResult with disk space status
    """
    start = time.time()
    paths = paths or [DATA_DIR, OUTPUT_DIR]

    try:
        import shutil

        results = {}
        low_space = []

        for path in paths:
            if not path.exists():
                continue

            usage = shutil.disk_usage(path)
            free_gb = usage.free / (1024 ** 3)
            total_gb = usage.total / (1024 ** 3)
            used_pct = (usage.used / usage.total) * 100

            results[str(path)] = {
                "free_gb": round(free_gb, 2),
                "total_gb": round(total_gb, 2),
                "used_percent": round(used_pct, 1),
            }

            if free_gb < min_free_gb:
                low_space.append(str(path))

        duration_ms = int((time.time() - start) * 1000)

        if low_space:
            return HealthCheckResult(
                name="disk_space",
                status=HealthStatus.DEGRADED,
                message=f"Low disk space on: {', '.join(low_space)}",
                details={
                    "paths": results,
                    "min_free_gb": min_free_gb,
                },
                duration_ms=duration_ms,
            )

        return HealthCheckResult(
            name="disk_space",
            status=HealthStatus.HEALTHY,
            message="Adequate disk space available",
            details={
                "paths": results,
                "min_free_gb": min_free_gb,
            },
            duration_ms=duration_ms,
        )

    except Exception as e:
        return HealthCheckResult(
            name="disk_space",
            status=HealthStatus.UNKNOWN,
            message=f"Error checking disk space: {e}",
            details={"error": str(e)},
            duration_ms=int((time.time() - start) * 1000),
        )


def check_circuit_breakers() -> HealthCheckResult:
    """
    Check status of all circuit breakers.

    Returns:
        HealthCheckResult with circuit breaker status
    """
    start = time.time()

    try:
        from src.utils.circuit_breaker import (
            get_all_circuit_health,
            CircuitState,
        )

        health = get_all_circuit_health()
        duration_ms = int((time.time() - start) * 1000)

        if not health:
            return HealthCheckResult(
                name="circuit_breakers",
                status=HealthStatus.HEALTHY,
                message="No circuit breakers registered",
                details={},
                duration_ms=duration_ms,
            )

        open_circuits = [
            name for name, info in health.items()
            if info.get("state") == CircuitState.OPEN.value
        ]

        if open_circuits:
            return HealthCheckResult(
                name="circuit_breakers",
                status=HealthStatus.DEGRADED,
                message=f"Open circuits: {', '.join(open_circuits)}",
                details=health,
                duration_ms=duration_ms,
            )

        return HealthCheckResult(
            name="circuit_breakers",
            status=HealthStatus.HEALTHY,
            message="All circuit breakers closed",
            details=health,
            duration_ms=duration_ms,
        )

    except ImportError:
        return HealthCheckResult(
            name="circuit_breakers",
            status=HealthStatus.UNKNOWN,
            message="Circuit breaker module not available",
            details={},
            duration_ms=int((time.time() - start) * 1000),
        )
    except Exception as e:
        return HealthCheckResult(
            name="circuit_breakers",
            status=HealthStatus.UNKNOWN,
            message=f"Error checking circuits: {e}",
            details={"error": str(e)},
            duration_ms=int((time.time() - start) * 1000),
        )


class HealthChecker:
    """
    Comprehensive health checker for the system.

    Runs multiple health checks and aggregates results.

    Usage:
        checker = HealthChecker()
        report = checker.run_all_checks()
        print(report.to_dict())
    """

    def __init__(self, is_offline: bool = False):
        """
        Initialize with default checks.

        Args:
            is_offline: Indicate using bundled offline data
        """
        self._is_offline = is_offline
        self._checks: List[Callable[[], HealthCheckResult]] = [
            check_disk_space,
            check_circuit_breakers,
        ]

    def add_check(self, check_func: Callable[[], HealthCheckResult]) -> None:
        """
        Add a custom health check.

        Args:
            check_func: Function returning HealthCheckResult
        """
        self._checks.append(check_func)

    def run_all_checks(
        self,
        include_connectivity: bool = False
    ) -> SystemHealthReport:
        """
        Run all registered health checks.

        Args:
            include_connectivity: Include external API connectivity check
                                (disabled by default as it's slow)

        Returns:
            SystemHealthReport with all check results
        """
        # Start with data freshness check (needs is_offline parameter)
        results = [check_data_freshness(is_offline=self._is_offline)]

        # Run other checks
        checks = list(self._checks)
        if include_connectivity:
            checks.append(check_protocol_connectivity)

        for check_func in checks:
            try:
                result = check_func()
                results.append(result)
            except Exception as e:
                logger.error(f"Health check failed: {check_func.__name__}: {e}")
                results.append(HealthCheckResult(
                    name=check_func.__name__,
                    status=HealthStatus.UNKNOWN,
                    message=f"Check failed: {e}",
                    details={"error": str(e)},
                ))

        # Determine overall status
        statuses = [r.status for r in results]
        if HealthStatus.UNHEALTHY in statuses:
            overall = HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in statuses:
            overall = HealthStatus.DEGRADED
        elif HealthStatus.UNKNOWN in statuses:
            overall = HealthStatus.DEGRADED
        else:
            overall = HealthStatus.HEALTHY

        return SystemHealthReport(
            status=overall,
            checks=results,
            metadata={
                "checks_run": len(results),
                "include_connectivity": include_connectivity,
            },
        )


def get_system_health(
    include_connectivity: bool = False,
    is_offline: bool = False
) -> Dict[str, Any]:
    """
    Quick function to get system health status.

    Args:
        include_connectivity: Include API connectivity check
        is_offline: Indicate using bundled offline data

    Returns:
        Dictionary with health status and details
    """
    checker = HealthChecker(is_offline=is_offline)
    report = checker.run_all_checks(include_connectivity=include_connectivity)
    return report.to_dict()
