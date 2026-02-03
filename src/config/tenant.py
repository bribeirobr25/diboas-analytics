"""
Tenant Configuration System for multi-client B2B support.

Supports multiple tenants with different:
- Feature flags
- Enabled collectors, engines, personas, outputs
- API limits
- Access tiers

Usage:
    manager = TenantManager()
    config = manager.get("diboas")
    print(config.personas)  # ['ana', 'maria', 'felipe']
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import yaml
import logging

from src.policies.data_access import ClientTier

logger = logging.getLogger(__name__)


@dataclass
class TenantConfig:
    """
    Configuration for a single tenant (client).

    Attributes:
        tenant_id: Unique identifier for the tenant
        name: Human-readable name
        tier: Access tier (diboas, b2b_standard, b2b_premium)
        features: Feature flags dictionary
        collectors: Enabled data collectors
        engines: Enabled analytics engines
        personas: Enabled Adelaide personas
        output_formats: Enabled output formats
        locales: Supported locales
        api_calls_per_month: Monthly API limit (-1 for unlimited)
        strategies_limit: Maximum strategies (-1 for unlimited)
    """

    tenant_id: str
    name: str
    tier: str = "b2b_standard"

    # Feature flags
    features: Dict[str, Any] = field(default_factory=dict)

    # Enabled components
    collectors: List[str] = field(default_factory=list)
    engines: List[str] = field(default_factory=list)
    personas: List[str] = field(default_factory=list)
    output_formats: List[str] = field(default_factory=list)
    locales: List[str] = field(default_factory=list)

    # Limits
    api_calls_per_month: int = 1000
    strategies_limit: int = 10

    # Optional metadata
    contact_email: Optional[str] = None
    created_at: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.tenant_id:
            raise ValueError("tenant_id is required")
        if not self.name:
            raise ValueError("name is required")

        # Set defaults if empty
        if not self.collectors:
            self.collectors = ["yahoo_live"]
        if not self.engines:
            self.engines = ["battle_test"]
        if not self.personas:
            self.personas = ["maria"]
        if not self.output_formats:
            self.output_formats = ["newsletter_md"]
        if not self.locales:
            self.locales = ["en"]

    @classmethod
    def load(cls, config_path: Path) -> 'TenantConfig':
        """
        Load tenant config from YAML file.

        Args:
            config_path: Path to YAML configuration file

        Returns:
            TenantConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        logger.debug(f"Loading tenant config from {config_path}")

        with open(config_path) as f:
            data = yaml.safe_load(f)

        if data is None:
            raise ValueError(f"Empty config file: {config_path}")

        return cls(**data)

    def save(self, config_path: Path) -> None:
        """
        Save tenant config to YAML file.

        Args:
            config_path: Path to save configuration
        """
        data = {
            'tenant_id': self.tenant_id,
            'name': self.name,
            'tier': self.tier,
            'features': self.features,
            'collectors': self.collectors,
            'engines': self.engines,
            'personas': self.personas,
            'output_formats': self.output_formats,
            'locales': self.locales,
            'api_calls_per_month': self.api_calls_per_month,
            'strategies_limit': self.strategies_limit,
        }

        if self.contact_email:
            data['contact_email'] = self.contact_email
        if self.created_at:
            data['created_at'] = self.created_at
        if self.notes:
            data['notes'] = self.notes

        with open(config_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Saved tenant config to {config_path}")

    def get_client_tier(self) -> ClientTier:
        """
        Get the ClientTier enum for this tenant.

        Returns:
            ClientTier enum value
        """
        tier_map = {
            'diboas': ClientTier.DIBOAS_USER,
            'diboas_user': ClientTier.DIBOAS_USER,
            'b2b_standard': ClientTier.B2B_STANDARD,
            'b2b_premium': ClientTier.B2B_PREMIUM,
            'internal': ClientTier.INTERNAL,
        }
        return tier_map.get(self.tier.lower(), ClientTier.B2B_STANDARD)

    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if a feature flag is enabled.

        Args:
            feature: Feature name to check

        Returns:
            True if enabled, False otherwise
        """
        return self.features.get(feature, False)

    def can_use_collector(self, collector: str) -> bool:
        """Check if tenant can use a specific collector."""
        return collector in self.collectors

    def can_use_engine(self, engine: str) -> bool:
        """Check if tenant can use a specific engine."""
        return engine in self.engines

    def can_use_persona(self, persona: str) -> bool:
        """Check if tenant can use a specific persona."""
        return persona in self.personas

    def can_use_output_format(self, format_name: str) -> bool:
        """Check if tenant can use a specific output format."""
        return format_name in self.output_formats

    def can_use_locale(self, locale: str) -> bool:
        """Check if tenant can use a specific locale."""
        return locale in self.locales

    def has_unlimited_api_calls(self) -> bool:
        """Check if tenant has unlimited API calls."""
        return self.api_calls_per_month == -1

    def has_unlimited_strategies(self) -> bool:
        """Check if tenant has unlimited strategies."""
        return self.strategies_limit == -1

    @classmethod
    def default_diboas(cls) -> 'TenantConfig':
        """
        Create default configuration for diBoaS platform.

        Returns:
            TenantConfig with full access for diBoaS users
        """
        return cls(
            tenant_id="diboas",
            name="diBoaS Platform",
            tier="diboas",
            features={
                "estate_wallet_tracking": True,
                "whale_alerts": True,
                "real_time_data": True,
                "custom_strategies": True,
                "advanced_analytics": True,
            },
            collectors=[
                "fred",
                "yahoo_live",
                "defillama_live",
                "coingecko",
                "alternative",
            ],
            engines=[
                "battle_test",
                "monte_carlo",
                "monitoring",
                "anomaly",
            ],
            personas=["ana", "maria", "felipe"],
            output_formats=[
                "newsletter_md",
                "twitter_thread",
                "linkedin_post",
                "website_teaser",
                "substack",
            ],
            locales=["en", "pt-br"],
            api_calls_per_month=-1,  # Unlimited
            strategies_limit=-1,  # Unlimited
        )

    @classmethod
    def default_b2b_standard(cls, tenant_id: str, name: str) -> 'TenantConfig':
        """
        Create default B2B standard configuration.

        Args:
            tenant_id: Unique tenant identifier
            name: Tenant display name

        Returns:
            TenantConfig with standard B2B access
        """
        return cls(
            tenant_id=tenant_id,
            name=name,
            tier="b2b_standard",
            features={
                "estate_wallet_tracking": False,  # Blocked
                "whale_alerts": False,  # Blocked
                "real_time_data": False,
                "custom_strategies": False,
                "advanced_analytics": False,
            },
            collectors=["yahoo_live", "coingecko"],
            engines=["battle_test"],
            personas=["maria"],
            output_formats=["newsletter_md"],
            locales=["en"],
            api_calls_per_month=1000,
            strategies_limit=5,
        )

    @classmethod
    def default_b2b_premium(cls, tenant_id: str, name: str) -> 'TenantConfig':
        """
        Create default B2B premium configuration.

        Args:
            tenant_id: Unique tenant identifier
            name: Tenant display name

        Returns:
            TenantConfig with premium B2B access
        """
        return cls(
            tenant_id=tenant_id,
            name=name,
            tier="b2b_premium",
            features={
                "estate_wallet_tracking": False,  # Still blocked!
                "whale_alerts": False,  # Still blocked!
                "real_time_data": True,
                "custom_strategies": True,
                "advanced_analytics": True,
            },
            collectors=["fred", "yahoo_live", "defillama_live", "coingecko", "alternative"],
            engines=["battle_test", "monte_carlo"],
            personas=["ana", "maria", "felipe"],
            output_formats=["newsletter_md", "twitter_thread", "linkedin_post"],
            locales=["en", "pt-br"],
            api_calls_per_month=10000,
            strategies_limit=20,
        )


class TenantManager:
    """
    Manage multiple tenants.

    Usage:
        manager = TenantManager()
        config = manager.get("diboas")

        for tenant_id in manager.list_tenants():
            print(manager.get(tenant_id).name)
    """

    def __init__(self, config_dir: Path = None):
        """
        Initialize tenant manager.

        Args:
            config_dir: Directory containing tenant YAML configs
        """
        if config_dir is None:
            config_dir = Path("config/tenants")
        self.config_dir = Path(config_dir)
        self._tenants: Dict[str, TenantConfig] = {}
        self._load_tenants()

    def _load_tenants(self):
        """Load all tenant configs from directory."""
        # Always include default diBoaS config
        self._tenants["diboas"] = TenantConfig.default_diboas()
        logger.debug("Loaded default diBoaS tenant config")

        # Load additional tenant configs from YAML files
        if self.config_dir.exists():
            for config_file in self.config_dir.glob("*.yaml"):
                try:
                    tenant = TenantConfig.load(config_file)
                    self._tenants[tenant.tenant_id] = tenant
                    logger.info(f"Loaded tenant config: {tenant.tenant_id} from {config_file}")
                except Exception as e:
                    logger.error(f"Failed to load tenant config {config_file}: {e}")
        else:
            logger.debug(f"Tenant config directory not found: {self.config_dir}")

    def get(self, tenant_id: str) -> Optional[TenantConfig]:
        """
        Get tenant configuration by ID.

        Args:
            tenant_id: Tenant identifier

        Returns:
            TenantConfig or None if not found
        """
        return self._tenants.get(tenant_id)

    def get_or_default(self, tenant_id: str) -> TenantConfig:
        """
        Get tenant configuration, falling back to diBoaS default.

        Args:
            tenant_id: Tenant identifier

        Returns:
            TenantConfig (never None)
        """
        return self._tenants.get(tenant_id, self._tenants["diboas"])

    def list_tenants(self) -> List[str]:
        """
        List all registered tenant IDs.

        Returns:
            Sorted list of tenant IDs
        """
        return sorted(self._tenants.keys())

    def register(self, config: TenantConfig) -> None:
        """
        Register a new tenant configuration.

        Args:
            config: Tenant configuration to register
        """
        self._tenants[config.tenant_id] = config
        logger.info(f"Registered tenant: {config.tenant_id}")

    def unregister(self, tenant_id: str) -> bool:
        """
        Unregister a tenant.

        Args:
            tenant_id: Tenant to unregister

        Returns:
            True if removed, False if not found
        """
        if tenant_id == "diboas":
            logger.warning("Cannot unregister default diBoaS tenant")
            return False

        if tenant_id in self._tenants:
            del self._tenants[tenant_id]
            logger.info(f"Unregistered tenant: {tenant_id}")
            return True
        return False

    def reload(self) -> None:
        """Reload all tenant configurations from disk."""
        self._tenants.clear()
        self._load_tenants()
        logger.info(f"Reloaded {len(self._tenants)} tenant configs")

    def validate(self, tenant_id: str) -> Dict[str, Any]:
        """
        Validate a tenant configuration.

        Args:
            tenant_id: Tenant to validate

        Returns:
            Validation result dictionary
        """
        config = self.get(tenant_id)
        if not config:
            return {
                "valid": False,
                "tenant_id": tenant_id,
                "errors": ["Tenant not found"],
            }

        errors = []
        warnings = []

        # Check required fields
        if not config.tenant_id:
            errors.append("Missing tenant_id")
        if not config.name:
            errors.append("Missing name")

        # Check tier validity
        valid_tiers = ["diboas", "b2b_standard", "b2b_premium", "internal"]
        if config.tier not in valid_tiers:
            errors.append(f"Invalid tier: {config.tier}. Must be one of {valid_tiers}")

        # Check component availability
        valid_personas = ["ana", "maria", "felipe"]
        for persona in config.personas:
            if persona not in valid_personas:
                warnings.append(f"Unknown persona: {persona}")

        valid_formats = ["newsletter_md", "twitter_thread", "linkedin_post", "website_teaser", "substack"]
        for fmt in config.output_formats:
            if fmt not in valid_formats:
                warnings.append(f"Unknown output format: {fmt}")

        valid_locales = ["en", "pt-br"]
        for locale in config.locales:
            if locale not in valid_locales:
                warnings.append(f"Unknown locale: {locale}")

        return {
            "valid": len(errors) == 0,
            "tenant_id": tenant_id,
            "errors": errors,
            "warnings": warnings,
            "config": {
                "name": config.name,
                "tier": config.tier,
                "collectors": config.collectors,
                "engines": config.engines,
                "personas": config.personas,
                "output_formats": config.output_formats,
                "locales": config.locales,
                "api_calls_per_month": config.api_calls_per_month,
                "strategies_limit": config.strategies_limit,
            }
        }
