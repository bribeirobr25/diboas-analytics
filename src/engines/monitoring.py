"""
Protocol Monitoring Engine.

Health checks and alerting for DeFi protocols.
"""

from datetime import datetime
from typing import Optional
import logging
import uuid

from src.domain.alert import Alert, AlertSeverity, AlertType, ProtocolHealth
from config.thresholds import TVL_THRESHOLDS, UTILIZATION_THRESHOLDS, APY_THRESHOLDS

logger = logging.getLogger(__name__)


class MonitoringEngine:
    """
    Protocol health monitoring with alerting.

    Monitors:
    - TVL changes
    - APY deviations
    - Utilization rates
    - Data freshness
    """

    def __init__(self):
        self.thresholds = {
            'tvl_drop_warning': TVL_THRESHOLDS['drop_warning'],
            'tvl_drop_critical': TVL_THRESHOLDS['drop_critical'],
            'utilization_warning': UTILIZATION_THRESHOLDS['warning'],
            'utilization_critical': UTILIZATION_THRESHOLDS['critical'],
            'apy_deviation_warning': APY_THRESHOLDS['deviation_warning'],
            'apy_deviation_critical': APY_THRESHOLDS['deviation_critical'],
        }

    def check_protocol(
        self,
        protocol: str,
        current: dict,
        previous: dict
    ) -> ProtocolHealth:
        """
        Check health of a single protocol.

        Args:
            protocol: Protocol identifier
            current: Current metrics
            previous: Previous metrics (for comparison)

        Returns:
            ProtocolHealth with status and any alerts
        """
        alerts = []
        timestamp = datetime.utcnow()

        # Calculate changes
        tvl_change = self._safe_change(current.get('tvl', 0), previous.get('tvl', 0))
        apy_change = self._safe_change(current.get('apy', 0), previous.get('apy', 0))

        # TVL check
        tvl_alert = self._check_tvl(protocol, tvl_change, timestamp)
        if tvl_alert:
            alerts.append(tvl_alert)

        # Utilization check (for lending protocols)
        if current.get('utilization') is not None:
            util_alert = self._check_utilization(
                protocol,
                current['utilization'],
                timestamp
            )
            if util_alert:
                alerts.append(util_alert)

        # APY check
        apy_alert = self._check_apy(protocol, apy_change, timestamp)
        if apy_alert:
            alerts.append(apy_alert)

        # APY bounds check
        bounds_alert = self._check_apy_bounds(protocol, current.get('apy', 0), timestamp)
        if bounds_alert:
            alerts.append(bounds_alert)

        # Determine overall health
        critical_alerts = [
            a for a in alerts
            if a.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]
        ]
        is_healthy = len(critical_alerts) == 0

        return ProtocolHealth(
            protocol=protocol,
            timestamp=timestamp,
            tvl=current.get('tvl', 0),
            tvl_change_24h=tvl_change,
            apy=current.get('apy', 0),
            apy_change_24h=apy_change,
            utilization=current.get('utilization'),
            is_healthy=is_healthy,
            alerts=alerts
        )

    def _safe_change(self, current: float, previous: float) -> float:
        """Calculate percentage change safely."""
        if previous == 0:
            return 0.0
        return (current - previous) / previous

    def _check_tvl(
        self,
        protocol: str,
        tvl_change: float,
        timestamp: datetime
    ) -> Optional[Alert]:
        """Check TVL drop thresholds."""
        if tvl_change < self.thresholds['tvl_drop_critical']:
            return Alert(
                alert_id=str(uuid.uuid4())[:8],
                protocol=protocol,
                alert_type=AlertType.TVL_DROP,
                severity=AlertSeverity.CRITICAL,
                metric='tvl_change_24h',
                message=f"TVL dropped {tvl_change*100:.1f}% in 24h",
                value=tvl_change,
                threshold=self.thresholds['tvl_drop_critical'],
                timestamp=timestamp
            )
        elif tvl_change < self.thresholds['tvl_drop_warning']:
            return Alert(
                alert_id=str(uuid.uuid4())[:8],
                protocol=protocol,
                alert_type=AlertType.TVL_DROP,
                severity=AlertSeverity.WARNING,
                metric='tvl_change_24h',
                message=f"TVL dropped {tvl_change*100:.1f}% in 24h",
                value=tvl_change,
                threshold=self.thresholds['tvl_drop_warning'],
                timestamp=timestamp
            )
        return None

    def _check_utilization(
        self,
        protocol: str,
        utilization: float,
        timestamp: datetime
    ) -> Optional[Alert]:
        """Check utilization thresholds."""
        if utilization > self.thresholds['utilization_critical']:
            return Alert(
                alert_id=str(uuid.uuid4())[:8],
                protocol=protocol,
                alert_type=AlertType.UTILIZATION_HIGH,
                severity=AlertSeverity.CRITICAL,
                metric='utilization',
                message=f"Utilization at {utilization*100:.1f}%",
                value=utilization,
                threshold=self.thresholds['utilization_critical'],
                timestamp=timestamp
            )
        elif utilization > self.thresholds['utilization_warning']:
            return Alert(
                alert_id=str(uuid.uuid4())[:8],
                protocol=protocol,
                alert_type=AlertType.UTILIZATION_HIGH,
                severity=AlertSeverity.WARNING,
                metric='utilization',
                message=f"Utilization at {utilization*100:.1f}%",
                value=utilization,
                threshold=self.thresholds['utilization_warning'],
                timestamp=timestamp
            )
        return None

    def _check_apy(
        self,
        protocol: str,
        apy_change: float,
        timestamp: datetime
    ) -> Optional[Alert]:
        """Check APY deviation thresholds."""
        abs_change = abs(apy_change)

        if abs_change > self.thresholds['apy_deviation_critical']:
            return Alert(
                alert_id=str(uuid.uuid4())[:8],
                protocol=protocol,
                alert_type=AlertType.APY_DEVIATION,
                severity=AlertSeverity.CRITICAL,
                metric='apy_change_24h',
                message=f"APY changed {apy_change*100:.1f}% in 24h",
                value=apy_change,
                threshold=self.thresholds['apy_deviation_critical'],
                timestamp=timestamp
            )
        elif abs_change > self.thresholds['apy_deviation_warning']:
            return Alert(
                alert_id=str(uuid.uuid4())[:8],
                protocol=protocol,
                alert_type=AlertType.APY_DEVIATION,
                severity=AlertSeverity.WARNING,
                metric='apy_change_24h',
                message=f"APY changed {apy_change*100:.1f}% in 24h",
                value=apy_change,
                threshold=self.thresholds['apy_deviation_warning'],
                timestamp=timestamp
            )
        return None

    def _check_apy_bounds(
        self,
        protocol: str,
        apy: float,
        timestamp: datetime
    ) -> Optional[Alert]:
        """Check if APY is within reasonable bounds."""
        if apy < APY_THRESHOLDS['minimum']:
            return Alert(
                alert_id=str(uuid.uuid4())[:8],
                protocol=protocol,
                alert_type=AlertType.APY_DEVIATION,
                severity=AlertSeverity.WARNING,
                metric='apy',
                message=f"APY is negative: {apy:.1f}%",
                value=apy,
                threshold=APY_THRESHOLDS['minimum'],
                timestamp=timestamp
            )
        elif apy > APY_THRESHOLDS['maximum']:
            return Alert(
                alert_id=str(uuid.uuid4())[:8],
                protocol=protocol,
                alert_type=AlertType.APY_DEVIATION,
                severity=AlertSeverity.WARNING,
                metric='apy',
                message=f"APY suspiciously high: {apy:.1f}%",
                value=apy,
                threshold=APY_THRESHOLDS['maximum'],
                timestamp=timestamp
            )
        return None

    def check_all_protocols(
        self,
        current_data: dict[str, dict],
        previous_data: dict[str, dict]
    ) -> list[ProtocolHealth]:
        """
        Check health of all protocols.

        Args:
            current_data: Dictionary of protocol -> current metrics
            previous_data: Dictionary of protocol -> previous metrics

        Returns:
            List of ProtocolHealth for all protocols
        """
        results = []

        for protocol, current in current_data.items():
            previous = previous_data.get(protocol, {})
            health = self.check_protocol(protocol, current, previous)
            results.append(health)

            if not health.is_healthy:
                logger.warning(f"Protocol {protocol} unhealthy: {len(health.alerts)} alerts")

        return results

    def get_active_alerts(
        self,
        health_reports: list[ProtocolHealth]
    ) -> list[Alert]:
        """Get all active alerts across protocols."""
        alerts = []
        for health in health_reports:
            alerts.extend(health.active_alerts)
        return sorted(alerts, key=lambda a: a.severity.value, reverse=True)

    def generate_summary(
        self,
        health_reports: list[ProtocolHealth]
    ) -> dict:
        """Generate monitoring summary."""
        total = len(health_reports)
        healthy = sum(1 for h in health_reports if h.is_healthy)
        all_alerts = self.get_active_alerts(health_reports)

        return {
            'timestamp': datetime.utcnow().isoformat(),
            'total_protocols': total,
            'healthy': healthy,
            'unhealthy': total - healthy,
            'health_rate': (healthy / total * 100) if total > 0 else 100,
            'total_alerts': len(all_alerts),
            'critical_alerts': sum(1 for a in all_alerts if a.severity == AlertSeverity.CRITICAL),
            'warning_alerts': sum(1 for a in all_alerts if a.severity == AlertSeverity.WARNING),
            'protocols': [h.to_dict() for h in health_reports]
        }
