"""
Adelaide edition tracker.

Tracks edition numbers for spot-check requirement.
First N editions require CLO human review.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AdelaideEditionTracker:
    """
    Track Adelaide newsletter edition numbers.

    Used to enforce spot-check requirement for first N editions.
    Uses file-based storage ($0 budget constraint).
    """

    def __init__(self, state_file: str = "data/adelaide_state.json"):
        """
        Initialize tracker with state file.

        Args:
            state_file: Path to state file
        """
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        """Load state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    self.state = json.load(f)
                logger.debug(f"Loaded edition state from {self.state_file}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load edition state: {e}")
                self._init_state()
        else:
            self._init_state()

    def _init_state(self) -> None:
        """Initialize empty state."""
        self.state = {
            "next_edition": 1,
            "editions": [],
            "created_at": datetime.utcnow().isoformat(),
        }

    def _save(self) -> None:
        """Save state to file."""
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.state, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save edition state: {e}")

    def get_next_edition_number(self) -> int:
        """
        Get the next edition number.

        Returns:
            Next edition number (1-indexed)
        """
        return self.state["next_edition"]

    def record_edition(
        self,
        edition_type: str = "daily",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Record a new edition.

        Args:
            edition_type: Type of edition (daily, weekly, special)
            metadata: Optional metadata

        Returns:
            Edition number that was recorded
        """
        num = self.state["next_edition"]

        edition_record = {
            "number": num,
            "type": edition_type,
            "created_at": datetime.utcnow().isoformat(),
        }
        if metadata:
            edition_record["metadata"] = metadata

        self.state["editions"].append(edition_record)
        self.state["next_edition"] += 1
        self._save()

        logger.info(f"Recorded Adelaide edition #{num} ({edition_type})")
        return num

    def requires_spot_check(self, first_n: int = 20) -> bool:
        """
        Check if next edition requires spot-check.

        Args:
            first_n: Number of first editions requiring spot-check

        Returns:
            True if spot-check required, False otherwise
        """
        return self.get_next_edition_number() <= first_n

    def get_edition_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent edition history.

        Args:
            limit: Maximum editions to return

        Returns:
            List of recent editions
        """
        editions = self.state.get("editions", [])
        return list(reversed(editions[-limit:]))

    def get_stats(self) -> Dict[str, Any]:
        """
        Get edition statistics.

        Returns:
            Dict with edition stats
        """
        editions = self.state.get("editions", [])

        by_type = {}
        for edition in editions:
            t = edition.get("type", "unknown")
            by_type[t] = by_type.get(t, 0) + 1

        return {
            "total_editions": len(editions),
            "next_edition": self.state["next_edition"],
            "by_type": by_type,
            "created_at": self.state.get("created_at"),
            "last_edition": editions[-1] if editions else None,
        }

    def reset(self) -> None:
        """
        Reset edition counter.

        WARNING: This is destructive. Only use for testing.
        """
        logger.warning("Resetting Adelaide edition tracker")
        self._init_state()
        self._save()
