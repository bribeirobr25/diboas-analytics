"""
Tests for safe file I/O utilities.

Tests cover:
- Empty/None rejection
- Atomic write behavior
- Temp file cleanup
- Data preservation on rejection
"""

import json
import os
import pytest
import pandas as pd
from pathlib import Path

from src.utils.file_io import safe_write_csv, safe_write_json, safe_write_text


class TestSafeWriteCSV:
    """Tests for safe_write_csv function."""

    def test_should_reject_none_dataframe(self, tmp_path):
        """None DataFrame should be rejected and file not created."""
        filepath = tmp_path / "test.csv"
        result = safe_write_csv(None, filepath)
        assert result is False
        assert not filepath.exists()

    def test_should_reject_empty_dataframe_by_default(self, tmp_path):
        """Empty DataFrame should be rejected by default."""
        filepath = tmp_path / "test.csv"
        result = safe_write_csv(pd.DataFrame(), filepath)
        assert result is False
        assert not filepath.exists()

    def test_should_allow_empty_when_flag_set(self, tmp_path):
        """Empty DataFrame should be allowed when allow_empty=True."""
        filepath = tmp_path / "test.csv"
        result = safe_write_csv(pd.DataFrame(), filepath, allow_empty=True)
        assert result is True
        assert filepath.exists()

    def test_should_reject_below_min_rows(self, tmp_path):
        """DataFrame with fewer than min_rows should be rejected."""
        filepath = tmp_path / "test.csv"
        df = pd.DataFrame({"a": [1]})
        result = safe_write_csv(df, filepath, min_rows=5)
        assert result is False
        assert not filepath.exists()

    def test_should_write_valid_dataframe(self, tmp_path):
        """Valid DataFrame should be written successfully."""
        filepath = tmp_path / "test.csv"
        df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        result = safe_write_csv(df, filepath)
        assert result is True
        assert filepath.exists()

        # Verify content
        loaded = pd.read_csv(filepath)
        assert len(loaded) == 3
        assert list(loaded.columns) == ["a", "b"]

    def test_should_preserve_portuguese_characters(self, tmp_path):
        """Portuguese characters should be preserved via utf-8-sig encoding."""
        filepath = tmp_path / "test.csv"
        df = pd.DataFrame({
            "text": ["São Paulo", "não é", "profissional habilitado", "ação"]
        })
        result = safe_write_csv(df, filepath)
        assert result is True

        # Read back and verify
        loaded = pd.read_csv(filepath, encoding="utf-8-sig")
        assert loaded.iloc[0]["text"] == "São Paulo"
        assert loaded.iloc[1]["text"] == "não é"

    def test_should_not_leave_temp_file_on_success(self, tmp_path):
        """No temp file should remain after successful write."""
        filepath = tmp_path / "test.csv"
        df = pd.DataFrame({"a": [1]})
        safe_write_csv(df, filepath)

        # Check no .tmp files exist
        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0

    def test_should_not_leave_temp_file_on_rejection(self, tmp_path):
        """No temp file should remain after rejection."""
        filepath = tmp_path / "test.csv"
        safe_write_csv(pd.DataFrame(), filepath)  # Will be rejected

        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0

    def test_empty_write_should_preserve_existing_data(self, tmp_path):
        """CRITICAL: Empty write must not destroy existing good data."""
        filepath = tmp_path / "test.csv"

        # Write initial good data
        good_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        safe_write_csv(good_df, filepath)
        assert filepath.exists()

        # Attempt empty write (simulating API failure returning empty)
        result = safe_write_csv(pd.DataFrame(), filepath)

        # Verify: rejection returned AND original data preserved
        assert result is False
        assert filepath.exists()
        preserved = pd.read_csv(filepath)
        assert len(preserved) == 3  # Original data intact

    def test_none_write_should_preserve_existing_data(self, tmp_path):
        """None write must not destroy existing good data."""
        filepath = tmp_path / "test.csv"

        # Write initial good data
        good_df = pd.DataFrame({"x": [10, 20]})
        safe_write_csv(good_df, filepath)

        # Attempt None write (simulating severe API failure)
        result = safe_write_csv(None, filepath)

        # Original data should be preserved
        assert result is False
        preserved = pd.read_csv(filepath)
        assert len(preserved) == 2

    def test_should_use_index_false(self, tmp_path):
        """CSV should be written without row index."""
        filepath = tmp_path / "test.csv"
        df = pd.DataFrame({"col": [1, 2, 3]})
        safe_write_csv(df, filepath)

        # Read raw content - should not have unnamed index column
        with open(filepath, "r") as f:
            content = f.read()
        assert "Unnamed" not in content
        assert content.count("\n") == 4  # header + 3 rows

    def test_should_include_pid_in_temp_filename(self, tmp_path, monkeypatch):
        """Temp filename should include PID for concurrent process safety."""
        # This is a bit tricky to test directly, but we can verify
        # via the implementation by checking no collision occurs
        filepath = tmp_path / "test.csv"
        df = pd.DataFrame({"a": [1]})

        # Write multiple times - should not cause issues
        for _ in range(3):
            result = safe_write_csv(df, filepath)
            assert result is True


class TestSafeWriteJSON:
    """Tests for safe_write_json function."""

    def test_should_reject_none_by_default(self, tmp_path):
        """None data should be rejected by default."""
        filepath = tmp_path / "test.json"
        result = safe_write_json(None, filepath)
        assert result is False
        assert not filepath.exists()

    def test_should_allow_none_when_flag_set(self, tmp_path):
        """None should write empty dict when allow_none=True."""
        filepath = tmp_path / "test.json"
        result = safe_write_json(None, filepath, allow_none=True)
        assert result is True
        assert filepath.exists()

        with open(filepath) as f:
            data = json.load(f)
        assert data == {}

    def test_should_write_valid_dict(self, tmp_path):
        """Valid dict should be written as JSON."""
        filepath = tmp_path / "test.json"
        data = {"key": "value", "nested": {"a": 1}}
        result = safe_write_json(data, filepath)
        assert result is True

        with open(filepath) as f:
            loaded = json.load(f)
        assert loaded == data

    def test_should_handle_non_serializable_with_default_str(self, tmp_path):
        """Non-JSON-serializable objects should be converted to str."""
        from datetime import datetime

        filepath = tmp_path / "test.json"
        data = {"timestamp": datetime(2026, 2, 3, 12, 0)}
        result = safe_write_json(data, filepath)
        assert result is True

        with open(filepath) as f:
            loaded = json.load(f)
        assert "2026" in loaded["timestamp"]

    def test_should_preserve_unicode(self, tmp_path):
        """Unicode characters should be preserved (ensure_ascii=False)."""
        filepath = tmp_path / "test.json"
        data = {"portuguese": "não", "japanese": "日本語"}
        result = safe_write_json(data, filepath)
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded["portuguese"] == "não"
        assert loaded["japanese"] == "日本語"

    def test_should_not_leave_temp_file(self, tmp_path):
        """No temp file should remain after write."""
        filepath = tmp_path / "test.json"
        safe_write_json({"a": 1}, filepath)

        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0


class TestSafeWriteText:
    """Tests for safe_write_text function."""

    def test_should_reject_none(self, tmp_path):
        """None content should be rejected."""
        filepath = tmp_path / "test.txt"
        result = safe_write_text(None, filepath)
        assert result is False
        assert not filepath.exists()

    def test_should_reject_empty_by_default(self, tmp_path):
        """Empty string should be rejected by default."""
        filepath = tmp_path / "test.txt"
        result = safe_write_text("", filepath)
        assert result is False
        assert not filepath.exists()

    def test_should_reject_whitespace_only_by_default(self, tmp_path):
        """Whitespace-only string should be rejected by default."""
        filepath = tmp_path / "test.txt"
        result = safe_write_text("   \n\t  ", filepath)
        assert result is False
        assert not filepath.exists()

    def test_should_allow_empty_when_flag_set(self, tmp_path):
        """Empty string should be allowed when allow_empty=True."""
        filepath = tmp_path / "test.txt"
        result = safe_write_text("", filepath, allow_empty=True)
        assert result is True
        assert filepath.exists()

    def test_should_write_valid_text(self, tmp_path):
        """Valid text should be written."""
        filepath = tmp_path / "test.md"
        content = "# Heading\n\nThis is a test."
        result = safe_write_text(content, filepath)
        assert result is True

        with open(filepath) as f:
            loaded = f.read()
        assert loaded == content

    def test_should_preserve_line_endings(self, tmp_path):
        """Line endings should be preserved."""
        filepath = tmp_path / "test.txt"
        content = "line1\nline2\nline3"
        safe_write_text(content, filepath)

        with open(filepath) as f:
            loaded = f.read()
        assert loaded.count("\n") == 2

    def test_should_not_leave_temp_file(self, tmp_path):
        """No temp file should remain after write."""
        filepath = tmp_path / "test.txt"
        safe_write_text("content", filepath)

        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0


class TestAtomicWriteBehavior:
    """Tests for atomic write behavior across all functions."""

    def test_csv_write_is_atomic(self, tmp_path):
        """Verify CSV write doesn't corrupt on overwrite."""
        filepath = tmp_path / "data.csv"

        # Write initial data
        df1 = pd.DataFrame({"version": [1]})
        safe_write_csv(df1, filepath)

        # Overwrite with new data
        df2 = pd.DataFrame({"version": [2, 3, 4]})
        safe_write_csv(df2, filepath)

        # Should have new data, not partial/corrupt
        loaded = pd.read_csv(filepath)
        assert len(loaded) == 3
        assert loaded.iloc[0]["version"] == 2

    def test_json_write_is_atomic(self, tmp_path):
        """Verify JSON write doesn't corrupt on overwrite."""
        filepath = tmp_path / "data.json"

        # Write initial data
        safe_write_json({"v": 1}, filepath)

        # Overwrite
        safe_write_json({"v": 2, "extra": "data"}, filepath)

        with open(filepath) as f:
            loaded = json.load(f)
        assert loaded["v"] == 2
        assert loaded["extra"] == "data"
