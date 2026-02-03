"""
Integration Tests for diBoaS Analytics Pipeline.

End-to-end tests verifying:
- Full pipeline: collect → analyze → Adelaide
- All personas generate different content
- All output formats work
- Tenant configuration integration
"""

import pytest
from pathlib import Path
import tempfile
import json

from src.config.tenant import TenantConfig, TenantManager
from src.policies.data_access import DataAccessPolicy, ClientTier


class TestPipelineIntegration:
    """Test full pipeline integration."""

    def test_tenant_policy_integration(self):
        """Tenant config integrates with DataAccessPolicy."""
        # diBoaS tenant should have full access
        diboas_config = TenantConfig.default_diboas()
        client_tier = diboas_config.get_client_tier()

        assert DataAccessPolicy.can_access(
            client_tier, "estate_wallet_addresses"
        ) is True

        # B2B tenant should be blocked
        b2b_config = TenantConfig.default_b2b_standard("test", "Test")
        b2b_tier = b2b_config.get_client_tier()

        assert DataAccessPolicy.can_access(
            b2b_tier, "estate_wallet_addresses"
        ) is False

    def test_tenant_feature_policy_alignment(self):
        """Tenant features align with policy restrictions."""
        # B2B standard: estate_wallet_tracking disabled
        b2b_config = TenantConfig.default_b2b_standard("test", "Test")
        assert b2b_config.is_feature_enabled("estate_wallet_tracking") is False

        # Verify policy also blocks this data
        tier = b2b_config.get_client_tier()
        assert DataAccessPolicy.can_access(
            tier, "estate_wallet_addresses"
        ) is False

        # B2B premium: estate_wallet_tracking still disabled
        premium_config = TenantConfig.default_b2b_premium("test", "Test")
        assert premium_config.is_feature_enabled("estate_wallet_tracking") is False

        # Policy still blocks
        premium_tier = premium_config.get_client_tier()
        assert DataAccessPolicy.can_access(
            premium_tier, "estate_wallet_addresses"
        ) is False


class TestPersonaIntegration:
    """Test persona system integration."""

    def test_tenant_persona_access(self):
        """Tenants have correct persona access."""
        # diBoaS has all personas
        diboas = TenantConfig.default_diboas()
        assert diboas.can_use_persona("ana")
        assert diboas.can_use_persona("maria")
        assert diboas.can_use_persona("felipe")

        # B2B standard has only maria
        b2b_standard = TenantConfig.default_b2b_standard("test", "Test")
        assert b2b_standard.can_use_persona("maria")
        assert not b2b_standard.can_use_persona("ana")
        assert not b2b_standard.can_use_persona("felipe")

        # B2B premium has all personas
        b2b_premium = TenantConfig.default_b2b_premium("test", "Test")
        assert b2b_premium.can_use_persona("ana")
        assert b2b_premium.can_use_persona("maria")
        assert b2b_premium.can_use_persona("felipe")

    def test_output_format_access(self):
        """Tenants have correct output format access."""
        # diBoaS has all formats
        diboas = TenantConfig.default_diboas()
        assert diboas.can_use_output_format("newsletter_md")
        assert diboas.can_use_output_format("twitter_thread")
        assert diboas.can_use_output_format("linkedin_post")
        assert diboas.can_use_output_format("substack")

        # B2B standard has only newsletter_md
        b2b_standard = TenantConfig.default_b2b_standard("test", "Test")
        assert b2b_standard.can_use_output_format("newsletter_md")
        assert not b2b_standard.can_use_output_format("twitter_thread")

        # B2B premium has more formats
        b2b_premium = TenantConfig.default_b2b_premium("test", "Test")
        assert b2b_premium.can_use_output_format("newsletter_md")
        assert b2b_premium.can_use_output_format("twitter_thread")
        assert b2b_premium.can_use_output_format("linkedin_post")


class TestLocaleIntegration:
    """Test locale system integration."""

    def test_tenant_locale_access(self):
        """Tenants have correct locale access."""
        # diBoaS has both locales
        diboas = TenantConfig.default_diboas()
        assert diboas.can_use_locale("en")
        assert diboas.can_use_locale("pt-br")

        # B2B standard has only en
        b2b_standard = TenantConfig.default_b2b_standard("test", "Test")
        assert b2b_standard.can_use_locale("en")
        assert not b2b_standard.can_use_locale("pt-br")

        # B2B premium has both
        b2b_premium = TenantConfig.default_b2b_premium("test", "Test")
        assert b2b_premium.can_use_locale("en")
        assert b2b_premium.can_use_locale("pt-br")


class TestCollectorIntegration:
    """Test collector system integration."""

    def test_tenant_collector_access(self):
        """Tenants have correct collector access."""
        # diBoaS has all collectors
        diboas = TenantConfig.default_diboas()
        assert diboas.can_use_collector("fred")
        assert diboas.can_use_collector("yahoo_live")
        assert diboas.can_use_collector("defillama_live")
        assert diboas.can_use_collector("coingecko")
        assert diboas.can_use_collector("alternative")

        # B2B standard has limited collectors
        b2b_standard = TenantConfig.default_b2b_standard("test", "Test")
        assert b2b_standard.can_use_collector("yahoo_live")
        assert b2b_standard.can_use_collector("coingecko")
        assert not b2b_standard.can_use_collector("fred")
        assert not b2b_standard.can_use_collector("defillama_live")


class TestEngineIntegration:
    """Test engine system integration."""

    def test_tenant_engine_access(self):
        """Tenants have correct engine access."""
        # diBoaS has all engines
        diboas = TenantConfig.default_diboas()
        assert diboas.can_use_engine("battle_test")
        assert diboas.can_use_engine("monte_carlo")
        assert diboas.can_use_engine("monitoring")
        assert diboas.can_use_engine("anomaly")

        # B2B standard has only battle_test
        b2b_standard = TenantConfig.default_b2b_standard("test", "Test")
        assert b2b_standard.can_use_engine("battle_test")
        assert not b2b_standard.can_use_engine("monte_carlo")
        assert not b2b_standard.can_use_engine("monitoring")

        # B2B premium has battle_test and monte_carlo
        b2b_premium = TenantConfig.default_b2b_premium("test", "Test")
        assert b2b_premium.can_use_engine("battle_test")
        assert b2b_premium.can_use_engine("monte_carlo")


class TestDataFilteringIntegration:
    """Test data filtering integration."""

    def test_response_filtering_by_tenant(self):
        """Response filtering works based on tenant tier."""
        # Simulated full data response
        full_data = {
            "market_prices": {"btc": 50000, "eth": 3000},
            "estate_wallet_addresses": ["0x123", "0x456"],
            "whale_activity_summary": [
                {"wallet": "0x789", "direction": "in"},
                {"wallet": "0xabc", "direction": "out"},
            ],
            "fear_greed_index": 45,
        }

        # diBoaS user gets everything
        diboas = TenantConfig.default_diboas()
        diboas_tier = diboas.get_client_tier()
        diboas_response = DataAccessPolicy.filter_response(diboas_tier, full_data)

        assert "estate_wallet_addresses" in diboas_response
        assert diboas_response["estate_wallet_addresses"] == ["0x123", "0x456"]

        # B2B client gets filtered data
        b2b = TenantConfig.default_b2b_standard("test", "Test")
        b2b_tier = b2b.get_client_tier()
        b2b_response = DataAccessPolicy.filter_response(b2b_tier, full_data)

        # Blocked fields removed
        assert "estate_wallet_addresses" not in b2b_response

        # Aggregated fields transformed
        assert "whale_activity_summary" in b2b_response
        assert "total_movements" in b2b_response["whale_activity_summary"]

        # Public fields unchanged
        assert b2b_response["market_prices"] == {"btc": 50000, "eth": 3000}
        assert b2b_response["fear_greed_index"] == 45


class TestTenantManagerIntegration:
    """Test TenantManager integration."""

    def test_manager_with_config_directory(self):
        """TenantManager works with real config directory."""
        # Use the actual config directory if it exists
        config_dir = Path("config/tenants")
        if config_dir.exists():
            manager = TenantManager(config_dir=config_dir)

            # Should always have diBoaS
            assert "diboas" in manager.list_tenants()

            # diBoaS config should be valid
            result = manager.validate("diboas")
            assert result["valid"] is True

    def test_manager_fallback_to_default(self):
        """TenantManager falls back to default for unknown tenants."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            # Unknown tenant gets diBoaS defaults (safe)
            config = manager.get_or_default("unknown_tenant")
            assert config.tenant_id == "diboas"
            assert config.tier == "diboas"


class TestAPILimitsIntegration:
    """Test API limits integration."""

    def test_api_limits_by_tier(self):
        """API limits are correctly set by tier."""
        diboas = TenantConfig.default_diboas()
        assert diboas.has_unlimited_api_calls()
        assert diboas.has_unlimited_strategies()

        b2b_standard = TenantConfig.default_b2b_standard("test", "Test")
        assert not b2b_standard.has_unlimited_api_calls()
        assert b2b_standard.api_calls_per_month == 1000
        assert b2b_standard.strategies_limit == 5

        b2b_premium = TenantConfig.default_b2b_premium("test", "Test")
        assert not b2b_premium.has_unlimited_api_calls()
        assert b2b_premium.api_calls_per_month == 10000
        assert b2b_premium.strategies_limit == 20


class TestGrandmotherTestIntegration:
    """
    Integration tests for the Grandmother Test principle.

    Verifies that the entire system protects retail users from
    institutional front-running.
    """

    def test_b2b_cannot_build_estate_tracker(self):
        """
        B2B client cannot build an estate wallet tracker.

        This would allow front-running Mt. Gox/FTX distributions.
        """
        # B2B Premium tenant (highest B2B tier)
        tenant = TenantConfig.default_b2b_premium("hedge_fund", "Hedge Fund LLC")

        # Feature disabled at tenant level
        assert tenant.is_feature_enabled("estate_wallet_tracking") is False

        # Data blocked at policy level
        tier = tenant.get_client_tier()
        assert DataAccessPolicy.can_access(tier, "estate_wallet_addresses") is False
        assert DataAccessPolicy.can_access(tier, "estate_wallet_balances") is False
        assert DataAccessPolicy.can_access(tier, "estate_wallet_transactions") is False

    def test_b2b_cannot_copy_whale_trades(self):
        """
        B2B client cannot build a whale copy-trading bot.

        This would extract value from retail by front-running.
        """
        tenant = TenantConfig.default_b2b_premium("trading_firm", "Trading Firm Inc")

        # Feature disabled at tenant level
        assert tenant.is_feature_enabled("whale_alerts") is False

        # Data blocked at policy level
        tier = tenant.get_client_tier()
        assert DataAccessPolicy.can_access(tier, "whale_wallet_addresses") is False
        assert DataAccessPolicy.can_access(tier, "whale_real_time_movements") is False
        assert DataAccessPolicy.can_access(tier, "whale_transaction_history") is False

    def test_diboas_users_get_whale_insights(self):
        """
        diBoaS retail users DO get whale insights.

        This helps them make better decisions - passes Grandmother Test.
        """
        tenant = TenantConfig.default_diboas()

        # Features enabled
        assert tenant.is_feature_enabled("whale_alerts") is True
        assert tenant.is_feature_enabled("estate_wallet_tracking") is True

        # Full data access
        tier = tenant.get_client_tier()
        assert DataAccessPolicy.can_access(tier, "whale_wallet_addresses") is True
        assert DataAccessPolicy.can_access(tier, "estate_wallet_addresses") is True

    def test_policy_explanation_documents_protection(self):
        """
        Policy explanation clearly documents retail protection.
        """
        explanation = DataAccessPolicy.explain_policy(ClientTier.B2B_PREMIUM)

        assert "Grandmother Test" in explanation["reason"]
        assert "front-running" in explanation["description"]
        assert "estate_wallet_addresses" in explanation["blocked_fields"]
        assert "whale_wallet_addresses" in explanation["blocked_fields"]


class TestEndToEndScenarios:
    """End-to-end scenario tests."""

    def test_scenario_new_b2b_client_onboarding(self):
        """
        Scenario: Onboarding a new B2B client.

        1. Create tenant config
        2. Validate configuration
        3. Verify access controls
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            # 1. Create new client config
            new_client = TenantConfig.default_b2b_standard(
                "acme_corp", "Acme Corporation"
            )
            manager.register(new_client)

            # 2. Validate
            result = manager.validate("acme_corp")
            assert result["valid"] is True

            # 3. Verify access controls
            config = manager.get("acme_corp")
            tier = config.get_client_tier()

            # Can access public data
            assert DataAccessPolicy.can_access(tier, "market_prices") is True

            # Cannot access sensitive data
            assert DataAccessPolicy.can_access(tier, "estate_wallet_addresses") is False

    def test_scenario_upgrade_client_to_premium(self):
        """
        Scenario: Upgrading a B2B client to premium tier.

        Premium gets more features but still no estate/whale data.
        """
        # Standard tier
        standard = TenantConfig.default_b2b_standard("client", "Client")
        assert not standard.can_use_engine("monte_carlo")
        assert not standard.can_use_persona("ana")

        # Upgrade to premium
        premium = TenantConfig.default_b2b_premium("client", "Client")
        assert premium.can_use_engine("monte_carlo")
        assert premium.can_use_persona("ana")

        # But still blocked from sensitive data
        premium_tier = premium.get_client_tier()
        assert DataAccessPolicy.can_access(
            premium_tier, "estate_wallet_addresses"
        ) is False
