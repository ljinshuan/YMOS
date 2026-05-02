## ADDED Requirements

### Requirement: Sentiment skill triggers
ymos-sentiment SHALL trigger on `看一下 [ticker] 的情绪`、`[ticker] 多空怎么样`、`分析一下市场情绪`、`看一下情绪`。

#### Scenario: Single stock sentiment
- **WHEN** user says "看一下 NVDA 的情绪"
- **THEN** skill executes: fetch comments via Futu OpenD → run P19-comment-sentiment prompt → output sentiment report with bullish/bearish/neutral percentages, temperature score, and key takes

#### Scenario: Multi-stock sentiment
- **WHEN** user says "看一下腾讯、苹果、比亚迪的情绪"
- **THEN** skill fetches sentiment for each ticker in sequence and outputs a comparison table

#### Scenario: Portfolio-wide sentiment
- **WHEN** user says "看一下情绪" without specifying tickers
- **THEN** skill reads holdings + watchlist from state machines, fetches sentiment for all tickers, outputs a summary report

### Requirement: Sentiment CLI command
The system SHALL provide `ymos fetch-sentiment --ticker TICKER` CLI command that fetches comment data from Futu OpenD and outputs structured JSON.

#### Scenario: Single ticker fetch
- **WHEN** user runs `ymos fetch-sentiment --ticker 0700.HK`
- **THEN** CLI connects to Futu OpenD, fetches recent comments/posts for 0700.HK, outputs JSON with comment list, timestamp, and source metadata

#### Scenario: Batch fetch from state
- **WHEN** user runs `ymos fetch-sentiment --from-state`
- **THEN** CLI reads all tickers from holdings + watchlist state machines, fetches sentiment for each, outputs one JSON file per ticker to `data/reports/sentiment/raw/`

#### Scenario: OpenD not running
- **WHEN** user runs `ymos fetch-sentiment` and OpenD is not reachable
- **THEN** CLI outputs clear error message with instructions to start OpenD

### Requirement: P19-comment-sentiment prompt
The system SHALL provide P19-comment-sentiment prompt at `skills/ymos-sentiment/prompts/p19-comment-sentiment.md` that structures sentiment analysis output.

#### Scenario: Prompt output format
- **WHEN** LLM processes comment data using P19 prompt
- **THEN** output SHALL include: bullish percentage, bearish percentage, neutral percentage, temperature score (0-100), top 3 bull takes, top 3 bear takes, overall assessment paragraph

### Requirement: Sentiment output storage
The system SHALL store sentiment reports at `data/reports/sentiment/YYYY-MM/` with naming convention `情绪分析_YYYY-MM-DD.md`.

#### Scenario: Save sentiment report
- **WHEN** sentiment analysis completes for a ticker
- **THEN** report is saved to `data/reports/sentiment/YYYY-MM/情绪分析_YYYY-MM-DD.md`

### Requirement: Sentiment skill depends on ymos-core
ymos-sentiment SHALL declare `depends_on: [ymos-core]` in its SKILL.md frontmatter and follow standard skill structure.

#### Scenario: Skill directory structure
- **WHEN** ymos-sentiment skill is installed
- **THEN** it SHALL contain: SKILL.md, sop.md, prompts/p19-comment-sentiment.md
