"""
Shared constants and interfaces across domains.

This module contains constants that are used by multiple domains
(e.g., Adelaide, Reporters, Validators) to avoid cross-domain coupling.

Following DDD Principle 1: Domains should not directly import from each other.
Instead, shared data should be extracted to a neutral location.
"""

from src.shared.disclaimers import (
    HYPOTHETICAL_DISCLAIMERS,
    REGIONAL_DISCLAIMERS,
)

__all__ = [
    'HYPOTHETICAL_DISCLAIMERS',
    'REGIONAL_DISCLAIMERS',
]
