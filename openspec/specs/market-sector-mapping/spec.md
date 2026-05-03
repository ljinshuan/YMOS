## ADDED Requirements

### Requirement: 大盘锚点配置
系统 SHALL 在 `data/state/market_anchors.md` 中维护用户关注的市场指数 ETF 列表，作为大盘趋势判断的锚点。

#### Scenario: 默认大盘锚点
- **WHEN** 系统初始化（`ymos init dirs`）且 `market_anchors.md` 不存在
- **THEN** 系统创建默认配置：美股 QQQ、A 股 000300.SS（沪深300）、港股 2800.HK（盈富基金）

#### Scenario: 用户自定义大盘锚点
- **WHEN** 用户说「大盘锚点设为 SPY 和 IWM」
- **THEN** 系统更新 `market_anchors.md`，替换美股锚点为 SPY 和 IWM

#### Scenario: 多市场大盘锚点
- **WHEN** 用户持仓涉及多个市场（美股+A 股）
- **THEN** 系统为每个市场维护至少一个大盘锚点 ETF

### Requirement: 板块-个股映射表
系统 SHALL 在 `data/state/sector_mapping.md` 中维护 ticker 与板块 ETF 的映射关系。

#### Scenario: 新增持仓时自动建议映射
- **WHEN** ymos-target-mgmt 新增一个 ticker 到 holdings 或 watchlist
- **THEN** 系统基于 ticker 的市场信息建议对应的板块 ETF，经用户确认后写入 `sector_mapping.md`

#### Scenario: 映射表格式
- **WHEN** 映射表被读取
- **THEN** 每行包含：Ticker、名称、板块名称、板块 ETF、市场

#### Scenario: 从映射表获取板块 ETF 列表
- **WHEN** radar 或 strategy 流程需要扫描板块
- **THEN** 系统读取 `sector_mapping.md`，提取所有不重复的板块 ETF ticker 列表

### Requirement: 映射表与状态机同步
系统 SHALL 在 holdings/watchlist 状态机变更时同步更新 `sector_mapping.md`。

#### Scenario: 清仓移除映射
- **WHEN** 一个 ticker 从 holdings 和 watchlist 中都移除
- **THEN** 该 ticker 的板块映射条目从 `sector_mapping.md` 中删除
