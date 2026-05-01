## Why

P1 Genesis 分析采用单一视角的 7 维框架，缺乏多投资风格的交叉验证。参考 FinceptTerminal 的 11 个投资大师 Agent 设计，引入"大师会诊"机制可以显著降低单一分析框架的盲区风险，让每只股票在被深度研究时获得多维度的风格检验。

## What Changes

- 新建 P18 "大师会诊" prompt，包含 3-4 个核心投资大师的分析 lens（巴菲特-护城河、格雷厄姆-安全边际、马克斯-周期定位、林奇-成长分类）
- 每个大师 lens 输出结构化信号：bullish/neutral/bearish + 置信度 + 风格专属评分
- 最终输出"大师会诊综合报告"，包含共识/分歧点标注
- 在 ymos-research 的 P1 链条中增加可选的 P18 环节（P1 → P4 → P18 → P2）
- 在 ymos-core 的 routing.md 中注册 P18

## Capabilities

### New Capabilities
- `prompt-p18-master-consultation`: P18 大师会诊 prompt 定义，包含 3-4 个投资大师 lens、结构化输出格式、综合报告模板

### Modified Capabilities
- `ymos-core`: 在共享 prompts 目录增加 P18，更新 routing.md 中的 prompt 注册
- `skill-ymos-research`: 在 P1 链条中增加可选的 P18 环节

## Impact

- 新增文件：`skills/ymos-core/prompts/p18-master-consultation.md`
- 修改文件：`skills/ymos-core/routing.md`、`skills/ymos-research/SKILL.md`（链条更新）
- 无 CLI 代码变更，纯 prompt 层改动
- 不破坏现有流程，P18 为可选环节
