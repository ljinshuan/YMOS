## Context

当前所有 Futu OpenD 连接直接调用 `ft.OpenQuoteContext(host=host, port=port)`，默认绑定 `127.0.0.1:11111`。已有环境变量 `FUTU_OPEND_HOST` 和 `FUTU_OPEND_PORT`，但无加密支持。OpenD 现部署在远程 `192.168.41.237`，Futu SDK 要求远程连接必须启用 RSA 加密（`SysConfig.enable_proto_encrypt` + RSA 私钥文件）。

共 7 个文件直接创建 `OpenQuoteContext`，10+ 个文件调用 `check_opend_connection`。

## Goals / Non-Goals

**Goals:**
- 支持远程 Futu OpenD 连接，通过环境变量配置 host 和 RSA 私钥
- 远程连接自动启用加密，本地连接保持原样（零配置兼容）
- 所有 Futu 连接点统一走连接工厂，消除分散的 host/port 解析逻辑

**Non-Goals:**
- 不实现连接池或长连接复用（保持当前每次请求新建关闭的模式）
- 不修改 Futu SDK 本身的行为
- 不处理 OpenD 证书管理（使用固定私钥）

## Decisions

### 1. 连接工厂函数放在 `futu_utils.py`

**选择**: 在 `cli/core/futu_utils.py` 新增 `create_quote_context()` 和 `create_trade_context()`

**替代方案**: 新建独立模块 `cli/core/futu_connection.py`

**理由**: `futu_utils.py` 已是 Futu 相关共享工具的聚集地（`check_opend_connection`、`ticker_to_futu_symbol` 等），保持一致。文件体量可控（新增约 50 行），不值得拆分。

### 2. RSA 私钥存环境变量，运行时写临时文件

**选择**: `FUTU_OPEND_RSA_KEY` 环境变量存储 PEM 内容，运行时用 `tempfile.NamedTemporaryFile` 写入，设置 `delete=False`，使用后清理

**替代方案**: 直接引用文件路径

**理由**: 环境变量是 `.env` 文件的原生格式，无需额外管理文件路径。Futu SDK 的 `set_init_rsa_file` 要求文件路径，因此需要临时文件中转。

### 3. 自动检测远程 vs 本地

**选择**: 当 `FUTU_OPEND_HOST` 不为 `127.0.0.1`、`localhost` 或空时，自动启用加密

**替代方案**: 独立的 `FUTU_OPEND_ENCRYPT` 布尔变量

**理由**: 减少配置项。Futu SDK 远程连接必须加密是硬性要求，自动推断更不容易配错。保留显式 `FUTU_OPEND_ENCRYPT` 作为 override（覆盖自动检测）。

### 4. 工厂函数返回上下文管理器

**选择**: `create_quote_context()` 返回 `OpenQuoteContext` 实例，调用方仍手动 `close()`

**替代方案**: 返回上下文管理器（`with` 语句）

**理由**: 现有代码模式一致使用 `try/finally` 关闭，改为 `with` 需要改所有调用点。保持返回普通实例，侵入性最小。

## Risks / Trade-offs

- **[临时文件泄漏]** → 使用 `atexit` 注册清理函数，并在模块级别追踪临时文件路径
- **[私钥泄露]** → `.env` 已在 `.gitignore` 中；RSA 私钥仅在本地开发环境使用，非生产密钥
- **[远程连接延迟]** → 远程连接可能比本地慢，`check_opend_connection` 已有 3s timeout，工厂函数继承此超时
- **[加密配置遗漏]** → 自动检测机制确保远程连接必然启用加密，无需人工记住
