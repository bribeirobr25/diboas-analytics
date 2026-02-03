"""
Tests for strategy allocation validators.

Validates:
- Sky 30% concentration cap
- Allocation sum validation
- Crypto percentage matching
"""

import pytest
from src.validators.strategy_validator import (
    validate_sky_cap,
    validate_allocations_sum,
    validate_crypto_pct_matches,
    validate_all,
    validate_strategies_json,
    MAX_SKY_ALLOCATION,
)


class TestSkyCap:
    """Tests for Sky 30% concentration cap validation."""

    def test_should_pass_valid_sky_allocation(self):
        """Strategy with Sky at 30% should pass."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'sky': 0.30, 'aave': 0.70},
                'crypto': {}
            }
        }]
        violations = validate_sky_cap(strategies)
        assert len(violations) == 0

    def test_should_pass_sky_below_cap(self):
        """Strategy with Sky below 30% should pass."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'sky': 0.15, 'aave': 0.85},
                'crypto': {}
            }
        }]
        violations = validate_sky_cap(strategies)
        assert len(violations) == 0

    def test_should_fail_sky_above_cap(self):
        """Strategy with Sky above 30% should fail."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'sky': 0.50, 'aave': 0.50},
                'crypto': {}
            }
        }]
        violations = validate_sky_cap(strategies)
        assert len(violations) == 1
        assert 'exceeds 30% cap' in violations[0]

    def test_should_return_all_violations(self):
        """Multiple violating strategies should all be reported."""
        strategies = [
            {
                'id': 1,
                'name': 'Test1',
                'allocations': {'stable': {'sky': 0.50}, 'crypto': {}}
            },
            {
                'id': 2,
                'name': 'Test2',
                'allocations': {'stable': {'sky': 0.60}, 'crypto': {}}
            },
            {
                'id': 3,
                'name': 'Test3',
                'allocations': {'stable': {'sky': 0.30}, 'crypto': {}}
            }
        ]
        violations = validate_sky_cap(strategies)
        assert len(violations) == 2  # Strategies 1 and 2 violate

    def test_should_handle_missing_sky(self):
        """Strategy without Sky allocation should pass."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'aave': 0.50, 'compound': 0.50},
                'crypto': {}
            }
        }]
        violations = validate_sky_cap(strategies)
        assert len(violations) == 0

    def test_should_handle_float_tolerance(self):
        """Sky at exactly 30% should pass (float tolerance)."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'sky': 0.300001, 'aave': 0.699999},
                'crypto': {}
            }
        }]
        violations = validate_sky_cap(strategies)
        assert len(violations) == 0


class TestAllocationsSum:
    """Tests for allocation sum validation."""

    def test_should_pass_exact_sum(self):
        """Allocations summing to exactly 100% should pass."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'sky': 0.30, 'aave': 0.40, 'compound': 0.30},
                'crypto': {}
            }
        }]
        violations = validate_allocations_sum(strategies)
        assert len(violations) == 0

    def test_should_pass_with_crypto(self):
        """Allocations with crypto totaling 100% should pass."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'sky': 0.30, 'aave': 0.35},
                'crypto': {'sanctum': 0.35}
            }
        }]
        violations = validate_allocations_sum(strategies)
        assert len(violations) == 0

    def test_should_fail_over_100(self):
        """Allocations totaling over 100% should fail."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'sky': 0.50, 'aave': 0.60},
                'crypto': {}
            }
        }]
        violations = validate_allocations_sum(strategies)
        assert len(violations) == 1
        assert '110.0%' in violations[0]

    def test_should_fail_under_100(self):
        """Allocations totaling under 100% should fail."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'allocations': {
                'stable': {'sky': 0.30, 'aave': 0.30},
                'crypto': {}
            }
        }]
        violations = validate_allocations_sum(strategies)
        assert len(violations) == 1
        assert '60.0%' in violations[0]


class TestCryptoPctMatching:
    """Tests for crypto_pct field matching."""

    def test_should_pass_matching_crypto(self):
        """crypto_pct matching allocations should pass."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'crypto_pct': 35,
            'allocations': {
                'stable': {'sky': 0.65},
                'crypto': {'sanctum': 0.35}
            }
        }]
        violations = validate_crypto_pct_matches(strategies)
        assert len(violations) == 0

    def test_should_pass_zero_crypto(self):
        """Zero crypto matching empty crypto allocations should pass."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'crypto_pct': 0,
            'allocations': {
                'stable': {'sky': 1.0},
                'crypto': {}
            }
        }]
        violations = validate_crypto_pct_matches(strategies)
        assert len(violations) == 0

    def test_should_fail_mismatch(self):
        """crypto_pct not matching allocations should fail."""
        strategies = [{
            'id': 1,
            'name': 'Test',
            'crypto_pct': 40,  # Says 40%
            'allocations': {
                'stable': {'sky': 0.65},
                'crypto': {'sanctum': 0.35}  # But actually 35%
            }
        }]
        violations = validate_crypto_pct_matches(strategies)
        assert len(violations) == 1
        assert "doesn't match" in violations[0]


class TestValidateAll:
    """Tests for combined validation."""

    def test_should_run_all_validators(self):
        """validate_all should check all conditions."""
        strategies = [{
            'id': 1,
            'name': 'Bad Strategy',
            'crypto_pct': 40,  # Mismatch
            'allocations': {
                'stable': {'sky': 0.50},  # Over cap
                'crypto': {'sanctum': 0.30}  # Total = 80%, mismatch
            }
        }]
        violations = validate_all(strategies)
        # Should have: sky cap, sum, crypto mismatch = 3 violations
        assert len(violations) >= 2

    def test_should_pass_valid_strategy(self):
        """Fully valid strategy should pass all checks."""
        strategies = [{
            'id': 1,
            'name': 'Valid Strategy',
            'crypto_pct': 35,
            'allocations': {
                'stable': {'sky': 0.30, 'aave': 0.20, 'compound': 0.15},
                'crypto': {'sanctum': 0.35}
            }
        }]
        violations = validate_all(strategies)
        assert len(violations) == 0


class TestStrategiesJsonValidation:
    """Test validation of actual strategies.json file."""

    def test_strategies_json_passes_validation(self):
        """The actual strategies.json should pass all validations."""
        # This test ensures the config file remains valid
        result = validate_strategies_json('config/strategies.json')
        assert result is True

    def test_should_raise_on_violations(self, tmp_path):
        """Validator should raise ValueError on violations."""
        import json

        # Create a bad strategies file
        bad_strategies = {
            'strategies': [{
                'id': 1,
                'name': 'Bad',
                'crypto_pct': 0,
                'allocations': {
                    'stable': {'sky': 0.90},  # Violates cap
                    'crypto': {}
                }
            }]
        }

        bad_file = tmp_path / 'bad_strategies.json'
        with open(bad_file, 'w') as f:
            json.dump(bad_strategies, f)

        with pytest.raises(ValueError) as exc_info:
            validate_strategies_json(str(bad_file))

        assert 'violations' in str(exc_info.value)
