# 📊 市场洞察 SOP

> 暗号：`跑一下市场洞察`
> 模块：ymos-market-insight（市场事件监测）

---

## 一句话定位

市场洞察只回答一件事：**今天市场发生了什么，哪些方向值得进入下一步分析**

- 只处理事件 + 宏观信号
- **不负责价格扫描**（价格扫描在投资雷达里做）
- P14 板块猎手不是默认链路，有需要时再手动深挖

---

## 🔑 触发暗号

| 暗号 | 操作 |
|:---|:---|
| `跑一下市场洞察` | 完整流程（拉数据 → P13分析 → 保存） |
| `今天有什么新闻` | 快速浏览（拉1天数据 → 简要总结，不保存） |
| `抓 N 天数据` | 只抓数据不分析（运行脚本，存 Raw_Data） |

---

## ⚙️ 完整执行步骤

### Step 1：创建输出目录

```bash
mkdir -p "data/reports/market-insight/raw/$(date +%Y-%m)"
mkdir -p "data/reports/market-insight/$(date +%Y-%m)"
```

### Step 2：拉取市场数据（自动回退）

> 详细数据拉取流程和回退策略见 `sop/data-loading.md`

多源数据拉取：CIO 洞察 API → RSS 兜底，个股新闻（Finnhub + Futu），补充 RSS。

### Step 2.5：获取大盘技术面数据

> 在 P13 分析前，获取大盘锚点的量化技术面数据，作为新闻文字分析的补充。

```bash
# 读取大盘锚点配置
cat data/state/market_anchors.md

# 技术分析大盘 ETF（如 QQQ, SPY）
ymos tech-analysis analyze --symbols QQQ,SPY --source yahoo \
  --output-dir "data/reports/tech/$(date +%Y-%m)"
```

读取技术面报告，提取每个大盘 ETF 的 verdict（偏多/偏空/中性）和关键指标。

### Step 3：调用 P13 分析

> ⚠️ **无论数据来自 API 还是 RSS，都必须严格按照 P13 标准模板输出。**
> API 数据质量更高 ≠ 可以简化输出格式。P13 的价值不在于数据清洗（那是 CIO 的活），
> 而在于 **信号识别 + 结构化呈现**（战略信号仪表盘 + 势能分析 + 风险警告）。

**P13 分析输入文件（按优先级读取）**：
1. **主输入**：`financial_data_YYYYMMDD.json`（API 路径）或 `cio_processed_YYYYMMDD.md`（RSS 路径）
2. **补充输入**（如存在）：`finnhub_news_YYYYMMDD.json`
   - `p15_trigger=true` 的条目 → P13 报告中标注「建议跑 P15」
3. **补充输入**（如存在）：`supplementary_rss_YYYYMMDD.json`（用户自定义 RSS）
4. **量化输入**（Step 2.5 产出）：大盘 ETF 技术面 verdict + 关键指标（如 "QQQ 偏多，日线均线多头排列，RSI 58"）

调用：`prompts/p13-market-scanner.md`

**P13 分析时，参考过去几天的历史洞察（如有）**：
- 路径：`data/reports/market-insight/YYYY-MM/` 目录下最近几份报告

**输出格式硬约束**（缺一不可）：
1. **市场体温**标签（Risk On / Risk Off / Chaos）+ **核心看点**
2. **战略简报**（仪表盘表格 3-5 个信号 + 战略分析段落）
3. **五维度市场详情**（市场风向 / 美股核心动态 / AI 领域 / Crypto / A股内参，无信息的维度略过）
4. **机会评估与风险警告**（值得观察的机会 + 风险与纪律警告）
5. **后续观察方向**
6. 页脚声明（信息聚合与处理，非投资建议）
7. 每段内容末尾附来源超链接（Markdown 超链接格式，如 `[Bloomberg](url)`，不放裸链接）
8. **市场风向 section 包含大盘 ETF 技术面量化数据**（如 "QQQ 技术面偏多⬆，日线均线多头排列，RSI 58"）

**合规措辞约束**：不说"关注"说"观察"、不说"利好"说"验证/支撑"、不说"建议关注"说"后续市场焦点/变量可能在于"。

> 具体模板见 `prompts/p13-market-scanner.md` 的 `# Output Format` 区块。

> ⚠️ **P14 不在默认链路内**：用户明确要做板块深挖时再手动触发 `prompts/p14-sector-hunter.md`

### Step 4：保存洞察报告

**输出路径**：`data/reports/market-insight/YYYY-MM/YYYY-MM-DD_市场洞察.md`

### Step 5：在对话中输出

直接在对话中输出完整 Markdown 报告内容。

---

## 📦 产出物清单

| 文件 | 路径 | 命名规则 | 说明 |
|:---|:---|:---|:---|
| Raw Data（API/RSS） | `data/reports/market-insight/raw/YYYY-MM/` | `financial_data_YYYYMMDD.json` | 必有 |
| CIO 半成品情报 | `data/reports/market-insight/raw/YYYY-MM/` | `cio_processed_YYYYMMDD.md` | 仅 RSS 路径 |
| Finnhub News | `data/reports/market-insight/raw/YYYY-MM/` | `finnhub_news_YYYYMMDD.json` | 有 key 才有 |
| 市场洞察报告 | `data/reports/market-insight/YYYY-MM/` | `YYYY-MM-DD_市场洞察.md` | 必有 |

---

## 📤 下游分发规则

市场洞察本身不触发个股分析或策略制定，但它是投资雷达的核心输入：

- 生成的洞察报告会被 `跑一下投资雷达` 自动读取
- 洞察中出现的相关板块/事件信号，在投资雷达里会与持仓 + Watchlist 做关联匹配
- 重大事件在投资雷达报告的「下一步建议」中推荐对应的策略分析路由

---

## 📁 路径速查

| 内容 | 路径 |
|:---|:---|
| 市场数据脚本（API） | `cli/`（`ymos fetch-market`） |
| 市场数据脚本（RSS） | `cli/`（`ymos fetch-rss`） |
| RSS 源配置 | `cli/config/rss_sources.json` |
| CIO 处理提示词 | `prompts/cio-rss-processor.md` |
| Finnhub News 脚本 | `cli/`（`ymos fetch-news`） |
| P13 提示词 | `prompts/p13-market-scanner.md` |
| P14 提示词（手动深挖） | `prompts/p14-sector-hunter.md` |
| 历史洞察报告归档 | `data/reports/market-insight/YYYY-MM/` |
| Raw Data 归档 | `data/reports/market-insight/raw/YYYY-MM/` |

---

## ⚠️ 边界

- 市场洞察**不看持仓**，不看价格
- 不自动更新状态机
- 不进入策略判断

---

*SOP 版本：2026-05-03 · YMOS V4 Skills 架构 · 新增大盘 ETF 技术面量化输入*
