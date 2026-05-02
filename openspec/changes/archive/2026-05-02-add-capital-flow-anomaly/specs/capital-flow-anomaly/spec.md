## ADDED Requirements

### Requirement: Capital flow CLI command
The system SHALL provide `ymos fetch-capital-flow --ticker TICKER` CLI command that fetches capital flow data from Futu OpenD.

#### Scenario: Single ticker fetch
- **WHEN** user runs `ymos fetch-capital-flow --ticker 0700.HK`
- **THEN** CLI connects to Futu OpenD, fetches capital flow data including: fund distribution (main/retail), broker buy/sell activity, capital flow trend (multi-day), short sell volume and ratio

#### Scenario: Batch fetch from state
- **WHEN** user runs `ymos fetch-capital-flow --from-state`
- **THEN** CLI reads all tickers from holdings + watchlist state machines, fetches capital flow for each, outputs JSON files to `data/reports/radar/raw/`

#### Scenario: Market-specific data mapping
- **WHEN** fetching capital flow for different markets
- **THEN** CLI SHALL normalize data fields across HK/US/CN markets to a unified schema, documenting any missing fields per market

#### Scenario: OpenD not running
- **WHEN** user runs `ymos fetch-capital-flow` and OpenD is not reachable
- **THEN** CLI outputs clear error message with instructions to start OpenD

### Requirement: P20-capital-anomaly prompt
The system SHALL provide P20-capital-anomaly prompt at `skills/ymos-radar/prompts/p20-capital-anomaly.md` that structures capital flow anomaly analysis.

#### Scenario: Anomaly signal detection
- **WHEN** LLM processes capital flow data using P20 prompt
- **THEN** output SHALL include: anomaly signals (if any), signal strength (strong/moderate/weak), capital flow direction, broker activity summary, and recommended tier rating adjustment

#### Scenario: No anomaly detected
- **WHEN** capital flow data shows no significant anomalies
- **THEN** P20 output SHALL indicate "无显著异动" with brief data summary

### Requirement: Capital flow data output format
The system SHALL output capital flow data as JSON with a standardized schema.

#### Scenario: JSON schema
- **WHEN** capital flow data is fetched for a ticker
- **THEN** output JSON SHALL include: ticker, date, main_force_net_inflow, retail_net_inflow, top_brokers_buy (top 5), top_brokers_sell (top 5), short_sell_volume, short_sell_ratio, capital_flow_trend (7-day)
