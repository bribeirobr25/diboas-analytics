"""
Protocol registry for diBoaS Analytics.

Defines all supported DeFi protocols with their characteristics.
"""

PROTOCOLS = {
    # Stablecoin Yield (No Crypto Exposure)
    'sky': {
        'name': 'Sky SSR',
        'chain': 'arbitrum',
        'asset': 'USDS',
        'type': 'stablecoin_yield',
        'defillama_project': 'sky-lending',
        'crypto_exposure': False,
        'enabled': True
    },
    'aave': {
        'name': 'Aave V3',
        'chain': 'arbitrum',
        'asset': 'USDC',
        'type': 'lending',
        'defillama_project': 'aave-v3',
        'crypto_exposure': False,
        'enabled': True
    },
    'compound': {
        'name': 'Compound V3',
        'chain': 'arbitrum',
        'asset': 'USDC',
        'type': 'lending',
        'defillama_project': 'compound-v3',
        'crypto_exposure': False,
        'enabled': True
    },

    # Crypto Exposure
    'sanctum': {
        'name': 'Sanctum INF',
        'chain': 'solana',
        'asset': 'SOL LST Basket',
        'type': 'liquid_staking',
        'crypto_exposure': True,
        'price_exposure': 'SOL',
        'enabled': True,
        'notes': 'Diversified LST basket on Solana'
    },
    'jito': {
        'name': 'Jito',
        'chain': 'solana',
        'asset': 'JitoSOL',
        'type': 'liquid_staking_mev',
        'crypto_exposure': True,
        'price_exposure': 'SOL',
        'enabled': True,
        'notes': 'SOL staking + MEV rewards'
    },
    'jlp': {
        'name': 'Jupiter JLP',
        'chain': 'solana',
        'asset': 'Perps LP',
        'type': 'perps_lp',
        'crypto_exposure': True,
        'basket_composition': {
            'SOL': 0.45,
            'ETH': 0.27,
            'BTC': 0.27,
            'other': 0.01
        },
        'enabled': True,
        'notes': 'Crypto return = weighted basket + JLP APY'
    },

    # For Proxy Calculations Only
    'lido': {
        'name': 'Lido',
        'chain': 'ethereum',
        'asset': 'stETH',
        'type': 'liquid_staking',
        'defillama_project': 'lido',
        'crypto_exposure': True,
        'price_exposure': 'ETH',
        'used_for': 'proxy_calculations_only',
        'enabled': True
    }
}


def get_protocol(protocol_id: str) -> dict:
    """Get protocol configuration by ID."""
    if protocol_id not in PROTOCOLS:
        raise ValueError(f"Unknown protocol: {protocol_id}")
    return PROTOCOLS[protocol_id]


def get_enabled_protocols() -> dict:
    """Get all enabled protocols."""
    return {k: v for k, v in PROTOCOLS.items() if v.get('enabled', True)}


def get_protocols_by_chain(chain: str) -> dict:
    """Get all protocols on a specific chain."""
    return {k: v for k, v in PROTOCOLS.items() if v['chain'] == chain}


def get_crypto_protocols() -> dict:
    """Get all protocols with crypto exposure."""
    return {k: v for k, v in PROTOCOLS.items() if v['crypto_exposure']}


def get_stable_protocols() -> dict:
    """Get all protocols without crypto exposure."""
    return {k: v for k, v in PROTOCOLS.items() if not v['crypto_exposure']}
