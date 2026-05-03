## MODIFIED Requirements

### Requirement: Market insight skill triggers
The ymos-market-insight skill SHALL trigger on `跑一下市场洞察`, `今天有什么新闻`, and `抓 N 天数据`.

#### Scenario: Full pipeline
- **WHEN** user says "跑一下市场洞察"
- **THEN** skill executes: **fetch market/sector ETF technical data** → fetch news data → CIO process → P13 analysis (with quantitative input) → save report

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

## ADDED Requirements

### Requirement: Market insight 注入大盘技术面数据
ymos-market-insight SHALL 在 P13 分析前获取大盘锚点的技术面数据，作为量化输入补充新闻文字。

#### Scenario: 获取大盘技术面
- **WHEN** market insight 流程开始 P13 分析前
- **THEN** 读取 `data/state/market_anchors.md`，执行 `ymos tech-analysis analyze --symbols <大盘ETF列表>`，将技术面 verdict 注入 P13 的输入上下文

#### Scenario: P13 输出增加技术面锚点
- **WHEN** P13 分析完成
- **THEN** 报告「市场风向」section 包含大盘 ETF 的量化技术面判断（如 "QQQ 技术面偏多，日线均线多头排列，RSI 58"），与新闻文字分析并列呈现
