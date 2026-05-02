## ADDED Requirements

### Requirement: CLI command check-signals SHALL scan signal files
The system SHALL provide `ymos monitor check-signals` command that scans `data/monitor/signals/` directory for JSON signal files and detects new signals.

#### Scenario: New signal detected
- **WHEN** a signal file in `data/monitor/signals/` contains a signal not yet recorded in today's alert log
- **THEN** system generates a formatted alert entry and prints it to terminal

#### Scenario: No new signals
- **WHEN** all signals have already been recorded in today's alert log
- **THEN** system exits silently with code 0

#### Scenario: Filter by tickers
- **WHEN** user runs `ymos monitor check-signals --tickers SOXL,META`
- **THEN** system only checks signal files for SOXL.json and META.json

### Requirement: Check-signals SHALL deduplicate by signal_time and strategy_name
The system SHALL identify duplicate signals by the combination of `signal_time` + `strategy_name` fields. A signal with the same combination already recorded in alerts SHALL be skipped.

#### Scenario: Duplicate signal skipped
- **WHEN** signal file contains a signal with signal_time "14:35" and strategy_name "ma_cross", and this exact combination exists in today's alert log
- **THEN** system skips this signal without generating a duplicate alert

#### Scenario: Same time different strategy triggers alert
- **WHEN** a signal has signal_time "14:35" and strategy_name "rsi", while the alert log has "14:35" + "ma_cross"
- **THEN** system generates a new alert (different strategy)

### Requirement: Check-signals SHALL write alerts to daily markdown log
The system SHALL append new alerts to `data/monitor/alerts/YYYY-MM-DD.md` in markdown format with ticker, signal type, strength, strategy name, detail, and price.

#### Scenario: Alert appended to daily log
- **WHEN** a new buy signal is detected for SOXL at 14:35
- **THEN** system appends a formatted markdown entry to `data/monitor/alerts/2026-05-03.md` with signal details

#### Scenario: Alert log created for new day
- **WHEN** no alert file exists for today's date
- **THEN** system creates a new file with the date header before appending

### Requirement: Signal JSON SHALL follow defined schema
Each signal file at `data/monitor/signals/{TICKER}.json` SHALL contain fields: ticker (string), signal_time (datetime string), signal_type (buy|sell|hold|warning), strength (strong|medium|weak), strategy_name (string), detail (string), price_at_signal (number).

#### Scenario: Valid signal file processed
- **WHEN** signal file contains all required fields with valid values
- **THEN** system processes the signal and generates alert if new

#### Scenario: Malformed signal file skipped
- **WHEN** signal file is missing required fields or has invalid JSON
- **THEN** system prints a warning to stderr and skips the file, continues processing other signals
