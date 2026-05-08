---
name: ymos-radar
metadata:
  depends_on: [ymos-core]
description: |
  持仓与关注标的的价格扫描、信号追踪与桥接报告。触发方式：/ymos-radar、「跑一下投资雷达」「查一下价格」「看看有什么信号」
---

# ymos-radar：投资雷达

## 触发
- `跑一下投资雷达` — 完整流程（7 天趋势 + 价格扫描 + 资金流扫描 + 信号追踪 + 桥接报告）
- `查一下价格` — 只跑价格扫描
- `看看有什么信号` — 只做信号演变扫描
- `查一下资金流` — 只跑资金流扫描 + P20 异动分析
- `有什么资金异动` — 同上

## 前置条件
- **自动依赖 ymos-market-insight**：若当日洞察不存在，先自动触发 `跑一下市场洞察`
- `data/state/preferences.md` 应存在
- `data/state/holdings.md` 或 `data/state/watchlist.md` 应有内容

## 执行步骤
> 详细步骤见 sop.md

1. **加载用户上下文** — 读取投资偏好 + 持仓状态机 + Watchlist 状态机
2. **加载市场洞察（7 天趋势）** — 当日洞察 + 过去 7 天趋势分析
3. **加载上份投资雷达** — 提取连续跟踪信息
4. **大盘 + 板块 ETF 扫描**（三层信号基础）— 读取大盘锚点和板块映射 → price-scan + tech-analysis 大盘/板块 ETF → 三层信号联动判断 → P14 自动触发（板块信号显著时）
5. **价格扫描**（只扫状态机 ticker）
   ```
   ymos price-scan scan --from-state
   ```
   - 三源分流：美股/Crypto → Finnhub，A 股 → Tushare，港股 → Yahoo，兜底 → Yahoo
5. **资金流扫描**（复用 ticker 列表，非阻塞）
   ```
   ymos fetch-capital-flow fetch --from-state
   ```
   - 数据源：富途 OpenD `get_financial_unusual`
   - P20 资金异动分析：信号检测 + 强度评级 + Tier 调整建议
   - OpenD 未运行时跳过，不阻塞雷达流程
6. **综合分析** — 市场趋势回顾 + 资金异动信号 + 持仓动态 + Watchlist 动态 + 机会与风险信号 + 下一步建议
	5.5 **期权市场情绪扫描**（可选，复用 ticker 列表，非阻塞）
	   ```
	   ymos fetch-option-chain --from-state --output-dir "data/reports/radar/raw/$(date +%Y-%m)"
	   ```
	   - 数据源：富途 OpenD `get_option_chain` + `get_market_snapshot`
	   - 分析内容：IV 曲面、PCR 偏斜、未平仓变化、希腊值分布
	   - 调用 `P-option-sentiment` prompt 生成情绪摘要
	   - OpenD 未运行时跳过，不阻塞雷达流程
	   - 前置条件：`--with-options` 标志或 `data/state/preferences.md` 中 `option_analysis_enabled=true`
	6. **综合分析** — 市场趋势回顾 + 资金异动信号 + 期权市场情绪（可选）+ 持仓动态 + Watchlist 动态 + 机会与风险信号 + 下一步建议
7. **触发分流**（AI 自主分析）— 重大事件/财报/宏观事件触发对应 P 链
8. **生成投资雷达报告** → `data/reports/radar/YYYY-MM/投资雷达_YYYY-MM-DD.md`
9. **写回状态机** — P4 更新 + 价格更新 + 资金异动信号更新

## 产出物
- `data/reports/radar/YYYY-MM/投资雷达_YYYY-MM-DD.md`（桥接报告，核心产出）
- `data/reports/radar/raw/YYYY-MM/price_scan_YYYYMMDD.json`（价格数据）
- `data/reports/radar/raw/YYYY-MM/capital_flow_YYYYMMDD.json`（资金流数据，可选）
- `data/reports/tech/YYYY-MM/`（大盘+板块 ETF 技术面报告）
- 状态机更新（P4 + 价格）
- 个股知识库 P4 增量更新

## 边界
- 不做市场全景分析（市场洞察的事）
- 不做策略制定（策略分析的事）
- 不自动执行买卖（Human in the Loop）
- 只建议路由暗号，不给出买/卖/加仓/持有建议
