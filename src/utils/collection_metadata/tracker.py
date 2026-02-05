"""
Collection metadata tracker.

Main tracker class for monitoring data collection runs.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import asdict
import logging

from src.utils.collection_metadata.models import CollectionRun

logger = logging.getLogger(__name__)

# Default paths
DEFAULT_METADATA_PATH = Path("storage/collection_metadata.json")
MAX_HISTORY_RUNS = 100  # Keep last N runs


class CollectionMetadataTracker:
    """
    Tracks collection metadata for audit trail and debugging.

    Usage:
        tracker = CollectionMetadataTracker()
        run_id = tracker.start_run(mode="incremental")

        try:
            # ... collection logic ...
            tracker.record_file_update(run_id, filename, rows, source)
            tracker.end_run(run_id, status="success")
        except Exception as e:
            tracker.record_error(run_id, str(e))
            tracker.end_run(run_id, status="failed")
    """

    def __init__(self, metadata_path: Optional[Path] = None):
        """
        Initialize the metadata tracker.

        Args:
            metadata_path: Path to the metadata JSON file
        """
        self.metadata_path = metadata_path or DEFAULT_METADATA_PATH
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        """Load existing metadata from disk."""
        if self.metadata_path.exists():
            try:
                with open(self.metadata_path, 'r') as f:
                    data = json.load(f)
                    self.runs: List[Dict] = data.get("runs", [])
                    self.files: Dict[str, Dict] = data.get("files", {})
                    self.sources: Dict[str, Dict] = data.get("sources", {})
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load metadata: {e}. Starting fresh.")
                self._init_empty()
        else:
            self._init_empty()

    def _init_empty(self) -> None:
        """Initialize empty metadata."""
        self.runs: List[Dict] = []
        self.files: Dict[str, Dict] = {}
        self.sources: Dict[str, Dict] = {}

    def _save(self) -> None:
        """Save metadata to disk."""
        # Trim history if needed
        if len(self.runs) > MAX_HISTORY_RUNS:
            self.runs = self.runs[-MAX_HISTORY_RUNS:]

        data = {
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "runs": self.runs,
            "files": self.files,
            "sources": self.sources,
        }

        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except IOError as e:
            logger.error(f"Could not save metadata: {e}")

    def start_run(
        self,
        mode: str = "incremental",
        sources: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Start a new collection run.

        Args:
            mode: Collection mode (incremental, backfill, full)
            sources: List of source names being used
            metadata: Additional metadata for the run

        Returns:
            Run ID for tracking
        """
        import uuid
        run_id = f"run-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

        run = CollectionRun(
            run_id=run_id,
            started_at=datetime.utcnow().isoformat() + "Z",
            mode=mode,
            sources_used=sources or [],
            metadata=metadata or {},
        )

        self.runs.append(asdict(run))
        self._save()

        logger.info(f"Started collection run: {run_id} (mode={mode})")
        return run_id

    def end_run(
        self,
        run_id: str,
        status: str = "success",
        summary: Optional[Dict] = None
    ) -> None:
        """
        End a collection run.

        Args:
            run_id: Run ID from start_run()
            status: Final status (success, partial, failed)
            summary: Additional summary data
        """
        run = self._find_run(run_id)
        if not run:
            logger.warning(f"Run not found: {run_id}")
            return

        completed_at = datetime.utcnow().isoformat() + "Z"
        started = datetime.fromisoformat(run["started_at"].rstrip("Z"))
        duration = (datetime.utcnow() - started).total_seconds()

        run["completed_at"] = completed_at
        run["duration_seconds"] = round(duration, 2)
        run["status"] = status

        if summary:
            run["metadata"].update(summary)

        self._save()
        logger.info(f"Completed run {run_id}: {status} in {duration:.1f}s")

    def record_file_update(
        self,
        run_id: str,
        filename: str,
        total_rows: int,
        rows_added: int = 0,
        source: str = "unknown",
        date_range: Optional[tuple] = None
    ) -> None:
        """
        Record that a file was updated.

        Args:
            run_id: Run ID
            filename: Name of the file
            total_rows: Total rows in the file
            rows_added: New rows added in this run
            source: Data source name
            date_range: Tuple of (start_date, end_date)
        """
        now = datetime.utcnow().isoformat() + "Z"

        # Update file metadata
        file_path = Path("data") / filename
        file_size = file_path.stat().st_size if file_path.exists() else 0

        self.files[filename] = {
            "filename": filename,
            "last_updated": now,
            "total_rows": total_rows,
            "rows_added": rows_added,
            "source": source,
            "file_size_bytes": file_size,
            "date_range_start": date_range[0] if date_range else None,
            "date_range_end": date_range[1] if date_range else None,
        }

        # Update run's file list
        run = self._find_run(run_id)
        if run:
            if filename not in run["files_updated"]:
                run["files_updated"].append(filename)
            run["total_rows_fetched"] += rows_added

        # Update source metadata
        if source != "unknown":
            self._update_source_success(source)

        self._save()

    def record_file_failure(
        self,
        run_id: str,
        filename: str,
        error_message: str,
        source: str = "unknown"
    ) -> None:
        """
        Record that a file update failed.

        Args:
            run_id: Run ID
            filename: Name of the file
            error_message: Error description
            source: Data source name
        """
        run = self._find_run(run_id)
        if run:
            if filename not in run["files_failed"]:
                run["files_failed"].append(filename)

            run["errors"].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "file": filename,
                "source": source,
                "message": error_message,
            })

        if source != "unknown":
            self._update_source_failure(source, error_message)

        self._save()

    def record_error(
        self,
        run_id: str,
        message: str,
        context: Optional[Dict] = None
    ) -> None:
        """
        Record a general error during collection.

        Args:
            run_id: Run ID
            message: Error message
            context: Additional context
        """
        run = self._find_run(run_id)
        if run:
            run["errors"].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "message": message,
                "context": context or {},
            })
            self._save()

        logger.error(f"Collection error in {run_id}: {message}")

    def record_warning(
        self,
        run_id: str,
        message: str,
        context: Optional[Dict] = None
    ) -> None:
        """
        Record a warning during collection.

        Args:
            run_id: Run ID
            message: Warning message
            context: Additional context
        """
        run = self._find_run(run_id)
        if run:
            run["warnings"].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "message": message,
                "context": context or {},
            })
            self._save()

        logger.warning(f"Collection warning in {run_id}: {message}")

    def get_last_run(self) -> Optional[Dict]:
        """Get the most recent collection run."""
        if self.runs:
            return self.runs[-1]
        return None

    def get_file_info(self, filename: str) -> Optional[Dict]:
        """Get metadata for a specific file."""
        return self.files.get(filename)

    def get_source_info(self, source_name: str) -> Optional[Dict]:
        """Get metadata for a specific source."""
        return self.sources.get(source_name)

    def get_last_date(self, filename: str) -> Optional[str]:
        """
        Get the last date in a file (for incremental collection).

        Args:
            filename: Name of the file

        Returns:
            ISO date string or None
        """
        file_info = self.files.get(filename)
        if file_info:
            return file_info.get("date_range_end")
        return None

    def _find_run(self, run_id: str) -> Optional[Dict]:
        """Find a run by ID."""
        for run in reversed(self.runs):
            if run["run_id"] == run_id:
                return run
        return None

    def _update_source_success(self, source_name: str) -> None:
        """Update source metadata on success."""
        now = datetime.utcnow().isoformat() + "Z"

        if source_name not in self.sources:
            self.sources[source_name] = {
                "source_name": source_name,
                "total_api_calls": 0,
            }

        source = self.sources[source_name]
        source["last_success"] = now
        source["consecutive_successes"] = source.get("consecutive_successes", 0) + 1
        source["consecutive_failures"] = 0
        source["total_api_calls"] = source.get("total_api_calls", 0) + 1

    def _update_source_failure(self, source_name: str, error_message: str) -> None:
        """Update source metadata on failure."""
        now = datetime.utcnow().isoformat() + "Z"

        if source_name not in self.sources:
            self.sources[source_name] = {
                "source_name": source_name,
                "total_api_calls": 0,
            }

        source = self.sources[source_name]
        source["last_failure"] = now
        source["consecutive_failures"] = source.get("consecutive_failures", 0) + 1
        source["consecutive_successes"] = 0
        source["last_error_message"] = error_message
        source["total_api_calls"] = source.get("total_api_calls", 0) + 1


# Singleton instance for convenience
_tracker: Optional[CollectionMetadataTracker] = None


def get_tracker() -> CollectionMetadataTracker:
    """Get the global metadata tracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = CollectionMetadataTracker()
    return _tracker
