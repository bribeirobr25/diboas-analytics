"""
Chain configurations for diBoaS Analytics.

Defines supported blockchain networks and their parameters.
"""

CHAINS = {
    'arbitrum': {
        'name': 'Arbitrum One',
        'chain_id': 42161,
        'type': 'l2',
        'native_token': 'ETH',
        'gas_cost_usd': 0.30,
        'block_time_seconds': 0.25,
        'explorer': 'https://arbiscan.io',
        'enabled': True
    },
    'solana': {
        'name': 'Solana',
        'chain_id': None,  # Solana doesn't use chain IDs
        'type': 'l1',
        'native_token': 'SOL',
        'gas_cost_usd': 0.005,
        'block_time_seconds': 0.4,
        'explorer': 'https://solscan.io',
        'enabled': True
    },
    'ethereum': {
        'name': 'Ethereum Mainnet',
        'chain_id': 1,
        'type': 'l1',
        'native_token': 'ETH',
        'gas_cost_usd': 5.00,  # Reference only
        'block_time_seconds': 12,
        'explorer': 'https://etherscan.io',
        'enabled': False,  # Not used in Phase 1
        'notes': 'Used for proxy data only (Lido)'
    }
}


def get_chain(chain_id: str) -> dict:
    """Get chain configuration by ID."""
    if chain_id not in CHAINS:
        raise ValueError(f"Unknown chain: {chain_id}")
    return CHAINS[chain_id]


def get_enabled_chains() -> dict:
    """Get all enabled chains."""
    return {k: v for k, v in CHAINS.items() if v.get('enabled', True)}


def get_gas_cost(chain_id: str) -> float:
    """Get gas cost in USD for a chain."""
    return CHAINS[chain_id]['gas_cost_usd']
