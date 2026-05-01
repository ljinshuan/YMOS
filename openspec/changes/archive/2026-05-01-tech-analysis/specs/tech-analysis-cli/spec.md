## ADDED Requirements

### Requirement: CLI command for technical analysis
The system SHALL provide a `ymos tech-analysis` CLI command that generates technical analysis reports.

#### Scenario: Analyze specified symbols
- **WHEN** user runs `ymos tech-analysis --symbols AAPL,0700.HK,688008.SS`
- **THEN** the system SHALL fetch historical data, compute indicators across daily/weekly/monthly timeframes, generate signals, and write one Markdown report per symbol

#### Scenario: Read symbols from state
- **WHEN** user runs `ymos tech-analysis --from-state`
- **THEN** the system SHALL read all tickers from `holdings.md` and `watchlist.md` state machines and generate reports for each

#### Scenario: Custom output directory
- **WHEN** user runs `ymos tech-analysis --symbols AAPL --output-dir data/reports/tech/2026-05`
- **THEN** the system SHALL write reports to the specified directory

#### Scenario: Default output path
- **WHEN** no `--output-dir` is specified
- **THEN** reports SHALL be written to `data/reports/tech/{YYYY-MM}/` where YYYY-MM is the current month

### Requirement: Report output format
Each report SHALL follow a structured Markdown format.

#### Scenario: Report structure
- **WHEN** a report is generated for a ticker
- **THEN** it SHALL contain: title with ticker and date, summary verdict, daily indicators table, weekly indicators table, monthly indicators table, and key signals summary

#### Scenario: Same-day overwrite
- **WHEN** a report already exists for the same ticker on the same date
- **THEN** the system SHALL overwrite it without version suffix (no `_v2`)

#### Scenario: Indicators table format
- **WHEN** the indicators table is rendered
- **THEN** each row SHALL contain: dimension (趋势/动量/波动率/成交量), indicator name, current value, and signal (多头/空头/中性)

### Requirement: Strategy integration
The strategy skill SHALL reference technical analysis reports when available.

#### Scenario: P5 buy-point analysis references tech report
- **WHEN** P5 (买点判断) prompt is executed for a ticker
- **THEN** the prompt SHALL instruct the agent to check for an existing tech analysis report at `data/reports/tech/{YYYY-MM}/{TICKER}_技术面分析.md` and include the summary verdict and key signals as technical input

#### Scenario: P6 holding evaluation references tech report
- **WHEN** P6 (持仓评估) prompt is executed for a ticker
- **THEN** the prompt SHALL instruct the agent to check for an existing tech analysis report and include the summary verdict and key signals as technical input
