---
name: ymos-earnings-update
metadata:
  depends_on: [ymos-core]
description: |
  个股财报深度分析与报告生成。触发方式：/ymos-earnings-update、「看一下财报」「[ticker] 财报怎么样」「财报分析」
  可被 ymos-radar、ymos-strategy 组合引用。
---

# ymos-earnings-update：财报更新报告

## 触发
- `看一下财报 [ticker]` — 生成/查看该标的最新财报分析报告
- `[ticker] 财报怎么样` — 快速查看财报摘要
- `财报分析 [ticker]` — 深度财报分析
- `财报` — 交互式选择标的

## 前置条件
- 个股文件夹应有 `个股基础知识库.md`
- 需要财报数据（用户输入或数据源获取）
- `data/state/holdings.md` 或 `data/state/watchlist.md` 中应有该标的

## 执行步骤
> 详细步骤见 sop.md

1. **收集财报数据** — 获取当期财报核心数据 + 市场预期 + 历史数据
2. **执行 Beat/Miss 分析** — 计算差异、分类、解释原因
3. **生成执行摘要** — 核心表现 + 亮点 + 担忧 + 整体评价
4. **分部分析**（如适用）— 各业务线表现和贡献
5. **前瞻指引分析** — 管理层指引对比和变化
6. **估值影响分析** — 财报对估值的影响
7. **生成趋势数据** — 近 4 季度关键指标对比
8. **生成完整报告** — 使用模板生成结构化报告

## 产出物
- `data/reports/earnings/{ticker}/{ticker}_Q{Q}_{FY}_财报报告.md`
- 个股知识库中的 P4 财报摘要更新

## 边界
- 不提供实时财报推送（手动触发）
- 不替代专业分析师的深度研究
- 不做投资建议（估值影响仅为参考）
- V1 仅支持 Markdown 格式
