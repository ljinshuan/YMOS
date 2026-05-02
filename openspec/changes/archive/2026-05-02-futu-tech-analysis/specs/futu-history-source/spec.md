## ADDED Requirements

### Requirement: Futu OpenD historical K-line fetching
The system SHALL provide a `cli/core/sources/futu.py` module that fetches historical OHLCV daily data via Futu OpenD `get_history_kline` interface, returning a pandas DataFrame with columns: open, high, low, close, volume (float64), DatetimeIndex sorted ascending.

#### Scenario: Successfully fetch HK stock history
- **WHEN** calling `fetch_futu_history("0700.HK")` with Futu OpenD running and connected
- **THEN** returns a DataFrame with ~1 year of daily OHLCV data, DatetimeIndex sorted ascending, all columns as float64

#### Scenario: Successfully fetch US stock history
- **WHEN** calling `fetch_futu_history("AAPL")` with Futu OpenD running and connected
- **THEN** returns a DataFrame with ~1 year of daily OHLCV data for US.AAPL

#### Scenario: Successfully fetch A-share history
- **WHEN** calling `fetch_futu_history("688008.SS")` with Futu OpenD running and connected
- **THEN** returns a DataFrame with ~1 year of daily OHLCV data for SH.688008

#### Scenario: OpenD not running
- **WHEN** calling `fetch_futu_history("0700.HK")` with Futu OpenD not reachable
- **THEN** returns None and prints a warning message

#### Scenario: OpenD returns error
- **WHEN** `get_history_kline` returns a non-OK result code
- **THEN** returns None and prints the error message from Futu SDK

### Requirement: Ticker format conversion for Futu
The module SHALL convert YMOS ticker format to Futu standard symbol format: `0700.HK` → `HK.00700`, `AAPL` → `US.AAPL`, `688008.SS` → `SH.688008`, `000001.SZ` → `SZ.000001`.

#### Scenario: HK ticker conversion
- **WHEN** input is `0700.HK`
- **THEN** converts to `HK.00700` (zero-padded to 5 digits)

#### Scenario: US ticker conversion
- **WHEN** input is `AAPL` (no suffix)
- **THEN** converts to `US.AAPL`

#### Scenario: A-share SH conversion
- **WHEN** input is `688008.SS`
- **THEN** converts to `SH.688008`

#### Scenario: A-share SZ conversion
- **WHEN** input is `000001.SZ`
- **THEN** converts to `SZ.000001`
