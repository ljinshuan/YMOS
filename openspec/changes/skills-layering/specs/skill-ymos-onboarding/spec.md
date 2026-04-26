## MODIFIED Requirements

### Requirement: skill 文档自包含
ymos-onboarding SHALL 将其 SOP 纳入 skill 目录内部。SOP 存放于 `skills/ymos-onboarding/sop.md`。ymos-onboarding 无独占 prompts。

#### Scenario: onboarding skill 引用自己的 SOP
- **WHEN** ymos-onboarding 需要查看详细执行步骤
- **THEN** 引用路径 SHALL 为 `skills/ymos-onboarding/sop.md`
