---
name: ymos-sentiment
metadata:
  depends_on: [ymos-core]
description: |
  股票评论情绪分析能力。通过富途数据源获取个股/多股的社区评论，分析多空情绪分布，
  输出 bullish/bearish/neutral 百分比、temperature score 和关键观点摘要。
  触发方式：/ymos-sentiment
  「看一下 [ticker] 的情绪」「[ticker] 多空怎么样」「分析一下市场情绪」「看一下情绪」
---

# ymos-sentiment：评论情绪分析

## 触发

- `看一下 [ticker] 的情绪` — 单只股票情绪分析
- `[ticker] 多空怎么样` — 快速查看多空分布
- `分析一下市场情绪` — 全持仓+关注列表情绪概览
- `看一下情绪` — 同上（简写）
- `/ymos-sentiment` — 直接调用

## 前置条件

- 无强制前置（任何时刻可独立触发）
- 若需全持仓扫描：`data/state/holdings.md` 和 `data/state/watchlist.md` 应存在

## 执行步骤

> 详细步骤见 sop.md

1. 解析触发词，提取 ticker 列表（单票/多票/全持仓）
2. 运行 `ymos fetch-sentiment --ticker TICKER` 或 `--from-state` 获取评论数据
3. 读取 P19 prompt（`prompts/p19-comment-sentiment.md`），将评论数据喂给 LLM 做情绪分析
4. 输出情绪分析报告，保存到 `data/reports/sentiment/YYYY-MM/情绪分析_YYYY-MM-DD.md`
5. 若检测到极端情绪（bullish > 80% 或 bearish > 70%），在报告中标注预警

## 引用的 prompts

- `prompts/p19-comment-sentiment.md`（情绪结构化分析）

## 产出物

- `data/reports/sentiment/YYYY-MM/情绪分析_YYYY-MM-DD.md` — 情绪分析报告
- `data/reports/sentiment/raw/YYYY-MM/sentiment_YYYYMMDD.json` — 原始评论数据 JSON

## 边界

- 不做情绪预测或情绪交易策略（只做当前情绪快照）
- 不做实时情绪监控推送（batch 模式，按需查询）
- 不替代 P12 纪律审查（情绪仅作为辅助参考维度）
- 情绪数据来自社区评论，不构成投资建议
