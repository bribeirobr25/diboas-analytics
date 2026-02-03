"""Tests for cooldown manager."""

import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

from src.triggers.intelligence_cooldown_manager import IntelligenceCooldownManager


class TestCooldownManager:
    """Tests for IntelligenceCooldownManager."""

    @pytest.fixture
    def temp_state_file(self):
        """Create temporary state file."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            return f.name

    @pytest.fixture
    def manager(self, temp_state_file):
        """Create cooldown manager with temp file."""
        return IntelligenceCooldownManager(
            default_cooldown_minutes=60,
            state_file=temp_state_file
        )

    def test_should_not_be_on_cooldown_initially(self, manager):
        """New trigger is not on cooldown."""
        assert manager.is_on_cooldown("TEST-001") is False

    def test_should_be_on_cooldown_after_set(self, manager):
        """Trigger is on cooldown after set_cooldown."""
        manager.set_cooldown("TEST-001")
        assert manager.is_on_cooldown("TEST-001") is True

    def test_should_not_be_on_cooldown_for_different_trigger(self, manager):
        """Different trigger is not affected."""
        manager.set_cooldown("TEST-001")
        assert manager.is_on_cooldown("TEST-002") is False

    def test_should_clear_cooldown(self, manager):
        """Cooldown can be cleared."""
        manager.set_cooldown("TEST-001")
        assert manager.is_on_cooldown("TEST-001") is True
        manager.clear_cooldown("TEST-001")
        assert manager.is_on_cooldown("TEST-001") is False

    def test_should_return_false_for_clear_nonexistent(self, manager):
        """Clear returns False for nonexistent cooldown."""
        result = manager.clear_cooldown("NONEXISTENT")
        assert result is False

    def test_should_persist_state_to_file(self, temp_state_file):
        """State is persisted to file."""
        manager1 = IntelligenceCooldownManager(state_file=temp_state_file)
        manager1.set_cooldown("TEST-001", minutes=120)

        # Create new manager with same file
        manager2 = IntelligenceCooldownManager(state_file=temp_state_file)
        assert manager2.is_on_cooldown("TEST-001") is True

    def test_should_use_custom_cooldown_minutes(self, manager):
        """Custom cooldown duration works."""
        manager.set_cooldown("TEST-001", minutes=1)
        remaining = manager.get_remaining_minutes("TEST-001")
        assert remaining is not None
        assert remaining <= 1

    def test_should_return_none_remaining_when_not_on_cooldown(self, manager):
        """get_remaining_minutes returns None when not on cooldown."""
        remaining = manager.get_remaining_minutes("TEST-001")
        assert remaining is None

    def test_should_cleanup_expired_cooldowns(self, temp_state_file):
        """Expired cooldowns are cleaned up."""
        manager = IntelligenceCooldownManager(state_file=temp_state_file)

        # Manually set an expired cooldown
        expired_time = (datetime.utcnow() - timedelta(hours=1)).isoformat()
        manager.cooldowns["EXPIRED-001"] = expired_time
        manager._save_state()

        # Also set a valid cooldown
        manager.set_cooldown("VALID-001")

        removed = manager.cleanup_expired()
        assert removed == 1
        assert "EXPIRED-001" not in manager.cooldowns
        assert "VALID-001" in manager.cooldowns

    def test_should_handle_invalid_state_file(self, temp_state_file):
        """Invalid state file is handled gracefully."""
        # Write invalid JSON
        with open(temp_state_file, 'w') as f:
            f.write("invalid json{")

        manager = IntelligenceCooldownManager(state_file=temp_state_file)
        assert manager.cooldowns == {}  # Should initialize empty

    def test_should_create_parent_directories(self):
        """Parent directories are created if needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "subdir" / "cooldowns.json"
            manager = IntelligenceCooldownManager(state_file=str(state_file))
            manager.set_cooldown("TEST-001")
            assert state_file.exists()
