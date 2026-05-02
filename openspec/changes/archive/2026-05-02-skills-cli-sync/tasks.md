## 1. CLI 命令调用修复（子命令层级）

- [x] 1.1 修复 `skills/ymos-radar/SKILL.md:31`：`ymos price-scan --from-state` → `ymos price-scan scan --from-state`
- [x] 1.2 修复 `skills/ymos-radar/SKILL.md:36`：`ymos fetch-capital-flow --from-state` → `ymos fetch-capital-flow fetch --from-state`
- [x] 1.3 修复 `skills/ymos-radar/sop.md:91`：`ymos fetch-capital-flow --from-state` → `ymos fetch-capital-flow fetch --from-state`
- [x] 1.4 修复 `skills/ymos-radar/sop.md:74-75`：`--output` 参数改为 `--output-dir` + `--date-tag`
- [x] 1.5 修复 `skills/ymos-screener/SKILL.md:27`：`ymos screen --market` → `ymos screen screen --market`
- [x] 1.6 修复 `skills/ymos-sentiment/SKILL.md:32`：`ymos fetch-sentiment --ticker` → `ymos fetch-sentiment fetch --ticker`
- [x] 1.7 修复 `skills/ymos-sentiment/sop.md`（3处）：`uv run ymos fetch-sentiment --ticker` → 添加 `fetch` 子命令

## 2. 新闻 Futu 兜底描述更新

- [x] 2.1 更新 `skills/ymos-market-insight/SKILL.md:30`：fetch-news 描述改为"多源新闻：Finnhub + Futu 兜底，覆盖所有市场"
- [x] 2.2 更新 `skills/ymos-market-insight/sop.md:81-83`：补充 Futu 为 HK/CN ticker 提供兜底的说明

## 3. Position 接入 Skills

- [x] 3.1 在 `skills/ymos-reconcile/SKILL.md` 中添加可选步骤：调用 `ymos position fetch` 获取真实持仓进行校验
- [x] 3.2 在 `skills/ymos-reconcile/sop.md` 中添加 Step 1.5：Futu 持仓校验（OpenD 在线时执行，离线跳过）
- [x] 3.3 在 `skills/ymos-radar/sop.md` Step 5.2 中添加可选数据源说明：Futu 真实持仓数据

## 4. routing.md 更新

- [x] 4.1 在 `skills/ymos-core/routing.md` 中添加持仓同步入口（position fetch → reconcile）
- [x] 4.2 在 `skills/ymos-core/routing.md` 中更新新闻入口描述，反映 Futu 兜底
- [x] 4.3 在 `skills/ymos-core/routing.md` 中添加 tech-analysis --source 说明
