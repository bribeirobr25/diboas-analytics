"""
Application settings for diBoaS Analytics.

All configuration values that can be customized via environment variables.
"""

import os
from pathlib import Path

# Optional: load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use environment variables directly

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = Path(os.getenv('DATA_DIR', BASE_DIR / 'data'))
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', BASE_DIR / 'outputs'))
STORAGE_DIR = BASE_DIR / 'storage'
CONFIG_DIR = BASE_DIR / 'config'

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Simulation defaults
DEFAULT_SIMULATIONS = 5000
DEFAULT_HORIZON_MONTHS = 48
DEFAULT_START_DATE = '2022-05-01'
DEFAULT_END_DATE = '2025-12-31'
DEFAULT_RANDOM_SEED = 42

# Battle Test defaults
BATTLE_TEST_START_DATE = '2022-05-01'
BATTLE_TEST_END_DATE = '2025-12-31'

# Validation
VALIDATION_TOLERANCE = 0.01  # 0.01% for return matching

# Gas costs per transaction (USD)
GAS_COSTS = {
    'arbitrum': 0.30,
    'solana': 0.005,
    'ethereum': 5.00  # Reference only, not used in Phase 1
}

# Minimum deposits per strategy (USD)
MINIMUM_DEPOSITS = {
    1: 50, 2: 20, 3: 50, 4: 20, 5: 50,
    6: 30, 7: 50, 8: 100, 9: 50, 10: 200
}

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Dream Mode
BANK_COMPARISON_APY = 0.5  # 0.5% EU average
BANK_COMPARISON_SOURCE = "ECB Statistics, December 2024"

# API settings (optional - for live data)
DEFILLAMA_API_KEY = os.getenv('DEFILLAMA_API_KEY', '')
YAHOO_API_KEY = os.getenv('YAHOO_API_KEY', '')

# Notification settings
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
PAGERDUTY_API_KEY = os.getenv('PAGERDUTY_API_KEY', '')
