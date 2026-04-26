## Why

当前 `references/` 目录作为独立知识层存在，SOP、prompts、templates、knowledge 散落在 skills 之外。这导致：(1) 每个 skill 的 SKILL.md 用路径引用外部文件，skill 不自包含；(2) 共享文档（p2、p9、templates）归属不清，依赖关系隐式且脆弱；(3) 新增 skill 时不清楚哪些文档可复用、应放在哪里。

将所有 references 文档按归属抽入对应 skill 目录，共享文档归入新建的 `ymos-core` skill，使 skills 自包含且有显式依赖分层。

## What Changes

- **新建 `skills/ymos-core/`**：收纳跨 skill 共享的基础设施（共享 prompts、templates、路由速查、投资公理）
- **每个现有 skill 吸收其独占 references**：SOP 移入 skill 目录，独占 prompts 移入 skill 目录
- **`references/` 目录清空并移除**：所有文档迁移到 skills 后，删除空的 references 目录树
- **SKILL.md 更新**：所有 `references/...` 路径改为 skill 内相对路径或 `ymos-core` 依赖声明
- **BREAKING**：所有 skill 的文档引用路径变更，CLAUDE.md 的架构描述和路径规则同步更新

### 共享文档归属分析

| 文档 | 当前使用者 | 归属 |
|------|-----------|------|
| p2-phase-check | ymos-research, ymos-strategy | ymos-core |
| p9-valuation | ymos-research, ymos-strategy | ymos-core |
| templates/knowledge-base.md | ymos-target-mgmt, ymos-research | ymos-core |
| templates/memo.md | ymos-target-mgmt | ymos-core |
| route-cheatsheet.md | 多 skill 路由参考 | ymos-core |
| watchlist-update-workflow.md | ymos-radar, ymos-target-mgmt | ymos-core |
| knowledge/diagnosis/* | ymos-diagnosis | ymos-diagnosis |

## Capabilities

### New Capabilities
- `ymos-core`: 跨 skill 共享的基础设施 skill，包含共享 prompts (p2, p9)、templates、路由速查表、投资公理框架。其他 skill 通过依赖声明引用。

### Modified Capabilities
- `skill-ymos-strategy`: 吸收 SOP + 独占 prompts (p3, p5-p8, p10-p12, p17)，引用路径从 references/ 改为 skill 内
- `skill-ymos-research`: 吸收 SOP + 独占 prompts (p1, p4)，引用路径从 references/ 改为 skill 内
- `skill-ymos-market-insight`: 吸收 SOP + 独占 prompts (p13-p16, cio-rss-processor)
- `skill-ymos-radar`: 吸收 SOP
- `skill-ymos-onboarding`: 吸收 SOP
- `skill-ymos-reconcile`: 吸收 SOP
- `skill-ymos-target-mgmt`: 吸收 SOP
- `ymos-diagnosis`: 吸收 knowledge 文档

## Impact

- **目录结构**：`references/` 移除，`skills/` 每个子目录扩展为多文件结构
- **SKILL.md**：所有 8 个现有 skill 的引用路径需更新
- **CLAUDE.md**：架构描述从"四层"调整为"三层"（skills + data + cli），移除 references 层
- **AGENT_GUIDE.md**：文档引用路径同步更新
- **无代码影响**：此变更仅涉及 Markdown 文档移动和路径引用更新，不涉及 Python CLI 代码
