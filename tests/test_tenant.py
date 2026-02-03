"""
Tests for Tenant Configuration System.

Verifies multi-tenant support for B2B clients with:
- YAML configuration loading
- Feature flags
- Component access control
- API limits
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from src.config.tenant import TenantConfig, TenantManager
from src.policies.data_access import ClientTier


class TestTenantConfigCreation:
    """Test TenantConfig dataclass creation."""

    def test_create_minimal_config(self):
        """Create config with minimal required fields."""
        config = TenantConfig(
            tenant_id="test_client",
            name="Test Client Inc.",
        )
        assert config.tenant_id == "test_client"
        assert config.name == "Test Client Inc."
        assert config.tier == "b2b_standard"  # Default

    def test_create_full_config(self):
        """Create config with all fields specified."""
        config = TenantConfig(
            tenant_id="premium_client",
            name="Premium Corp",
            tier="b2b_premium",
            features={"custom_strategies": True},
            collectors=["fred", "yahoo_live"],
            engines=["battle_test", "monte_carlo"],
            personas=["ana", "maria"],
            output_formats=["newsletter_md", "twitter_thread"],
            locales=["en", "pt-br"],
            api_calls_per_month=10000,
            strategies_limit=20,
            contact_email="support@premium.com",
            notes="Premium tier client",
        )
        assert config.tier == "b2b_premium"
        assert "custom_strategies" in config.features
        assert config.api_calls_per_month == 10000

    def test_config_requires_tenant_id(self):
        """Config must have tenant_id."""
        with pytest.raises(ValueError, match="tenant_id is required"):
            TenantConfig(tenant_id="", name="Test")

    def test_config_requires_name(self):
        """Config must have name."""
        with pytest.raises(ValueError, match="name is required"):
            TenantConfig(tenant_id="test", name="")

    def test_defaults_populated(self):
        """Empty lists get sensible defaults."""
        config = TenantConfig(
            tenant_id="test",
            name="Test",
            collectors=[],
            engines=[],
            personas=[],
            output_formats=[],
            locales=[],
        )
        # Defaults should be populated
        assert "yahoo_live" in config.collectors
        assert "battle_test" in config.engines
        assert "maria" in config.personas
        assert "newsletter_md" in config.output_formats
        assert "en" in config.locales


class TestDefaultConfigs:
    """Test factory methods for default configurations."""

    def test_default_diboas_config(self):
        """Default diBoaS config has full access."""
        config = TenantConfig.default_diboas()

        assert config.tenant_id == "diboas"
        assert config.tier == "diboas"

        # Full feature access
        assert config.features["estate_wallet_tracking"] is True
        assert config.features["whale_alerts"] is True
        assert config.features["real_time_data"] is True

        # All collectors
        assert "fred" in config.collectors
        assert "yahoo_live" in config.collectors
        assert "defillama_live" in config.collectors

        # All personas
        assert "ana" in config.personas
        assert "maria" in config.personas
        assert "felipe" in config.personas

        # Unlimited
        assert config.api_calls_per_month == -1
        assert config.strategies_limit == -1

    def test_default_b2b_standard_config(self):
        """Default B2B standard config has limited access."""
        config = TenantConfig.default_b2b_standard("acme", "Acme Corp")

        assert config.tenant_id == "acme"
        assert config.name == "Acme Corp"
        assert config.tier == "b2b_standard"

        # Estate/whale features blocked
        assert config.features["estate_wallet_tracking"] is False
        assert config.features["whale_alerts"] is False

        # Limited collectors
        assert "yahoo_live" in config.collectors
        assert "fred" not in config.collectors

        # Limited personas
        assert "maria" in config.personas
        assert "ana" not in config.personas

        # API limits
        assert config.api_calls_per_month == 1000
        assert config.strategies_limit == 5

    def test_default_b2b_premium_config(self):
        """Default B2B premium config has more access but still restricted."""
        config = TenantConfig.default_b2b_premium("bigcorp", "Big Corp LLC")

        assert config.tenant_id == "bigcorp"
        assert config.tier == "b2b_premium"

        # Estate/whale STILL blocked even for premium
        assert config.features["estate_wallet_tracking"] is False
        assert config.features["whale_alerts"] is False

        # But other advanced features enabled
        assert config.features["real_time_data"] is True
        assert config.features["custom_strategies"] is True

        # More collectors
        assert "fred" in config.collectors
        assert "defillama_live" in config.collectors

        # All personas
        assert "ana" in config.personas
        assert "maria" in config.personas
        assert "felipe" in config.personas

        # Higher limits
        assert config.api_calls_per_month == 10000
        assert config.strategies_limit == 20


class TestClientTierMapping:
    """Test mapping to ClientTier enum."""

    def test_diboas_tier_mapping(self):
        """diBoaS tier maps to DIBOAS_USER."""
        config = TenantConfig.default_diboas()
        assert config.get_client_tier() == ClientTier.DIBOAS_USER

    def test_b2b_standard_tier_mapping(self):
        """b2b_standard tier maps correctly."""
        config = TenantConfig.default_b2b_standard("test", "Test")
        assert config.get_client_tier() == ClientTier.B2B_STANDARD

    def test_b2b_premium_tier_mapping(self):
        """b2b_premium tier maps correctly."""
        config = TenantConfig.default_b2b_premium("test", "Test")
        assert config.get_client_tier() == ClientTier.B2B_PREMIUM

    def test_internal_tier_mapping(self):
        """internal tier maps correctly."""
        config = TenantConfig(
            tenant_id="internal_tool",
            name="Internal Tool",
            tier="internal",
        )
        assert config.get_client_tier() == ClientTier.INTERNAL

    def test_unknown_tier_defaults_to_b2b_standard(self):
        """Unknown tier defaults to B2B standard (safe default)."""
        config = TenantConfig(
            tenant_id="unknown",
            name="Unknown",
            tier="unknown_tier",
        )
        assert config.get_client_tier() == ClientTier.B2B_STANDARD


class TestFeatureFlags:
    """Test feature flag checking."""

    def test_feature_enabled(self):
        """Check if feature is enabled."""
        config = TenantConfig.default_diboas()
        assert config.is_feature_enabled("estate_wallet_tracking") is True
        assert config.is_feature_enabled("whale_alerts") is True

    def test_feature_disabled(self):
        """Check if feature is disabled."""
        config = TenantConfig.default_b2b_standard("test", "Test")
        assert config.is_feature_enabled("estate_wallet_tracking") is False
        assert config.is_feature_enabled("whale_alerts") is False

    def test_unknown_feature_returns_false(self):
        """Unknown features return False by default."""
        config = TenantConfig.default_diboas()
        assert config.is_feature_enabled("nonexistent_feature") is False


class TestComponentAccess:
    """Test component access checking."""

    def test_can_use_collector(self):
        """Check collector access."""
        config = TenantConfig.default_diboas()
        assert config.can_use_collector("fred") is True
        assert config.can_use_collector("yahoo_live") is True
        assert config.can_use_collector("nonexistent") is False

    def test_can_use_engine(self):
        """Check engine access."""
        config = TenantConfig.default_diboas()
        assert config.can_use_engine("battle_test") is True
        assert config.can_use_engine("monte_carlo") is True
        assert config.can_use_engine("nonexistent") is False

    def test_can_use_persona(self):
        """Check persona access."""
        config = TenantConfig.default_diboas()
        assert config.can_use_persona("ana") is True
        assert config.can_use_persona("maria") is True
        assert config.can_use_persona("felipe") is True
        assert config.can_use_persona("nonexistent") is False

    def test_can_use_output_format(self):
        """Check output format access."""
        config = TenantConfig.default_diboas()
        assert config.can_use_output_format("newsletter_md") is True
        assert config.can_use_output_format("twitter_thread") is True
        assert config.can_use_output_format("nonexistent") is False

    def test_can_use_locale(self):
        """Check locale access."""
        config = TenantConfig.default_diboas()
        assert config.can_use_locale("en") is True
        assert config.can_use_locale("pt-br") is True
        assert config.can_use_locale("es") is False


class TestLimits:
    """Test API and strategy limits."""

    def test_unlimited_api_calls(self):
        """Check unlimited API calls."""
        config = TenantConfig.default_diboas()
        assert config.has_unlimited_api_calls() is True

        config_limited = TenantConfig.default_b2b_standard("test", "Test")
        assert config_limited.has_unlimited_api_calls() is False

    def test_unlimited_strategies(self):
        """Check unlimited strategies."""
        config = TenantConfig.default_diboas()
        assert config.has_unlimited_strategies() is True

        config_limited = TenantConfig.default_b2b_standard("test", "Test")
        assert config_limited.has_unlimited_strategies() is False


class TestYAMLSerialization:
    """Test YAML save/load functionality."""

    def test_save_and_load_config(self):
        """Save and load config from YAML file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test_tenant.yaml"

            # Create and save config
            original = TenantConfig(
                tenant_id="yaml_test",
                name="YAML Test Client",
                tier="b2b_premium",
                features={"custom_strategies": True, "real_time_data": False},
                collectors=["yahoo_live", "coingecko"],
                engines=["battle_test"],
                personas=["ana", "maria"],
                output_formats=["newsletter_md"],
                locales=["en"],
                api_calls_per_month=5000,
                strategies_limit=10,
                contact_email="test@example.com",
                notes="Test notes",
            )
            original.save(config_path)

            # Load and verify
            loaded = TenantConfig.load(config_path)
            assert loaded.tenant_id == original.tenant_id
            assert loaded.name == original.name
            assert loaded.tier == original.tier
            assert loaded.features == original.features
            assert loaded.collectors == original.collectors
            assert loaded.api_calls_per_month == original.api_calls_per_month
            assert loaded.contact_email == original.contact_email

    def test_load_nonexistent_file_raises(self):
        """Loading nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            TenantConfig.load(Path("/nonexistent/path/config.yaml"))

    def test_load_empty_file_raises(self):
        """Loading empty file raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "empty.yaml"
            config_path.write_text("")

            with pytest.raises(ValueError, match="Empty config file"):
                TenantConfig.load(config_path)


class TestTenantManager:
    """Test TenantManager class."""

    def test_manager_loads_default_diboas(self):
        """Manager always has default diBoaS config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            diboas = manager.get("diboas")
            assert diboas is not None
            assert diboas.tenant_id == "diboas"
            assert diboas.tier == "diboas"

    def test_manager_lists_tenants(self):
        """Manager lists all registered tenants."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            tenants = manager.list_tenants()
            assert "diboas" in tenants
            assert tenants == sorted(tenants)  # Should be sorted

    def test_manager_get_or_default(self):
        """Manager returns default for unknown tenant."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            # Unknown tenant gets diBoaS default
            config = manager.get_or_default("nonexistent")
            assert config.tenant_id == "diboas"

    def test_manager_register_tenant(self):
        """Manager can register new tenants."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            new_config = TenantConfig(
                tenant_id="new_client",
                name="New Client Corp",
            )
            manager.register(new_config)

            assert "new_client" in manager.list_tenants()
            assert manager.get("new_client") == new_config

    def test_manager_unregister_tenant(self):
        """Manager can unregister tenants."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            # Register then unregister
            config = TenantConfig(tenant_id="temp", name="Temp")
            manager.register(config)
            assert "temp" in manager.list_tenants()

            result = manager.unregister("temp")
            assert result is True
            assert "temp" not in manager.list_tenants()

    def test_manager_cannot_unregister_diboas(self):
        """Manager cannot unregister default diBoaS tenant."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            result = manager.unregister("diboas")
            assert result is False
            assert "diboas" in manager.list_tenants()

    def test_manager_loads_yaml_configs(self):
        """Manager loads configs from YAML files in directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Create a YAML config file
            yaml_config = {
                "tenant_id": "yaml_client",
                "name": "YAML Client",
                "tier": "b2b_standard",
                "collectors": ["yahoo_live"],
                "engines": ["battle_test"],
                "personas": ["maria"],
                "output_formats": ["newsletter_md"],
                "locales": ["en"],
            }
            with open(config_dir / "yaml_client.yaml", "w") as f:
                yaml.dump(yaml_config, f)

            # Manager should load it
            manager = TenantManager(config_dir=config_dir)
            assert "yaml_client" in manager.list_tenants()

            loaded = manager.get("yaml_client")
            assert loaded.name == "YAML Client"
            assert loaded.tier == "b2b_standard"


class TestTenantValidation:
    """Test tenant configuration validation."""

    def test_validate_valid_tenant(self):
        """Valid tenant passes validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            result = manager.validate("diboas")
            assert result["valid"] is True
            assert result["tenant_id"] == "diboas"
            assert len(result["errors"]) == 0

    def test_validate_nonexistent_tenant(self):
        """Nonexistent tenant fails validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            result = manager.validate("nonexistent")
            assert result["valid"] is False
            assert "Tenant not found" in result["errors"]

    def test_validate_unknown_persona_warning(self):
        """Unknown persona generates warning."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            config = TenantConfig(
                tenant_id="test_warn",
                name="Test Warning",
                personas=["ana", "unknown_persona"],
            )
            manager.register(config)

            result = manager.validate("test_warn")
            assert result["valid"] is True  # Still valid
            assert any("unknown_persona" in w for w in result["warnings"])

    def test_validate_invalid_tier_error(self):
        """Invalid tier generates error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TenantManager(config_dir=Path(tmpdir))

            config = TenantConfig(
                tenant_id="test_invalid",
                name="Test Invalid",
                tier="invalid_tier",
            )
            manager.register(config)

            result = manager.validate("test_invalid")
            assert result["valid"] is False
            assert any("Invalid tier" in e for e in result["errors"])


class TestTenantManagerReload:
    """Test tenant manager reload functionality."""

    def test_reload_picks_up_new_files(self):
        """Reload picks up newly added config files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            manager = TenantManager(config_dir=config_dir)

            # Initially just diBoaS
            assert "new_tenant" not in manager.list_tenants()

            # Add a new config file
            yaml_config = {
                "tenant_id": "new_tenant",
                "name": "New Tenant",
                "tier": "b2b_standard",
            }
            with open(config_dir / "new_tenant.yaml", "w") as f:
                yaml.dump(yaml_config, f)

            # Reload
            manager.reload()

            # Now should have new tenant
            assert "new_tenant" in manager.list_tenants()
