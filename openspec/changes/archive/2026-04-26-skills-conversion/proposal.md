## Why

当前 YMOS 的 8 个核心能力（入职引导、市场洞察、投资雷达、策略分析、初始调研、标的管理、持仓收口、投资诊断）中，只有投资诊断（ymos-diagnosis）已 skill 化。其余 7 个能力以 SOP 形式散落在各模块目录下，通过 agent 读取 SOP + 拼接 bash 命令执行。

需要将所有能力统一转换为 skill 格式（SKILL.md），放在项目根目录的 `skills/` 下，让 agent 通过标准 skill 机制发现和调用。

## What Changes

- 新建 `skills/` 顶层目录（不在 `.claude/skills/` 中）
- 创建 8 个 skill 子目录，每个包含 `SKILL.md`
- skill 通过 CLAUDE.md 中的路径声明被 agent 发现
- skill 内部引用 `references/sops/` 下的 SOP 获取详细步骤
- skill 内部调用 `ymos` CLI 命令执行数据操作
- 共享 skill（ymos-research/初始调研）被其他 skill 引用时采用混合模式：独立可调用 + 可被组合引用
- `Brain/ymos-diagnosis/SKILL.md` 迁移至 `skills/ymos-diagnosis/SKILL.md`

## Capabilities

### New Capabilities
- `skill-ymos-onboarding`: 入职引导 skill，触发词"开始使用"/"初始化系统"
- `skill-ymos-market-insight`: 市场洞察 skill，触发词"跑一下市场洞察"/"今天有什么新闻"
- `skill-ymos-radar`: 投资雷达 skill，触发词"跑一下投资雷达"/"查一下价格"
- `skill-ymos-strategy`: 策略分析 skill，触发词"我想买/卖/加仓/持有怎么看"
- `skill-ymos-research`: 初始调研 skill（共享），触发词"调研一下 TICKER"
- `skill-ymos-target-mgmt`: 标的管理 skill，触发词"关注/建仓/移除/清仓"
- `skill-ymos-reconcile`: 持仓收口 skill，触发词"收口一下"/"刷新持仓视图"

### Modified Capabilities
- `ymos-diagnosis`: 从 `Brain/ymos-diagnosis/` 迁移至 `skills/ymos-diagnosis/`，knowledge 路径更新为 `references/knowledge/diagnosis/`

## Impact

- **依赖关系**：依赖于 cli-infrastructure、data-layer-separation、references-reorganization 三个 change 完成
- **CLAUDE.md 更新**：需要在 entry-files-update 中同步更新
- **Agent 行为**：agent 通过 CLAUDE.md 中的 skill 路径发现能力，不再直接读取散落的 SOP
- **共享 skill 协议**：ymos-research 被其他 skill 引用时，约定调用方式为"调用 ymos-research"
