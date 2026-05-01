## ADDED Requirements

### Requirement: Unified historical OHLCV data fetching
The system SHALL provide a `fetch_history` function that accepts a list of ticker symbols and returns a dictionary mapping each symbol to a pandas DataFrame with columns `open`, `high`, `low`, `close`, `volume` indexed by `DatetimeIndex`.

#### Scenario: Fetch A-share historical data
- **WHEN** a ticker ending with `.SS` or `.SZ` is provided
- **THEN** the system SHALL fetch approximately 1 year of daily OHLCV data from Tushare using `fetch_daily` with `start_date` set to 1 year before today and return a DataFrame sorted by date ascending

#### Scenario: Fetch HK stock historical data
- **WHEN** a ticker ending with `.HK` is provided
- **THEN** the system SHALL fetch 1 year of daily OHLCV data from Yahoo using `fetch_one(period="1y", interval="1d")` and return a DataFrame sorted by date ascending

#### Scenario: Fetch US stock or crypto historical data
- **WHEN** a ticker without `.SS`/`.SZ`/`.HK` suffix is provided
- **THEN** the system SHALL fetch 1 year of daily OHLCV data from Yahoo (not Finnhub) and return a DataFrame sorted by date ascending

#### Scenario: Handle fetch failure gracefully
- **WHEN** a data source returns an error or no data for a given ticker
- **THEN** the system SHALL skip that ticker and log a warning, continuing with remaining tickers

#### Scenario: Multiple tickers in single call
- **WHEN** multiple tickers are provided spanning different markets (e.g., `AAPL`, `0700.HK`, `688008.SS`)
- **THEN** the system SHALL route each ticker to the appropriate data source and return results for all successfully fetched tickers

### Requirement: DataFrame output format
All fetched historical data SHALL conform to a standard DataFrame format.

#### Scenario: Standard column names and types
- **WHEN** historical data is fetched from any source
- **THEN** the DataFrame SHALL have columns `open`, `high`, `low`, `close`, `volume` (all float64 except volume which is int64) with a timezone-naive `DatetimeIndex` of dates

#### Scenario: Minimum data length
- **WHEN** historical data is fetched
- **THEN** the DataFrame SHALL contain at least 200 rows of valid OHLCV data; if fewer rows are available, the system SHALL log a warning but still return the available data
