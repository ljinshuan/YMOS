## MODIFIED Requirements

### Requirement: Historical data routing with Futu priority
The `cli/core/sources/history.py` `fetch_history()` function SHALL route symbol data fetching with the following priority: (1) check Futu OpenD reachability, (2) if reachable, attempt Futu `get_history_kline` first, (3) if Futu fails or is unreachable, fall back to existing Tushare/Yahoo routing. The `--source` parameter on `ymos tech analyze` SHALL allow overriding with values: `auto` (default), `futu`, `yahoo`, `tushare`.

#### Scenario: Auto mode with Futu available
- **WHEN** `fetch_history(["0700.HK", "AAPL"])` is called and Futu OpenD is reachable
- **THEN** both symbols are fetched via Futu `get_history_kline`, returning DataFrames

#### Scenario: Auto mode with Futu unavailable
- **WHEN** `fetch_history(["0700.HK", "688008.SS"])` is called and Futu OpenD is not reachable
- **THEN** `0700.HK` is fetched via Yahoo, `688008.SS` is fetched via Tushare (existing behavior)

#### Scenario: Auto mode with partial Futu failure
- **WHEN** `fetch_history(["0700.HK", "AAPL"])` is called, Futu is reachable, but `get_history_kline` fails for `AAPL`
- **THEN** `0700.HK` returns Futu data, `AAPL` falls back to Yahoo, both produce DataFrames

#### Scenario: Explicit futu source
- **WHEN** `ymos tech analyze --symbols AAPL --source futu` is called and Futu OpenD is not reachable
- **THEN** command prints connection error and exits with code 1

#### Scenario: Explicit yahoo source
- **WHEN** `ymos tech analyze --symbols AAPL --source yahoo` is called
- **THEN** data is fetched via Yahoo Finance regardless of Futu availability

#### Scenario: Explicit tushare source
- **WHEN** `ymos tech analyze --symbols 688008.SS --source tushare` is called without TUSHARE_TOKEN
- **THEN** command prints error about missing Tushare token and exits with code 1
