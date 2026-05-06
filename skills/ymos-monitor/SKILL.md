---
name: ymos-monitor
metadata:
  depends_on: [ymos-core]
description: |
  自动化盯盘：定时抓价、K线累积、策略信号监控与告警。触发方式：「开始盯盘」「停一下盯盘」「查看告警」「监控状态」
---

# ymos-monitor：盯盘

## 触发
- `开始盯盘` — 提供 cron 配置指引，启动自动监控
- `停一下盯盘` — 提供停止 cron 的命令
- `查看告警` — 读取当日告警日志
- `监控状态` — 查看 history/ 文件统计信息

## 前置条件
- Futu OpenD 已启动（`127.0.0.1:11111`）
- `data/state/holdings.md` 或 `data/state/watchlist.md` 应有内容

## CLI 命令

### 抓取价格（Futu OpenD）
```bash
# 从状态机提取 ticker，获取日K + 5分钟K
uv run ymos monitor fetch-prices --from-state

# 手动指定 ticker
uv run ymos monitor fetch-prices --symbols SOXL,META

# 自定义K线周期
uv run ymos monitor fetch-prices --from-state --kline 15m

# 自定义K线数量
uv run ymos monitor fetch-prices --from-state --count 30
```

### 检查信号
```bash
# 扫描所有信号文件
uv run ymos monitor check-signals

# 只检查指定 ticker
uv run ymos monitor check-signals --tickers SOXL,META
```

## 数据流

```
cron → ymos monitor fetch-prices → data/monitor/history/
                                        ↓
                          naught_backtest (外部策略引擎)
                                        ↓
                                  data/monitor/signals/
                                        ↓
       cron → ymos monitor check-signals → data/monitor/alerts/ + 终端
```

## 文件接口

| 目录 | 读/写 | 说明 |
|------|-------|------|
| `data/monitor/prices/` | fetch-prices 写 | 价格快照 JSON |
| `data/monitor/history/` | fetch-prices 写，naught_backtest 读 | K线CSV |
| `data/monitor/signals/` | naught_backtest 写，check-signals 读 | 策略信号 JSON |
| `data/monitor/alerts/` | check-signals 写 | 告警日志 MD |

## 与雷达的关系

盯盘是**自动化的浅层监控**，雷达是**手动触发的深度分析**。两者互不干扰：
- 盯盘不更新状态机
- 盯盘数据源走 Futu OpenD（雷达走三源分流）
- 雷达手动触发时才更新 holdings 状态机

> 详细步骤见 sop.md，信号类型参考见 knowledge/signal-ref.md
