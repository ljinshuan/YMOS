# 🏷️ 标的管理 SOP

> 暗号：`关注 XXX` / `建仓 XXX` / `移除关注 XXX` / `清仓 XXX`
> 模块：ymos-target-mgmt（标的状态管理）

---

## 一句话定位

标的管理做两件事：**维护持仓与关注的状态真相源** + **触发初始调研（同步或异步）**

- 关注 = 创建目录 + 初始化文档 + 智能触发初始调研
- 建仓/清仓只是状态迁移，不包含买卖决策（那是策略分析的事）
- 初始调研的实际执行由 `skills/ymos-research/sop.md` 负责

---

## 🔑 触发暗号

| 暗号 | 动作 | 说明 |
|:---|:---|:---|
| `关注 [ticker/名称]` | 新增到 Watchlist + 触发初始调研 | 询问是否立即调研，否则异步 |
| `建仓 [ticker/名称]` | 从 Watchlist 升级到持仓 | 状态迁移 + 前置检查 |
| `移除关注 [ticker/名称]` | 从 Watchlist 归档 | 状态迁移 + 归档 |
| `清仓 [ticker/名称]` | 从持仓归档（保留观察） | 状态迁移 + 复盘提醒 |

---

## ⚙️ 执行步骤

### 动作 A：关注（新增 Watchlist + 触发初始调研）

> 详细执行步骤见 `sop/action-a-watch.md`

---

### 动作 B：建仓（Watchlist → 持仓）

> 详细执行步骤见 `sop/action-b-position.md`

---

### 动作 C：移除关注（Watchlist → 归档）

> 详细执行步骤见 `sop/action-c-remove.md`

---

### 动作 D：清仓（持仓 → Watchlist 保留观察）

> 详细执行步骤见 `sop/action-d-liquidate.md`

---

## 📦 产出物清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 个股基础知识库 | `data/{位置}/名称_TICKER/个股基础知识库.md` | 关注时初始化 |
| 买入卖出备忘录 | `data/持仓/名称_TICKER/买入卖出备忘录.md` | 建仓时初始化 |
| 状态机 | `data/state/watchlist.md` / `data/state/holdings.md` | 每次更新 |

---

## 📁 路径速查

| 内容 | 路径 |
|:---|:---|
| 初始调研 SOP | `skills/ymos-research/sop.md` |
| P 提示词目录 | `skills/<skill>/prompts/` 或 `skills/ymos-core/prompts/` |
| 模板 | `skills/ymos-core/templates/` |
| 状态机 | `data/state/watchlist.md` / `data/state/holdings.md` |

---

## ⚠️ 边界

- 标的管理的**分析部分由初始调研子模块 SOP 负责**
- 建仓/清仓只是状态迁移，**不包含买卖决策**
- 目录命名统一为 `名称_TICKER`，价格扫描只认状态机 Ticker 列
- Watchlist 不需要买入卖出备忘录（建仓时才初始化）

---

*SOP 版本：2026-04-27 · YMOS V4 Skills 架构*
