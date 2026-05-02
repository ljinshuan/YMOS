## 1. Infrastructure

- [x] 1.1 Create `cli/monitor/__init__.py` module directory
- [x] 1.2 Implement `cli/monitor/trading_hours.py` — market trading hours detection (US/HK/A) with DST handling
- [x] 1.3 Implement `cli/monitor/dedup.py` — CSV timestamp dedup and signal (signal_time + strategy_name) dedup
- [x] 1.4 Implement `cli/monitor/history.py` — CSV history file read, merge with dedup, and write operations
- [x] 1.5 Implement `cli/monitor/signal_reader.py` — scan signal JSON files, parse schema, compare with alert log

## 2. fetch-prices Command

- [x] 2.1 Implement `cli/commands/monitor.py` — `fetch-prices` subcommand with typer, all parameters (--from-state, --symbols, --output-dir, --kline, --count, --skip-non-trading-hours)
- [x] 2.2 Wire fetch-prices to Futu OpenD `request_history_kline` using existing `futu_utils.py` (connection check, ticker conversion) and `futu.py` pattern (kline fetch)
- [x] 2.3 Implement price snapshot JSON output to `data/monitor/prices/YYYY-MM-DD/HHMM.json`
- [x] 2.4 Implement kline CSV merge with dedup to `data/monitor/history/{TICKER}_daily.csv` and `{TICKER}_{kline}.csv`
- [x] 2.5 Implement trading hours filter — skip tickers outside their market trading hours when flag enabled
- [x] 2.6 Register `monitor` command group in `cli/main.py`

## 3. check-signals Command

- [x] 3.1 Implement `check-signals` subcommand in `cli/commands/monitor.py` with typer parameters (--tickers, --signal-dir, --output-dir)
- [x] 3.2 Implement signal file scanning — read all JSON files from signals directory, validate schema, skip malformed files with stderr warning
- [x] 3.3 Implement alert dedup — compare signals against existing alert log by signal_time + strategy_name
- [x] 3.4 Implement alert log write — append formatted markdown entries to `data/monitor/alerts/YYYY-MM-DD.md`, create file with header if not exists
- [x] 3.5 Implement terminal output — print new alerts to stdout, silent exit 0 when no new signals

## 4. ymos-monitor Skill

- [x] 4.1 Create `skills/ymos-monitor/SKILL.md` — capability definition, trigger phrases (开始盯盘/停一下盯盘/查看告警/监控状态), CLI command reference
- [x] 4.2 Create `skills/ymos-monitor/sop.md` — standard monitoring operation flow (setup cron, check status, view alerts)
- [x] 4.3 Create `skills/ymos-monitor/knowledge/signal-ref.md` — signal type reference table (buy/sell/hold/warning, strength levels)
- [x] 4.4 Update `skills/ymos-core/routing.md` — add monitor trigger phrase routing entries

## 5. Testing

- [x] 5.1 Unit tests for `trading_hours.py` — all 3 markets, DST edge cases, non-trading hours skip
- [x] 5.2 Unit tests for `dedup.py` — CSV timestamp dedup, signal composite key dedup
- [x] 5.3 Unit tests for `history.py` — new CSV creation, merge with existing, dedup behavior
- [x] 5.4 Unit tests for `signal_reader.py` — valid signal parsing, malformed file handling, alert log comparison
- [x] 5.5 Integration test — fetch-prices end-to-end (mock Futu) → CSV output → check-signals end-to-end with test signal files → alert log output
