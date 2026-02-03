"""
Cooldown manager to prevent trigger spam.

Uses file-based storage ($0 budget constraint).
Can be replaced with Redis/PostgreSQL in Phase 2+.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class IntelligenceCooldownManager:
    """
    Manage trigger cooldowns to prevent alert spam.

    When a trigger fires, it enters cooldown and cannot fire again
    until the cooldown period expires. Default is 60 minutes.

    Storage: File-based JSON (data/trigger_cooldowns.json)
    """

    def __init__(
        self,
        default_cooldown_minutes: int = 60,
        state_file: str = "data/trigger_cooldowns.json",
    ):
        """
        Initialize cooldown manager.

        Args:
            default_cooldown_minutes: Default cooldown period
            state_file: Path to state persistence file
        """
        self.default_cooldown_minutes = default_cooldown_minutes
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.cooldowns: Dict[str, str] = {}
        self._load_state()

    def _load_state(self) -> None:
        """Load cooldown state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    self.cooldowns = json.load(f)
                logger.debug(f"Loaded {len(self.cooldowns)} cooldowns from {self.state_file}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load cooldown state: {e}")
                self.cooldowns = {}
        else:
            self.cooldowns = {}

    def _save_state(self) -> None:
        """Save cooldown state to file."""
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.cooldowns, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save cooldown state: {e}")

    def is_on_cooldown(self, trigger_id: str) -> bool:
        """
        Check if a trigger is currently on cooldown.

        Args:
            trigger_id: Unique trigger identifier

        Returns:
            True if on cooldown, False otherwise
        """
        if trigger_id not in self.cooldowns:
            return False

        try:
            expires_at = datetime.fromisoformat(self.cooldowns[trigger_id])
            return datetime.utcnow() < expires_at
        except (ValueError, TypeError):
            # Invalid timestamp, remove it
            del self.cooldowns[trigger_id]
            self._save_state()
            return False

    def set_cooldown(self, trigger_id: str, minutes: Optional[int] = None) -> None:
        """
        Set cooldown for a trigger.

        Args:
            trigger_id: Unique trigger identifier
            minutes: Cooldown duration (uses default if None)
        """
        minutes = minutes or self.default_cooldown_minutes
        expires_at = datetime.utcnow() + timedelta(minutes=minutes)
        self.cooldowns[trigger_id] = expires_at.isoformat()
        self._save_state()
        logger.debug(f"Set cooldown for {trigger_id}: {minutes} minutes")

    def clear_cooldown(self, trigger_id: str) -> bool:
        """
        Clear cooldown for a trigger.

        Args:
            trigger_id: Unique trigger identifier

        Returns:
            True if cooldown was cleared, False if not found
        """
        if trigger_id in self.cooldowns:
            del self.cooldowns[trigger_id]
            self._save_state()
            logger.debug(f"Cleared cooldown for {trigger_id}")
            return True
        return False

    def get_remaining_minutes(self, trigger_id: str) -> Optional[int]:
        """
        Get remaining cooldown time in minutes.

        Args:
            trigger_id: Unique trigger identifier

        Returns:
            Minutes remaining, or None if not on cooldown
        """
        if trigger_id not in self.cooldowns:
            return None

        try:
            expires_at = datetime.fromisoformat(self.cooldowns[trigger_id])
            remaining = expires_at - datetime.utcnow()
            if remaining.total_seconds() > 0:
                return int(remaining.total_seconds() / 60)
            return None
        except (ValueError, TypeError):
            return None

    def cleanup_expired(self) -> int:
        """
        Remove expired cooldowns from state.

        Returns:
            Number of cooldowns removed
        """
        now = datetime.utcnow()
        expired = []

        for trigger_id, expires_str in self.cooldowns.items():
            try:
                expires_at = datetime.fromisoformat(expires_str)
                if now >= expires_at:
                    expired.append(trigger_id)
            except (ValueError, TypeError):
                expired.append(trigger_id)

        for trigger_id in expired:
            del self.cooldowns[trigger_id]

        if expired:
            self._save_state()
            logger.info(f"Cleaned up {len(expired)} expired cooldowns")

        return len(expired)
