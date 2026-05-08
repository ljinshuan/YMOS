## 1. Option Chain Data Source Module

- [x] 1.1 Create `cli/core/sources/option_chain.py` module with function stubs
- [x] 1.2 Implement `fetch_expiration_dates(ticker, host, port)` to get expiry dates via `get_option_expiration_date`
- [x] 1.3 Implement `fetch_option_chain_static(ticker, start, end, option_type, moneyness, host, port)` via `get_option_chain`
- [x] 1.4 Implement `fetch_option_quotes(option_codes, host, port)` via subscribe + `get_market_snapshot`
- [x] 1.5 Implement `build_derived_metrics(chain_data, quotes_data)` to calculate PCR, IV percentile, OI change
- [x] 1.6 Implement `fetch_option_chain(ticker, ...)` main function orchestrating the fetch and combining data
- [x] 1.7 Add error handling for OpenD connection failures and permission denied
- [ ] 1.3 Implement `fetch_option_chain_static(ticker, start, end, option_type, moneyness, host, port)` via `get_option_chain`
- [ ] 1.4 Implement `fetch_option_quotes(option_codes, host, port)` via subscribe + `get_market_snapshot`
- [ ] 1.5 Implement `build_derived_metrics(chain_data, quotes_data)` to calculate PCR, IV percentile, OI change
- [ ] 1.6 Implement `fetch_option_chain(ticker, ...)` main function orchestrating the fetch and combining data
- [ ] 1.7 Add error handling for OpenD connection failures and permission denied

## 2. Option Chain CLI Command

- [x] 2.1 Create `cli/commands/option_chain.py` with typer app
- [x] 2.2 Implement `--ticker` parameter for single ticker
- [x] 2.3 Implement `--from-state` parameter to read from holdings/watchlist
- [x] 2.4 Implement `--start` and `--end` parameters for date range filtering
- [x] 2.5 Implement `--option-type` parameter (ALL/CALL/PUT)
- [x] 2.6 Implement `--moneyness` parameter (ALL/ATM/OUTSIDE/WITHIN)
- [x] 2.7 Implement `--with-options` flag to enable optional fetching in radar
- [x] 2.8 Integrate with `option_chain.py` data source
- [x] 2.9 Implement JSON output with standardized schema
- [x] 2.10 Add OpenD connection check at command start with clear error messages

## 3. Register CLI Command

- [x] 3.1 Register `option_chain` command in `cli/main.py`
- [x] 3.2 Add to CLI help documentation

## 4. Option Analysis Prompts

- [x] 4.1 Create `P-option-sentiment.md` prompt for option market sentiment analysis
- [x] 4.2 Define input format: option chain JSON with IV, Greeks, OI, PCR
- [x] 4.3 Define output format: sentiment summary with key signals (IV level, PCR skew, OI trend, unusual activity)

## 5. Radar Integration

- [x] 5.1 Modify ymos-radar skill to optionally fetch option data via `--with-options` flag
- [x] 5.2 Add option data fetching step after capital flow analysis (if enabled)
- [x] 5.3 Integrate P-option-sentiment prompt processing
- [x] 5.4 Modify bridge report template to include "期权市场情绪" section (conditional)
- [x] 5.5 Add graceful degradation when option data is unavailable

## 6. Strategy Integration

- [x] 6.1 Modify ymos-strategy skill P12 (Referee) analysis to accept option data
- [x] 6.2 Add option signal interpretation logic (IV percentile, PCR thresholds, block trades)
- [x] 6.3 Update P12 prompt to include option-based positive/negative signals
- [x] 6.4 Add option sentiment as optional confirmation factor (non-blocking)

## 7. Documentation and Testing

- [x] 7.1 Add CLI command documentation for `ymos fetch-option-chain`
- [x] 7.2 Document option data integration in radar and strategy skills
- [x] 7.3 Add test cases for option chain fetching (with mock OpenD)
- [x] 7.4 Add test cases for derived metrics calculation
- [x] 7.5 Integration test for radar with option data enabled
- [x] 7.6 Integration test for strategy with option confirmation

## 8. Migration and Deployment

- [x] 8.1 Verify OpenD permission handling works for accounts without option access
- [x] 8.2 Test graceful degradation when OpenD is unavailable
- [x] 8.3 Confirm radar and strategy skills work with and without option data
- [x] 8.4 Update CLAUDE.md with new option data capabilities
