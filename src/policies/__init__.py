"""
Policies module for ethical B2B guardrails.

Implements the Grandmother Test:
"Would this help my grandmother build wealth, or help sophisticated
players extract value from her?"

Key Policies:
- DataAccessPolicy: Controls what data B2B clients can access
- Estate/whale wallet data is BLOCKED for B2B to prevent front-running
"""

from src.policies.data_access import (
    DataAccessPolicy,
    ClientTier,
)

__all__ = [
    'DataAccessPolicy',
    'ClientTier',
]
