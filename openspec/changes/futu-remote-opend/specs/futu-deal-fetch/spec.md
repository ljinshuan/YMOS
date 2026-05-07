## MODIFIED Requirements

### Requirement: Deal fetch uses connection factory
`fetch_deals()` SHALL 使用 `create_trade_context()` 工厂函数创建连接，而非直接调用 `OpenSecTradeContext()`。

#### Scenario: Remote deal fetch with encryption
- **WHEN** `FUTU_OPEND_HOST` 指向远程地址且 RSA 私钥已配置
- **THEN** `fetch_deals` SHALL 通过工厂函数自动启用加密连接获取成交记录
