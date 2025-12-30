"""
Dream Mode configuration.

Maps the 10 internal strategies to 3 simplified consumer paths.
Used by the Dream Mode Export module to generate frontend data.
"""

# Path definitions for Dream Mode UI
DREAM_MODE_PATHS = {
    'safety': {
        'strategies': [1, 3, 5, 7, 9],  # All 0% crypto strategies
        'label': 'Safety First',
        'description': 'Stable yield, no crypto exposure',
        'color': '#2563EB',  # Blue
        'risk_level': 'Minimal'
    },
    'balance': {
        'strategies': [2, 4, 6],  # 30-40% crypto strategies
        'label': 'Balanced Growth',
        'description': 'Moderate crypto exposure (30-40%)',
        'color': '#7C3AED',  # Purple
        'risk_level': 'Low-Medium'
    },
    'growth': {
        'strategies': [8, 10],  # 70-85% crypto strategies
        'label': 'Maximum Growth',
        'description': 'High crypto exposure (70-85%)',
        'color': '#DC2626',  # Red
        'risk_level': 'High'
    }
}

# Bank comparison baseline (CLO-approved)
BANK_COMPARISON = {
    'apy': 0.5,  # 0.5% APY
    'source': 'ECB Statistics',
    'date': 'December 2024',
    'note': 'Average EU savings account rate. Rates may vary.'
}

# CLO-mandated disclaimers
DISCLAIMERS = {
    'simulation': (
        "This is a simulation based on historical data from May 2022 to December 2025. "
        "Past performance does not guarantee future returns."
    ),
    'risk': "Capital is at risk. Actual results may differ significantly.",
    'not_advice': (
        "This is for educational purposes only and does not constitute investment advice."
    ),
    'card_watermark': "SIMULATION - Based on historical data. Not a guarantee. diboas.com",
    'bank_comparison': (
        "Bank comparison based on average EU savings account rate of 0.5% APY. "
        "Source: ECB Statistics, December 2024. Rates may vary."
    )
}

# Enhanced disclaimers for specific regions
REGIONAL_DISCLAIMERS = {
    'pt-BR': (
        "SIMULACAO EDUCACIONAL - Este recurso utiliza dados historicos apenas para fins "
        "ilustrativos. Nao constitui oferta de investimento, promessa de retorno ou "
        "aconselhamento financeiro. Resultados reais podem diferir significativamente."
    ),
    'en-US': (
        "EDUCATIONAL SIMULATION - This feature uses historical data for illustrative "
        "purposes only. It does not constitute an offer of investment, promise of returns, "
        "or financial advice. Actual results may differ significantly."
    )
}


def get_path_for_strategy(strategy_id: int) -> str:
    """Get the Dream Mode path for a strategy ID."""
    for path_id, path_config in DREAM_MODE_PATHS.items():
        if strategy_id in path_config['strategies']:
            return path_id
    raise ValueError(f"Strategy {strategy_id} not mapped to any path")


def get_strategies_for_path(path_id: str) -> list[int]:
    """Get all strategy IDs for a Dream Mode path."""
    if path_id not in DREAM_MODE_PATHS:
        raise ValueError(f"Unknown path: {path_id}")
    return DREAM_MODE_PATHS[path_id]['strategies']
