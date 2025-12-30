"""
Alert thresholds for protocol monitoring.

Defines warning and critical thresholds for various metrics.
"""

# TVL (Total Value Locked) thresholds
TVL_THRESHOLDS = {
    'drop_warning': -0.15,      # -15% TVL drop in 24h
    'drop_critical': -0.30,     # -30% TVL drop in 24h
    'minimum_usd': 1_000_000,   # Minimum TVL to be considered healthy
}

# Utilization thresholds (for lending protocols)
UTILIZATION_THRESHOLDS = {
    'warning': 0.85,            # 85% utilization
    'critical': 0.95,           # 95% utilization
}

# APY deviation thresholds
APY_THRESHOLDS = {
    'deviation_warning': 0.50,  # 50% change from baseline
    'deviation_critical': 1.00, # 100% change from baseline
    'minimum': 0.0,             # APY should not be negative
    'maximum': 500.0,           # APY above 500% is suspicious
}

# Z-score thresholds for anomaly detection
ZSCORE_THRESHOLDS = {
    'warning': 2.5,             # 2.5 standard deviations
    'critical': 3.0,            # 3.0 standard deviations
}

# Isolation Forest parameters
ISOLATION_FOREST_CONFIG = {
    'contamination': 0.05,      # Expected fraction of outliers
    'n_estimators': 100,
    'random_state': 42,
}

# Correlation monitoring
CORRELATION_THRESHOLDS = {
    'min_expected': 0.60,       # Minimum expected correlation between crypto assets
    'deviation_warning': 0.20,  # Warning if correlation deviates by 20%
}

# Response time thresholds (for monitoring)
RESPONSE_TIME_THRESHOLDS = {
    'warning_ms': 5000,         # 5 seconds
    'critical_ms': 15000,       # 15 seconds
}


def get_tvl_threshold(severity: str) -> float:
    """Get TVL threshold by severity level."""
    if severity == 'warning':
        return TVL_THRESHOLDS['drop_warning']
    elif severity == 'critical':
        return TVL_THRESHOLDS['drop_critical']
    raise ValueError(f"Unknown severity: {severity}")


def get_utilization_threshold(severity: str) -> float:
    """Get utilization threshold by severity level."""
    if severity == 'warning':
        return UTILIZATION_THRESHOLDS['warning']
    elif severity == 'critical':
        return UTILIZATION_THRESHOLDS['critical']
    raise ValueError(f"Unknown severity: {severity}")
