# Route Cheatsheet（暗号 → Skill → 提示词 → 写回）

> 一页速查：先判触发类型，再按 Watchlist / 持仓分流。
> 完整暗号表见 `总入口暗号.md`，各 SOP 见 `skills/ymos-*/sop.md`。

---

## 0) 智能路由（意图分类层）

用户输入先进入意图分类层，再路由到具体 Skill。

```
用户输入
  ├── 命中触发词？ ──是──→ 直达对应 Skill（跳过分类）
  └── 否 ──→ intent-classifier.md 分类 → 8 种意图 → 路由表 → Skill 链路
```

**8 种意图 → Skill 映射：**

| 意图 | 路由目标 | 提示词 |
|:---|:---|:---|
| `market-overview` | ymos-market-insight | CIO + P13 |
| `investment-radar` | ymos-radar | 价格扫描 + 7天趋势 |
| `stock-research` | ymos-research | P1 → P4 → P2 |
| `buy-entry` | ymos-strategy Route A/B | P2 → P9 → P5 → P12 |
| `hold-evaluate` | ymos-strategy Route C | P2 → P6 → P12 |
| `sell-reduce` | ymos-strategy Route D | P2 → P6 → P10 → P12 |
| `portfolio-mgmt` | ymos-strategy Route E + reconcile | P7 / 一致性校验 |
| `system-ops` | onboarding / target-mgmt / diagnosis | 按 SOP 执行 |

**复合意图：** 多意图自动拆分为有序任务列表，按逻辑依赖排序（调研 → 策略 → 管理）。
详见 `skills/ymos-core/prompts/intent-classifier.md`。

---

## 1) 通用前置

执行策略前必须确认：
1. 已读取 `个股基础知识库.md`
2. 已执行 P2（阶段与玩家）
3. 已读取 `买入卖出备忘录.md`
4. 已读取 `data/state/preferences.md`
5. 最终过 P12（纪律审查）

---

## 2) 市场扫描入口

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| `跑一下市场洞察` | `skills/ymos-market-insight/sop.md` | CIO + P13（+ P14 按需） | `data/reports/market-insight/YYYY-MM/` |
| `跑一下投资雷达` | `skills/ymos-radar/sop.md` | 7天趋势 + 价格扫描 + 资金流扫描 + 多源新闻 | `data/reports/radar/YYYY-MM/` + 状态机 |
| `查一下价格` | `skills/ymos-radar/sop.md`（子流程） | Finnhub/Tushare/Yahoo/Futu 价格路由 | `data/reports/radar/raw/YYYY-MM/` |
| `查一下资金流` | `skills/ymos-radar/sop.md`（子流程） | P20 资金异动分析 | `data/reports/radar/raw/YYYY-MM/` |
| `有什么资金异动` | `skills/ymos-radar/sop.md`（子流程） | P20 资金异动分析 | `data/reports/radar/raw/YYYY-MM/` |

---

## 3) Watchlist 分流（目标：建仓机会）

| 触发 | Skill 链路 | 提示词顺序 | 写回 |
|:---|:---|:---|:---|
| 价格触发 | ymos-radar → ymos-strategy | Quotes → P2/P9(按需) → P5/P10 → P12 | `data/state/watchlist.md` + 标的双文档 |
| 事件触发 | ymos-radar → ymos-strategy | P13/P14 → P3/P15/P16(按需) + P2 → P5/P10 → P12 | 同上 |
| 宏观触发 | ymos-radar → ymos-strategy | P13 → P8 + P2 → P5(更严格门槛) → P12 | 同上 |

---

## 4) 持仓分流（目标：加仓/持有/卖出）

| 触发 | Skill 链路 | 提示词顺序 | 写回 |
|:---|:---|:---|:---|
| 价格触发 | ymos-radar → ymos-strategy | Quotes → P2/P3(按需) → P6/P10 → P12 | `data/state/holdings.md` + 标的`买入卖出备忘录.md` |
| 事件触发 | ymos-radar → ymos-strategy | P13/P14 → P3/P15/P16 + P2 → P6/P10 → P12 | 同上 |
| 宏观触发 | ymos-radar → ymos-strategy | P13 → P8 + P2 → P6(必要时) → P12 | 同上 |

---

## 5) 人工意图直达

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| `调研一下 [股票]` | `skills/ymos-research/sop.md` | P1 → P4（可加 P9） | 标的`个股基础知识库.md` |
| `大师会诊 [股票]` | `skills/ymos-research/sop.md` | P1 → P4 → P18 → P2 | 标的`个股基础知识库.md`（含大师会诊章节） |
| `我想买 [股票]` | `skills/ymos-strategy/sop.md` | P2 → P9 → P5/P10 → P12 | 标的`买入卖出备忘录.md` + `data/reports/strategy/` |
| `我想卖 [股票]` | `skills/ymos-strategy/sop.md` | P2 → P6/P10 → P12 | 标的`买入卖出备忘录.md` + `data/reports/strategy/` |
| `复盘一下` | `skills/ymos-strategy/sop.md` | P11（个股）/ P7（组合） | `data/reports/strategy/` |

---

## 6) 策略分析五大路由（详细版）

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

## 7) 标的管理

| 暗号 | SOP | 动作 | 写回 |
|:---|:---|:---|:---|
| `关注 XX` | `skills/ymos-target-mgmt/sop.md` | 新增 Watchlist + 可选初始调研 | `data/state/watchlist.md` + 标的文件夹 |
| `建仓 XX` | `skills/ymos-target-mgmt/sop.md` | 新增持仓 + 可选初始调研 | `data/state/holdings.md` + 标的文件夹 |
| `移除关注 XX` | `skills/ymos-target-mgmt/sop.md` | Watchlist → 归档 | `data/state/watchlist.md` |
| `清仓 XX` | `skills/ymos-target-mgmt/sop.md` | 持仓 → 归档/降级 | `data/state/holdings.md` |

---

## 8) 情绪分析入口

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| `看一下 [ticker] 的情绪` | `skills/ymos-sentiment/sop.md` | P19（评论情绪分析） | `data/reports/sentiment/YYYY-MM/` |
| `[ticker] 多空怎么样` | `skills/ymos-sentiment/sop.md` | P19 | `data/reports/sentiment/YYYY-MM/` |
| `分析一下市场情绪` | `skills/ymos-sentiment/sop.md`（全持仓模式） | P19 × N | `data/reports/sentiment/YYYY-MM/` |
| `看一下情绪` | 同上 | P19 × N | 同上 |

**情绪数据与策略/雷达的关系：**
- ymos-strategy：P5（FOMO Killer）和 P12（纪律审查）可引用情绪数据作为辅助维度（非阻塞）
- ymos-radar：信号检测环节可检测极端情绪（bullish > 80% 或 bearish > 70%）作为预警信号

---

## 8.5) 资金流入口

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| `查一下资金流` | `skills/ymos-radar/sop.md`（资金流子流程） | P20（资金异动分析） | `data/reports/radar/raw/YYYY-MM/` + P4 更新 |
| `有什么资金异动` | `skills/ymos-radar/sop.md`（资金流子流程） | P20 | 同上 |

**资金流数据与策略/雷达的关系：**
- ymos-radar：Step 4.5 资金流扫描 → P20 分析 → 异动信号纳入 Tier 1/Tier 2 事件评级
- ymos-strategy：Route A/B 中 P12（纪律审查）可引用资金流数据作为辅助确认维度（非阻塞）
- 数据源：`ymos fetch-capital-flow fetch`（富途 OpenD `get_financial_unusual`）
- 前置条件：本地需运行 Futu OpenD（localhost:11111），未运行时跳过（非阻塞）

---

## 8.7) 持仓同步入口

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| `收口一下` | `skills/ymos-reconcile/sop.md`（Step 1.5） | Futu 真实持仓 vs 状态机校验 | `data/position/` + 缺口清单 |

**持仓数据与收口/雷达的关系：**
- ymos-reconcile：Step 1.5 调用 `ymos position fetch` 获取 broker 真实持仓，与状态机 ticker/数量做一致性校验
- ymos-radar：Step 5.2 持仓监控可引用 Futu 真实市值和盈亏数据（可选，非阻塞）
- 数据源：`ymos position fetch`（富途 OpenD `position_list_query`，需 `OpenSecTradeContext`）
- 前置条件：本地需运行 Futu OpenD（localhost:11111），未运行时跳过（非阻塞）

---

## 9) 选股筛选入口

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| `帮我选股` | `skills/ymos-screener/sop.md` | 预设模板或自定义筛选 | `data/reports/screener/YYYY-MM/` |
| `筛选一下 [市场]` | `skills/ymos-screener/sop.md` | 按市场筛选 | 同上 |
| `找一下 [类型]股` | `skills/ymos-screener/sop.md` | 按类型（成长/价值/高息/动量）筛选 | 同上 |
| `选股` | `skills/ymos-screener/sop.md` | 交互式选股 | 同上 |

**筛选 → 调研衔接**：
- 用户从筛选结果中选择标的 → `调研一下 [ticker]` → ymos-research P1→P4→P2
- 调研完成后 → 建议通过 `关注 [ticker]` 加入 Watchlist
- 数据源：`ymos screen`（富途 OpenD `get_stock_filter`）
- 前置条件：本地需运行 Futu OpenD（localhost:11111），未运行时提示启动

---

---

## 8.9) 交易记录入口

| 暗号 | SOP | 提示词 | 写回 |
|:---|:---|:---|:---|
| （内部调用） | `skills/ymos-strategy/sop.md`（P12 可选输入） | 交易行为实证 | `data/trade-history/` |
| （内部调用） | `skills/ymos-diagnosis/SKILL.md`（Phase 2B） | 行为偏误分析 | `data/trade-history/` |

**交易记录数据与策略/诊断的关系：**
- ymos-strategy：P12（纪律审查）可引用近期成交记录作为行为偏误的客观实证（如频繁换手、追涨杀跌）
- ymos-diagnosis：Phase 2B（情绪审计 + 仓位纪律）可引用成交记录分析交易行为模式
- ymos-reconcile：Step 2.5 可用成交记录校验状态机操作记录的完整性
- 数据源：`ymos trade-history fetch`（富途 OpenD `history_deal_list_query`，需 `OpenSecTradeContext`）
- 前置条件：本地需运行 Futu OpenD（localhost:11111），未运行时跳过（非阻塞）

---

## 10.5) 技术分析数据源

| 命令 | 数据源选项 | 说明 |
|:---|:---|:---|
| `ymos tech-analysis analyze --source auto` | Futu 优先 → Yahoo/Tushare 兜底 | 默认模式 |
| `ymos tech-analysis analyze --source futu` | 仅 Futu OpenD | OpenD 不可用时直接报错 |
| `ymos tech-analysis analyze --source yahoo` | 仅 Yahoo | 跳过 Futu |
| `ymos tech-analysis analyze --source tushare` | 仅 Tushare | 跳过 Futu |

**与策略分析的关系：**
- ymos-strategy 的 P2（阶段判断）和 P9（估值）可引用技术分析指标作为辅助维度
- 默认 `auto` 模式下，Futu 在线时优先使用富途 K 线数据（覆盖港股/A 股/美股）

---

## 10) 输出格式建议（每次）

1. 一句话结论
2. 动作建议（优先级）
3. 写回路径（具体文件）
