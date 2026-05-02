## Why

当前新闻获取 (`ymos fetch-news`) 仅支持 Finnhub 的 company-news API，且仅覆盖 US/Crypto 持仓，对港股和 A 股标的完全没有新闻数据。Futu 平台的新闻搜索 API（`ai-news-search.futunn.com/news_search`）覆盖 HK/US/CN 全市场，且无需 OpenD 本地运行（纯 HTTP 接口），适合作为新闻数据的兜底和补充来源。

## What Changes

- 新增 `cli/core/sources/futu_news.py`，封装 Futu 新闻搜索 API（`GET /news_search`），支持按关键词搜索、按类型过滤（新闻/公告/研报）
- 修改 `cli/commands/news.py`，增加 Futu 作为新闻数据源：当 Finnhub 无数据或不覆盖的市场（HK/CN）时，自动调用 Futu 新闻搜索兜底
- 修改 `cli/commands/rss.py`（如适用），在 RSS 数据不足时可引用 Futu 新闻作为补充
- 修改 `cli/core/sources/news.py` 的 `extract_tickers_from_state_machine`，扩展支持读取全市场 ticker（当前 news 命令仅读 US ticker）

## Capabilities

### New Capabilities
- `futu-news-source`: Futu 新闻搜索数据源，通过 `ai-news-search.futunn.com/news_search` HTTP API 获取全市场（HK/US/CN）新闻、公告、研报

### Modified Capabilities
- `news-fetch-flow`: `cli/commands/news.py` 的新闻获取流程从单一 Finnhub 扩展为 Finnhub（US/Crypto 优先）+ Futu（全市场兜底）的双源架构

## Impact

- **代码**: 新增 `cli/core/sources/futu_news.py`，修改 `cli/commands/news.py`、`cli/core/sources/news.py`
- **依赖**: 无新依赖（Futu 新闻搜索是纯 HTTP 接口，不需要 `futu-api` SDK）
- **兼容性**: 完全向后兼容，Finnhub API key 仍为可选，无 key 时也能通过 Futu 获取新闻
- **数据**: 新闻输出 JSON 格式统一（source 字段区分来源），下游 P15 触发词检测逻辑不变
