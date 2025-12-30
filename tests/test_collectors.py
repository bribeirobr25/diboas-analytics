"""
Tests for data collectors.
"""

import pytest
from pathlib import Path


class TestFileLoader:
    """Test FileLoader functionality."""

    def test_files_dictionary(self):
        """Test that FILES dictionary has expected sources."""
        from src.collectors.file_loader import FileLoader

        expected = ['defillama', 'yahoo', 'jupiter', 'perps']
        for source in expected:
            assert source in FileLoader.FILES

    def test_load_unknown_source_raises(self):
        """Unknown source should raise ValueError."""
        from src.collectors.file_loader import FileLoader

        loader = FileLoader()
        with pytest.raises(ValueError):
            loader.load('unknown_source')


class TestProxyCalculations:
    """Test APY proxy calculations."""

    def test_sanctum_proxy(self):
        """Test Sanctum proxy formula."""
        from src.utils.proxies import get_sanctum_apy

        # Lido at 4% -> Sanctum at 4*2 + 0.5 = 8.5%
        result = get_sanctum_apy(4.0)
        assert result == 8.5

    def test_jito_proxy(self):
        """Test Jito proxy formula."""
        from src.utils.proxies import get_jito_apy

        # Lido at 4% -> Jito at 4*2 + 1 = 9%
        result = get_jito_apy(4.0)
        assert result == 9.0

    def test_jlp_proxy_default(self):
        """Test JLP proxy returns default."""
        from src.utils.proxies import get_jlp_apy

        result = get_jlp_apy()
        assert result == 25.0

    def test_compound_proxy(self):
        """Test Compound proxy formula."""
        from src.utils.proxies import get_compound_apy

        # Aave at 5% -> Compound at 5*1.1 = 5.5%
        result = get_compound_apy(5.0)
        assert result == 5.5

    def test_sky_proxy(self):
        """Test Sky proxy formula."""
        from src.utils.proxies import get_sky_apy

        # Aave at 5% -> Sky at 5*0.9 = 4.5%
        result = get_sky_apy(5.0)
        assert result == 4.5


class TestProxyCalculator:
    """Test ProxyCalculator class."""

    def test_needs_proxy_sanctum(self):
        """Sanctum should always need proxy (no historical data)."""
        from src.utils.proxies import ProxyCalculator
        from datetime import date

        calc = ProxyCalculator()
        assert calc.needs_proxy('sanctum', date(2024, 1, 1)) is True

    def test_needs_proxy_jlp_before_2024(self):
        """JLP should need proxy before January 2024."""
        from src.utils.proxies import ProxyCalculator
        from datetime import date

        calc = ProxyCalculator()
        assert calc.needs_proxy('jlp', date(2023, 6, 1)) is True
        assert calc.needs_proxy('jlp', date(2024, 6, 1)) is False

    def test_get_protocol_apy_uses_actual_when_available(self):
        """Should use actual APY when available and proxy not needed."""
        from src.utils.proxies import ProxyCalculator
        from datetime import date

        calc = ProxyCalculator()
        # Aave doesn't need proxy in recent dates
        result = calc.get_protocol_apy('aave', date(2024, 6, 1), actual_apy=6.5)
        assert result == 6.5
