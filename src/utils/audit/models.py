"""
Audit data models.

Contains data classes for audit records.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict


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
