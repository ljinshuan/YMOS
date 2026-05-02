## MODIFIED Requirements

### Requirement: SKILL.md 命令调用必须包含完整的子命令层级
所有 SKILL.md 和 sop.md 中引用 `ymos` CLI 命令时，MUST 使用完整的二级命令格式（`ymos <command> <subcommand>`），不允许省略子命令。

#### Scenario: price-scan 命令引用
- **WHEN** agent 读取 SKILL.md 或 sop.md 中的 price-scan 引用
- **THEN** 文档中的调用格式为 `ymos price-scan scan --from-state`

#### Scenario: fetch-capital-flow 命令引用
- **WHEN** agent 读取 SKILL.md 或 sop.md 中的 fetch-capital-flow 引用
- **THEN** 文档中的调用格式为 `ymos fetch-capital-flow fetch --from-state`

#### Scenario: fetch-sentiment 命令引用
- **WHEN** agent 读取 SKILL.md 或 sop.md 中的 fetch-sentiment 引用
- **THEN** 文档中的调用格式为 `ymos fetch-sentiment fetch --ticker TICKER` 或 `ymos fetch-sentiment fetch --from-state`

#### Scenario: screen 命令引用
- **WHEN** agent 读取 SKILL.md 或 sop.md 中的 screen 引用
- **THEN** 文档中的调用格式为 `ymos screen screen --market MARKET`

### Requirement: price-scan 参数名必须与 CLI 一致
sop.md 中 price-scan 的输出参数 MUST 使用 `--output-dir`（目录）和 `--date-tag`（日期标签），不允许使用不存在的 `--output`。

#### Scenario: price-scan 输出参数
- **WHEN** agent 按 sop.md 执行 price-scan
- **THEN** 命令使用 `--output-dir "data/reports/radar/raw/YYYY-MM"` 和 `--date-tag YYYYMMDD`
