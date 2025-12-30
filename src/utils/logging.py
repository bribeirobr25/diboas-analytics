"""
Logging setup for diBoaS Analytics.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from config.settings import LOG_LEVEL, LOG_FORMAT, OUTPUT_DIR


def setup_logging(
    level: str = None,
    log_file: bool = True,
    console: bool = True
) -> logging.Logger:
    """
    Setup logging for the application.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Whether to log to file
        console: Whether to log to console

    Returns:
        Root logger
    """
    level = level or LOG_LEVEL
    level_int = getattr(logging, level.upper(), logging.INFO)

    # Create root logger
    logger = logging.getLogger('diboas')
    logger.setLevel(level_int)

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)

    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level_int)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_dir = OUTPUT_DIR / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = log_dir / f'diboas_{timestamp}.log'

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level_int)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name: Module name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f'diboas.{name}')


class ProgressLogger:
    """
    Logger for tracking progress of long-running operations.
    """

    def __init__(self, total: int, name: str = 'Progress', log_interval: int = 10):
        """
        Initialize progress logger.

        Args:
            total: Total number of items
            name: Name of the operation
            log_interval: Percentage interval for logging (default 10%)
        """
        self.total = total
        self.name = name
        self.log_interval = log_interval
        self.current = 0
        self.last_logged_pct = 0
        self.logger = get_logger('progress')

    def update(self, n: int = 1):
        """Update progress by n items."""
        self.current += n
        pct = (self.current / self.total) * 100 if self.total > 0 else 100

        if pct >= self.last_logged_pct + self.log_interval:
            self.logger.info(f"{self.name}: {pct:.0f}% ({self.current}/{self.total})")
            self.last_logged_pct = int(pct / self.log_interval) * self.log_interval

    def complete(self):
        """Mark operation as complete."""
        self.logger.info(f"{self.name}: Complete ({self.total}/{self.total})")


class AuditLogger:
    """
    Logger for audit trail events.

    Records important events for compliance and debugging.
    """

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or OUTPUT_DIR
        self.logger = get_logger('audit')
        self.events = []

    def log_event(
        self,
        event_type: str,
        description: str,
        details: dict = None
    ):
        """
        Log an audit event.

        Args:
            event_type: Type of event (e.g., 'simulation_start', 'data_load')
            description: Human-readable description
            details: Additional details as dictionary
        """
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'description': description,
            'details': details or {}
        }
        self.events.append(event)
        self.logger.info(f"[AUDIT] {event_type}: {description}")

    def log_error(self, error: Exception, context: str = ''):
        """Log an error event."""
        self.log_event(
            'error',
            str(error),
            {'context': context, 'error_type': type(error).__name__}
        )

    def save(self, filename: str = 'audit_log.json'):
        """Save audit log to file."""
        import json
        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            json.dump(self.events, f, indent=2)
        self.logger.info(f"Audit log saved to {output_path}")
