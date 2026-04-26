## MODIFIED Requirements

### Requirement: skill 文档自包含
ymos-market-insight SHALL 将其 SOP 和独占 prompts 纳入 skill 目录内部。SOP 存放于 `skills/ymos-market-insight/sop.md`，独占 prompts 存放于 `skills/ymos-market-insight/prompts/`。

独占 prompts：p13-market-scanner、p14-sector-hunter、p15-insight、p16-earnings、cio-rss-processor。

#### Scenario: market-insight skill 引用独占 prompt
- **WHEN** ymos-market-insight 执行 P13 市场扫描分析
- **THEN** 引用路径 SHALL 为 `skills/ymos-market-insight/prompts/p13-market-scanner.md`

#### Scenario: market-insight skill 引用 CIO processor
- **WHEN** ymos-market-insight 使用 RSS 数据源需执行 CIO 半成品处理
- **THEN** 引用路径 SHALL 为 `skills/ymos-market-insight/prompts/cio-rss-processor.md`

#### Scenario: market-insight skill 引用自己的 SOP
- **WHEN** ymos-market-insight 需要查看详细执行步骤
- **THEN** 引用路径 SHALL 为 `skills/ymos-market-insight/sop.md`
