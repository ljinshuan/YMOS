## MODIFIED Requirements

### Requirement: skill 文档自包含
ymos-target-mgmt SHALL 将其 SOP 纳入 skill 目录内部。SOP 存放于 `skills/ymos-target-mgmt/sop.md`。ymos-target-mgmt 无独占 prompts，共享模板通过 ymos-core 引用。

#### Scenario: target-mgmt skill 引用自己的 SOP
- **WHEN** ymos-target-mgmt 需要查看详细执行步骤
- **THEN** 引用路径 SHALL 为 `skills/ymos-target-mgmt/sop.md`

#### Scenario: target-mgmt skill 引用共享模板
- **WHEN** ymos-target-mgmt 初始化个股知识库需要模板
- **THEN** 引用路径 SHALL 为 `skills/ymos-core/templates/knowledge-base.md`
