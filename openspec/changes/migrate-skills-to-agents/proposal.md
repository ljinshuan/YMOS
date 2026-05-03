## Why

当前 YMOS 技能定义分散在 `skills/` 目录，而 Claude Code 的 agent skill 发现机制（`.agents/skills/`）才是标准路径。将技能迁移到 `.agents/skills/` 可以让 Agent 自动发现并加载技能，无需手动读取路径；同时 `.agents/` 目录已有 openspec 相关技能，迁移后所有技能统一管理。

## What Changes

- **BREAKING**: 将 `skills/` 下全部 11 个技能目录迁移到 `.agents/skills/` 下
- 删除旧的 `skills/` 目录
- 更新 `CLAUDE.md` 中所有 `skills/` 路径引用为 `.agents/skills/`
- 更新 `AGENT_GUIDE.md` 中所有 `skills/` 路径引用为 `.agents/skills/`
- 更新 `总入口暗号.md` 中的路径引用
- 更新 `openspec/specs/` 中相关 spec 文件的路径引用（如有）
- 更新 `.gitignore` 如有 `skills/` 相关规则

## Capabilities

### New Capabilities
- `skill-directory-migration`: 定义技能从 `skills/` 迁移到 `.agents/skills/` 的完整流程，包括文件移动、路径引用更新、验证

### Modified Capabilities
- `ymos-core`: 路径从 `skills/ymos-core` 变为 `.agents/skills/ymos-core`
- `skill-ymos-onboarding`: 路径更新
- `skill-ymos-market-insight`: 路径更新
- `skill-ymos-radar`: 路径更新
- `skill-ymos-research`: 路径更新
- `skill-ymos-strategy`: 路径更新
- `skill-ymos-target-mgmt`: 路径更新
- `skill-ymos-reconcile`: 路径更新
- `data-directory-layout`: 架构描述中 skills/ 路径需更新

## Impact

- **CLAUDE.md**: 大量 `skills/` 引用需改为 `.agents/skills/`
- **AGENT_GUIDE.md**: 路径引用全面更新
- **总入口暗号.md**: 路由表路径更新
- **openspec/specs/**: ~10 个 spec 文件可能包含 `skills/` 路径引用
- **skills/**: 11 个目录、72 个文件整体迁移
- **.agents/skills/**: 现有 10 个 openspec 技能目录保持不变，新增 11 个 ymos 技能目录
- **Git**: 大量文件 rename（`git mv`），但内容不变，git 历史可追踪
