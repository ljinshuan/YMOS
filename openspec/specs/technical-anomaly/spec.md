## ADDED Requirements

### Requirement: Technical anomaly CLI command
The system SHALL provide `ymos fetch-technical-anomaly --ticker TICKER` CLI command that fetches technical anomaly data from Futu OpenD `get_technical_unusual`.

#### Scenario: Single ticker full scan
- **WHEN** user runs `ymos fetch-technical-anomaly --ticker 0700.HK`
- **THEN** CLI connects to Futu OpenD, calls `get_technical_unusual` for the ticker, fetches all technical indicators including K-line pattern + 14 indicators (MACD, RSI6, RSI12, RSI24, KDJ, CCI, BIAS, AR, BR, VR, PSY, OSC, WMSR, BOLL, MA), outputs JSON

#### Scenario: Single ticker with indicator filter
- **WHEN** user runs `ymos fetch-technical-anomaly --ticker 0700.HK --indicators MACD RSI6 RSI12 RSI24`
- **THEN** CLI fetches only the specified indicators plus K-line pattern

#### Scenario: Batch fetch from state
- **WHEN** user runs `ymos fetch-technical-anomaly --from-state`
- **THEN** CLI reads all tickers from holdings + watchlist state machines, fetches technical anomaly for each, outputs JSON files to `data/reports/radar/raw/`

#### Scenario: Time range parameter
- **WHEN** user runs `ymos fetch-technical-anomaly --ticker AAPL --time-range 14`
- **THEN** CLI scans the last 14 natural days for anomalies

#### Scenario: OpenD not running
- **WHEN** user runs `ymos fetch-technical-anomaly` and OpenD is not reachable
- **THEN** CLI outputs clear error message and exits gracefully, does not block radar pipeline

### Requirement: Ticker normalization for Futu OpenD
The system SHALL normalize YMOS ticker format to Futu OpenD format before calling any OpenD API.

#### Scenario: HK stock normalization
- **WHEN** ticker is `0700.HK`
- **THEN** normalize to `HK.00700`

#### Scenario: US stock normalization
- **WHEN** ticker is `AAPL`
- **THEN** normalize to `US.AAPL`

#### Scenario: A-share normalization (Shanghai)
- **WHEN** ticker is `688008.SS`
- **THEN** normalize to `SH.688008`

#### Scenario: A-share normalization (Shenzhen)
- **WHEN** ticker is `000001.SZ`
- **THEN** normalize to `SZ.000001`

### Requirement: Technical anomaly output format
The system SHALL output technical anomaly data as JSON with a standardized schema.

#### Scenario: JSON output structure
- **WHEN** technical anomaly data is fetched for a ticker
- **THEN** output JSON SHALL include: ticker, time_range (start_date, end_date), anomalies array where each item has: date, indicator (e.g. "MACD", "RSI", "K线形态"), signal_direction, description, support/resistance levels (if applicable), probability (if K-line pattern)

#### Scenario: No anomaly detected
- **WHEN** no technical anomalies are found in the time window
- **THEN** output SHALL indicate empty anomalies array with a `summary: "无异常"` field

### Requirement: Technical anomaly integration in radar
The system SHALL integrate technical anomaly signals into the investment radar report.

#### Scenario: Radar includes technical signals
- **WHEN** investment radar pipeline runs and OpenD is available
- **THEN** radar report SHALL include a "技术面信号" section after the capital flow section, listing only indicators with anomalies

#### Scenario: OpenD unavailable
- **WHEN** investment radar pipeline runs and OpenD is not reachable
- **THEN** radar report SHALL skip technical anomaly section with a note "技术面数据不可用（OpenD 未连接）"
