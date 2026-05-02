## 1. Futu 新闻数据源

- [x] 1.1 创建 `cli/core/sources/futu_news.py`，实现 `ticker_to_news_keyword(ticker)` 函数（YMOS ticker → Futu 搜索关键词）
- [x] 1.2 实现 `fetch_futu_news(keyword, size, news_type, lang)` 函数，调用 `GET /news_search` on `ai-news-search.futunn.com`
- [x] 1.3 实现文章标准化：Futu 原始返回 → 统一格式 dict（id, title, summary, published_at, url, source, ticker, p15_trigger）
- [x] 1.4 实现 `publish_time` 时间戳转换（毫秒/秒级 → `YYYY-MM-DD HH:MM` 格式）
- [x] 1.5 实现错误处理：API 返回非零 code 返回空列表，网络超时（15s）返回空列表

## 2. 双源新闻命令改造

- [x] 2.1 修改 `cli/commands/news.py`，将 ticker 提取改为 `us_only=False` 以支持全市场
- [x] 2.2 修改 Finnhub 无 API key 时的行为：从 `exit(0)` 改为继续使用 Futu 获取新闻
- [x] 2.3 实现按市场路由：US/Crypto → Finnhub 优先 + Futu 兜底；HK/CN → 直接 Futu
- [x] 2.4 实现跨源去重：合并 Finnhub 和 Futu 结果后按标题前 40 字符去重
- [x] 2.5 统一输出 JSON 格式，`source` 字段区分来源（`finnhub` / `futu_news_search`）

## 3. 验证

- [x] 3.1 验证无 `FINNHUB_API_KEY` 时，`ymos fetch-news` 仍能通过 Futu 获取全市场新闻
- [x] 3.2 验证 HK/CN ticker 能正确获取 Futu 新闻
- [x] 3.3 验证跨源去重正常工作（Finnhub + Futu 相同标题不重复）
- [x] 3.4 验证 P15 触发词检测对 Futu 来源文章正常工作
