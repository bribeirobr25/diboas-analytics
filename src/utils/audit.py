"""
Audit trail utilities for regulatory compliance.

Provides structured audit logging, data checksums, and
execution tracking for CLO/regulatory requirements.
"""

import json
import hashlib
import platform
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
import logging

from config.settings import OUTPUT_DIR
from src.utils.file_io import safe_write_json

logger = logging.getLogger(__name__)


@dataclass
class DataChecksum:
    """Checksum for a data file."""
    filepath: str
    filename: str
    checksum: str
    algorithm: str
    size_bytes: int
    last_modified: str
    record_count: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExecutionContext:
    """Context information for an execution."""
    run_id: str
    command: str
    timestamp: str
    user: str
    hostname: str
    python_version: str
    platform: str
    working_directory: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditEvent:
    """A single audit event."""
    event_id: str
    event_type: str
    timestamp: str
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    severity: str = 'info'  # info, warning, error, critical
    run_id: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditReport:
    """Complete audit report for an execution."""
    report_id: str
    generated_at: str
    execution_context: ExecutionContext
    input_checksums: List[DataChecksum]
    output_checksums: List[DataChecksum]
    events: List[AuditEvent]
    validation_summary: Dict[str, Any]
    duration_seconds: float
    status: str  # success, partial, failed

    def to_dict(self) -> dict:
        return {
            'report_id': self.report_id,
            'generated_at': self.generated_at,
            'execution_context': self.execution_context.to_dict(),
            'input_checksums': [c.to_dict() for c in self.input_checksums],
            'output_checksums': [c.to_dict() for c in self.output_checksums],
            'events': [e.to_dict() for e in self.events],
            'validation_summary': self.validation_summary,
            'duration_seconds': self.duration_seconds,
            'status': self.status
        }


def generate_checksum(filepath: Path, algorithm: str = 'sha256') -> str:
    """
    Generate checksum for a file.

    Args:
        filepath: Path to file
        algorithm: Hash algorithm (sha256, md5)

    Returns:
        Hex digest of file hash
    """
    hash_func = hashlib.new(algorithm)

    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def count_records(filepath: Path) -> Optional[int]:
    """
    Count records in a data file.

    Args:
        filepath: Path to file

    Returns:
        Number of records or None if not countable
    """
    suffix = filepath.suffix.lower()

    try:
        if suffix == '.csv':
            with open(filepath, 'r') as f:
                return sum(1 for _ in f) - 1  # Subtract header
        elif suffix == '.json':
            with open(filepath, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return len(data)
                elif isinstance(data, dict) and 'results' in data:
                    return len(data['results'])
        return None
    except Exception:
        return None


def create_data_checksum(filepath: Path) -> DataChecksum:
    """
    Create checksum record for a data file.

    Args:
        filepath: Path to file

    Returns:
        DataChecksum object
    """
    stat = filepath.stat()

    return DataChecksum(
        filepath=str(filepath.absolute()),
        filename=filepath.name,
        checksum=generate_checksum(filepath),
        algorithm='sha256',
        size_bytes=stat.st_size,
        last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
        record_count=count_records(filepath)
    )


class AuditTrail:
    """
    Audit trail manager for regulatory compliance.

    Tracks all operations, data inputs/outputs, and generates
    structured audit reports.
    """

    def __init__(self, run_id: str = None, command: str = 'unknown'):
        """
        Initialize audit trail.

        Args:
            run_id: Unique run identifier
            command: CLI command being executed
        """
        from src.utils.hashing import generate_run_id

        self.run_id = run_id or generate_run_id('audit')
        self.command = command
        self.start_time = datetime.utcnow()
        self.events: List[AuditEvent] = []
        self.input_checksums: List[DataChecksum] = []
        self.output_checksums: List[DataChecksum] = []
        self.validation_results: Dict[str, Any] = {}
        self.parameters: Dict[str, Any] = {}
        self._event_counter = 0

    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        self._event_counter += 1
        return f"{self.run_id}-evt-{self._event_counter:04d}"

    def set_parameters(self, params: Dict[str, Any]):
        """Set execution parameters for audit."""
        self.parameters = {k: str(v) for k, v in params.items()}
        self.log_event('parameters_set', 'Execution parameters configured', params)

    def log_event(
        self,
        event_type: str,
        description: str,
        details: Dict[str, Any] = None,
        severity: str = 'info'
    ):
        """
        Log an audit event.

        Args:
            event_type: Type of event (e.g., 'data_load', 'validation')
            description: Human-readable description
            details: Additional details
            severity: Event severity
        """
        event = AuditEvent(
            event_id=self._generate_event_id(),
            event_type=event_type,
            timestamp=datetime.utcnow().isoformat(),
            description=description,
            details=details or {},
            severity=severity,
            run_id=self.run_id
        )

        self.events.append(event)

        # Also log to standard logger
        log_func = getattr(logger, severity, logger.info)
        log_func(f"[AUDIT:{event_type}] {description}")

    def log_input_file(self, filepath: Path):
        """
        Log an input file with checksum.

        Args:
            filepath: Path to input file
        """
        if not filepath.exists():
            self.log_event(
                'input_file_missing',
                f"Input file not found: {filepath}",
                {'filepath': str(filepath)},
                severity='warning'
            )
            return

        checksum = create_data_checksum(filepath)
        self.input_checksums.append(checksum)

        self.log_event(
            'input_file_loaded',
            f"Loaded input file: {filepath.name}",
            {
                'filepath': str(filepath),
                'checksum': checksum.checksum[:12],
                'records': checksum.record_count
            }
        )

    def log_output_file(self, filepath: Path):
        """
        Log an output file with checksum.

        Args:
            filepath: Path to output file
        """
        if not filepath.exists():
            self.log_event(
                'output_file_missing',
                f"Output file not created: {filepath}",
                {'filepath': str(filepath)},
                severity='error'
            )
            return

        checksum = create_data_checksum(filepath)
        self.output_checksums.append(checksum)

        self.log_event(
            'output_file_created',
            f"Created output file: {filepath.name}",
            {
                'filepath': str(filepath),
                'checksum': checksum.checksum[:12],
                'records': checksum.record_count
            }
        )

    def log_validation_result(self, rule_id: str, passed: bool, details: Dict = None):
        """
        Log a validation result.

        Args:
            rule_id: Validation rule ID (e.g., 'CV-01')
            passed: Whether validation passed
            details: Additional details
        """
        self.validation_results[rule_id] = {
            'passed': passed,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        }

        severity = 'info' if passed else 'warning'
        status = 'PASSED' if passed else 'FAILED'

        self.log_event(
            'validation',
            f"Validation {rule_id}: {status}",
            {'rule_id': rule_id, 'passed': passed, **(details or {})},
            severity=severity
        )

    def log_error(self, error: Exception, context: str = ''):
        """
        Log an error.

        Args:
            error: The exception
            context: Context where error occurred
        """
        self.log_event(
            'error',
            f"Error: {error}",
            {
                'error_type': type(error).__name__,
                'error_message': str(error),
                'context': context
            },
            severity='error'
        )

    def get_execution_context(self) -> ExecutionContext:
        """Get execution context information."""
        import sys

        return ExecutionContext(
            run_id=self.run_id,
            command=self.command,
            timestamp=self.start_time.isoformat(),
            user=os.environ.get('USER', os.environ.get('USERNAME', 'unknown')),
            hostname=platform.node(),
            python_version=sys.version.split()[0],
            platform=f"{platform.system()} {platform.release()}",
            working_directory=os.getcwd(),
            parameters=self.parameters
        )

    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of validation results."""
        total = len(self.validation_results)
        passed = sum(1 for r in self.validation_results.values() if r['passed'])
        failed = total - passed

        return {
            'total_rules': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'status': 'PASSED' if failed == 0 else 'FAILED',
            'results': self.validation_results
        }

    def generate_report(self) -> AuditReport:
        """
        Generate complete audit report.

        Returns:
            AuditReport object
        """
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()

        # Determine overall status
        has_errors = any(e.severity == 'error' for e in self.events)
        has_validation_failures = any(
            not r['passed'] for r in self.validation_results.values()
        )

        if has_errors:
            status = 'failed'
        elif has_validation_failures:
            status = 'partial'
        else:
            status = 'success'

        return AuditReport(
            report_id=f"{self.run_id}-report",
            generated_at=end_time.isoformat(),
            execution_context=self.get_execution_context(),
            input_checksums=self.input_checksums,
            output_checksums=self.output_checksums,
            events=self.events,
            validation_summary=self.get_validation_summary(),
            duration_seconds=round(duration, 2),
            status=status
        )

    def save_report(self, output_dir: Path = None) -> Path:
        """
        Save audit report to JSON file.

        Args:
            output_dir: Output directory (default: outputs/)

        Returns:
            Path to saved report
        """
        output_dir = output_dir or OUTPUT_DIR
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        report = self.generate_report()
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"audit_report_{timestamp}_{self.run_id[:8]}.json"
        filepath = output_dir / filename

        safe_write_json(report.to_dict(), filepath)

        logger.info(f"Audit report saved to: {filepath}")
        return filepath

    def print_summary(self):
        """Print audit summary to console."""
        report = self.generate_report()

        print("\n" + "=" * 50)
        print("AUDIT SUMMARY")
        print("=" * 50)
        print(f"Run ID: {self.run_id}")
        print(f"Command: {self.command}")
        print(f"Duration: {report.duration_seconds:.2f}s")
        print(f"Status: {report.status.upper()}")
        print()
        print(f"Input files: {len(self.input_checksums)}")
        print(f"Output files: {len(self.output_checksums)}")
        print(f"Events logged: {len(self.events)}")
        print()

        validation = report.validation_summary
        if validation['total_rules'] > 0:
            print(f"Validation: {validation['passed']}/{validation['total_rules']} passed")
            print(f"Pass rate: {validation['pass_rate']:.1f}%")

        print("=" * 50)


# Global audit trail instance (can be replaced per execution)
_current_audit: Optional[AuditTrail] = None


def get_audit_trail() -> Optional[AuditTrail]:
    """Get current audit trail instance."""
    return _current_audit


def set_audit_trail(audit: AuditTrail):
    """Set current audit trail instance."""
    global _current_audit
    _current_audit = audit


def create_audit_trail(run_id: str = None, command: str = 'unknown') -> AuditTrail:
    """
    Create and set a new audit trail.

    Args:
        run_id: Optional run ID
        command: CLI command

    Returns:
        New AuditTrail instance
    """
    audit = AuditTrail(run_id=run_id, command=command)
    set_audit_trail(audit)
    return audit
