## Context

YMOS 经历了从 V3（三模块制：Eyes / Brain / 持仓与关注）到 V4（9 skills + ymos-core 共享层）的架构重构。目录结构已迁移完毕：

| V3 旧路径 | V4 新路径 |
|:---|:---|
| `Eyes/市场洞察/` | `data/reports/market-insight/` |
| `Eyes/投资雷达/` | `data/reports/radar/` |
| `Brain/策略分析/` | `data/reports/strategy/` |
| `Eyes/scripts/fetch_*.py` | `cli/`（统一 ymos CLI） |
| `Brain/SOP_初始调研.md` | `skills/ymos-research/sop.md` |
| `Brain/SOP_策略分析.md` | `skills/ymos-strategy/sop.md` |
| `Eyes/SOP_市场洞察.md` | `skills/ymos-market-insight/sop.md` |
| `Eyes/SOP_投资雷达.md` | `skills/ymos-radar/sop.md` |
| `持仓与关注/` | `data/stocks/holdings/` + `data/stocks/watchlist/` |

但 SOP、SKILL.md、routing.md 中的路径引用和模块描述仍停留在 V3，与实际目录不一致。

## Goals / Non-Goals

**Goals:**
- 所有 skills/ 下的 markdown 文件路径引用与当前 V4 目录结构一致
- 模块描述从"Eyes/Brain"术语更新为对应 skill 名称
- 版本标注统一为 YMOS V4

**Non-Goals:**
- 不修改 cli/ 代码或 data/ 目录结构
- 不修改 CLAUDE.md（已正确描述 V4 架构）
- 不修改 `data/` 下的运行时数据文件

## Decisions

**D1: 路径映射表**

采用上述映射表，逐文件全局替换。关键转换规则：
- `Eyes/市场洞察/YYYY-MM/Raw_Data/` → `data/reports/market-insight/raw/YYYY-MM/`
- `Eyes/投资雷达/YYYY-MM/Raw_Data/` → `data/reports/radar/raw/YYYY-MM/`
- `Brain/策略分析/Raw_Data/` → `data/reports/strategy/raw/`
- `Eyes/scripts/` → `cli/`（所有 fetch_* 脚本已合并为 `ymos` CLI 子命令）
- `持仓与关注/{holdings,watchlist}/` → `data/stocks/{holdings,watchlist}/`

**D2: 模块描述更新**

- `> 模块：Eyes/（眼睛 — 盯市场）` → `> 模块：ymos-market-insight / ymos-radar（市场监控）`
- `> 模块：Brain/（大脑 — 策略路由 + 分析）` → `> 模块：ymos-strategy / ymos-research（策略分析）`
- `Eyes → Brain` 流程描述 → 对应 skill 调用链

**D3: 版本标注统一**

`*SOP 版本：2026-03-18 · YMOS V3 三模块制（Eyes / Brain / 持仓与关注）*` → `*SOP 版本：2026-04-27 · YMOS V4 Skills 架构*`

**D4: 执行策略**

按 skill 分组逐文件修改，每个 skill 的 sop.md 和 SKILL.md 一起处理，确保路径一致性。ymos-core 的 routing.md 最后处理（它引用最多）。

## Risks / Trade-offs

- [遗漏引用] → 修改后用 grep 验证无残留 `Eyes/`、`Brain/`、`持仓与关注` 引用
- [Raw_Data vs raw 大小写] → 实际目录同时存在两套，SOP 统一使用 `raw`（小写，新标准）
- [routing.md 概念描述] → 保留"Eyes → Brain"作为流程概念说明的可读性，但具体路径全部替换为实际路径
