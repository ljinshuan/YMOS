## MODIFIED Requirements

### Requirement: fetch-news 描述必须反映多源能力
`ymos-market-insight` 的 SKILL.md 和 sop.md 中关于 `fetch-news` 的描述 MUST 反映 Futu 兜底能力，不再局限于"Finnhub 仅美股/Crypto"。

#### Scenario: SKILL.md 新闻数据源描述
- **WHEN** agent 读取 ymos-market-insight SKILL.md
- **THEN** fetch-news 描述为"多源新闻：Finnhub + Futu 兜底，覆盖美股/Crypto/港股/A股"

#### Scenario: sop.md 新闻覆盖范围描述
- **WHEN** agent 读取 ymos-market-insight sop.md Step 2.6
- **THEN** 文档说明 Finnhub 处理美股/Crypto，Futu 为所有市场提供兜底（特别是 HK/CN ticker）
