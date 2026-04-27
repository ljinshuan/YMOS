## ADDED Requirements

### Requirement: Price scan with multi-source routing
The `ymos price-scan` command SHALL route symbols to the correct data source (Finnhub/Tushare/Yahoo) based on ticker suffix and API key availability, with Yahoo as universal fallback.

#### Scenario: Scan mixed symbols with all API keys
- **WHEN** user runs `ymos price-scan --symbols AAPL,688008.SS,0700.HK` with FINNHUB_API_KEY and TUSHARE_TOKEN set
- **THEN** AAPL goes to Finnhub, 688008.SS goes to Tushare, 0700.HK goes to Yahoo, results saved to output directory

#### Scenario: Fallback when API key missing
- **WHEN** user runs `ymos price-scan --symbols AAPL` without FINNHUB_API_KEY
- **THEN** AAPL falls back to Yahoo Finance

#### Scenario: Scan from state machine
- **WHEN** user runs `ymos price-scan --from-state`
- **THEN** system reads tickers from holdings and watchlist state machines, scans all, outputs combined results

### Requirement: RSS feed fetching
The `ymos fetch-rss` command SHALL fetch RSS feeds from configured sources with configurable lookback days.

#### Scenario: Fetch with default config
- **WHEN** user runs `ymos fetch-rss --days 1`
- **THEN** system fetches from default RSS sources, outputs JSON to specified path

#### Scenario: Fetch with custom config
- **WHEN** user runs `ymos fetch-rss --days 3 --config custom_sources.json`
- **THEN** system fetches from custom source list, outputs JSON

### Requirement: Market event API fetching
The `ymos fetch-market` command SHALL fetch market events from the configured API, with graceful fallback when API key is unavailable.

#### Scenario: Fetch with API key
- **WHEN** user runs `ymos fetch-market --days 1` with YMOS_MARKET_API_KEY set
- **THEN** system fetches from API, outputs JSON

#### Scenario: No API key
- **WHEN** user runs `ymos fetch-market --days 1` without YMOS_MARKET_API_KEY
- **THEN** system exits with code 0 and prints message suggesting RSS fallback

### Requirement: Individual stock news fetching
The `ymos fetch-news` command SHALL fetch company news for holdings from Finnhub, filtering to US stocks and Crypto only.

#### Scenario: Fetch news for holdings
- **WHEN** user runs `ymos fetch-news --hours 24` with FINNHUB_API_KEY
- **THEN** system reads holdings state machine, fetches news for US/Crypto tickers only, outputs JSON

#### Scenario: No Finnhub key
- **WHEN** user runs `ymos fetch-news` without FINNHUB_API_KEY
- **THEN** command silently exits without error

### Requirement: Crypto symbol normalization
The CLI SHALL normalize crypto bare symbols (BTC, ETH, etc.) to source-specific formats (BINANCE:BTCUSDT for Finnhub, BTC-USD for Yahoo).

#### Scenario: Crypto via Finnhub
- **WHEN** BTC is routed to Finnhub source
- **THEN** symbol is normalized to BINANCE:BTCUSDT before API call

#### Scenario: Crypto via Yahoo fallback
- **WHEN** BTC falls back to Yahoo
- **THEN** symbol is normalized to BTC-USD before API call
