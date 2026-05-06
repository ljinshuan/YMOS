## MODIFIED Requirements

### Requirement: Extended quotes fetch uses connection factory
`fetch_extended_quotes()` 和 `fetch_futu_history()` SHALL 使用 `create_quote_context()` 工厂函数创建连接，而非直接调用 `ft.OpenQuoteContext()`。

#### Scenario: Extended quotes with remote host
- **WHEN** `FUTU_OPEND_HOST` 指向远程地址
- **THEN** `fetch_extended_quotes` SHALL 通过工厂函数自动启用加密连接

#### Scenario: History fetch with remote host
- **WHEN** `FUTU_OPEND_HOST` 指向远程地址
- **THEN** `fetch_futu_history` SHALL 通过工厂函数自动启用加密连接
