## ADDED Requirements

### Requirement: Derivatives anomaly CLI command
The system SHALL provide `ymos fetch-derivatives-anomaly --ticker TICKER` CLI command that fetches derivatives anomaly data from Futu OpenD `get_derivative_unusual`.

#### Scenario: Single ticker full scan
- **WHEN** user runs `ymos fetch-derivatives-anomaly --ticker 0700.HK`
- **THEN** CLI connects to Futu OpenD, calls `get_derivative_unusual` for the ticker, fetches all 7 derivatives dimensions (warrant_ratio, warrant_price_distribution, option_unusual, option_volatility, option_volume_price, option_sentiment, option_comprehensive), outputs JSON

#### Scenario: Single ticker with dimension filter
- **WHEN** user runs `ymos fetch-derivatives-anomaly --ticker AAPL --dimensions option_unusual option_volatility`
- **THEN** CLI fetches only the specified derivatives dimensions

#### Scenario: Batch fetch from state
- **WHEN** user runs `ymos fetch-derivatives-anomaly --from-state`
- **THEN** CLI reads all tickers from holdings + watchlist state machines, fetches derivatives anomaly for each, outputs JSON files to `data/reports/radar/raw/`

#### Scenario: Time range parameter
- **WHEN** user runs `ymos fetch-derivatives-anomaly --ticker NVDA --time-range 7`
- **THEN** CLI scans the last 7 natural days for anomalies

#### Scenario: OpenD not running
- **WHEN** user runs `ymos fetch-derivatives-anomaly` and OpenD is not reachable
- **THEN** CLI outputs clear error message and exits gracefully, does not block radar pipeline

### Requirement: Warrant dimensions only for HK stocks
Warrant-related dimensions (warrant_ratio, warrant_price_distribution) SHALL only apply to Hong Kong listed stocks.

#### Scenario: HK stock warrant scan
- **WHEN** fetching derivatives anomaly for `HK.00700`
- **THEN** all 7 dimensions including warrant_ratio and warrant_price_distribution SHALL be scanned

#### Scenario: Non-HK stock warrant exclusion
- **WHEN** fetching derivatives anomaly for `US.AAPL`
- **THEN** warrant_ratio and warrant_price_dimensions SHALL be excluded from the scan, only 5 option dimensions returned

### Requirement: Derivatives anomaly output format
The system SHALL output derivatives anomaly data as JSON with a standardized schema.

#### Scenario: JSON output structure
- **WHEN** derivatives anomaly data is fetched for a ticker
- **THEN** output JSON SHALL include: ticker, market (HK/US/CN), time_range, anomalies array grouped by dimension, where each item has: dimension, anomaly_date, description, direction, key metrics (volume/OI/IV/PCR/strike/expiry as applicable)

#### Scenario: No anomaly detected
- **WHEN** no derivatives anomalies are found in the time window
- **THEN** output SHALL indicate empty anomalies array with a `summary: "无异常"` field per dimension

### Requirement: Derivatives anomaly integration in radar
The system SHALL integrate derivatives anomaly signals into the investment radar report.

#### Scenario: Radar includes derivatives signals
- **WHEN** investment radar pipeline runs and OpenD is available
- **THEN** radar report SHALL include a "衍生品信号" section after the technical anomaly section, listing only dimensions with anomalies

#### Scenario: OpenD unavailable
- **WHEN** investment radar pipeline runs and OpenD is not reachable
- **THEN** radar report SHALL skip derivatives anomaly section with a note "衍生品数据不可用（OpenD 未连接）"
