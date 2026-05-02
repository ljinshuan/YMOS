## MODIFIED Requirements

### Requirement: Capital flow CLI command
The system SHALL provide `ymos fetch-capital-flow --ticker TICKER` CLI command that fetches capital flow data from Futu OpenD.

#### Scenario: Single ticker fetch
- **WHEN** user runs `ymos fetch-capital-flow --ticker 0700.HK`
- **THEN** CLI connects to Futu OpenD, fetches capital flow data including: fund distribution (main/retail), broker buy/sell activity, capital flow trend (multi-day), short sell volume and ratio, short sell anomaly detection, broker activity anomaly tracking

#### Scenario: Single ticker with dimension filter
- **WHEN** user runs `ymos fetch-capital-flow --ticker 0700.HK --dimensions funds_distribution short_sell_ratio`
- **THEN** CLI fetches only the specified capital flow dimensions

#### Scenario: Batch fetch from state
- **WHEN** user runs `ymos fetch-capital-flow --from-state`
- **THEN** CLI reads all tickers from holdings + watchlist state machines, fetches capital flow for each, outputs JSON files to `data/reports/radar/raw/`

#### Scenario: Market-specific data mapping
- **WHEN** fetching capital flow for different markets
- **THEN** CLI SHALL normalize data fields across HK/US/CN markets to a unified schema, documenting any missing fields per market

#### Scenario: OpenD not running
- **WHEN** user runs `ymos fetch-capital-flow` and OpenD is not reachable
- **THEN** CLI outputs clear error message with instructions to start OpenD

## ADDED Requirements

### Requirement: Short sell anomaly dimension
The system SHALL support short sell anomaly detection as a dedicated capital flow dimension.

#### Scenario: Short sell number anomaly
- **WHEN** `--dimensions short_sell_number` is specified
- **THEN** CLI SHALL detect abnormal short sell volume changes within the time window, including daily change rate and comparison to historical average

#### Scenario: Short sell ratio anomaly
- **WHEN** `--dimensions short_sell_ratio` is specified
- **THEN** CLI SHALL detect abnormal short sell ratio changes, including ratio trend and percentile ranking

#### Scenario: Short sell combined anomaly
- **WHEN** both short sell number and ratio show simultaneous anomalies
- **THEN** output SHALL flag this as a combined anomaly signal with stronger signal strength

### Requirement: Broker activity anomaly tracking
The system SHALL detect unusual broker buy/sell activity patterns.

#### Scenario: Top broker concentration shift
- **WHEN** broker buy/sell rankings change significantly from previous period
- **THEN** CLI SHALL flag the shift with: which brokers increased/decreased activity, directional change (bullish/bearish), and magnitude

#### Scenario: Cross-border broker activity
- **WHEN** HK stock shows significant southbound/northbound broker activity
- **THEN** CLI SHALL identify the cross-border flow direction and magnitude
