# Collection Metadata Tracking Specification

**Document:** COLLECTION_METADATA_TRACKING_SPEC.md  
**Created:** February 4, 2026  
**Author:** Rakia Board  
**Priority:** P0 (Pre-Launch)  
**Effort:** 0.25 day

---

## 1. OVERVIEW

### 1.1 Problem Statement

Currently, there is no tracking of:
- When data was last collected
- How many records were added in each run
- Which API sources succeeded/failed
- Collection mode used (full backfill vs incremental)

This makes debugging, auditing, and monitoring difficult.

### 1.2 Solution

Implement a `collection_metadata.json` file that tracks:
- Last run timestamp
- Records added/total per file
- Run mode (backfill vs incremental)
- API source status
- Errors encountered

---

## 2. METADATA SCHEMA

### 2.1 `storage/collection_metadata.json`

```json
{
  "last_run": {
    "timestamp": "2026-02-04T10:30:00Z",
    "mode": "incremental",
    "duration_seconds": 45.2,
    "status": "success",
    "triggered_by": "daily_run.sh"
  },
  "files": {
    "crypto_prices.csv": {
      "last_updated": "2026-02-04T10:30:05Z",
      "total_rows": 4250,
      "rows_added": 1,
      "date_range": {
        "start": "2014-09-17",
        "end": "2026-02-04"
      },
      "source": "yahoo_live",
      "status": "success"
    },
    "treasury_yields.csv": {
      "last_updated": "2026-02-04T10:30:12Z",
      "total_rows": 16500,
      "rows_added": 1,
      "date_range": {
        "start": "1962-01-02",
        "end": "2026-02-03"
      },
      "source": "fred",
      "status": "success"
    },
    "defillama_historical_apy.csv": {
      "last_updated": "2026-02-04T10:30:18Z",
      "total_rows": 8200,
      "rows_added": 4,
      "date_range": {
        "start": "2022-05-01",
        "end": "2026-02-04"
      },
      "source": "defillama_live",
      "status": "success"
    }
  },
  "sources": {
    "fred": {
      "last_success": "2026-02-04T10:30:12Z",
      "last_failure": null,
      "consecutive_successes": 45,
      "consecutive_failures": 0,
      "api_calls_today": 12,
      "rate_limit_remaining": 108
    },
    "yahoo_live": {
      "last_success": "2026-02-04T10:30:05Z",
      "last_failure": null,
      "consecutive_successes": 45,
      "consecutive_failures": 0,
      "api_calls_today": 25,
      "rate_limit_remaining": null
    },
    "defillama_live": {
      "last_success": "2026-02-04T10:30:18Z",
      "last_failure": "2026-02-01T10:30:00Z",
      "consecutive_successes": 3,
      "consecutive_failures": 0,
      "api_calls_today": 8,
      "rate_limit_remaining": 52
    }
  },
  "errors": [],
  "warnings": [
    {
      "timestamp": "2026-02-04T10:30:15Z",
      "source": "yahoo_live",
      "file": "tradfi_benchmark_data.csv",
      "message": "TradFi markets closed - no new data for SPY, QQQ",
      "severity": "info"
    }
  ],
  "history": [
    {
      "timestamp": "2026-02-04T10:30:00Z",
      "mode": "incremental",
      "files_updated": 8,
      "total_rows_added": 15,
      "status": "success"
    },
    {
      "timestamp": "2026-02-03T10:30:00Z",
      "mode": "incremental",
      "files_updated": 8,
      "total_rows_added": 18,
      "status": "success"
    }
  ]
}
```

---

## 3. IMPLEMENTATION

### 3.1 New Module: `src/utils/collection_metadata.py`

```python
"""
Collection Metadata Tracker.

Tracks data collection runs, API status, and file updates.
Stores metadata in storage/collection_metadata.json.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import pandas as pd

logger = logging.getLogger(__name__)

METADATA_FILE = Path("storage/collection_metadata.json")
MAX_HISTORY_ENTRIES = 30  # Keep last 30 runs


@dataclass
class FileMetadata:
    """Metadata for a single data file."""
    last_updated: str
    total_rows: int
    rows_added: int
    date_range: Dict[str, str]
    source: str
    status: str


@dataclass
class SourceMetadata:
    """Metadata for an API source."""
    last_success: Optional[str]
    last_failure: Optional[str]
    consecutive_successes: int
    consecutive_failures: int
    api_calls_today: int
    rate_limit_remaining: Optional[int]


@dataclass
class RunMetadata:
    """Metadata for a collection run."""
    timestamp: str
    mode: str
    duration_seconds: float
    status: str
    triggered_by: str


class CollectionMetadataTracker:
    """
    Track collection metadata across runs.
    
    Usage:
        tracker = CollectionMetadataTracker()
        tracker.start_run(mode="incremental", triggered_by="daily_run.sh")
        
        # After collecting each file
        tracker.record_file_update(
            filename="crypto_prices.csv",
            rows_added=1,
            total_rows=4250,
            source="yahoo_live",
            date_range={"start": "2014-09-17", "end": "2026-02-04"}
        )
        
        # Record any errors
        tracker.record_error(
            source="defillama_live",
            message="Rate limit exceeded",
            file="defillama_historical_apy.csv"
        )
        
        # End run
        tracker.end_run(status="success")
    """
    
    def __init__(self, metadata_file: Path = METADATA_FILE):
        self.metadata_file = metadata_file
        self.metadata = self._load_or_create()
        self._run_start_time: Optional[datetime] = None
        self._current_run: Optional[Dict] = None
    
    def _load_or_create(self) -> Dict:
        """Load existing metadata or create new."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Corrupted metadata file, creating new")
        
        return {
            "last_run": None,
            "files": {},
            "sources": {},
            "errors": [],
            "warnings": [],
            "history": []
        }
    
    def _save(self):
        """Save metadata to file."""
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2, default=str)
    
    def start_run(self, mode: str = "incremental", triggered_by: str = "manual"):
        """
        Start tracking a new collection run.
        
        Args:
            mode: "incremental" or "backfill"
            triggered_by: What triggered this run (e.g., "daily_run.sh", "manual")
        """
        self._run_start_time = datetime.now(timezone.utc)
        self._current_run = {
            "mode": mode,
            "triggered_by": triggered_by,
            "files_updated": 0,
            "total_rows_added": 0
        }
        
        # Clear errors/warnings for new run
        self.metadata["errors"] = []
        self.metadata["warnings"] = []
        
        logger.info(f"Started collection run: mode={mode}, triggered_by={triggered_by}")
    
    def record_file_update(
        self,
        filename: str,
        rows_added: int,
        total_rows: int,
        source: str,
        date_range: Dict[str, str],
        status: str = "success"
    ):
        """
        Record metadata for a file update.
        
        Args:
            filename: Name of the CSV file
            rows_added: Number of new rows added
            total_rows: Total rows in file after update
            source: API source used (e.g., "fred", "yahoo_live")
            date_range: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
            status: "success" or "failed"
        """
        now = datetime.now(timezone.utc).isoformat()
        
        self.metadata["files"][filename] = {
            "last_updated": now,
            "total_rows": total_rows,
            "rows_added": rows_added,
            "date_range": date_range,
            "source": source,
            "status": status
        }
        
        # Update current run stats
        if self._current_run:
            self._current_run["files_updated"] += 1
            self._current_run["total_rows_added"] += rows_added
        
        # Update source stats
        self._update_source_stats(source, success=(status == "success"))
        
        logger.info(
            f"Recorded update: {filename} - "
            f"+{rows_added} rows, total={total_rows}, source={source}"
        )
    
    def _update_source_stats(self, source: str, success: bool):
        """Update API source statistics."""
        now = datetime.now(timezone.utc).isoformat()
        
        if source not in self.metadata["sources"]:
            self.metadata["sources"][source] = {
                "last_success": None,
                "last_failure": None,
                "consecutive_successes": 0,
                "consecutive_failures": 0,
                "api_calls_today": 0,
                "rate_limit_remaining": None
            }
        
        stats = self.metadata["sources"][source]
        stats["api_calls_today"] = stats.get("api_calls_today", 0) + 1
        
        if success:
            stats["last_success"] = now
            stats["consecutive_successes"] = stats.get("consecutive_successes", 0) + 1
            stats["consecutive_failures"] = 0
        else:
            stats["last_failure"] = now
            stats["consecutive_failures"] = stats.get("consecutive_failures", 0) + 1
            stats["consecutive_successes"] = 0
    
    def record_error(
        self,
        source: str,
        message: str,
        file: Optional[str] = None
    ):
        """Record an error during collection."""
        self.metadata["errors"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "file": file,
            "message": message,
            "severity": "error"
        })
        
        self._update_source_stats(source, success=False)
        logger.error(f"Collection error: {source} - {message}")
    
    def record_warning(
        self,
        source: str,
        message: str,
        file: Optional[str] = None,
        severity: str = "warning"
    ):
        """Record a warning during collection."""
        self.metadata["warnings"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "file": file,
            "message": message,
            "severity": severity
        })
        
        logger.warning(f"Collection warning: {source} - {message}")
    
    def end_run(self, status: str = "success"):
        """
        End the current collection run and save metadata.
        
        Args:
            status: "success", "partial", or "failed"
        """
        if not self._run_start_time or not self._current_run:
            logger.warning("end_run called without start_run")
            return
        
        now = datetime.now(timezone.utc)
        duration = (now - self._run_start_time).total_seconds()
        
        # Update last_run
        self.metadata["last_run"] = {
            "timestamp": self._run_start_time.isoformat(),
            "mode": self._current_run["mode"],
            "duration_seconds": round(duration, 2),
            "status": status,
            "triggered_by": self._current_run["triggered_by"]
        }
        
        # Add to history
        history_entry = {
            "timestamp": self._run_start_time.isoformat(),
            "mode": self._current_run["mode"],
            "files_updated": self._current_run["files_updated"],
            "total_rows_added": self._current_run["total_rows_added"],
            "status": status
        }
        
        self.metadata["history"].insert(0, history_entry)
        
        # Trim history to max entries
        self.metadata["history"] = self.metadata["history"][:MAX_HISTORY_ENTRIES]
        
        # Save to file
        self._save()
        
        logger.info(
            f"Collection run complete: status={status}, "
            f"duration={duration:.1f}s, "
            f"files={self._current_run['files_updated']}, "
            f"rows_added={self._current_run['total_rows_added']}"
        )
        
        # Reset run state
        self._run_start_time = None
        self._current_run = None
    
    def get_file_info(self, filename: str) -> Optional[Dict]:
        """Get metadata for a specific file."""
        return self.metadata["files"].get(filename)
    
    def get_source_info(self, source: str) -> Optional[Dict]:
        """Get metadata for a specific API source."""
        return self.metadata["sources"].get(source)
    
    def get_last_run(self) -> Optional[Dict]:
        """Get metadata for the last collection run."""
        return self.metadata.get("last_run")
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict]:
        """Get recent errors."""
        return self.metadata.get("errors", [])[:limit]
    
    def get_summary(self) -> Dict:
        """Get a summary of collection status."""
        last_run = self.metadata.get("last_run")
        files = self.metadata.get("files", {})
        sources = self.metadata.get("sources", {})
        
        return {
            "last_run": last_run,
            "total_files": len(files),
            "total_sources": len(sources),
            "recent_errors": len(self.metadata.get("errors", [])),
            "recent_warnings": len(self.metadata.get("warnings", [])),
            "files_summary": {
                name: {
                    "rows": info.get("total_rows"),
                    "last_updated": info.get("last_updated")
                }
                for name, info in files.items()
            }
        }


# Global instance for easy access
_tracker: Optional[CollectionMetadataTracker] = None


def get_tracker() -> CollectionMetadataTracker:
    """Get or create the global metadata tracker."""
    global _tracker
    if _tracker is None:
        _tracker = CollectionMetadataTracker()
    return _tracker
```

### 3.2 Integration with Collectors

```python
# In src/commands/collect.py

from src.utils.collection_metadata import get_tracker

def run_collect(args):
    """Execute data collection with metadata tracking."""
    tracker = get_tracker()
    
    # Determine mode
    mode = "incremental" if getattr(args, 'append', False) else "backfill"
    triggered_by = "cli" if not os.getenv("GITHUB_ACTIONS") else "github_actions"
    
    # Start tracking
    tracker.start_run(mode=mode, triggered_by=triggered_by)
    
    try:
        # ... existing collection logic ...
        
        # After each file is saved:
        tracker.record_file_update(
            filename="crypto_prices.csv",
            rows_added=rows_added,
            total_rows=len(df),
            source="yahoo_live",
            date_range={
                "start": str(df['date'].min().date()),
                "end": str(df['date'].max().date())
            }
        )
        
        # End run
        tracker.end_run(status="success")
        
    except Exception as e:
        tracker.record_error(source="aggregator", message=str(e))
        tracker.end_run(status="failed")
        raise
```

---

## 4. CLI COMMANDS

### 4.1 View Collection Status

```bash
# Add new command: python main.py collection-status
python main.py collection-status

# Output:
# Collection Status
# ================
# Last Run: 2026-02-04T10:30:00Z (incremental, success)
# Duration: 45.2s
# Files Updated: 8
# Rows Added: 15
#
# Files:
#   crypto_prices.csv: 4,250 rows (2014-09-17 to 2026-02-04)
#   treasury_yields.csv: 16,500 rows (1962-01-02 to 2026-02-03)
#   ...
#
# API Sources:
#   fred: OK (45 consecutive successes)
#   yahoo_live: OK (45 consecutive successes)
#   defillama_live: OK (3 consecutive successes)
```

---

## 5. VERIFICATION CHECKLIST

| # | Item | Expected | Pass? |
|---|------|----------|-------|
| 1 | `collection_metadata.py` created | File exists | ☐ |
| 2 | `storage/collection_metadata.json` created after run | File exists | ☐ |
| 3 | Metadata tracks last run timestamp | Correct timestamp | ☐ |
| 4 | Metadata tracks rows_added per file | Correct counts | ☐ |
| 5 | Metadata tracks source status | Success/failure tracked | ☐ |
| 6 | History limited to 30 entries | Max 30 items | ☐ |
| 7 | `collection-status` command works | Shows summary | ☐ |

---

*Specification created by Rakia Board for collection metadata tracking*
