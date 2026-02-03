"""
Gate 1 Freshness Checker - Validates data is not stale.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List
import os

from src.validators.gate1.gate1_type_validator import Gate1ValidationIssue


class Gate1FreshnessChecker:
    """
    Check data freshness based on file modification time.

    Issues warning if file is older than max_age_hours.
    """

    def check(
        self,
        file_path: Path,
        max_age_hours: int,
        filename: str
    ) -> List[Gate1ValidationIssue]:
        """
        Check if file is fresher than max_age_hours.

        Args:
            file_path: Path to the file
            max_age_hours: Maximum allowed age in hours
            filename: File name for error reporting

        Returns:
            List of validation issues (empty if fresh)
        """
        issues = []

        try:
            mtime = os.path.getmtime(file_path)
            file_age = datetime.utcnow() - datetime.utcfromtimestamp(mtime)
            max_age = timedelta(hours=max_age_hours)

            if file_age > max_age:
                hours_old = file_age.total_seconds() / 3600
                issues.append(Gate1ValidationIssue(
                    code="G1-FRS-001",
                    severity="warning",
                    message=f"Data is {hours_old:.1f}h old (max: {max_age_hours}h)",
                    file=filename
                ))

        except OSError as e:
            issues.append(Gate1ValidationIssue(
                code="G1-FRS-002",
                severity="warning",
                message=f"Could not check freshness: {e}",
                file=filename
            ))

        return issues

    def get_file_age_hours(self, file_path: Path) -> float:
        """
        Get file age in hours.

        Args:
            file_path: Path to the file

        Returns:
            Age in hours, or -1 if cannot determine
        """
        try:
            mtime = os.path.getmtime(file_path)
            file_age = datetime.utcnow() - datetime.utcfromtimestamp(mtime)
            return file_age.total_seconds() / 3600
        except OSError:
            return -1

    def is_fresh(self, file_path: Path, max_age_hours: int) -> bool:
        """
        Check if file is fresh.

        Args:
            file_path: Path to the file
            max_age_hours: Maximum allowed age in hours

        Returns:
            True if file is fresh, False otherwise
        """
        age = self.get_file_age_hours(file_path)
        if age < 0:
            return False
        return age <= max_age_hours
