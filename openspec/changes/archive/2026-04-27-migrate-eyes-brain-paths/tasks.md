## 1. ymos-market-insight 路径修正

- [x] 1.1 修正 `skills/ymos-market-insight/sop.md`：替换所有 `Eyes/市场洞察/` → `data/reports/market-insight/`，`Eyes/scripts/` → `cli/`，模块描述 → V4，版本标注 → V4
- [x] 1.2 修正 `skills/ymos-market-insight/SKILL.md`：替换所有 `Eyes/市场洞察/` → `data/reports/market-insight/`
- [x] 1.3 修正 `skills/ymos-market-insight/prompts/p13-market-scanner.md`：替换 `Eyes/` 路径引用
- [x] 1.4 修正 `skills/ymos-market-insight/prompts/p14-sector-hunter.md`：替换 `Eyes/` 路径引用

## 2. ymos-radar 路径修正

- [x] 2.1 修正 `skills/ymos-radar/sop.md`：替换所有 `Eyes/投资雷达/` → `data/reports/radar/`，`Eyes/scripts/` → `cli/`，`Eyes/市场洞察/` → `data/reports/market-insight/`，模块描述 → V4，版本标注 → V4
- [x] 2.2 修正 `skills/ymos-radar/SKILL.md`：替换所有 `Eyes/投资雷达/` → `data/reports/radar/`

## 3. ymos-strategy 路径修正

- [x] 3.1 修正 `skills/ymos-strategy/sop.md`：替换所有 `Brain/策略分析/` → `data/reports/strategy/`，`Eyes/投资雷达/` → `data/reports/radar/`，`Brain/SOP_初始调研.md` → `skills/ymos-research/sop.md`，`Brain/SOP_策略分析.md` → `skills/ymos-strategy/sop.md`，`持仓与关注/` → `data/stocks/`，模块描述 → V4，版本标注 → V4
- [x] 3.2 修正 `skills/ymos-strategy/SKILL.md`：替换所有 `Brain/` 和 `Eyes/` 路径引用

## 4. ymos-research 路径修正

- [x] 4.1 修正 `skills/ymos-research/sop.md`：模块描述 → V4，版本标注 → V4

## 5. ymos-target-mgmt 路径修正

- [x] 5.1 修正 `skills/ymos-target-mgmt/sop.md`：替换 `Brain/SOP_初始调研.md` → `skills/ymos-research/sop.md`，`持仓与关注/` → `data/stocks/`，版本标注 → V4

## 6. ymos-reconcile 路径修正

- [x] 6.1 修正 `skills/ymos-reconcile/sop.md`：替换 `Eyes/` → `data/reports/`，`Brain/` → `data/reports/`
- [x] 6.2 修正 `skills/ymos-reconcile/SKILL.md`：替换 `Eyes/` → `data/reports/`，`Brain/` → `data/reports/`

## 7. ymos-core 路径修正

- [x] 7.1 修正 `skills/ymos-core/routing.md`：全面替换所有 `Eyes/`、`Brain/`、`持仓与关注/` 路径引用为 V4 对应路径
- [x] 7.2 修正 `skills/ymos-core/watchlist-update-workflow.md`：替换 `Eyes/投资雷达/` → `data/reports/radar/`

## 8. 验证

- [x] 8.1 全局 grep 验证：`skills/` 下无残留 `Eyes/`、`Brain/`、`持仓与关注` 路径引用
- [x] 8.2 确认所有版本标注已更新为 `YMOS V4`
