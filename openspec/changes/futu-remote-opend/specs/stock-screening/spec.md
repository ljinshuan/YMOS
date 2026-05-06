## MODIFIED Requirements

### Requirement: Stock screening uses connection factory
选股数据获取 SHALL 使用 `create_quote_context()` 工厂函数创建连接。

#### Scenario: Remote screening with encryption
- **WHEN** `FUTU_OPEND_HOST` 指向远程地址
- **THEN** 选股数据获取 SHALL 通过工厂函数自动启用加密连接
