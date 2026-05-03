# 动作 B：建仓（Watchlist → 持仓）

**前置**：标的必须已在 Watchlist 中，且 P1+P4+P2 已完成

**Step 1**：检查前置
- 确认 `动态Watchlist/名称_TICKER/个股基础知识库.md` 存在且有 P1+P4+P2
- **若标的不在 Watchlist**：自动先执行「动作 A：关注」完整流程
- **若缺少 P1/P4/P2**：调用 `skills/ymos-research/sop.md` 补跑

**Step 2**：迁移目录
```bash
mv "data/stocks/watchlist/名称_TICKER" "data/stocks/holdings/名称_TICKER"
```

**Step 3**：初始化买入卖出备忘录
- 从模板创建 `买入卖出备忘录.md`（持仓才需要）

**Step 4**：更新状态机
- `Watchlist_状态机.md`：移除或标记「已建仓」
- `持仓_状态机.md`：新增，状态「持仓中」

**Step 5**：确认
```
✅ [名称]（[TICKER]）已从 Watchlist 升级为持仓
- 目录：data/持仓/名称_TICKER/
- 买入卖出备忘录已初始化
- 下一步：建议执行「我想买 TICKER」进入策略分析
```
