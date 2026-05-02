## Context

当前新闻获取命令 `ymos fetch-news` 仅支持 Finnhub company-news API，限制为 US/Crypto 持仓标的，对港股和 A 股完全没有新闻覆盖。Futu 新闻搜索 API（`ai-news-search.futunn.com/news_search`）是纯 HTTP 接口，无需本地 OpenD 运行，覆盖 HK/US/CN 全市场，适合作为补充和兜底来源。

### 现状
- `cli/commands/news.py` — 仅 Finnhub，仅 US ticker
- `cli/core/sources/news.py` — `extract_tickers_from_state_machine()` 支持 `us_only` 参数
- `.futu-skills/futu/search-skills/futu-news-search/SKILL.md` — 详细的 Futu 新闻搜索 API 规范

## Goals / Non-Goals

**Goals:**
- 新增 Futu 新闻搜索作为全市场新闻数据源
- 修改 news 命令为双源架构：Finnhub（US 优先）+ Futu（全市场兜底）
- 统一新闻输出格式，保持下游 P15 触发词检测兼容

**Non-Goals:**
- 不替换 RSS 数据源（`ymos fetch-rss`）
- 不实现 stock-digest 解读功能（由 `.futu-skills/futu-stock-digest` 覆盖）
- 不修改 `cli/commands/sentiment.py`（已有独立的 Futu feed 实现）

## Decisions

### 1. 独立模块 `cli/core/sources/futu_news.py`

封装 Futu 新闻搜索 API 为独立数据源模块，提供 `fetch_futu_news(keyword, size, news_type, lang)` 函数。参考 `.futu-skills/futu-news-search/SKILL.md` 中的 API 规范。

**理由**: 与现有 `cli/core/sources/news.py`（Finnhub）平级，职责分离清晰。

### 2. 双源新闻获取策略

修改 `cli/commands/news.py` 的获取逻辑：
1. 读取全市场 tickers（`us_only=False`）
2. US/Crypto ticker → 优先 Finnhub，无结果时 Futu 兜底
3. HK/CN ticker → 直接走 Futu
4. 合并去重（按标题前 40 字符去重，复用现有 `deduplicate()` 逻辑）
5. 统一输出 JSON，通过 `source` 字段区分来源

### 3. 新闻类型映射

Futu API 的 `news_type` 参数：1=新闻, 2=公告, 3=研报。默认获取类型 1（新闻），后续可扩展为通过命令行参数选择。

### 4. 无新依赖

Futu 新闻搜索是纯 HTTP GET 接口，使用 `urllib.request` 即可，无需额外依赖。

## Risks / Trade-offs

- **Futu API 稳定性** → 外部 HTTP 接口可能超时或限流，设置 15s timeout，失败时返回空列表不影响 Finnhub 数据
- **搜索关键词匹配** → Futu 按关键词搜索可能返回不相关结果，通过 ticker→关键词转换提高精度（如 `0700.HK` → `00700`）
- **去重跨源** → Finnhub 和 Futu 可能返回相同新闻的不同标题，使用模糊去重（前 40 字符）降低重复率
