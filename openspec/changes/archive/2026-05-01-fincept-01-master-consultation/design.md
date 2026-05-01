## Context

YMOS 的 ymos-research skill 执行 P1 Genesis → P4 Radar → P2 Phase Check 链条。P1 是单一视角的 7 维公司分析框架，虽然覆盖全面，但缺少不同投资风格的交叉验证。FinceptTerminal 通过 11 个独立的投资大师 Agent 实现多视角分析，每个 Agent 有数百行 system prompt 编码其投资哲学。

YMOS 是 prompt 驱动系统，不适合复制 FinceptTerminal 的 11 个 agent 架构。正确的吸收方式是：将 3-4 个核心大师的分析框架压缩为一个结构化 prompt（P18），作为 P1 链条的可选后续环节。

## Goals / Non-Goals

**Goals:**
- 用最少的 prompt 改动实现多投资风格的交叉验证
- 选取 3-4 个与 YMOS 用户画像最契合的大师 lens
- 保持 P18 为可选环节，不破坏现有 P1 → P4 → P2 流程
- 输出结构化的共识/分歧点，便于用户快速决策

**Non-Goals:**
- 不复制 FinceptTerminal 的 11 个独立 agent 架构
- 不引入代码层面的 agent 框架
- 不让 P18 成为 P1 链条的必选环节
- 不模拟大师的"人格"或对话风格

## Decisions

### D1: 选取 4 个大师 lens

**选择**：巴菲特（护城河）、格雷厄姆（安全边际）、马克斯（周期定位）、林奇（成长分类）

**理由**：这 4 位覆盖了价值投资的核心维度——护城河质量、价格安全、周期位置、成长类型，且风格互不重叠。

**备选方案**：
- 11 个全部引入 → prompt 过长，Token 成本高，且部分大师风格重叠（Klarman vs Graham）
- 2 个（Buffett + Graham）→ 覆盖面不足，缺少周期和成长维度

### D2: 单 prompt vs 多 prompt

**选择**：单个 P18 prompt，内部按大师分 section

**理由**：YMOS 的 prompt 模型是每个 P 一个文件，保持一致性。LLM 在单次调用中可以输出多个视角，避免多次调用的延迟和成本。

**备选方案**：4 个独立 prompt（P18a/b/c/d）→ 4 次 LLM 调用，Token 成本 x4，收益不成比例

### D3: P18 在链条中的位置

**选择**：P1 → P4 → P18 → P2（P18 在 P4 之后、P2 之前）

**理由**：P4 提供了实时监控数据，P18 基于 P1 的基本面 + P4 的动态数据做多视角检验，最后 P2 做阶段判断。这样 P2 可以参考大师会诊的结论。

## Risks / Trade-offs

- **[Token 成本增加]** → P18 会增加 ~2000-3000 Token 输出，但作为可选环节可控
- **[分析重复]** → P1 已包含估值和护城河分析，P18 可能部分重叠 → 通过 P18 聚焦"风格检验"而非"全面重分析"来规避
- **[用户认知负担]** → 增加一个报告 section → 通过"共识/分歧"摘要让用户 30 秒内获取核心结论
