# 数据拉取流程和回退策略

### Step 2：拉取市场数据（自动回退）

**方式 A：市场信息 API（优先）**
```bash
ymos fetch-market fetch --days 1 \
  --output "data/reports/market-insight/raw/$(date +%Y-%m)/financial_data_$(date +%Y%m%d).json"
```

> 脚本会自动加载 `.env` 中的 `YMOS_MARKET_API_KEY`。无 key 时脚本以 exit(0) 退出并提示使用 RSS。

**方式 B：RSS 免费数据源（回退 / 无 API Key 时使用）**
```bash
ymos fetch-rss fetch --days 1 \
  --output "data/reports/market-insight/raw/$(date +%Y-%m)/financial_data_$(date +%Y%m%d).json"
```

**Agent 执行规则**：
1. 先尝试方式 A
2. 若方式 A 的脚本输出包含"跳过 API 数据源"或未生成输出文件 → 自动回退到方式 B
3. 用户指定天数时，把 `1` 替换为对应天数

### Step 2.5：CIO 半成品处理（仅 RSS 路径需要）

> **仅当 Step 2 使用了方式 B（RSS）时执行此步。**
> API 路径（方式 A）的数据已经过清洗和分类，跳过此步。

读取 Step 2 生成的 RSS 原始 JSON，调用：
- `prompts/cio-rss-processor.md`

CIO 处理器会执行：去重合并 → 噪音过滤 → 事件聚类 → 信号提取

**输出路径**：`data/reports/market-insight/raw/YYYY-MM/cio_processed_YYYYMMDD.md`

### Step 2.6：拉取持仓个股新闻（补充数据源，可选）

> **自动执行，无需 API key。** `ymos fetch-news` 内置双源路由：Finnhub（需 `FINNHUB_API_KEY`）+ Futu 兜底（HTTP 直接调用，无需 OpenD）。

```bash
ymos fetch-news fetch \
  --hours 24 \
  --output "data/reports/market-insight/raw/$(date +%Y-%m)/finnhub_news_$(date +%Y%m%d).json"
```

**策略说明**：
- 美股/Crypto 标的优先使用 Finnhub，无结果时自动 Futu 兜底
- 港股/A股标的直接使用 Futu 新闻搜索（`ai-news-search.futunn.com`）
- Watchlist 不拉个股新闻（节省 rate limit）

### Step 2.7：拉取补充 RSS 数据（可选）

> **仅当 `cli/config/rss_sources_custom.json` 存在时执行。无此文件则静默跳过。**
>
> 补充 RSS 与主数据源（API 或默认 RSS）独立运行，不互斥。
> 适用场景：用户已有 Market Data API，但还想订阅特定行业/深度分析的 RSS 源。

```bash
ymos fetch-rss fetch {天数} \
  --config cli/config/rss_sources_custom.json \
  --output "data/reports/market-insight/raw/$(date +%Y-%m)/supplementary_rss_$(date +%Y%m%d).json"
```

**Agent 执行规则**：
1. 检查 `cli/config/rss_sources_custom.json` 是否存在
2. 存在 → 执行拉取，输出为 `supplementary_rss_YYYYMMDD.json`
3. 不存在 → 静默跳过，不提示用户
