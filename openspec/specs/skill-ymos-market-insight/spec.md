# skill-ymos-market-insight Specification

## Purpose
TBD - created by archiving change skills-conversion. Update Purpose after archive.
## Requirements
### Requirement: Market insight skill triggers
The ymos-market-insight skill SHALL trigger on `跑一下市场洞察`, `今天有什么新闻`, and `抓 N 天数据`.

#### Scenario: Full pipeline
- **WHEN** user says "跑一下市场洞察"
- **THEN** skill executes: fetch data → CIO process → P13 analysis → save report

#### Scenario: Quick browse
- **WHEN** user says "今天有什么新闻"
- **THEN** skill fetches 1-day data and summarizes without saving

### Requirement: Market insight uses CLI for data fetching
The skill SHALL use `ymos fetch-market`, `ymos fetch-rss`, `ymos fetch-news` for data operations.

#### Scenario: Fetch with fallback
- **WHEN** skill starts data fetching
- **THEN** it runs `ymos fetch-market --days 1` first, falls back to `ymos fetch-rss --days 1` if market API unavailable

### Requirement: Market insight references P13 prompt
The skill SHALL reference `references/prompts/p13-market-scanner.md` for analysis.

#### Scenario: P13 analysis
- **WHEN** data is fetched
- **THEN** agent reads references/prompts/p13-market-scanner.md and applies it to the fetched data

