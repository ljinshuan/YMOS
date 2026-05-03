# 动作 C：移除关注（Watchlist → 归档）

**Step 1**：归档目录
```bash
mkdir -p "data/stocks/watchlist/_archive"
mv "data/stocks/watchlist/名称_TICKER" "data/stocks/watchlist/_archive/名称_TICKER"
```

**Step 2**：更新 `Watchlist_状态机.md`（标记「已归档」+ 日期）

**Step 3**：清理板块映射
- 检查该 ticker 是否仍在 `data/state/holdings.md` 中
- 若不在持仓也不在 watchlist 中，从 `data/state/sector_mapping.md` 删除对应行
