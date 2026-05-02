## MODIFIED Requirements

### Requirement: Dual-source news fetching with Futu fallback
The `cli/commands/news.py` fetch command SHALL support dual data sources: Finnhub (for US/Crypto) and Futu news search (for all markets as fallback). When Finnhub returns no results for a US/Crypto ticker, Futu SHALL be used as fallback. For HK/CN tickers, Futu SHALL be the primary source.

#### Scenario: US ticker with Finnhub results
- **WHEN** fetching news for `AAPL` and Finnhub returns articles
- **THEN** Finnhub articles are used, Futu is not called for this ticker

#### Scenario: US ticker with no Finnhub results
- **WHEN** fetching news for `AAPL` and Finnhub returns empty
- **THEN** Futu news search is called as fallback

#### Scenario: HK ticker
- **WHEN** fetching news for `0700.HK`
- **THEN** Futu news search is called directly (Finnhub does not cover HK)

#### Scenario: A-share ticker
- **WHEN** fetching news for `688008.SS`
- **THEN** Futu news search is called directly (Finnhub does not cover A-shares)

#### Scenario: Cross-source deduplication
- **WHEN** both Finnhub and Futu return articles with similar headlines for the same ticker
- **THEN** articles are deduplicated by first 40 chars of headline (case-insensitive), keeping the earlier source

### Requirement: Full market ticker extraction for news
The `news` command SHALL read tickers from holdings state machine with `us_only=False`, enabling news fetching for all markets (US, HK, CN, Crypto).

#### Scenario: Holdings include multi-market tickers
- **WHEN** holdings state machine contains `AAPL`, `0700.HK`, `688008.SS`
- **THEN** all three tickers are included in the news fetch

#### Scenario: No Finnhub API key
- **WHEN** `FINNHUB_API_KEY` is not set
- **THEN** all tickers (including US) are fetched via Futu, command does not exit early
