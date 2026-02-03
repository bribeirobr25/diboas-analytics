"""
Tests for DataAccessPolicy - Ethical B2B guardrails.

Verifies the Grandmother Test:
"Would this help my grandmother build wealth, or help sophisticated
players extract value from her?"

Key test cases:
- diBoaS users can access ALL data including estate/whale wallets
- B2B clients CANNOT access estate/whale wallet data
- B2B clients get aggregated versions of sensitive data
- Internal tier has full access
"""

import pytest
from src.policies.data_access import (
    DataAccessPolicy,
    ClientTier,
    validate_access,
)


class TestClientTier:
    """Test ClientTier enum values."""

    def test_client_tier_values(self):
        """Verify all client tier values exist."""
        assert ClientTier.DIBOAS_USER.value == "diboas_user"
        assert ClientTier.B2B_STANDARD.value == "b2b_standard"
        assert ClientTier.B2B_PREMIUM.value == "b2b_premium"
        assert ClientTier.INTERNAL.value == "internal"

    def test_client_tier_count(self):
        """Verify correct number of tiers."""
        assert len(ClientTier) == 4


class TestBlockedDataAccess:
    """Test that B2B clients cannot access sensitive data."""

    @pytest.mark.parametrize("blocked_field", [
        "estate_wallet_addresses",
        "estate_wallet_balances",
        "estate_wallet_transactions",
        "whale_wallet_addresses",
        "whale_real_time_movements",
        "whale_transaction_history",
        "individual_wallet_data",
    ])
    def test_b2b_standard_cannot_access_blocked_data(self, blocked_field):
        """B2B standard clients cannot access estate/whale wallet data."""
        assert DataAccessPolicy.can_access(
            ClientTier.B2B_STANDARD, blocked_field
        ) is False

    @pytest.mark.parametrize("blocked_field", [
        "estate_wallet_addresses",
        "estate_wallet_balances",
        "estate_wallet_transactions",
        "whale_wallet_addresses",
        "whale_real_time_movements",
        "whale_transaction_history",
        "individual_wallet_data",
    ])
    def test_b2b_premium_cannot_access_blocked_data(self, blocked_field):
        """B2B premium clients ALSO cannot access estate/whale wallet data."""
        # The Grandmother Test: Premium B2B still blocked from sensitive data
        assert DataAccessPolicy.can_access(
            ClientTier.B2B_PREMIUM, blocked_field
        ) is False


class TestFullAccess:
    """Test that diBoaS users and internal tools have full access."""

    @pytest.mark.parametrize("data_type", [
        "estate_wallet_addresses",
        "estate_wallet_balances",
        "whale_wallet_addresses",
        "whale_real_time_movements",
        "market_prices",
        "fear_greed_index",
        "anything_else",
    ])
    def test_diboas_users_can_access_all_data(self, data_type):
        """diBoaS users can access ALL data including estate/whale wallets."""
        assert DataAccessPolicy.can_access(
            ClientTier.DIBOAS_USER, data_type
        ) is True

    @pytest.mark.parametrize("data_type", [
        "estate_wallet_addresses",
        "estate_wallet_balances",
        "whale_wallet_addresses",
        "whale_real_time_movements",
        "market_prices",
        "fear_greed_index",
    ])
    def test_internal_tier_can_access_all_data(self, data_type):
        """Internal tier has full access."""
        assert DataAccessPolicy.can_access(
            ClientTier.INTERNAL, data_type
        ) is True


class TestPublicDataAccess:
    """Test that public data is accessible to all tiers."""

    @pytest.mark.parametrize("public_field", [
        "market_prices",
        "fear_greed_index",
        "vix",
        "credit_spreads",
        "protocol_tvl",
        "strategy_performance",
        "historical_backtest",
        "monte_carlo_results",
    ])
    def test_b2b_standard_can_access_public_data(self, public_field):
        """B2B standard clients can access public market data."""
        assert DataAccessPolicy.can_access(
            ClientTier.B2B_STANDARD, public_field
        ) is True

    @pytest.mark.parametrize("public_field", [
        "market_prices",
        "fear_greed_index",
        "vix",
        "credit_spreads",
        "protocol_tvl",
        "strategy_performance",
        "historical_backtest",
        "monte_carlo_results",
    ])
    def test_b2b_premium_can_access_public_data(self, public_field):
        """B2B premium clients can access public market data."""
        assert DataAccessPolicy.can_access(
            ClientTier.B2B_PREMIUM, public_field
        ) is True


class TestAccessLevel:
    """Test get_access_level method."""

    def test_diboas_user_always_full(self):
        """diBoaS users always get full access level."""
        assert DataAccessPolicy.get_access_level(
            ClientTier.DIBOAS_USER, "estate_wallet_addresses"
        ) == "full"
        assert DataAccessPolicy.get_access_level(
            ClientTier.DIBOAS_USER, "market_prices"
        ) == "full"

    def test_internal_always_full(self):
        """Internal tier always gets full access level."""
        assert DataAccessPolicy.get_access_level(
            ClientTier.INTERNAL, "whale_wallet_addresses"
        ) == "full"

    def test_b2b_blocked_level(self):
        """B2B gets 'blocked' for sensitive data."""
        assert DataAccessPolicy.get_access_level(
            ClientTier.B2B_STANDARD, "estate_wallet_addresses"
        ) == "blocked"
        assert DataAccessPolicy.get_access_level(
            ClientTier.B2B_PREMIUM, "whale_wallet_addresses"
        ) == "blocked"

    def test_b2b_aggregated_level(self):
        """B2B gets 'aggregated' for semi-sensitive data."""
        assert DataAccessPolicy.get_access_level(
            ClientTier.B2B_STANDARD, "whale_activity_summary"
        ) == "aggregated"
        assert DataAccessPolicy.get_access_level(
            ClientTier.B2B_PREMIUM, "estate_risk_score"
        ) == "aggregated"

    def test_b2b_full_for_public(self):
        """B2B gets 'full' for public data."""
        assert DataAccessPolicy.get_access_level(
            ClientTier.B2B_STANDARD, "market_prices"
        ) == "full"


class TestFilterResponse:
    """Test response filtering for B2B clients."""

    def test_diboas_user_gets_full_response(self):
        """diBoaS users receive unfiltered response."""
        full_data = {
            "market_prices": {"btc": 50000},
            "estate_wallet_addresses": ["0x123", "0x456"],
            "whale_activity_summary": [{"wallet": "0x789", "direction": "in"}],
        }
        filtered = DataAccessPolicy.filter_response(
            ClientTier.DIBOAS_USER, full_data
        )
        assert filtered == full_data

    def test_internal_gets_full_response(self):
        """Internal tier receives unfiltered response."""
        full_data = {
            "estate_wallet_balances": {"0x123": 1000000},
            "whale_real_time_movements": [{"tx": "0xabc"}],
        }
        filtered = DataAccessPolicy.filter_response(
            ClientTier.INTERNAL, full_data
        )
        assert filtered == full_data

    def test_b2b_blocked_fields_removed(self):
        """B2B clients have blocked fields completely removed."""
        full_data = {
            "market_prices": {"btc": 50000},
            "estate_wallet_addresses": ["0x123", "0x456"],
            "whale_wallet_addresses": ["0x789"],
        }
        filtered = DataAccessPolicy.filter_response(
            ClientTier.B2B_STANDARD, full_data
        )

        # Blocked fields should be removed
        assert "estate_wallet_addresses" not in filtered
        assert "whale_wallet_addresses" not in filtered

        # Public fields should remain
        assert "market_prices" in filtered
        assert filtered["market_prices"] == {"btc": 50000}

    def test_b2b_aggregated_fields_transformed(self):
        """B2B clients get aggregated versions of sensitive data."""
        full_data = {
            "whale_activity_summary": [
                {"wallet": "0x123", "direction": "in"},
                {"wallet": "0x456", "direction": "out"},
                {"wallet": "0x789", "direction": "in"},
            ],
        }
        filtered = DataAccessPolicy.filter_response(
            ClientTier.B2B_STANDARD, full_data
        )

        # Should be aggregated, not individual wallets
        summary = filtered["whale_activity_summary"]
        assert "total_movements" in summary
        assert summary["total_movements"] == 3
        assert "net_direction" in summary
        assert "note" in summary
        assert "individual wallets not disclosed" in summary["note"].lower()

    def test_b2b_estate_risk_score_aggregated(self):
        """Estate risk score is converted to categories for B2B."""
        # Low risk
        filtered_low = DataAccessPolicy.filter_response(
            ClientTier.B2B_STANDARD, {"estate_risk_score": 25}
        )
        assert filtered_low["estate_risk_score"]["risk_level"] == "low"

        # Medium risk
        filtered_med = DataAccessPolicy.filter_response(
            ClientTier.B2B_STANDARD, {"estate_risk_score": 50}
        )
        assert filtered_med["estate_risk_score"]["risk_level"] == "medium"

        # High risk
        filtered_high = DataAccessPolicy.filter_response(
            ClientTier.B2B_STANDARD, {"estate_risk_score": 85}
        )
        assert filtered_high["estate_risk_score"]["risk_level"] == "high"


class TestPolicyExplanation:
    """Test policy explanation method."""

    def test_diboas_user_explanation(self):
        """diBoaS user gets full access explanation."""
        explanation = DataAccessPolicy.explain_policy(ClientTier.DIBOAS_USER)
        assert explanation["tier"] == "diboas_user"
        assert explanation["access_level"] == "full"
        assert explanation["blocked_fields"] == []
        assert explanation["aggregated_fields"] == []

    def test_internal_explanation(self):
        """Internal tier gets full access explanation."""
        explanation = DataAccessPolicy.explain_policy(ClientTier.INTERNAL)
        assert explanation["access_level"] == "full"

    def test_b2b_standard_explanation(self):
        """B2B standard gets restricted access explanation."""
        explanation = DataAccessPolicy.explain_policy(ClientTier.B2B_STANDARD)
        assert explanation["access_level"] == "restricted"
        assert len(explanation["blocked_fields"]) > 0
        assert "estate_wallet_addresses" in explanation["blocked_fields"]
        assert "Grandmother Test" in explanation["reason"]

    def test_b2b_premium_explanation(self):
        """B2B premium also gets restricted explanation (still blocked)."""
        explanation = DataAccessPolicy.explain_policy(ClientTier.B2B_PREMIUM)
        assert explanation["access_level"] == "restricted"
        assert "estate_wallet_addresses" in explanation["blocked_fields"]


class TestValidateAccess:
    """Test the validate_access utility function."""

    def test_validate_multiple_fields(self):
        """Validate access to multiple fields at once."""
        fields = [
            "market_prices",
            "estate_wallet_addresses",
            "whale_activity_summary",
        ]
        result = validate_access(ClientTier.B2B_STANDARD, fields)

        assert result["market_prices"] == "full"
        assert result["estate_wallet_addresses"] == "blocked"
        assert result["whale_activity_summary"] == "aggregated"

    def test_validate_diboas_all_full(self):
        """diBoaS user gets full access to all fields."""
        fields = ["estate_wallet_addresses", "whale_wallet_addresses"]
        result = validate_access(ClientTier.DIBOAS_USER, fields)

        assert all(level == "full" for level in result.values())


class TestBlockedFieldsLists:
    """Test the helper methods for listing blocked/aggregated fields."""

    def test_get_blocked_fields(self):
        """Get list of blocked fields."""
        blocked = DataAccessPolicy.get_blocked_fields()
        assert "estate_wallet_addresses" in blocked
        assert "whale_wallet_addresses" in blocked
        assert isinstance(blocked, list)
        assert blocked == sorted(blocked)  # Should be sorted

    def test_get_aggregated_fields(self):
        """Get list of aggregated fields."""
        aggregated = DataAccessPolicy.get_aggregated_fields()
        assert "whale_activity_summary" in aggregated
        assert "estate_risk_score" in aggregated
        assert isinstance(aggregated, list)
        assert aggregated == sorted(aggregated)  # Should be sorted


class TestGrandmotherTestScenarios:
    """
    Scenario-based tests for the Grandmother Test.

    These tests verify that the policy protects retail users from
    institutional front-running in realistic scenarios.
    """

    def test_scenario_mtgox_distribution_protection(self):
        """
        Scenario: Mt. Gox estate is about to distribute BTC.
        B2B clients should NOT be able to front-run this.
        """
        # B2B client requests estate wallet data
        can_access_addresses = DataAccessPolicy.can_access(
            ClientTier.B2B_PREMIUM, "estate_wallet_addresses"
        )
        can_access_balances = DataAccessPolicy.can_access(
            ClientTier.B2B_PREMIUM, "estate_wallet_balances"
        )
        can_access_txs = DataAccessPolicy.can_access(
            ClientTier.B2B_PREMIUM, "estate_wallet_transactions"
        )

        # All blocked - protects retail from front-running
        assert can_access_addresses is False
        assert can_access_balances is False
        assert can_access_txs is False

    def test_scenario_whale_copy_trading_prevention(self):
        """
        Scenario: Hedge fund wants to copy whale trades.
        B2B clients should NOT be able to identify whale wallets.
        """
        # B2B client requests whale identification data
        can_access_addresses = DataAccessPolicy.can_access(
            ClientTier.B2B_PREMIUM, "whale_wallet_addresses"
        )
        can_access_movements = DataAccessPolicy.can_access(
            ClientTier.B2B_PREMIUM, "whale_real_time_movements"
        )
        can_access_history = DataAccessPolicy.can_access(
            ClientTier.B2B_PREMIUM, "whale_transaction_history"
        )

        # All blocked - prevents copy trading
        assert can_access_addresses is False
        assert can_access_movements is False
        assert can_access_history is False

    def test_scenario_diboas_user_full_insight(self):
        """
        Scenario: diBoaS retail user wants whale insights.
        Our users SHOULD see this data for better decisions.
        """
        # diBoaS user requests whale activity
        can_access_summary = DataAccessPolicy.can_access(
            ClientTier.DIBOAS_USER, "whale_activity_summary"
        )
        can_access_movements = DataAccessPolicy.can_access(
            ClientTier.DIBOAS_USER, "whale_real_time_movements"
        )

        # Full access - helps our users build wealth
        assert can_access_summary is True
        assert can_access_movements is True

    def test_scenario_b2b_gets_useful_aggregates(self):
        """
        Scenario: B2B client wants market sentiment.
        They can get aggregated whale sentiment without specific wallets.
        """
        full_data = {
            "whale_activity_summary": [
                {"wallet": "0x123", "direction": "in", "amount": 100},
                {"wallet": "0x456", "direction": "in", "amount": 200},
                {"wallet": "0x789", "direction": "out", "amount": 50},
            ],
        }

        filtered = DataAccessPolicy.filter_response(
            ClientTier.B2B_STANDARD, full_data
        )
        summary = filtered["whale_activity_summary"]

        # B2B gets useful aggregate info
        assert summary["total_movements"] == 3
        assert summary["net_direction"] == "accumulation"

        # But NOT specific wallet addresses
        assert "0x123" not in str(summary)
        assert "wallet" not in str(summary).lower() or "wallets not disclosed" in str(summary).lower()
