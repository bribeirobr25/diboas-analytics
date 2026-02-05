"""
Collection Metadata Tracking for diBoaS Analytics.

Tracks all data collection runs for audit trail and debugging.

Implementation based on: docs/all_boards/Rakia/COLLECTION_METADATA_TRACKING_SPEC.md
"""

from src.utils.collection_metadata.models import (
    FileMetadata,
    SourceMetadata,
    CollectionRun,
)
from src.utils.collection_metadata.tracker import (
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
