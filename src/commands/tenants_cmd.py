"""
Tenant Management CLI Commands.

Commands:
    python main.py tenants list                    # List all tenants
    python main.py tenants validate --tenant X     # Validate tenant config
    python main.py tenants show --tenant X         # Show tenant details
    python main.py tenants policy --tenant X       # Show data access policy
"""

import logging
from pathlib import Path

from src.config.tenant import TenantManager
from src.policies.data_access import DataAccessPolicy

logger = logging.getLogger(__name__)


def run_tenants(args):
    """Handle tenant management commands."""
    action = getattr(args, 'tenants_action', None)

    if action is None:
        print("Usage: python main.py tenants <action>")
        print("\nActions:")
        print("  list                    List all registered tenants")
        print("  validate --tenant X     Validate a tenant configuration")
        print("  show --tenant X         Show tenant details")
        print("  policy --tenant X       Show data access policy for tenant")
        return

    manager = TenantManager()

    if action == 'list':
        run_tenants_list(manager)
    elif action == 'validate':
        run_tenants_validate(manager, args.tenant)
    elif action == 'show':
        run_tenants_show(manager, args.tenant)
    elif action == 'policy':
        tenant_id = getattr(args, 'tenant', None) or 'diboas'
        run_tenants_policy(manager, tenant_id)
    else:
        print(f"Unknown action: {action}")


def run_tenants_list(manager: TenantManager):
    """List all registered tenants."""
    print("\n  Registered Tenants")
    print("  " + "=" * 60)
    print()

    tenants = manager.list_tenants()

    # Table header
    print(f"  {'ID':<20} {'Name':<25} {'Tier':<15}")
    print("  " + "-" * 60)

    for tenant_id in tenants:
        config = manager.get(tenant_id)
        if config:
            print(f"  {config.tenant_id:<20} {config.name:<25} {config.tier:<15}")

    print()
    print(f"  Total: {len(tenants)} tenant(s)")
    print()


def run_tenants_validate(manager: TenantManager, tenant_id: str):
    """Validate a tenant configuration."""
    print(f"\n  Validating Tenant: {tenant_id}")
    print("  " + "=" * 60)
    print()

    result = manager.validate(tenant_id)

    if result['valid']:
        print("  Status: VALID")
    else:
        print("  Status: INVALID")

    print()

    if result.get('errors'):
        print("  Errors:")
        for error in result['errors']:
            print(f"    - {error}")
        print()

    if result.get('warnings'):
        print("  Warnings:")
        for warning in result['warnings']:
            print(f"    - {warning}")
        print()

    if result['valid'] and 'config' in result:
        config = result['config']
        print("  Configuration Summary:")
        print(f"    Name: {config.get('name', 'N/A')}")
        print(f"    Tier: {config.get('tier', 'N/A')}")
        print(f"    Collectors: {', '.join(config.get('collectors', []))}")
        print(f"    Engines: {', '.join(config.get('engines', []))}")
        print(f"    Personas: {', '.join(config.get('personas', []))}")
        print(f"    Output Formats: {', '.join(config.get('output_formats', []))}")
        print(f"    Locales: {', '.join(config.get('locales', []))}")
        print(f"    API Calls/Month: {config.get('api_calls_per_month', 'N/A')}")
        print(f"    Strategies Limit: {config.get('strategies_limit', 'N/A')}")
        print()


def run_tenants_show(manager: TenantManager, tenant_id: str):
    """Show detailed tenant configuration."""
    print(f"\n  Tenant Details: {tenant_id}")
    print("  " + "=" * 60)
    print()

    config = manager.get(tenant_id)

    if not config:
        print(f"  Tenant not found: {tenant_id}")
        print()
        return

    print(f"  ID:            {config.tenant_id}")
    print(f"  Name:          {config.name}")
    print(f"  Tier:          {config.tier}")
    print()

    print("  Features:")
    if config.features:
        for key, value in config.features.items():
            status = "Enabled" if value else "Disabled"
            print(f"    {key}: {status}")
    else:
        print("    (none)")
    print()

    print(f"  Collectors:    {', '.join(config.collectors)}")
    print(f"  Engines:       {', '.join(config.engines)}")
    print(f"  Personas:      {', '.join(config.personas)}")
    print(f"  Output Formats: {', '.join(config.output_formats)}")
    print(f"  Locales:       {', '.join(config.locales)}")
    print()

    api_limit = "Unlimited" if config.api_calls_per_month == -1 else str(config.api_calls_per_month)
    strat_limit = "Unlimited" if config.strategies_limit == -1 else str(config.strategies_limit)
    print("  Limits:")
    print(f"    API Calls/Month:  {api_limit}")
    print(f"    Strategies Limit: {strat_limit}")
    print()

    if config.contact_email:
        print(f"  Contact: {config.contact_email}")
    if config.notes:
        print(f"  Notes:   {config.notes}")
    print()


def run_tenants_policy(manager: TenantManager, tenant_id: str):
    """Show data access policy for a tenant."""
    print(f"\n  Data Access Policy: {tenant_id}")
    print("  " + "=" * 60)
    print()

    config = manager.get(tenant_id)

    if not config:
        print(f"  Tenant not found: {tenant_id}")
        print()
        return

    client_tier = config.get_client_tier()
    explanation = DataAccessPolicy.explain_policy(client_tier)

    print(f"  Tier:         {explanation['tier']}")
    print(f"  Access Level: {explanation['access_level'].upper()}")
    print()
    print(f"  Description:")
    print(f"    {explanation['description']}")
    print()

    if explanation.get('reason'):
        print(f"  Reason:")
        print(f"    {explanation['reason']}")
        print()

    if explanation.get('blocked_fields'):
        print("  Blocked Data Fields:")
        for field in explanation['blocked_fields']:
            print(f"    - {field}")
        print()

    if explanation.get('aggregated_fields'):
        print("  Aggregated Data Fields:")
        for field in explanation['aggregated_fields']:
            print(f"    - {field}")
        print()

    # Show data access table
    print("  Data Access Summary:")
    print("  " + "-" * 50)
    print(f"  {'Data Type':<35} {'Access':<15}")
    print("  " + "-" * 50)

    test_fields = [
        ("estate_wallet_addresses", "Estate Wallet Addresses"),
        ("estate_wallet_balances", "Estate Wallet Balances"),
        ("whale_wallet_addresses", "Whale Wallet Addresses"),
        ("whale_real_time_movements", "Whale Real-Time Movements"),
        ("whale_activity_summary", "Whale Activity Summary"),
        ("estate_risk_score", "Estate Risk Score"),
        ("market_prices", "Market Prices"),
        ("fear_greed_index", "Fear & Greed Index"),
        ("strategy_performance", "Strategy Performance"),
    ]

    for field, label in test_fields:
        level = DataAccessPolicy.get_access_level(client_tier, field)
        if level == "full":
            access_str = "Full"
        elif level == "aggregated":
            access_str = "Aggregated"
        else:
            access_str = "BLOCKED"
        print(f"  {label:<35} {access_str:<15}")

    print()
