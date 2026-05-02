## ADDED Requirements

### Requirement: Screener skill triggers
ymos-screener SHALL trigger on `帮我选股`、`筛选一下 [市场]`、`找一下 [类型]股`、`选股`.

#### Scenario: Preset screening
- **WHEN** user says "帮我选一下港股成长股"
- **THEN** skill executes: parse market=HK + preset=growth → run `ymos screen --market HK --preset growth` → display results table → offer research follow-up

#### Scenario: Custom screening
- **WHEN** user says "筛选一下 PE 小于 15 市值大于 100 亿的港股"
- **THEN** skill parses natural language into screening criteria → generates config JSON → runs `ymos screen --market HK --config <path>` → display results

#### Scenario: Direct research follow-up
- **WHEN** user says "帮我选股然后调研一下" after seeing screening results
- **THEN** skill displays results, user picks tickers, then triggers ymos-research for each selected ticker

### Requirement: Screener CLI command
The system SHALL provide `ymos screen` CLI command that executes stock screening via Futu OpenD.

#### Scenario: Preset template screening
- **WHEN** user runs `ymos screen --market HK --preset growth --limit 20`
- **THEN** CLI loads preset "growth" criteria, queries Futu OpenD screener API, outputs JSON with matching stocks sorted by relevance

#### Scenario: Custom config screening
- **WHEN** user runs `ymos screen --market US --config screener-config.json`
- **THEN** CLI reads JSON config with custom filter criteria, queries Futu OpenD, outputs results

#### Scenario: List available presets
- **WHEN** user runs `ymos screen --list-presets`
- **THEN** CLI lists all preset template names with descriptions

#### Scenario: OpenD not running
- **WHEN** user runs `ymos screen` and OpenD is not reachable
- **THEN** CLI outputs clear error message with instructions to start OpenD

### Requirement: Preset screening templates
The system SHALL provide at least 4 preset screening templates: growth (成长股), value (价值股), high-dividend (高息股), momentum (动量股).

#### Scenario: Growth preset
- **WHEN** preset "growth" is used
- **THEN** criteria SHALL include: revenue growth > 20%, net profit growth > 15%, market cap > threshold

#### Scenario: Value preset
- **WHEN** preset "value" is used
- **THEN** criteria SHALL include: PE < 15, PB < 1.5, ROE > 10%, dividend yield > 2%

### Requirement: Screener output storage
The system SHALL store screening results at `data/reports/screener/YYYY-MM/` with naming convention `选股结果_YYYY-MM-DD.md`.

#### Scenario: Save screening results
- **WHEN** screening completes
- **THEN** results are saved as both JSON (raw data) and Markdown (readable report) to the screener output directory

### Requirement: Screener skill structure
ymos-screener SHALL follow standard YMOS skill structure with `depends_on: [ymos-core]`.

#### Scenario: Skill directory structure
- **WHEN** ymos-screener skill is installed
- **THEN** it SHALL contain: SKILL.md, sop.md, knowledge/screening-templates.md (preset template definitions)
