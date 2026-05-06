# 盯盘功能设计文档

日期: 2026-05-03
状态: 已确认

## 概述

为 YMOS 新增自动化盯盘能力：定时获取价格数据 → naught_backtest 计算策略信号 → 监控信号触发告警。盯盘与手动雷达流程互不干扰。

## 架构

```
cron ──→ ymos monitor fetch-prices ──→ data/monitor/history/
                                            ↓
                              naught_backtest (cron 触发)
                                            ↓
                                      data/monitor/signals/
                                            ↓
         cron ──→ ymos monitor check-signals ──→ alerts/ + 终端
```

两个无状态 CLI 命令，调度交给 cron（本地）/ systemd timer（服务器）。

## 目录结构

```
data/monitor/
├── prices/                  # 价格快照（每次抓取一个文件）
│   └── YYYY-MM-DD/
│       └── HHMM.json        # 单次快照，所有 ticker 汇总
├── history/                 # 累积K线历史（naught_backtest 读取）
│   ├── SOXL_daily.csv       # 日K
│   ├── SOXL_5m.csv          # 5分钟K
│   └── ...
├── signals/                 # 策略信号（naught_backtest 写入）
│   ├── SOXL.json
│   └── ...
└── alerts/
    └── YYYY-MM-DD.md        # 每日告警日志
```

## 数据格式

### 价格快照 (prices/YYYY-MM-DD/HHMM.json)

```json
{
  "fetched_at": "2026-05-03 14:30:00",
  "tickers": {
    "SOXL": {
      "price": 130.42,
      "open": 129.0,
      "high": 131.5,
      "low": 128.8,
      "close": 130.42,
      "volume": 1234567,
      "change_pct": 1.23,
      "source": "futu_opend"
    }
  }
}
```

### K线历史 (history/{TICKER}_daily.csv / {TICKER}_5m.csv)

```csv
timestamp,open,high,low,close,volume
2026-05-03 09:30:00,129.00,131.50,128.80,130.42,1234567
2026-05-03 09:35:00,130.50,132.00,130.20,131.80,987654
```

每次 fetch-prices 拉取最近 60 根K线，与本地 CSV 合并，按 timestamp 去重后写入。

### 策略信号 (signals/{TICKER}.json)

naught_backtest 写入，YMOS 读取：

```json
{
  "ticker": "SOXL",
  "signal_time": "2026-05-03 14:35:00",
  "signal_type": "buy|sell|hold|warning",
  "strength": "strong|medium|weak",
  "strategy_name": "ma_cross",
  "detail": "5日均线上穿20日均线",
  "price_at_signal": 130.42
}
```

### 告警日志 (alerts/YYYY-MM-DD.md)

```markdown
# 告警日志 2026-05-03

## 14:35 SOXL - 买入信号 [强]
- 策略: ma_cross
- 详情: 5日均线上穿20日均线
- 触发价: 130.42

## 15:10 META - 卖出信号 [中]
- 策略: rsi_divergence
- 详情: RSI顶背离
- 触发价: 512.80
```

## CLI 命令

### ymos monitor fetch-prices

```bash
# 从状态机提取 ticker（holdings + watchlist）
uv run ymos monitor fetch-prices --from-state

# 手动指定 ticker
uv run ymos monitor fetch-prices --symbols SOXL,META,TSLA

# 指定输出目录（默认 data/monitor）
uv run ymos monitor fetch-prices --from-state --output-dir data/monitor

# 指定K线周期（默认 5m）
uv run ymos monitor fetch-prices --from-state --kline 1m
```

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--from-state` | bool | False | 从 holdings.md + watchlist.md 提取 ticker |
| `--symbols` | str | "" | 手动指定逗号分隔的 ticker 列表 |
| `--output-dir` | str | data/monitor | 输出根目录 |
| `--kline` | str | 5m | 分钟K线周期: 1m/5m/15m/60m |
| `--count` | int | 60 | 获取最近 N 根K线 |
| `--skip-non-trading-hours` | bool | True | 非交易时段自动跳过 |

**执行流程：**
1. 解析 ticker 来源（`--from-state` 或 `--symbols`）
2. 检查 OpenD 连接（复用 `futu_utils.check_opend_connection`）
3. 对每个 ticker，调用 `request_history_kline` 获取最近 60 根日K + 60 根分钟K
4. 写入快照文件 `prices/YYYY-MM-DD/HHMM.json`
5. 与本地 `history/{TICKER}_daily.csv` 和 `history/{TICKER}_{kline}.csv` 合并，按 timestamp 去重
6. 终端打印简要汇总

**数据源：Futu OpenD 统一获取**（盯盘模式专用，不影响手动雷达的三源分流逻辑）。

### ymos monitor check-signals

```bash
# 扫描所有信号文件
uv run ymos monitor check-signals

# 只检查指定 ticker
uv run ymos monitor check-signals --tickers SOXL,META

# 指定信号目录
uv run ymos monitor check-signals --signal-dir data/monitor/signals
```

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--tickers` | str | "" | 指定 ticker，空则扫描全部 |
| `--signal-dir` | str | data/monitor/signals | 信号文件目录 |
| `--output-dir` | str | data/monitor | 输出根目录 |

**执行流程：**
1. 扫描 `signals/` 目录下所有 JSON 文件
2. 读取每个信号，与 `alerts/YYYY-MM-DD.md` 中已记录的信号对比（按 `signal_time` + `strategy_name` 去重）
3. 新信号 → 格式化告警内容 → 追加到 `alerts/YYYY-MM-DD.md` + 终端打印
4. 无新信号则静默退出（exit 0）

## 去重策略

| 文件 | 去重键 | 策略 |
|------|--------|------|
| history CSV | timestamp | 同时间戳整行跳过，不覆盖 |
| signals JSON | signal_time + strategy_name | 已存在则跳过 |
| alerts MD | 由 check-signals 根据信号去重写入 | 不重复 |

## 交易时段

| 市场 | 交易时间 (北京) |
|------|----------------|
| US | 21:30 - 04:00 (次日，夏令时提前 1 小时) |
| HK | 09:30 - 16:00 |
| A | 09:30 - 11:30, 13:00 - 15:00 |

`fetch-prices` 默认开启 `--skip-non-trading-hours`，自动检测 ticker 市场后跳过非交易时段。cron 可全天候配置，由命令自行过滤。

## Cron 配置示例

```bash
# 每 5 分钟抓取价格（交易时段，由 --skip-non-trading-hours 过滤）
*/5 * * * * cd /path/to/YMOS && uv run ymos monitor fetch-prices --from-state >> /tmp/ymos-prices.log 2>&1

# 每 5 分钟检查信号
*/5 * * * * cd /path/to/YMOS && uv run ymos monitor check-signals >> /tmp/ymos-signals.log 2>&1

# naught_backtest：读取 history/ 写入 signals/（由 naught_backtest 自己配置 cron）
```

## 与现有 YMOS 的关系

### 盯盘 vs 雷达

```
盯盘（自动、高频、轻量）          雷达（手动、低频、深度）
─────────────────────          ─────────────────────
fetch-prices (Futu OpenD)       price-scan (三源分流)
→ K线历史累积                    → 即时报价 + 资金流
→ naught_backtest 信号           → AI 综合分析
→ check-signals 告警             → 写回状态机 + 报告
```

两者互不干扰：盯盘不更新状态机，雷达手动触发时才更新。

### 新增 skill: ymos-monitor

```
skills/ymos-monitor/
├── SKILL.md           # 能力定义、触发暗号
├── sop.md             # 标准操作流程
└── knowledge/
    └── signal-ref.md  # 信号类型参考表
```

触发暗号：`"开始盯盘"`、`"停一下盯盘"`、`"查看告警"`、`"监控状态"`

路由表更新：在 `skills/ymos-core/routing.md` 新增盯盘路由。

### 不修改的部分

- 现有 `router.py`（三源分流）不动
- 现有 `price-scan` 命令不动
- Holdings/watchlist 状态机更新逻辑不动
- 雷达流程不动

## 新增代码结构

```
cli/
├── commands/
│   └── monitor.py          # fetch-prices + check-signals 命令
└── monitor/
    ├── __init__.py
    ├── dedup.py            # 去重逻辑（CSV 时间戳 + 信号去重）
    ├── history.py          # CSV 历史文件读写（合并+去重）
    ├── signal_reader.py    # 信号文件扫描 + 告警生成
    └── trading_hours.py    # 交易时段判断

skills/ymos-monitor/
├── SKILL.md
├── sop.md
└── knowledge/
    └── signal-ref.md
```

复用现有模块：
- `cli/core/futu_utils.py` — 连接检查、ticker 格式转换
- `cli/core/sources/futu.py` — K线获取模式参考
- ticker 提取逻辑 — 从 `news.py` 的 `extract_tickers_from_state_machine()` 复用

## 依赖

零新依赖。纯 Python 标准库（csv、json、datetime）+ 已有的 futu-api。

## 迁移路径

本地开发 → cron 调度
服务器部署 → systemd timer + 同样的 CLI 命令
