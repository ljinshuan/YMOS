---
name: ymos-target-mgmt
metadata:
  depends_on: [ymos-core]
description: |
  标的状态管理（关注/建仓/移除/清仓）。触发方式：/ymos-target-mgmt、「关注/建仓/移除关注/清仓 [ticker]」
---

# ymos-target-mgmt：标的管理

## 触发
- `关注 [ticker/名称]` — 新增到 Watchlist + 触发初始调研
- `建仓 [ticker/名称]` — Watchlist → 持仓
- `移除关注 [ticker/名称]` — Watchlist → 归档
- `清仓 [ticker/名称]` — 持仓 → Watchlist（保留观察）+ 复盘提醒

## 前置条件
- 关注：无前置
- 建仓：标的需已在 Watchlist 且 P1+P4+P2 已完成（缺失时自动调用 `ymos-research` 补跑）
- 移除/清仓：标的需存在于对应状态机

## 执行步骤
> 详细步骤见 sop.md

### 动作 A：关注
1. 确认标的信息 + 自动补全 ticker 后缀（A股 `.SS/.SZ`，港股 `.HK`）
2. 创建目录：`data/动态Watchlist/名称_TICKER/`
3. 初始化 `个股基础知识库.md`（从模板或最小骨架）
4. 写入 `Watchlist_状态机.md`（新增行）
5. 询问是否立即调研 → 是则调用 `ymos-research`，否则异步（雷达会捕获）

### 动作 B：建仓
1. 检查前置（标的在 Watchlist + P1/P4/P2 完整）
2. 迁移目录：`动态Watchlist/名称_TICKER` → `持仓/名称_TICKER`
3. 初始化 `买入卖出备忘录.md`
4. 更新状态机（Watchlist 移除/标记 + 持仓新增）

### 动作 C：移除关注
1. 归档：`动态Watchlist/名称_TICKER` → `动态Watchlist/_archive/名称_TICKER`
2. 更新 Watchlist 状态机

### 动作 D：清仓
1. 迁移：`持仓/名称_TICKER` → `动态Watchlist/名称_TICKER`
2. 更新状态机（持仓移除 + Watchlist 新增「观察中（已清仓）」）
3. 追加清仓记录到 `买入卖出备忘录.md`
4. 生成复盘提醒：`data/投资复盘/YYYY-MM-DD_TICKER_清仓复盘.md`

## 产出物
- 个股文件夹（`data/{持仓,动态Watchlist}/名称_TICKER/`）
- `个股基础知识库.md`（关注时初始化）
- `买入卖出备忘录.md`（建仓时初始化）
- 状态机更新（每次操作）

## 边界
- 分析部分由 `ymos-research` 负责，标的管理只做状态迁移
- 建仓/清仓不包含买卖决策（那是 `ymos-strategy` 的事）
- Watchlist 不需要买入卖出备忘录（建仓时才初始化）
