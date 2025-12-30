"""
Anomaly Detection Engine.

ML-based detection of unusual behavior in protocol data.
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Optional
import logging

from src.domain.alert import AnomalyResult
from config.thresholds import ZSCORE_THRESHOLDS, ISOLATION_FOREST_CONFIG

logger = logging.getLogger(__name__)


class ZScoreDetector:
    """
    Statistical anomaly detection using Z-scores.

    Flags values that deviate significantly from rolling mean.
    """

    def __init__(
        self,
        window: int = 30,
        threshold: float = None
    ):
        """
        Initialize Z-score detector.

        Args:
            window: Rolling window size for mean/std calculation
            threshold: Z-score threshold for anomaly (default from config)
        """
        self.window = window
        self.threshold = threshold or ZSCORE_THRESHOLDS['critical']

    def detect(
        self,
        series: pd.Series,
        protocol: str = ''
    ) -> list[AnomalyResult]:
        """
        Detect anomalies in time series.

        Args:
            series: Time series data
            protocol: Protocol name for reporting

        Returns:
            List of detected anomalies
        """
        if len(series) < self.window:
            return []

        rolling_mean = series.rolling(window=self.window).mean()
        rolling_std = series.rolling(window=self.window).std()

        # Avoid division by zero
        rolling_std = rolling_std.replace(0, np.nan)

        z_scores = (series - rolling_mean) / rolling_std

        anomalies = []
        for idx, (value, z) in enumerate(zip(series, z_scores)):
            if pd.notna(z) and abs(z) > self.threshold:
                timestamp = series.index[idx] if hasattr(series, 'index') else datetime.utcnow()
                if isinstance(timestamp, pd.Timestamp):
                    timestamp = timestamp.to_pydatetime()

                anomalies.append(AnomalyResult(
                    protocol=protocol,
                    metric=series.name if hasattr(series, 'name') and series.name else 'value',
                    value=float(value),
                    expected_value=float(rolling_mean.iloc[idx]) if pd.notna(rolling_mean.iloc[idx]) else 0,
                    score=float(abs(z)),
                    is_anomaly=True,
                    detection_method='zscore',
                    timestamp=timestamp if isinstance(timestamp, datetime) else datetime.utcnow(),
                    threshold=self.threshold,
                    details={
                        'z_score': float(z),
                        'rolling_mean': float(rolling_mean.iloc[idx]) if pd.notna(rolling_mean.iloc[idx]) else None,
                        'rolling_std': float(rolling_std.iloc[idx]) if pd.notna(rolling_std.iloc[idx]) else None
                    }
                ))

        return anomalies

    def score(self, series: pd.Series) -> pd.Series:
        """
        Get Z-scores for entire series.

        Args:
            series: Time series data

        Returns:
            Series of Z-scores
        """
        rolling_mean = series.rolling(window=self.window).mean()
        rolling_std = series.rolling(window=self.window).std()
        rolling_std = rolling_std.replace(0, np.nan)

        return (series - rolling_mean) / rolling_std


class IsolationForestDetector:
    """
    ML-based anomaly detection using Isolation Forest.

    Detects unusual transactions and behavior patterns.
    """

    def __init__(
        self,
        contamination: float = None,
        n_estimators: int = None,
        random_state: int = None
    ):
        """
        Initialize Isolation Forest detector.

        Args:
            contamination: Expected fraction of outliers
            n_estimators: Number of trees
            random_state: Random seed
        """
        try:
            from sklearn.ensemble import IsolationForest
            self.model = IsolationForest(
                contamination=contamination or ISOLATION_FOREST_CONFIG['contamination'],
                n_estimators=n_estimators or ISOLATION_FOREST_CONFIG['n_estimators'],
                random_state=random_state or ISOLATION_FOREST_CONFIG['random_state']
            )
            self.is_fitted = False
            self._sklearn_available = True
        except ImportError:
            logger.warning("scikit-learn not available, IsolationForest disabled")
            self.model = None
            self.is_fitted = False
            self._sklearn_available = False

    def fit(self, data: pd.DataFrame):
        """
        Fit model on historical data.

        Args:
            data: Training data (numeric features only)
        """
        if not self._sklearn_available:
            return

        # Ensure data is numeric
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            logger.warning("No numeric data for Isolation Forest training")
            return

        # Handle missing values
        numeric_data = numeric_data.fillna(numeric_data.mean())

        self.model.fit(numeric_data)
        self.is_fitted = True
        logger.info(f"Isolation Forest fitted on {len(numeric_data)} samples")

    def detect(
        self,
        data: pd.DataFrame,
        protocol: str = ''
    ) -> list[AnomalyResult]:
        """
        Detect anomalies in data.

        Args:
            data: Data to check
            protocol: Protocol name for reporting

        Returns:
            List of detected anomalies (-1 = anomaly, 1 = normal)
        """
        if not self._sklearn_available or not self.is_fitted:
            return []

        numeric_data = data.select_dtypes(include=[np.number]).fillna(0)
        if numeric_data.empty:
            return []

        predictions = self.model.predict(numeric_data)
        scores = self.model.decision_function(numeric_data)

        anomalies = []
        for idx, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:  # Anomaly
                timestamp = data.index[idx] if hasattr(data, 'index') else datetime.utcnow()
                if isinstance(timestamp, pd.Timestamp):
                    timestamp = timestamp.to_pydatetime()

                anomalies.append(AnomalyResult(
                    protocol=protocol,
                    metric='multivariate',
                    value=float(score),
                    expected_value=0.0,
                    score=float(abs(score)),
                    is_anomaly=True,
                    detection_method='isolation_forest',
                    timestamp=timestamp if isinstance(timestamp, datetime) else datetime.utcnow(),
                    threshold=0.0,
                    details={
                        'row_index': idx,
                        'decision_score': float(score)
                    }
                ))

        return anomalies

    def score(self, data: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores.

        Lower (more negative) = more anomalous

        Args:
            data: Data to score

        Returns:
            Array of anomaly scores
        """
        if not self._sklearn_available or not self.is_fitted:
            return np.zeros(len(data))

        numeric_data = data.select_dtypes(include=[np.number]).fillna(0)
        if numeric_data.empty:
            return np.zeros(len(data))

        return self.model.decision_function(numeric_data)


class CorrelationMonitor:
    """
    Monitor correlations between crypto assets.

    Detects when correlations deviate from expected values.
    """

    # Expected correlations from QR Board analysis
    EXPECTED_CORRELATIONS = {
        ('SOL', 'ETH'): 0.75,
        ('SOL', 'BTC'): 0.70,
        ('ETH', 'BTC'): 0.85
    }

    def __init__(self, window: int = 30, deviation_threshold: float = 0.20):
        """
        Initialize correlation monitor.

        Args:
            window: Rolling window for correlation calculation
            deviation_threshold: Threshold for significant deviation
        """
        self.window = window
        self.deviation_threshold = deviation_threshold

    def check_correlations(
        self,
        price_data: pd.DataFrame
    ) -> list[AnomalyResult]:
        """
        Check if correlations are within expected ranges.

        Args:
            price_data: DataFrame with columns for each asset

        Returns:
            List of anomalies if correlations deviate
        """
        anomalies = []

        for (asset1, asset2), expected in self.EXPECTED_CORRELATIONS.items():
            if asset1 not in price_data.columns or asset2 not in price_data.columns:
                continue

            # Calculate rolling correlation
            returns1 = price_data[asset1].pct_change()
            returns2 = price_data[asset2].pct_change()

            rolling_corr = returns1.rolling(window=self.window).corr(returns2)

            # Check latest correlation
            if len(rolling_corr) > 0 and pd.notna(rolling_corr.iloc[-1]):
                current_corr = rolling_corr.iloc[-1]
                deviation = abs(current_corr - expected)

                if deviation > self.deviation_threshold:
                    anomalies.append(AnomalyResult(
                        protocol='correlation',
                        metric=f'{asset1}_{asset2}_correlation',
                        value=float(current_corr),
                        expected_value=expected,
                        score=float(deviation),
                        is_anomaly=True,
                        detection_method='correlation',
                        timestamp=datetime.utcnow(),
                        threshold=self.deviation_threshold,
                        details={
                            'asset1': asset1,
                            'asset2': asset2,
                            'expected_correlation': expected,
                            'deviation': float(deviation)
                        }
                    ))

        return anomalies


class AnomalyEngine:
    """
    Combined anomaly detection engine.

    Uses multiple detection methods for comprehensive monitoring.
    """

    def __init__(self):
        self.zscore_detector = ZScoreDetector()
        self.isolation_detector = IsolationForestDetector()
        self.correlation_monitor = CorrelationMonitor()

    def fit(self, historical_data: pd.DataFrame):
        """Fit models on historical data."""
        self.isolation_detector.fit(historical_data)

    def detect_all(
        self,
        data: pd.DataFrame,
        protocol: str = ''
    ) -> list[AnomalyResult]:
        """
        Run all anomaly detection methods.

        Args:
            data: Data to analyze
            protocol: Protocol name

        Returns:
            Combined list of anomalies from all methods
        """
        anomalies = []

        # Z-score detection on each numeric column
        for col in data.select_dtypes(include=[np.number]).columns:
            series = data[col]
            series.name = col
            col_anomalies = self.zscore_detector.detect(series, protocol)
            anomalies.extend(col_anomalies)

        # Isolation Forest detection
        if_anomalies = self.isolation_detector.detect(data, protocol)
        anomalies.extend(if_anomalies)

        return anomalies

    def generate_report(
        self,
        anomalies: list[AnomalyResult]
    ) -> dict:
        """Generate anomaly detection report."""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'total_anomalies': len(anomalies),
            'by_method': {
                'zscore': sum(1 for a in anomalies if a.detection_method == 'zscore'),
                'isolation_forest': sum(1 for a in anomalies if a.detection_method == 'isolation_forest'),
                'correlation': sum(1 for a in anomalies if a.detection_method == 'correlation')
            },
            'anomalies': [a.to_dict() for a in anomalies]
        }
