"""
Alert domain model for diBoaS Analytics.

Represents monitoring alerts and health check results.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'
    EMERGENCY = 'emergency'

    def __lt__(self, other):
        order = ['info', 'warning', 'critical', 'emergency']
        return order.index(self.value) < order.index(other.value)


class AlertType(Enum):
    """Types of alerts."""
    TVL_DROP = 'tvl_drop'
    APY_DEVIATION = 'apy_deviation'
    UTILIZATION_HIGH = 'utilization_high'
    ANOMALY_DETECTED = 'anomaly_detected'
    API_ERROR = 'api_error'
    DATA_STALE = 'data_stale'
    VALIDATION_FAILED = 'validation_failed'


@dataclass
class Alert:
    """
    A monitoring alert.

    Represents an issue detected during protocol monitoring.
    """
    alert_id: str
    protocol: str
    alert_type: AlertType
    severity: AlertSeverity
    metric: str
    message: str
    value: float
    threshold: float
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    notes: Optional[str] = None

    @property
    def is_active(self) -> bool:
        """Check if alert is still active (not resolved)."""
        return not self.resolved

    @property
    def exceeds_threshold_by(self) -> float:
        """Calculate how much the value exceeds the threshold."""
        if self.threshold == 0:
            return abs(self.value)
        return abs(self.value - self.threshold) / abs(self.threshold) * 100

    def resolve(self, notes: str = None):
        """Mark alert as resolved."""
        self.resolved = True
        self.resolved_at = datetime.utcnow()
        if notes:
            self.notes = notes

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'alert_id': self.alert_id,
            'protocol': self.protocol,
            'alert_type': self.alert_type.value,
            'severity': self.severity.value,
            'metric': self.metric,
            'message': self.message,
            'value': round(self.value, 4),
            'threshold': round(self.threshold, 4),
            'timestamp': self.timestamp.isoformat(),
            'acknowledged': self.acknowledged,
            'resolved': self.resolved,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'notes': self.notes
        }


@dataclass
class ProtocolHealth:
    """
    Health status of a protocol.

    Aggregates current metrics and any active alerts.
    """
    protocol: str
    timestamp: datetime

    # Metrics
    tvl: float
    tvl_change_24h: float
    apy: float
    apy_change_24h: float
    utilization: Optional[float] = None

    # Status
    is_healthy: bool = True
    alerts: list[Alert] = field(default_factory=list)

    @property
    def active_alerts(self) -> list[Alert]:
        """Get only active (unresolved) alerts."""
        return [a for a in self.alerts if a.is_active]

    @property
    def critical_alerts(self) -> list[Alert]:
        """Get only critical or emergency alerts."""
        return [
            a for a in self.alerts
            if a.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]
        ]

    @property
    def health_score(self) -> float:
        """
        Calculate health score (0-100).

        100 = no alerts
        Deduct points based on alert severity.
        """
        score = 100.0
        for alert in self.active_alerts:
            if alert.severity == AlertSeverity.EMERGENCY:
                score -= 50
            elif alert.severity == AlertSeverity.CRITICAL:
                score -= 25
            elif alert.severity == AlertSeverity.WARNING:
                score -= 10
            elif alert.severity == AlertSeverity.INFO:
                score -= 2
        return max(0, score)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'protocol': self.protocol,
            'timestamp': self.timestamp.isoformat(),
            'tvl': round(self.tvl, 2),
            'tvl_change_24h': round(self.tvl_change_24h, 4),
            'apy': round(self.apy, 2),
            'apy_change_24h': round(self.apy_change_24h, 4),
            'utilization': round(self.utilization, 4) if self.utilization else None,
            'is_healthy': self.is_healthy,
            'health_score': round(self.health_score, 1),
            'active_alerts_count': len(self.active_alerts),
            'alerts': [a.to_dict() for a in self.alerts]
        }


@dataclass
class AnomalyResult:
    """
    Result from anomaly detection.

    Represents a detected anomaly in protocol data.
    """
    protocol: str
    metric: str
    value: float
    expected_value: float
    score: float  # Anomaly score (higher = more anomalous)
    is_anomaly: bool
    detection_method: str  # 'zscore', 'isolation_forest', etc.
    timestamp: datetime
    threshold: float
    details: Optional[dict] = None

    @property
    def deviation_pct(self) -> float:
        """Calculate percentage deviation from expected."""
        if self.expected_value == 0:
            return float('inf') if self.value != 0 else 0
        return abs(self.value - self.expected_value) / abs(self.expected_value) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'protocol': self.protocol,
            'metric': self.metric,
            'value': round(self.value, 4),
            'expected_value': round(self.expected_value, 4),
            'score': round(self.score, 4),
            'is_anomaly': self.is_anomaly,
            'detection_method': self.detection_method,
            'timestamp': self.timestamp.isoformat(),
            'threshold': round(self.threshold, 4),
            'deviation_pct': round(self.deviation_pct, 2),
            'details': self.details
        }
