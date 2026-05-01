## Context

YMOS 的用户入口是 `总入口暗号.md`，通过触发词（如"跑一下投资雷达"、"我想买 AAPL"）路由到对应 skill。`routing.md` 维护了完整的触发词 → skill → prompt 链映射。这个设计对熟悉系统的用户很高效，但对新用户或使用自然语言的场景不友好。

FinceptTerminal 的 SuperAgent 实现了 9 种意图的自动分类路由。YMOS 可以用 prompt-based 意图识别实现类似效果，不需要代码层面的 agent 框架。

## Goals / Non-Goals

**Goals:**
- 让用户可以用自然语言描述需求，系统自动识别意图并路由
- 定义 7-9 种投资意图分类，每种映射到最优 skill 链
- 支持复合意图的分步执行
- 保持向后兼容：触发词仍然有效，绕过意图识别

**Non-Goals:**
- 不做复杂的 NLU/意图分类模型
- 不改变现有 skill 的内部逻辑
- 不引入代码层面的路由引擎（纯 prompt 实现）
- 不做上下文记忆/对话状态管理

## Decisions

### D1: 意图识别的实现方式

**选择**：新建一个 intent-classifier.md prompt，由 Agent 在入口处调用

**理由**：YMOS 运行在 Claude Code 上，LLM 本身具备强大的意图理解能力。一个结构化 prompt 足以覆盖 90% 的意图分类场景。

**备选方案**：
- 关键词匹配代码 → 灵活度不够，无法处理自然语言
- 独立的小模型分类器 → 过度工程化

### D2: 意图分类体系

**选择**：8 种意图：

| 意图 | 映射 |
|---|---|
| 市场概览 | → market-insight |
| 投资雷达 | → radar |
| 个股研究 | → research |
| 买入/建仓 | → strategy Route A/B |
| 持有评估 | → strategy Route C |
| 卖出/减仓 | → strategy Route D |
| 组合管理 | → strategy Route E + reconcile |
| 系统操作 | → target-mgmt / onboarding / diagnosis |

**理由**：与现有 9 个 skill 的职责域基本对齐，不引入新的抽象层。

### D3: 复合意图处理

**选择**：识别到复合意图时，输出有序的任务列表（先研究后策略等），按依赖顺序执行

**理由**：YMOS 本身就有严格的流程依赖（market-insight → radar → strategy），复合意图只需要明确顺序。

### D4: 集成位置

**选择**：在 `总入口暗号.md` 中增加"智能路由"section，作为第一层判断

**理由**：`总入口暗号.md` 是 Agent 的入口文件，在这里加入意图识别最自然。原有触发词路由保持不变，作为 fallback。

## Risks / Trade-offs

- **[意图误分类]** → 用户说"帮我看看 NIO"可能被识别为"研究"或"雷达" → 通过在输出中标注意图并允许用户纠正来缓解
- **[增加一次 LLM 调用]** → 意图识别本身消耗 Token → 可以将意图识别压缩为极短 prompt（<500 Token），成本可忽略
- **[过度路由]** → 用户只是想聊天却被路由到分析 → 增加"闲聊"意图作为兜底
