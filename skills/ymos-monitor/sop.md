# ymos-monitor SOP

## 1. 开始盯盘

### 步骤

1. 确认 Futu OpenD 已启动
2. 确认 holdings.md / watchlist.md 有 ticker
3. 提供以下 cron 配置：

```bash
# 编辑 crontab
crontab -e

# 添加以下内容（每 5 分钟执行一次）
# fetch-prices: 交易时段自动过滤，可全天候配置
*/5 * * * * cd /path/to/YMOS && uv run ymos monitor fetch-prices --from-state >> /tmp/ymos-prices.log 2>&1

# check-signals: 扫描信号并告警
*/5 * * * * cd /path/to/YMOS && uv run ymos monitor check-signals >> /tmp/ymos-signals.log 2>&1
```

4. 验证 cron 生效：等待一个周期后检查日志

### 注意事项
- 路径替换为实际 YMOS 项目路径
- naught_backtest 需要单独配置 cron，读取 `data/monitor/history/` 写入 `data/monitor/signals/`
- `fetch-prices` 默认跳过非交易时段，无需精确配置时段

## 2. 停一下盯盘

```bash
# 查看 cron 任务
crontab -l

# 编辑并删除 monitor 相关行
crontab -e
```

## 3. 查看告警

```bash
# 直接读取告警文件
cat data/monitor/alerts/$(date +%Y-%m-%d).md

# 或通过 CLI
uv run ymos monitor check-signals
```

## 4. 监控状态

检查 history/ 文件统计：
```bash
# 查看有哪些 ticker 的历史数据
ls data/monitor/history/

# 查看某个 ticker 的数据行数
wc -l data/monitor/history/SOXL_daily.csv
wc -l data/monitor/history/SOXL_5m.csv

# 查看最近快照
ls data/monitor/prices/$(date +%Y-%m-%d)/
```
