## ADDED Requirements

### Requirement: CLI command fetch-prices SHALL fetch kline data via Futu OpenD
The system SHALL provide `ymos monitor fetch-prices` command that fetches daily and minute kline data for specified tickers via Futu OpenD `request_history_kline`.

#### Scenario: Fetch from state machines
- **WHEN** user runs `ymos monitor fetch-prices --from-state`
- **THEN** system extracts tickers from holdings.md and watchlist.md, fetches 60 daily candles and 60 minute candles per ticker via Futu OpenD

#### Scenario: Fetch specified tickers
- **WHEN** user runs `ymos monitor fetch-prices --symbols SOXL,META`
- **THEN** system fetches kline data only for SOXL and META

#### Scenario: OpenD not running
- **WHEN** Futu OpenD is not reachable at configured host:port
- **THEN** system prints OpenD startup guide and exits with non-zero code

### Requirement: Fetch-prices SHALL write price snapshots
The system SHALL write a JSON snapshot file per fetch cycle to `data/monitor/prices/YYYY-MM-DD/HHMM.json` containing all fetched ticker data with fields: price, open, high, low, close, volume, change_pct, source.

#### Scenario: Snapshot file created
- **WHEN** fetch-prices completes successfully
- **THEN** a JSON file exists at `data/monitor/prices/YYYY-MM-DD/HHMM.json` with all ticker data

### Requirement: Fetch-prices SHALL accumulate kline history to CSV
The system SHALL merge fetched kline data into per-ticker CSV files at `data/monitor/history/{TICKER}_daily.csv` and `data/monitor/history/{TICKER}_{kline}.csv`. Each CSV SHALL have columns: timestamp, open, high, low, close, volume.

#### Scenario: New CSV created on first fetch
- **WHEN** no CSV file exists for a ticker
- **THEN** system creates a new CSV with the fetched 60 candles

#### Scenario: Existing CSV merged with dedup
- **WHEN** CSV file already exists
- **THEN** system merges new data, skips rows with duplicate timestamps, and writes the combined result

### Requirement: Fetch-prices SHALL support configurable kline period
The system SHALL accept `--kline` parameter with values `1m`, `5m`, `15m`, `60m`. Default SHALL be `5m`.

#### Scenario: Custom kline period
- **WHEN** user runs `ymos monitor fetch-prices --symbols SOXL --kline 15m`
- **THEN** system fetches 15-minute candles and writes to `SOXL_15m.csv`

### Requirement: Fetch-prices SHALL skip non-trading hours by default
The system SHALL accept `--skip-non-trading-hours` flag (default True). When enabled, system SHALL detect each ticker's market and skip fetching if outside trading hours.

#### Scenario: US stock outside US trading hours
- **WHEN** current time is outside US market trading hours (21:30-04:00 Beijing, adjusted for DST)
- **THEN** system skips US tickers and prints a skip notice

#### Scenario: All tickers outside trading hours
- **WHEN** all tickers are outside their respective trading hours
- **THEN** system exits with code 0 and prints "all tickers outside trading hours"

### Requirement: Fetch-prices SHALL support configurable candle count
The system SHALL accept `--count` parameter (default 60) to control how many recent candles to fetch.

#### Scenario: Custom count
- **WHEN** user runs `ymos monitor fetch-prices --symbols SOXL --count 30`
- **THEN** system fetches 30 candles instead of 60
