## Why

skills/ 目录已从 V3 三模块制（Eyes / Brain / 持仓与关注）重构为 V4 Skills 架构（9 个 ymos-* skill + ymos-core 共享层），数据目录也从 `Eyes/`、`Brain/`、`持仓与关注/` 迁移到 `data/reports/`、`data/stocks/`、`data/state/`。但 SOP、SKILL.md、routing.md 等文件中仍大量引用旧路径，导致文档与实际目录结构不一致。

## What Changes

- 修正所有 `Eyes/市场洞察/` 引用 → `data/reports/market-insight/`
- 修正所有 `Eyes/投资雷达/` 引用 → `data/reports/radar/`
- 修正所有 `Brain/策略分析/` 引用 → `data/reports/strategy/`
- 修正所有 `Eyes/scripts/fetch_*.py` 引用 → `cli/`（统一 ymos CLI）
- 修正所有 `Brain/SOP_初始调研.md` 引用 → `skills/ymos-research/sop.md`
- 修正所有 `Brain/SOP_策略分析.md` 引用 → `skills/ymos-strategy/sop.md`
- 修正所有 `Eyes/SOP_市场洞察.md` 引用 → `skills/ymos-market-insight/sop.md`
- 修正所有 `Eyes/SOP_投资雷达.md` 引用 → `skills/ymos-radar/sop.md`
- 修正所有 `持仓与关注/{位置}/名称_TICKER/` 引用 → `data/stocks/holdings/` 或 `data/stocks/watchlist/`
- 修正模块描述 `Eyes/（眼睛 — 盯市场）` → 当前 skill 对应描述
- 修正模块描述 `Brain/（大脑 — 策略路由 + 分析）` → 当前 skill 对应描述
- 修正版本标注 `YMOS V3 三模块制（Eyes / Brain / 持仓与关注）` → `YMOS V4 Skills 架构`
- 修正流程描述 `Eyes → Brain` → 对应 skill 调用链

## Capabilities

### New Capabilities

（无新能力引入）

### Modified Capabilities

- `ymos-market-insight`: SOP 路径引用修正（Eyes → data/reports/market-insight）
- `ymos-radar`: SOP + SKILL.md 路径引用修正（Eyes → data/reports/radar）
- `ymos-strategy`: SOP + SKILL.md 路径引用修正（Brain → data/reports/strategy）
- `ymos-research`: SOP 版本标注修正
- `ymos-target-mgmt`: SOP 路径引用修正（Brain/SOP → skills/ymos-*）
- `ymos-reconcile`: SOP + SKILL.md 路径引用修正
- `ymos-core`: routing.md + watchlist-update-workflow.md 全面路径更新

## Impact

- 影响文件：6 个 skill 的 sop.md / SKILL.md + ymos-core 的 routing.md / watchlist-update-workflow.md，共约 15 个文件
- 纯文档修正，无代码变更，无功能影响
- 不影响 CLI 工具或数据目录结构
