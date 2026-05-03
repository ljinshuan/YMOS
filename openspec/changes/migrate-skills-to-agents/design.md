## Context

YMOS 的 11 个技能目录（72 个文件）位于项目根目录 `skills/`，而 Claude Code 的 agent skill 发现机制使用 `.agents/skills/` 标准路径。`.agents/skills/` 已有 10 个 openspec 相关技能。本次重构将所有 ymos 技能迁移到标准路径下，统一管理。

当前状态：
- `skills/` — 11 个 ymos 技能（ymos-core, ymos-onboarding, ymos-market-insight, ymos-radar, ymos-research, ymos-strategy, ymos-target-mgmt, ymos-reconcile, ymos-diagnosis, ymos-screener, ymos-sentiment）
- `.agents/skills/` — 10 个 openspec 技能
- CLAUDE.md、AGENT_GUIDE.md、总入口暗号.md 中大量 `skills/` 路径引用

## Goals / Non-Goals

**Goals:**
- 将全部 11 个技能目录从 `skills/` 迁移到 `.agents/skills/`
- 更新所有文档中的路径引用，确保引用正确
- 保持 git 历史可追踪（使用 `git mv`）

**Non-Goals:**
- 不改变任何技能内容或业务逻辑
- 不修改 openspec/specs 中的功能规格
- 不改变 CLI 工具的路径引用（cli/ 不引用 skills/ 路径）

## Decisions

### 1. 使用 `git mv` 而非手动复制

**选择**: `git mv skills/<skill> .agents/skills/<skill>`

**替代方案**: 手动复制 + 删除旧目录

**理由**: `git mv` 保留文件历史，便于后续追溯变更

### 2. 逐个 skill 迁移而非批量

**选择**: 每个 skill 单独 `git mv`，迁移后立即验证

**替代方案**: `mv skills/* .agents/skills/` 一次性移动

**理由**: 逐个迁移更安全，出现问题时容易回滚；也便于分步提交

### 3. 路径引用更新采用全局替换

**选择**: 对每个文档文件进行 `skills/` → `.agents/skills/` 的精确替换

**理由**: 引用点集中在 CLAUDE.md、AGENT_GUIDE.md、总入口暗号.md 三个文件，全局替换高效且准确

### 4. spec 文件中路径不修改

**选择**: openspec/specs/ 下的 spec 文件保持原样

**理由**: spec 描述的是能力行为（WHAT），不是文件位置（WHERE）。路径是实现细节，spec 层面无需变更

## Risks / Trade-offs

- **[风险] Agent 路径发现失败** → 迁移后立即验证每个 SKILL.md 的可访问性，确认 Agent 能从新路径读取
- **[风险] 遗漏路径引用** → 使用 `grep -r "skills/" ` 全项目扫描，确保无遗漏
- **[风险] `.agents/` 在 `.gitignore` 中被忽略** → 验证 `.gitignore` 规则，确保 `.agents/skills/` 可被 git 追踪
- **[Trade-off] `.agents/` 是隐藏目录，IDE 中默认不可见** → 这是 Claude Code 的标准约定，接受此 trade-off

## Migration Plan

1. 验证 `.agents/skills/` 不在 `.gitignore` 中
2. 逐个 `git mv` 迁移 11 个 skill 目录
3. 更新 CLAUDE.md、AGENT_GUIDE.md、总入口暗号.md 中的路径引用
4. 全项目 grep 扫描确认无遗漏
5. 验证 Agent 可从新路径发现并读取技能
6. 删除空的 `skills/` 目录

**回滚策略**: `git reset` 或 `git revert` 即可完全回滚
