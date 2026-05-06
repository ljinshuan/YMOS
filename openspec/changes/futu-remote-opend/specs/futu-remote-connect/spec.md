## ADDED Requirements

### Requirement: Environment variable configuration for Futu OpenD connection
系统 SHALL 从以下环境变量读取 Futu OpenD 连接配置：
- `FUTU_OPEND_HOST`: OpenD 地址，默认 `127.0.0.1`
- `FUTU_OPEND_PORT`: OpenD 端口，默认 `11111`
- `FUTU_OPEND_RSA_KEY`: RSA 私钥 PEM 内容（可选，远程连接时需要）

#### Scenario: Local connection with defaults
- **WHEN** 未设置 `FUTU_OPEND_HOST` 和 `FUTU_OPEND_RSA_KEY`
- **THEN** 系统 SHALL 使用 `127.0.0.1:11111` 连接本地 OpenD，不启用加密

#### Scenario: Remote connection with RSA key
- **WHEN** `FUTU_OPEND_HOST` 设置为非 localhost 地址且 `FUTU_OPEND_RSA_KEY` 已配置
- **THEN** 系统 SHALL 自动启用 `SysConfig.enable_proto_encrypt(is_encrypt=True)`，将私钥写入临时文件并通过 `SysConfig.set_init_rsa_file()` 加载

#### Scenario: Remote host without RSA key
- **WHEN** `FUTU_OPEND_HOST` 设置为非 localhost 地址但 `FUTU_OPEND_RSA_KEY` 未配置
- **THEN** 系统 SHALL 打印警告信息并尝试连接（可能因缺少加密而失败）

### Requirement: Quote context factory function
系统 SHALL 提供 `create_quote_context(host="", port=0)` 函数，返回配置好的 `OpenQuoteContext` 实例。

#### Scenario: Factory resolves host and port from env
- **WHEN** 调用 `create_quote_context()` 不传参数
- **THEN** 函数 SHALL 从 `FUTU_OPEND_HOST` / `FUTU_OPEND_PORT` 环境变量获取连接参数

#### Scenario: Factory with explicit params overrides env
- **WHEN** 调用 `create_quote_context(host="10.0.0.1", port=22222)`
- **THEN** 函数 SHALL 使用传入的参数，忽略环境变量

#### Scenario: Factory enables encryption for remote host
- **WHEN** host 不是 `127.0.0.1`、`localhost` 或空字符串
- **THEN** 函数 SHALL 在创建 context 前启用加密并配置 RSA 私钥

#### Scenario: Factory skips encryption for localhost
- **WHEN** host 是 `127.0.0.1` 或 `localhost`
- **THEN** 函数 SHALL 不启用加密，直接创建 context

### Requirement: Trade context factory function
系统 SHALL 提供 `create_trade_context(host="", port=0)` 函数，行为与 `create_quote_context` 一致但返回 `OpenSecTradeContext`。

#### Scenario: Remote trade connection with encryption
- **WHEN** host 为远程地址且 RSA 私钥已配置
- **THEN** 函数 SHALL 启用加密后返回 `OpenSecTradeContext` 实例

### Requirement: RSA private key temporary file management
系统 SHALL 将 `FUTU_OPEND_RSA_KEY` 环境变量中的 PEM 内容写入临时文件供 Futu SDK 使用。

#### Scenario: Temporary file created and registered for cleanup
- **WHEN** 首次需要 RSA 私钥
- **THEN** 系统 SHALL 创建临时文件写入 PEM 内容，并通过 `atexit` 注册清理函数

#### Scenario: Reuse temp file on subsequent calls
- **WHEN** RSA 临时文件已创建
- **THEN** 后续调用 SHALL 复用同一文件，不重复创建

### Requirement: check_opend_connection reads environment variables
`check_opend_connection()` 函数 SHALL 在未传入参数时从环境变量读取 host 和 port。

#### Scenario: Default connection check uses env vars
- **WHEN** 调用 `check_opend_connection()` 不传参数
- **THEN** 函数 SHALL 使用 `FUTU_OPEND_HOST` / `FUTU_OPEND_PORT` 环境变量检查连接
