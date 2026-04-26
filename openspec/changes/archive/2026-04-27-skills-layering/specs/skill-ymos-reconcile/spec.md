## MODIFIED Requirements

### Requirement: skill 文档自包含
ymos-reconcile SHALL 将其 SOP 纳入 skill 目录内部。SOP 存放于 `skills/ymos-reconcile/sop.md`。ymos-reconcile 无独占 prompts。

#### Scenario: reconcile skill 引用自己的 SOP
- **WHEN** ymos-reconcile 需要查看详细执行步骤
- **THEN** 引用路径 SHALL 为 `skills/ymos-reconcile/sop.md`
