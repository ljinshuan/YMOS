# 动作 C：移除关注（Watchlist → 归档）

**Step 1**：归档目录
```bash
mkdir -p "data/stocks/watchlist/_archive"
mv "data/stocks/watchlist/名称_TICKER" "data/stocks/watchlist/_archive/名称_TICKER"
```

**Step 2**：更新 `Watchlist_状态机.md`（标记「已归档」+ 日期）
