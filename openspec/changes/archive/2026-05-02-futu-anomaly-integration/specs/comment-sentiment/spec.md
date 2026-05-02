## MODIFIED Requirements

### Requirement: Sentiment CLI command
The system SHALL provide `ymos fetch-sentiment --ticker TICKER` CLI command that fetches comment data from Futu OpenD and outputs structured JSON.

#### Scenario: Single ticker fetch
- **WHEN** user runs `ymos fetch-sentiment --ticker 0700.HK`
- **THEN** CLI connects to Futu OpenD, fetches recent comments/posts for 0700.HK, outputs JSON with comment list, timestamp, source metadata, and normalized output contract (request, generated_at, mode, symbols array with per-symbol sentiment breakdown)

#### Scenario: Multi-ticker fetch with group aggregation
- **WHEN** user runs `ymos fetch-sentiment --ticker 0700.HK,AAPL,NVDA`
- **THEN** CLI fetches sentiment for each ticker, computes group-level aggregate (group_bull_pct, group_bear_pct, group_neutral_pct, group_summary), and outputs JSON with mode="multi" plus per-symbol breakdown

#### Scenario: Batch fetch from state
- **WHEN** user runs `ymos fetch-sentiment --from-state`
- **THEN** CLI reads all tickers from holdings + watchlist state machines, fetches sentiment for each, outputs one JSON file per ticker to `data/reports/sentiment/raw/`

#### Scenario: OpenD not running
- **WHEN** user runs `ymos fetch-sentiment` and OpenD is not reachable
- **THEN** CLI outputs clear error message with instructions to start OpenD

## ADDED Requirements

### Requirement: Normalized sentiment output contract
The system SHALL output sentiment data with a standardized JSON contract.

#### Scenario: Single symbol output schema
- **WHEN** sentiment is fetched for one ticker
- **THEN** output JSON SHALL include: request (symbol_list, lang), generated_at, mode="single", symbols array with each symbol containing: status, label (bullish/bearish/neutral/mixed), bull_pct, bear_pct, neutral_pct, post_count, time_range, summary, top_opinions (text + published_at), signals (bullish_signals, bearish_signals, uncertainties)

#### Scenario: Multi-symbol group output schema
- **WHEN** sentiment is fetched for multiple tickers
- **THEN** output JSON SHALL additionally include: group object with label, bull_pct, bear_pct, neutral_pct, post_count, summary; plus top_opinions across the group

### Requirement: Empty result fallback
The system SHALL handle empty sentiment results gracefully.

#### Scenario: No community data for ticker
- **WHEN** Futu OpenD returns no comments for a ticker
- **THEN** CLI SHALL mark that ticker's status as "empty" in the output, continue processing other tickers, and NOT abort the batch

#### Scenario: All tickers return empty
- **WHEN** all tickers in a batch return no community data
- **THEN** CLI SHALL output a clear message: "暂无相关数据，请稍后再试" and exit with code 0

### Requirement: Multi-symbol group aggregation
The system SHALL aggregate sentiment across multiple symbols into a group-level view.

#### Scenario: Group sentiment calculation
- **WHEN** sentiment is fetched for 2+ tickers
- **THEN** CLI SHALL compute group_bull_pct, group_bear_pct, group_neutral_pct from the combined retained posts across all symbols, generate a one-line group summary, and identify which symbols drive the group tone

#### Scenario: Mixed group label
- **WHEN** group bullish and bearish percentages are within 15% of each other AND both >= 25%
- **THEN** group label SHALL be "mixed"
