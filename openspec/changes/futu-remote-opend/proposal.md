## Why

Futu OpenD 当前硬编码 `127.0.0.1`，只能连接本地实例。OpenD 已部署到远程服务器 `192.168.41.237`，远程连接需要 RSA 加密传输。需要将 host 地址和 RSA 私钥通过环境变量配置，让所有 Futu 连接自动适配本地/远程模式。

## What Changes

- 新增环境变量 `FUTU_OPEND_RSA_KEY`，存储 RSA 私钥内容（PEM 格式）
- 新增连接工厂函数，统一处理 host/port 解析 + 远程加密逻辑
- 当 host 非 `127.0.0.1`/`localhost` 时，自动启用 `SysConfig.enable_proto_encrypt` 并将私钥写入临时文件
- 替换所有 7 处直接 `ft.OpenQuoteContext(...)` 调用为工厂函数
- 替换所有 `check_opend_connection()` 调用，使其也读取环境变量中的 host

## Capabilities

### New Capabilities
- `futu-remote-connect`: 统一的 Futu OpenD 远程连接工厂，处理 host 解析、加密启用、RSA 私钥管理

### Modified Capabilities
- `monitor-price-fetch`: 改用连接工厂替代直接 OpenQuoteContext 调用
- `futu-deal-fetch`: 同上
- `capital-flow-anomaly`: 同上
- `technical-anomaly`: 同上
- `derivatives-anomaly`: 同上
- `stock-screening`: 同上

## Impact

- **代码**: `cli/core/futu_utils.py`（新增工厂函数）、7 个调用文件（替换连接创建方式）
- **环境变量**: `.env` 新增 `FUTU_OPEND_RSA_KEY`（私钥内容）和 `FUTU_OPEND_HOST`（默认改为 `192.168.41.237`）
- **依赖**: 无新增依赖，仅使用 `futu` SDK 已有的加密 API
- **兼容性**: 向后兼容 — 不配置新变量时行为与当前完全一致（本地连接，无加密）
