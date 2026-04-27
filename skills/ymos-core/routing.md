# Route Cheatsheet（暗号 → Skill → 提示词 → 写回）

> 一页速查：先判触发类型，再按 Watchlist / 持仓分流。
> 完整暗号表见 `总入口暗号.md`，各 SOP 见 `skills/ymos-*/sop.md`。

---

## 0) 通用前置

执行策略前必须确认：
1. 已读取 `个股基础知识库.md`
2. 已执行 P2（阶段与玩家）
3. 已读取 `买入卖出备忘录.md`
4. 已读取 `data/state/preferences.md`
5. 最终过 P12（纪律审查）

---

## 1) 市场扫描入口

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| `跑一下市场洞察` | `skills/ymos-market-insight/sop.md` | CIO + P13（+ P14 按需） | `data/reports/market-insight/YYYY-MM/` |
| `跑一下投资雷达` | `skills/ymos-radar/sop.md` | 7天趋势 + 价格扫描 + Finnhub新闻 | `data/reports/radar/YYYY-MM/` + 状态机 |
| `查一下价格` | `skills/ymos-radar/sop.md`（子流程） | Finnhub/Tushare/Yahoo 价格路由 | `data/reports/radar/raw/YYYY-MM/` |

---

## 2) Watchlist 分流（目标：建仓机会）

| 触发 | Skill 链路 | 提示词顺序 | 写回 |
|:---|:---|:---|:---|
| 价格触发 | ymos-radar → ymos-strategy | Quotes → P2/P9(按需) → P5/P10 → P12 | `data/state/watchlist.md` + 标的双文档 |
| 事件触发 | ymos-radar → ymos-strategy | P13/P14 → P3/P15/P16(按需) + P2 → P5/P10 → P12 | 同上 |
| 宏观触发 | ymos-radar → ymos-strategy | P13 → P8 + P2 → P5(更严格门槛) → P12 | 同上 |

---

## 3) 持仓分流（目标：加仓/持有/卖出）

| 触发 | Skill 链路 | 提示词顺序 | 写回 |
|:---|:---|:---|:---|
| 价格触发 | ymos-radar → ymos-strategy | Quotes → P2/P3(按需) → P6/P10 → P12 | `data/state/holdings.md` + 标的`买入卖出备忘录.md` |
| 事件触发 | ymos-radar → ymos-strategy | P13/P14 → P3/P15/P16 + P2 → P6/P10 → P12 | 同上 |
| 宏观触发 | ymos-radar → ymos-strategy | P13 → P8 + P2 → P6(必要时) → P12 | 同上 |

---

## 4) 人工意图直达

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| `调研一下 [股票]` | `skills/ymos-research/sop.md` | P1 → P4（可加 P9） | 标的`个股基础知识库.md` |
| `我想买 [股票]` | `skills/ymos-strategy/sop.md` | P2 → P9 → P5/P10 → P12 | 标的`买入卖出备忘录.md` + `data/reports/strategy/` |
| `我想卖 [股票]` | `skills/ymos-strategy/sop.md` | P2 → P6/P10 → P12 | 标的`买入卖出备忘录.md` + `data/reports/strategy/` |
| `复盘一下` | `skills/ymos-strategy/sop.md` | P11（个股）/ P7（组合） | `data/reports/strategy/` |

---

## 5) 策略分析五大路由（详细版）

> 完整 SOP 见 `skills/ymos-strategy/sop.md`
> 进入任何路由前必须完成四项强制前置校验（P2 / 个股知识库 / 备忘录 / 当前策略）

| 动作意图 | 提示词顺序 | 归档路径 |
|:---|:---|:---|
| **买入（首次建仓）** | P2 → P9 → P5 → [P10] → P12 | `data/reports/strategy/YYYY-MM/YYYY-MM-DD_TICKER_买入.md` |
| **加仓** | P2 → P3/P9(按需) → P5 → P12 | `data/reports/strategy/YYYY-MM/YYYY-MM-DD_TICKER_加仓.md` |
| **持有评估** | P2 → P6 → [P3/P8] → P12 | `data/reports/strategy/YYYY-MM/YYYY-MM-DD_TICKER_持有.md` |
| **减仓/卖出** | 读备忘录核对买入理由 → P2 → P6 → [P10] → P12 | `data/reports/strategy/YYYY-MM/YYYY-MM-DD_TICKER_卖出.md` |
| **仓位再平衡** | 读状态机 → P7 → [P6×n] → P12 | `data/reports/strategy/YYYY-MM/YYYY-MM-DD_仓位再平衡.md` |

---

## 6) 标的管理

| 暗号 | SOP | 动作 | 写回 |
|:---|:---|:---|:---|
| `关注 XX` | `skills/ymos-target-mgmt/sop.md` | 新增 Watchlist + 可选初始调研 | `data/state/watchlist.md` + 标的文件夹 |
| `建仓 XX` | `skills/ymos-target-mgmt/sop.md` | 新增持仓 + 可选初始调研 | `data/state/holdings.md` + 标的文件夹 |
| `移除关注 XX` | `skills/ymos-target-mgmt/sop.md` | Watchlist → 归档 | `data/state/watchlist.md` |
| `清仓 XX` | `skills/ymos-target-mgmt/sop.md` | 持仓 → 归档/降级 | `data/state/holdings.md` |

---

## 7) 输出格式建议（每次）

1. 一句话结论
2. 动作建议（优先级）
3. 写回路径（具体文件）
