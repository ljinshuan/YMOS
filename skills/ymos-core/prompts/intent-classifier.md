# 意图分类器 (Intent Classifier)

> 轻量级意图识别层，将用户自然语言映射到 YMOS skill 链路。
> 触发词命中时直接跳过本层，不消耗分类开销。

---

## 8 种意图定义

| ID | 意图 | 典型表达 | 路由目标 |
|:---|:---|:---|:---|
| `market-overview` | 市场概览 | "今天大盘怎么样"、"市场发生了什么" | ymos-market-insight |
| `investment-radar` | 投资雷达 | "和我持仓有什么关系"、"有没有需要关注的" | ymos-radar |
| `stock-research` | 个股调研 | "帮我看看NIO"、"这个公司怎么样" | ymos-research (P1→P4→P2) |
| `buy-entry` | 买入/建仓 | "想买AAPL"、"NIO可以入吗"、"这个价位能不能建仓" | ymos-strategy Route A/B (P2→P9→P5→P12) |
| `hold-evaluate` | 持有评估 | "AAPL还拿着吗"、"现在持有怎么看" | ymos-strategy Route C (P2→P6→P12) |
| `sell-reduce` | 卖出/减仓 | "想卖NIO"、"要不要减仓"、"止损吧" | ymos-strategy Route D (P2→P6→P10→P12) |
| `portfolio-mgmt` | 组合管理 | "做个再平衡"、"仓位怎么调"、"收口一下" | ymos-strategy Route E (P7) + ymos-reconcile |
| `system-ops` | 系统操作 | "开始使用"、"关注AAPL"、"清仓NIO"、"诊断一下" | ymos-onboarding / ymos-target-mgmt / ymos-diagnosis |

---

## 路由表

```
意图            → Skill 链路                              → 提示词顺序              → 写回
─────────────────────────────────────────────────────────────────────────────────────────────────
market-overview → ymos-market-insight                      → CIO + P13               → data/reports/market-insight/
investment-radar→ ymos-radar                               → 价格扫描 + 7天趋势       → data/reports/radar/
stock-research  → ymos-research                            → P1 → P4 → P2            → 标的 个股基础知识库.md
buy-entry       → ymos-strategy                            → P2 → P9 → P5 → P12     → 标的 买入卖出备忘录.md
hold-evaluate   → ymos-strategy                            → P2 → P6 → P12          → 标的 买入卖出备忘录.md
sell-reduce     → ymos-strategy                            → P2 → P6 → P10 → P12    → 标的 买入卖出备忘录.md
portfolio-mgmt  → ymos-strategy + ymos-reconcile           → P7 / 一致性校验          → data/reports/strategy/
system-ops      → ymos-onboarding / target-mgmt / diagnosis → 按 SOP 执行             → 对应状态机
```

---

## 复合意图处理

当用户一句话包含多个意图时，拆分为有序任务列表。

**规则：**
1. 按逻辑依赖排序：调研 → 策略 → 标的管理（数据必须先就位）
2. 每个子任务独立标注意图 ID
3. 前序任务输出作为后续任务的输入上下文

**示例：**

| 用户输入 | 解析结果 |
|:---|:---|
| "研究NIO然后看要不要加仓" | `[{stock-research, NIO}, {buy-entry, NIO}]` |
| "跑一下雷达，有问题的帮我分析一下" | `[{investment-radar}, {hold-evaluate, 从雷达结果提取}]` |
| "AAPL卖了吧，顺便收口一下" | `[{sell-reduce, AAPL}, {portfolio-mgmt}]` |

---

## 输出格式

```json
{
  "intents": [
    {"id": "stock-research", "ticker": "NIO", "order": 1},
    {"id": "buy-entry", "ticker": "NIO", "order": 2}
  ],
  "compound": true,
  "confidence": 0.9
}
```

- 单意图时 `compound: false`，`intents` 数组长度为 1
- `confidence` 低于 0.7 时，向用户确认意图

---

## 分类提示词

```
你是 YMOS 投资系统的意图分类器。根据用户输入，判断属于以下哪种意图（可多选）：

1. market-overview — 市场大盘/新闻/宏观
2. investment-radar — 持仓关联分析/雷达
3. stock-research — 个股调研/了解公司
4. buy-entry — 买入/建仓/加仓考虑
5. hold-evaluate — 持有评估/拿着怎么看
6. sell-reduce — 卖出/减仓/止损
7. portfolio-mgmt — 组合管理/再平衡/收口
8. system-ops — 系统操作（关注/建仓/清仓/初始化/诊断）

规则：
- 提取 ticker（股票代码）
- 多意图时按逻辑依赖排序
- 仅输出 JSON，不要解释

用户输入：{{user_input}}
```
