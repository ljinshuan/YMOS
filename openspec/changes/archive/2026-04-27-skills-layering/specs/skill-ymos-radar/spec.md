## MODIFIED Requirements

### Requirement: skill 文档自包含
ymos-radar SHALL 将其 SOP 纳入 skill 目录内部。SOP 存放于 `skills/ymos-radar/sop.md`。ymos-radar 无独占 prompts，共享文档通过 ymos-core 引用。

#### Scenario: radar skill 引用自己的 SOP
- **WHEN** ymos-radar 需要查看详细执行步骤
- **THEN** 引用路径 SHALL 为 `skills/ymos-radar/sop.md`

#### Scenario: radar skill 引用共享 watchlist workflow
- **WHEN** ymos-radar 建议新增关注标的
- **THEN** 引用路径 SHALL 为 `skills/ymos-core/watchlist-update-workflow.md`
