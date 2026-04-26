## MODIFIED Requirements

### Requirement: skill 文档自包含
ymos-diagnosis SHALL 将其 knowledge 文档纳入 skill 目录内部。知识文档存放于 `skills/ymos-diagnosis/knowledge/`。

独占 knowledge：investment_axioms_and_framework.md、diagnosis_case_library.md。

#### Scenario: diagnosis skill 引用自己的 knowledge
- **WHEN** ymos-diagnosis 需要深度参考投资公理框架
- **THEN** 引用路径 SHALL 为 `skills/ymos-diagnosis/knowledge/investment_axioms_and_framework.md`

#### Scenario: diagnosis skill 引用案例库
- **WHEN** ymos-diagnosis 需要参考诊断案例
- **THEN** 引用路径 SHALL 为 `skills/ymos-diagnosis/knowledge/diagnosis_case_library.md`
