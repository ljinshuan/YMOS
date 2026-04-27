---
name: ymos-market-insight
description: |
  市场事件监测与洞察报告生成。触发方式：/ymos-market-insight、「跑一下市场洞察」「今天有什么新闻」「抓 N 天数据」
---

# ymos-market-insight：市场洞察

## 触发
- `跑一下市场洞察` — 完整流程（拉数据 → P13 分析 → 保存）
- `今天有什么新闻` — 快速浏览（拉 1 天数据 → 简要总结，不保存）
- `抓 N 天数据` — 只抓数据不分析

## 前置条件
- 无强制前置（市场洞察是每日 pipeline 的第一步）

## 执行步骤
> 详细步骤见 sop.md

1. **创建输出目录**
   ```
   mkdir -p "data/reports/market-insight/raw/YYYY-MM"
   mkdir -p "data/reports/market-insight/YYYY-MM"
   ```
2. **拉取市场数据**（自动回退）
   - 优先：`ymos fetch-market`（API，需 `YMOS_MARKET_API_KEY`）
   - 回退：`ymos fetch-rss`（RSS 免费数据源）
   - RSS 路径需额外执行 CIO 半成品处理（`prompts/cio-rss-processor.md`）
3. **补充数据源**（可选，有 key/config 才执行）
   - `ymos fetch-news`（Finnhub 个股新闻，需 `FINNHUB_API_KEY`，仅持仓美股/Crypto）
   - 补充 RSS（需 `cli/config/rss_sources_custom.json` 存在）
4. **调用 P13 分析**（`prompts/p13-market-scanner.md`）
   - 输出硬约束：市场体温 + 战略简报 + 五维度详情 + 机会与风险 + 后续方向 + 页脚声明
5. **保存报告** → `data/reports/market-insight/YYYY-MM/YYYY-MM-DD_市场洞察.md`

## 产出物
- `data/reports/market-insight/raw/YYYY-MM/financial_data_YYYYMMDD.json`（原始数据）
- `data/reports/market-insight/raw/YYYY-MM/cio_processed_YYYYMMDD.md`（仅 RSS 路径）
- `data/reports/market-insight/raw/YYYY-MM/finnhub_news_YYYYMMDD.json`（有 key 时）
- `data/reports/market-insight/YYYY-MM/YYYY-MM-DD_市场洞察.md`（核心产出）

## 边界
- 不看持仓，不看价格
- 不自动更新状态机
- 不进入策略判断
- P14 板块猎手不在默认链路内，用户明确要求时才手动触发
