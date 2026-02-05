"""
Adelaide Generator Package.

Orchestrates newsletter generation by combining:
- Market data -> Regime classification
- Templates -> Content structure
- Personas -> Voice adaptation
- Formatters -> Multi-channel output
"""

from src.adelaide.generator.generator import AdelaideGenerator, generate_adelaide

__all__ = [
    'AdelaideGenerator',
    'generate_adelaide',
]
