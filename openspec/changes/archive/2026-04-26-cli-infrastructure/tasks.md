## 1. 项目骨架搭建

- [x] 1.1 创建 `cli/` 目录结构（main.py、commands/、core/、sources/、utils/）
- [x] 1.2 实现 `cli/main.py` typer app 入口，注册所有子命令组
- [x] 1.3 更新 `pyproject.toml`：添加 typer、rich 依赖，注册 `[project.scripts] ymos = "cli.main:app"`
- [x] 1.4 实现 `cli/utils/env_loader.py`（从 `Eyes/scripts/env_loader.py` 迁移）

## 2. 路径管理

- [x] 2.1 实现 `cli/core/paths.py`：Paths 类，集中定义所有路径常量（data/、references/、state 等）
- [x] 2.2 实现 YMOS 根目录自动检测逻辑（向上查找 CLAUDE.md）
- [x] 2.3 实现 `ymos init dirs` 子命令：创建所有 data/ 子目录

## 3. 数据源迁移

- [x] 3.1 迁移 `fetch_price_api.py` → `cli/core/sources/finnhub.py`，适配 typer 接口
- [x] 3.2 迁移 `fetch_price_tushare.py` → `cli/core/sources/tushare.py`
- [x] 3.3 迁移 `fetch_price_yahoo.py` → `cli/core/sources/yahoo.py`
- [x] 3.4 迁移 `fetch_rss.py` → `cli/core/sources/rss.py`
- [x] 3.5 迁移 `fetch_market_api.py` → `cli/core/sources/market.py`
- [x] 3.6 迁移 `fetch_finnhub_news.py` → `cli/core/sources/news.py`
- [x] 3.7 迁移 `fetch_price_router.py` → `cli/core/router.py` + `cli/core/crypto.py`
- [x] 3.8 迁移 `price_scan_from_state.py` 逻辑整合到 `price-scan --from-state` 命令

## 4. 数据抓取命令

- [x] 4.1 实现 `cli/commands/price.py`：`ymos price-scan` 子命令（--symbols、--from-state、--output-dir、--date-tag）
- [x] 4.2 实现 `cli/commands/rss.py`：`ymos fetch-rss` 子命令（--days、--config、--output）
- [x] 4.3 实现 `cli/commands/market.py`：`ymos fetch-market` 子命令（--days、--output）
- [x] 4.4 实现 `cli/commands/news.py`：`ymos fetch-news` 子命令（--hours、--output）

## 5. 状态机操作

- [x] 5.1 实现 `cli/core/state.py`：Markdown 表格解析器（读取状态机为结构化数据）
- [x] 5.2 实现 `cli/core/state.py`：Markdown 表格写入器（修改字段、保留格式、更新时间戳和变更日志）
- [x] 5.3 实现 `cli/commands/state.py`：`ymos state read` 子命令
- [x] 5.4 实现 `cli/commands/state.py`：`ymos state update` 子命令（--ticker、--field、--value）
- [x] 5.5 实现 `cli/commands/state.py`：`ymos state validate` 子命令

## 6. 初始化与模板命令

- [x] 6.1 实现 `cli/commands/init.py`：`ymos init stock` 子命令（--ticker、--name、--location）
- [x] 6.2 实现 `cli/commands/init.py`：`ymos init template` 子命令（--type、--ticker、--name）
- [x] 6.3 实现 `cli/commands/report.py`：`ymos report list` 子命令（--type、--latest、--date）

## 7. 迁移命令

- [x] 7.1 实现 `ymos migrate` 命令：自动将旧目录结构的数据迁移到 data/
- [x] 7.2 保留 `Eyes/scripts/` 下已迁移的脚本文件（不删除，由 entry-files-update 负责）

## 8. 验证

- [x] 8.1 CLI 可安装（pip install -e .）并注册 `ymos` 入口命令
- [x] 8.2 `ymos --help` 输出正常，所有 8 个子命令可见
- [x] 8.3 路径检测正确（`ymos state validate` 读取 data/state/ 下的文件）
- [x] 8.4 `ymos init dirs` 创建所有 data/ 子目录
- [x] 8.5 `ymos state read holdings --json` 正确解析 Markdown 表格
- [x] 8.6 `ymos report list-reports` 正确列出 data/reports/ 下的报告
