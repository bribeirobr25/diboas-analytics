"""
Collection metadata data models.

Contains data classes for tracking collection runs.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class FileMetadata:
    """Metadata for a single data file."""
    filename: str
    last_updated: str  # ISO 8601 timestamp
    total_rows: int
    rows_added: int = 0
    date_range_start: Optional[str] = None
    date_range_end: Optional[str] = None
    source: str = "unknown"
    file_size_bytes: int = 0
    checksum: Optional[str] = None


@dataclass
class SourceMetadata:
    """Metadata for a data source (API/collector)."""
    source_name: str
    last_success: Optional[str] = None  # ISO 8601 timestamp
    last_failure: Optional[str] = None
    consecutive_successes: int = 0
    consecutive_failures: int = 0
    total_api_calls: int = 0
    last_error_message: Optional[str] = None


@dataclass
class CollectionRun:
    """Metadata for a single collection run."""
    run_id: str
    started_at: str  # ISO 8601 timestamp
    completed_at: Optional[str] = None
    mode: str = "incremental"  # "incremental", "backfill", "full"
    duration_seconds: Optional[float] = None
    status: str = "running"  # "running", "success", "partial", "failed"
    files_updated: List[str] = field(default_factory=list)
    files_failed: List[str] = field(default_factory=list)
    sources_used: List[str] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    total_rows_fetched: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
