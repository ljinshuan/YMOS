## ADDED Requirements

### Requirement: Option chain CLI command
The system SHALL provide `ymos fetch-option-chain --ticker TICKER` CLI command that fetches complete option chain data from Futu OpenD.

#### Scenario: Single ticker full chain
- **WHEN** user runs `ymos fetch-option-chain --ticker AAPL`
- **THEN** CLI fetches all option contracts for AAPL, outputs JSON with static data (strike, expiry, type) and dynamic data (price, IV, Greeks, OI)

#### Scenario: Filter by expiry date
- **WHEN** user runs `ymos fetch-option-chain --ticker BABA --start 2026-05-08 --end 2026-05-15`
- **THEN** CLI fetches only options expiring within the specified date range

#### Scenario: Filter by option type
- **WHEN** user runs `ymos fetch-option-chain --ticker AAPL --option-type CALL`
- **THEN** CLI fetches only call options

#### Scenario: Filter by moneyness
- **WHEN** user runs `ymos fetch-option-chain --ticker NVDA --moneyness ATM`
- **THEN** CLI fetches only at-the-money options (or OUTSIDE/WITHIN/ALL)

#### Scenario: Batch fetch from state
- **WHEN** user runs `ymos fetch-option-chain --from-state`
- **THEN** CLI reads all tickers from holdings + watchlist state machines, fetches option chain for each, outputs JSON to `data/reports/radar/raw/option_chain_YYYYMMDD.json`

### Requirement: Option chain data format
The system SHALL output option chain data as JSON with standardized schema.

#### Scenario: JSON output structure
- **WHEN** option chain data is fetched for a ticker
- **THEN** output JSON SHALL include: ticker, market, fetched_at, expiry_dates, contracts array where each contract has: code, option_type, strike_price, expiry_date, days_to_expiry, last_price, ask_price, bid_price, implied_volatility, delta, gamma, vega, theta, rho, open_interest, volume

#### Scenario: Derived metrics
- **WHEN** option chain data is fetched
- **THEN** output JSON SHALL include derived metrics: put_call_ratio, iv_percentile (by expiry), oi_change_pct (if historical data available)

### Requirement: Option data source module
The system SHALL provide `cli/core/sources/option_chain.py` module that encapsulates option chain fetching logic.

#### Scenario: Fetch expiration dates
- **WHEN** calling `fetch_expiration_dates(ticker)`
- **THEN** function returns list of expiry dates with days remaining

#### Scenario: Fetch option chain static data
- **WHEN** calling `fetch_option_chain(ticker, ...)`
- **THEN** function returns DataFrame with contract static data (strike, expiry, type)

#### Scenario: Fetch option chain dynamic data
- **WHEN** calling `fetch_option_quotes(option_codes)`
- **THEN** function returns DataFrame with live data (price, IV, Greeks, OI)

### Requirement: Option data error handling
The system SHALL handle OpenD connection errors gracefully.

#### Scenario: OpenD not running
- **WHEN** user runs option chain command and OpenD is not reachable
- **THEN** CLI outputs clear error message and exits gracefully

#### Scenario: OpenD permission denied
- **WHEN** user runs option chain command but OpenD account lacks option data permission
- **THEN** CLI outputs specific error message "期权数据权限不足，请联系富途开通期权行情"

#### Scenario: No options available for ticker
- **WHEN** user runs option chain command for a ticker without options (e.g., ETF with no options)
- **THEN** CLI outputs empty contracts array with a message "该标的暂无期权合约"
