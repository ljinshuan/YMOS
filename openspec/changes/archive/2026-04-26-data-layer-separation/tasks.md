## 1. 创建目录结构

- [x] 1.1 创建 `data/` 顶层目录及全部子目录（state/、stocks/holdings/、stocks/watchlist/、reports/market-insight/raw/、reports/radar/raw/、reports/strategy/raw/、dashboard/）

## 2. 迁移状态数据

- [x] 2.1 迁移 `持仓与关注/持仓_状态机.md` → `data/state/holdings.md`
- [x] 2.2 迁移 `持仓与关注/Watchlist_状态机.md` → `data/state/watchlist.md`
- [x] 2.3 迁移 `持仓与关注/当前关注方向与投资偏好.md` → `data/state/preferences.md`
- [x] 2.4 迁移 `持仓与关注/持仓备忘录_视图.md` → `data/state/memo-view.md`

## 3. 迁移个股文件夹

- [x] 3.1 迁移 `持仓与关注/持仓/` 下所有标的目录 → `data/stocks/holdings/`
- [x] 3.2 迁移 `持仓与关注/动态Watchlist/` 下所有标的目录 → `data/stocks/watchlist/`

## 4. 迁移报告

- [x] 4.1 迁移 `Eyes/市场洞察/` 报告和 Raw_Data → `data/reports/market-insight/`
- [x] 4.2 迁移 `Eyes/投资雷达/` 报告和 Raw_Data → `data/reports/radar/`
- [x] 4.3 迁移 `Brain/策略分析/` 报告和 Raw_Data → `data/reports/strategy/`（源目录为空，仅 .gitkeep，无需迁移）

## 5. 更新 .gitignore

- [x] 5.1 在 `.gitignore` 中添加 `data/` 忽略规则

## 6. 清理旧目录

- [ ] 6.1 确认所有数据迁移完成后，删除旧目录下的已迁移文件和空目录

## 7. 验证

- [x] 7.1 验证所有文件迁移路径正确、内容完整（diff 验证通过）
- [ ] 7.2 验证 `ymos migrate` 命令可以自动完成以上迁移（对测试数据）
