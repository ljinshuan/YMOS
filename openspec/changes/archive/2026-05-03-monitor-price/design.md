## Context

YMOS 是一个 CLI + Markdown SOP 驱动的投资研究系统。当前价格获取完全依赖手动触发（`ymos price-scan` 或 AI 对话），没有自动化定时监控能力。数据源走 Finnhub/Tushare/Yahoo 三源分流。

用户本地已安装 Futu OpenD（富途网关），项目已有完整的 Futu SDK 集成（K线获取、ticker 格式转换、连接检查）。外部项目 naught_backtest 负责策略计算，YMOS 需要定义与它的文件接口。

## Goals / Non-Goals

**Goals:**
- 提供两个无状态 CLI 命令，可通过 cron/systemd 调度实现自动化盯盘
- 通过 Futu OpenD 统一获取日K + 分钟K线数据，累积写入 CSV
- 扫描 naught_backtest 产出的策略信号文件，对新信号生成终端/文件告警
- 与现有雷达流程完全独立，不修改状态机、不修改三源分流逻辑

**Non-Goals:**
- 不实现内置调度器（交给外部 cron/systemd）
- 不实现手机推送告警（仅终端/文件）
- 不修改现有 `price-scan`、`router.py`、状态机更新逻辑
- 不直接执行交易（仅告警）
- 不实现实时 WebSocket 推送（轮询模式，cron 粒度）

## Decisions

### 1. 数据源：盯盘走 Futu OpenD，不复用三源分流

**选择**: 盯盘命令通过 Futu OpenD `request_history_kline` 获取K线数据。

**原因**: Futu OpenD 统一覆盖美股/港股/A股，数据质量稳定，且用户本地已安装。三源分流（Finnhub/Tushare/Yahoo）保持给手动雷达流程使用，两条路径互不干扰。

**备选**: 复用现有 router.py 三源分流 — 但三个源返回格式不统一，Finnhub 只有即时报价无K线，合并处理复杂。

### 2. 调度方式：外部 cron，不内建调度器

**选择**: CLI 命令无状态、幂等，调度交给 cron/systemd timer。

**原因**: 符合 YMOS"CLI 是轻量工具"的设计哲学；本地用 cron，服务器用 systemd timer，迁移零成本；每个命令可独立测试。

**备选**: Python schedule/asyncio 内建调度 — 增加进程管理复杂度，与项目风格不符。

### 3. 历史数据：每次拉 60 根K线，合并去重写入 CSV

**选择**: 每次 `fetch-prices` 拉取最近 60 根日K + 60 根分钟K，与本地 CSV 按 timestamp 去重合并。

**原因**: 60 根足够覆盖策略计算需求；CSV 格式通用，naught_backtest 可直接读取；追加去重保证幂等性，cron 重复执行不会产生脏数据。

### 4. 信号接口：文件系统，naught_backtest 写入 JSON

**选择**: `data/monitor/signals/{TICKER}.json`，每 ticker 一个文件，naught_backtest 负责写入。

**原因**: 最简集成 — 两个项目不需要网络通信或共享数据库；JSON 格式灵活，naught_backtest 可以扩展字段；YMOS 的 `check-signals` 只需扫描目录即可。

### 5. 交易时段过滤：命令内置，不依赖 cron 精确配置

**选择**: `fetch-prices` 默认开启 `--skip-non-trading-hours`，内部按 ticker 市场判断交易时段，非交易时段跳过。

**原因**: cron 精确配置多市场时段复杂且易出错（美股跨日、夏令时变化）；命令内部过滤更可靠，cron 可以全天候运行。

## Risks / Trade-offs

- **[Futu OpenD 依赖]** → OpenD 未启动时 `fetch-prices` 会失败并打印启动指引。cron 场景下写入日志，不影响其他命令。无 fallback（盯盘专用 Futu，不复用三源）。
- **[信号检测延迟]** → cron 最小粒度约 1 分钟，不是毫秒级实时。对于投资策略告警场景足够。
- **[CSV 文件增长]** → 每次 60 根K线合并去重，文件不会无限增长。日K一年约 250 行，5 分钟K一天约 48 行（美股交易时间）。长期运行可手动归档。
- **[naught_backtest 接口未定型]** → YMOS 先定义接口格式，naught_backtest 负责适配。接口变更只需调整信号 JSON schema。
