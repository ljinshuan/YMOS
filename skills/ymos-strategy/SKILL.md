---
name: ymos-strategy
metadata:
  depends_on: [ymos-core]
description: |
  投资策略分析与路由分发。触发方式：/ymos-strategy、「我想买/卖/加仓/持有怎么看 [ticker]」「做个仓位再平衡」「跑一下策略分析」
---

# ymos-strategy：策略分析

## 触发
- `我想买 [ticker]` — 首次建仓 → 路由 A
- `加仓 [ticker]` — 已有仓位再加 → 路由 B
- `我想卖 [ticker]` — 减仓/清仓 → 路由 D
- `持有怎么看 [ticker]` — 持有评估 → 路由 C
- `做个仓位再平衡` — 组合级调整 → 路由 E
- `跑一下策略分析` — 定时/手动批量 → 自动模式

## 前置条件
- `data/state/preferences.md` 必须存在（否则阻塞）
- 投资雷达报告作为触发来源（`跑一下策略分析` 模式）
- 各标的应有 P1+P4+P2（缺失时自动调用 `ymos-research` 补足）

## 执行步骤
> 详细步骤见 sop.md

1. **确定触发来源与目标** — 手动暗号直接分流；自动模式读取雷达报告
2. **加载用户上下文** — 投资偏好 + 状态机
3. **前置检查与补足** — 逐标的检查 P1/P4/P2，缺失时调用 `ymos-research` 补足
4. **执行策略路由**：

   | 路由 | 提示词链 | 关键约束 |
   |:---|:---|:---|
   | A 买入 | P2 → 横向对比 → P9 → P5 → P12 → P17 | 必须含横向对比 + 仓位建议 |
   | B 加仓 | P2 → 横向对比 → P3/P9 → P5 → P12 → P17 | 对比加仓 vs 买其他候选 |
   | C 持有 | P2 → P6 → [P3] → [P8] → P12 | 读取备忘录原始买入理由 |
   | D 卖出 | 读取备忘录 → P2 → P6 → [P10] → P12 | 完全清仓强制 P11 复盘 |
   | E 再平衡 | P17(逐标的) → P7 → P6 → P12 | 先算偏差再做组合决策 |

5. **写回产出物** — 策略报告 + 状态机更新 + 知识库增量 + 策略分析日志
6. **在对话中输出策略报告**

## 引用的 prompts
- `skills/ymos-core/prompts/p2-phase-check.md`（每次必跑）
- `prompts/p3-event-impact.md`（事件触发）
- `prompts/p5-fomo-killer.md`（买入/加仓审计）
- `prompts/p6-profit-keeper.md`（持有/卖出审计）
- `prompts/p7-portfolio-check.md`（再平衡）
- `prompts/p8-macro-filter.md`（宏观过滤）
- `skills/ymos-core/prompts/p9-valuation.md`（反向 DCF 估值）
- `prompts/p10-options.md`（期权策略，可选）
- `prompts/p11-autopsy.md`（清仓复盘，强制）
- `prompts/p12-referee.md`（纪律审查，每次最终必过）
- `prompts/p17-position-sizing.md`（仓位计算器）

## 产出物
- `data/reports/strategy/YYYY-MM/YYYY-MM-DD_TICKER_动作类型.md`（最终挪入个股文件夹）
- `data/reports/strategy/raw/YYYY-MM/strategy_context_*.json`（中间件）
- `data/reports/strategy/YYYY-MM/策略分析日志_YYYY-MM-DD.md`（当日汇总）
- 状态机更新 + 个股知识库增量 + 买入卖出备忘录追加

## 边界
- 不做市场洞察（ymos-market-insight 的事）
- 不做信号发现（投资雷达的事）
- 不自动执行买卖（Human in the Loop）
- 永远不跳过 P2 直接进 P5/P6，永远不缺 P12 就给买卖建议
