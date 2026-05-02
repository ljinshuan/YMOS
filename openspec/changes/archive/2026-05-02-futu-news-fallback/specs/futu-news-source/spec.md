## ADDED Requirements

### Requirement: Futu news search API client
The system SHALL provide `cli/core/sources/futu_news.py` with a `fetch_futu_news(keyword, size, news_type, lang)` function that calls `GET /news_search` on `https://ai-news-search.futunn.com` and returns a list of normalized article dicts.

#### Scenario: Successfully fetch news for HK stock
- **WHEN** calling `fetch_futu_news("00700", size=10, news_type=1, lang="zh-CN")`
- **THEN** returns a list of article dicts with keys: id, title, summary, published_at, url, source, ticker

#### Scenario: Successfully fetch news for US stock
- **WHEN** calling `fetch_futu_news("AAPL", size=10, news_type=1, lang="zh-CN")`
- **THEN** returns a list of article dicts for Apple-related news

#### Scenario: API returns error
- **WHEN** the Futu API returns a non-zero code
- **THEN** returns an empty list and prints a warning

#### Scenario: Network timeout
- **WHEN** the HTTP request times out (15 seconds)
- **THEN** returns an empty list and prints a warning

### Requirement: Ticker to Futu news keyword conversion
The module SHALL provide `ticker_to_news_keyword(ticker)` that converts YMOS ticker format to Futu search keyword: `0700.HK` → `00700`, `AAPL` → `AAPL`, `688008.SS` → `688008`.

#### Scenario: HK ticker keyword
- **WHEN** input is `0700.HK`
- **THEN** keyword is `00700`

#### Scenario: US ticker keyword
- **WHEN** input is `AAPL`
- **THEN** keyword is `AAPL`

#### Scenario: A-share keyword
- **WHEN** input is `688008.SS`
- **THEN** keyword is `688008`

### Requirement: Normalized article format
Each article returned by `fetch_futu_news` SHALL be normalized to a dict with keys: `id` (str), `title` (str), `summary` (str), `published_at` (str, YYYY-MM-DD HH:MM format), `url` (str), `source` (str, "futu_news_search"), `ticker` (str, original YMOS ticker), `p15_trigger` (bool).

#### Scenario: Article normalization
- **WHEN** Futu API returns a raw article with publish_time (timestamp), title, desc, url
- **THEN** the normalized article has published_at as formatted datetime string, desc mapped to summary, and p15_trigger computed from title + summary keywords
