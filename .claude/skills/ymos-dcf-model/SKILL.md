---
name: ymos-dcf-model
metadata:
  depends_on: [ymos-core]
description: |
  DCF 现金流折现深度估值模型，包含 WACC 计算、终值分析、敏感性/情景分析。
  触发方式：/ymos-dcf-model、「DCF 分析」「估值建模」「算一下 DCF [ticker]」
  可被 ymos-research、ymos-strategy 组合引用。
---

# ymos-dcf-model：DCF 估值模型

## 触发
- `DCF 分析 [ticker]` — 启动完整 DCF 建模流程
- `估值建模 [ticker]` — 同上
- `算一下 DCF [ticker]` — 快速 DCF 估算
- `DCF` — 交互式选择标的

## 前置条件
- 个股文件夹应有 `个股基础知识库.md`（P1/P4 数据来源）
- 需要历史财务数据（收入、利润率、资本支出等）
- `data/state/holdings.md` 或 `data/state/watchlist.md` 中应有该标的

## 执行步骤
> 详细步骤见 sop.md

1. **收集假设数据** — 历史财务数据 + 用户假设 + 默认参数
2. **构建现金流预测** — 5-10 年 FCF 预测
3. **计算 WACC** — CAPM + 权益/债务成本分解
4. **计算终值** — 永续增长法 + 退出倍数法
5. **计算现值** — 折现 FCF + 终值
6. **敏感性分析** — 双变量敏感性表
7. **情景分析** — 乐观/基准/悲观三情景
8. **生成报告** — Markdown 报告 + Excel 模型

## 产出物
- `data/reports/valuation/{ticker}/DCF分析_{ticker}_{date}.md`（Markdown 报告）
- `data/reports/valuation/{ticker}/excel/DCF模型_{ticker}_{date}.xlsx`（Excel 模型）

## 边界
- 不提供实时估值更新（手动触发）
- 不实现行业特定 DCF 变体
- 不替代专业金融模型
- DCF 输出仅供参考，不构成投资建议
