## 1. 依赖与基础设施

- [ ] 1.1 在 `pyproject.toml` 添加 `pandas>=2.0` 和 `pandas-ta>=0.3.14b` 依赖
- [ ] 1.2 运行 `uv sync` 安装新依赖，验证 import 正常

## 2. 历史数据获取模块 (`cli/core/sources/history.py`)

- [ ] 2.1 实现 `fetch_history(symbols, tushare_token)` 函数，路由 A 股到 Tushare、其他到 Yahoo，返回 `dict[str, pd.DataFrame]`
- [ ] 2.2 扩展 Tushare 调用：设置 `start_date` 为 1 年前，`end_date` 为今天，获取完整日线数据
- [ ] 2.3 扩展 Yahoo 调用：设置 `period="1y", interval="1d"`，将 bars 转换为标准 DataFrame（列名 open/high/low/close/volume，DatetimeIndex）
- [ ] 2.4 处理获取失败的 ticker：跳过并 log warning，不影响其他 ticker

## 3. 技术指标计算引擎 (`cli/core/tech.py`)

- [ ] 3.1 实现 `compute_indicators(df)` — 在 DataFrame 上追加 MA(5/10/20/60/120/250)、MACD(12/26/9)、ADX/+DI/-DI(14)、RSI(6/14)、KDJ(9/3/3)、Williams %R(14)、布林带(20,2)、ATR(14)、OBV、成交量 MA(5/20)
- [ ] 3.2 实现多周期 resample：日线→周线（W）、日线→月线（ME），对每个周期调用 `compute_indicators`
- [ ] 3.3 实现 `generate_signals(indicators_df)` — 对每个指标提取最新值，判断多头/空头/中性信号，返回 `list[dict]`
- [ ] 3.4 实现 `summarize(daily_signals, weekly_signals, monthly_signals)` — 汇总三周期信号，计算多空比例，返回综合判断和共振描述
- [ ] 3.5 实现 `analyze(df)` — 整合以上函数，返回完整分析结果 dict

## 4. CLI 命令 (`cli/commands/tech.py`)

- [ ] 4.1 实现 `tech_analysis` 命令：支持 `--symbols`、`--from-state`、`--output-dir` 参数
- [ ] 4.2 实现 `--from-state` 逻辑：读取 `holdings.md` 和 `watchlist.md` 中的 ticker 列表
- [ ] 4.3 实现 Markdown 报告生成：综合判断 → 日线表格 → 周线表格 → 月线表格 → 关键信号摘要
- [ ] 4.4 实现输出路径逻辑：默认 `data/reports/tech/{YYYY-MM}/{TICKER}_技术面分析.md`，同日覆盖

## 5. 注册与集成

- [ ] 5.1 在 `cli/main.py` 注册 `tech-analysis` 命令
- [ ] 5.2 在 `skills/ymos-strategy/prompts/` 的 P5 和 P6 中增加技术面报告引用指引

## 6. 验证

- [ ] 6.1 端到端测试：`uv run ymos tech-analysis --symbols AAPL` 生成报告，验证内容正确
- [ ] 6.2 多市场测试：同时测试美股（AAPL）、港股（0700.HK）、A股（688008.SS）
- [ ] 6.3 `--from-state` 测试：从持仓/关注列表读取 ticker 并批量生成报告
