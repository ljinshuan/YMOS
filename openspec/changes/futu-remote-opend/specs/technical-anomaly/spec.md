## MODIFIED Requirements

### Requirement: Technical anomaly detection uses connection factory
技术异动数据获取 SHALL 使用 `create_quote_context()` 工厂函数创建连接。

#### Scenario: Remote technical anomaly with encryption
- **WHEN** `FUTU_OPEND_HOST` 指向远程地址
- **THEN** 技术异动检测 SHALL 通过工厂函数自动启用加密连接
