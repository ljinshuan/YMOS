## Why

P12 Referee 当前的纪律扫描基于"死亡边界"规则清单，覆盖了杠杆、情绪交易、风格漂移等红线，但行为金融学的系统性认知偏误检测不够完善。参考 FinceptTerminal 的独立 behavioral_finance_analyst Agent 设计，将行为金融学的偏误检测框架系统化融入 P12，让 Referee 从"规则检查器"升级为"认知偏误扫描仪"。

## What Changes

- 在 P12 Referee 中增加"行为偏误扫描"模块
- 覆盖 8 大核心偏误：处置效应、锚定效应、损失厌恶、过度自信、确认偏误、近因偏差、羊群效应、沉没成本谬误
- 每个偏误配备：定义、在投资决策中的典型表现、自检问题
- P12 输出增加"行为偏误风险评级"字段
- 在 ymos-diagnosis 的案例库中补充行为偏误导致亏损的典型案例

## Capabilities

### New Capabilities
- `behavioral-finance-scanner`: 行为金融偏误扫描框架，包含 8 大偏误定义、自检清单、风险评级输出

### Modified Capabilities
- `ymos-core`: 更新 `prompts/p12-referee.md`，增加行为偏误扫描章节
- `skill-ymos-strategy`: P12 输出格式变更影响所有 Route 的最终审核环节
- `ymos-diagnosis`: 在案例库中补充行为偏误案例

## Impact

- 修改文件：`skills/ymos-core/prompts/p12-referee.md`、`skills/ymos-diagnosis/knowledge/diagnosis_case_library.md`
- 可能影响：`skills/ymos-strategy/SKILL.md`（P12 输出新增字段）
- 无 CLI 代码变更，纯 prompt/知识层改动
- 不破坏现有流程，偏误扫描为 P12 的增强模块
