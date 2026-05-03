# 动作 D：清仓（持仓 → Watchlist 保留观察）

**Step 1**：迁移到 Watchlist
```bash
mv "data/stocks/holdings/名称_TICKER" "data/stocks/watchlist/名称_TICKER"
```

**Step 2**：更新状态机
- `持仓_状态机.md`：移除或标记「已清仓」
- `Watchlist_状态机.md`：新增，状态「观察中（已清仓）」

**Step 3**：在 `买入卖出备忘录.md` 追加清仓记录

**Step 4**：生成复盘提醒
- 在 `data/reports/strategy/` 下创建 `YYYY-MM-DD_TICKER_清仓复盘.md`

**Step 5**：清理板块映射
- 若该 ticker 转入 watchlist，板块映射保留
- 若该 ticker 完全退出系统（不在 holdings 也不在 watchlist），从 `data/state/sector_mapping.md` 删除对应行
