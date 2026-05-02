"""Tests for cli.core.futu_utils — ticker conversion and connection check."""

from cli.core.futu_utils import futu_symbol_to_ticker, ticker_to_futu_symbol


class TestTickerToFutuSymbol:
    def test_hk_stock(self):
        assert ticker_to_futu_symbol("0700.HK") == "HK.00700"

    def test_hk_stock_already_padded(self):
        assert ticker_to_futu_symbol("09988.HK") == "HK.09988"

    def test_us_stock(self):
        assert ticker_to_futu_symbol("AAPL") == "US.AAPL"

    def test_us_stock_nvda(self):
        assert ticker_to_futu_symbol("NVDA") == "US.NVDA"

    def test_shanghai_stock(self):
        assert ticker_to_futu_symbol("688008.SS") == "SH.688008"

    def test_shenzhen_stock(self):
        assert ticker_to_futu_symbol("000001.SZ") == "SZ.000001"

    def test_crypto_no_suffix(self):
        assert ticker_to_futu_symbol("BTC") == "US.BTC"

    def test_lowercase_hk(self):
        assert ticker_to_futu_symbol("0700.hk") == "HK.00700"

    def test_lowercase_ss(self):
        assert ticker_to_futu_symbol("688008.ss") == "SH.688008"


class TestFutuSymbolToTicker:
    def test_hk_symbol(self):
        assert futu_symbol_to_ticker("HK.00700") == "0700.HK"

    def test_us_symbol(self):
        assert futu_symbol_to_ticker("US.AAPL") == "AAPL"

    def test_sh_symbol(self):
        assert futu_symbol_to_ticker("SH.688008") == "688008.SS"

    def test_sz_symbol(self):
        assert futu_symbol_to_ticker("SZ.000001") == "000001.SZ"

    def test_roundtrip_hk(self):
        original = "0700.HK"
        assert futu_symbol_to_ticker(ticker_to_futu_symbol(original)) == original

    def test_roundtrip_us(self):
        original = "AAPL"
        assert futu_symbol_to_ticker(ticker_to_futu_symbol(original)) == original

    def test_roundtrip_ss(self):
        original = "688008.SS"
        assert futu_symbol_to_ticker(ticker_to_futu_symbol(original)) == original

    def test_roundtrip_sz(self):
        original = "000001.SZ"
        assert futu_symbol_to_ticker(ticker_to_futu_symbol(original)) == original
