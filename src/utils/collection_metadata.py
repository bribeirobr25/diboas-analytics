"""
Collection Metadata Tracking for diBoaS Analytics.

Tracks all data collection runs for audit trail and debugging.

Implementation based on: docs/all_boards/Rakia/COLLECTION_METADATA_TRACKING_SPEC.md

Note: This module has been refactored into the collection_metadata/ package.
This file provides backward compatibility for existing imports.

Usage:
    from src.utils.collection_metadata import CollectionMetadataTracker, get_tracker

    tracker = get_tracker()
    run_id = tracker.start_run(mode="incremental")
"""

# Re-export all public symbols from the new package structure
from src.utils.collection_metadata import (
    # Models
    FileMetadata,
    SourceMetadata,
    CollectionRun,
    # Tracker
    CollectionMetadataTracker,
    get_tracker,
    DEFAULT_METADATA_PATH,
    MAX_HISTORY_RUNS,
)

__all__ = [
    # Models
    'FileMetadata',
    'SourceMetadata',
    'CollectionRun',
    # Tracker
    'CollectionMetadataTracker',
    'get_tracker',
    'DEFAULT_METADATA_PATH',
    'MAX_HISTORY_RUNS',
]
