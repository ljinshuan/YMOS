## 1. CLI 数据获取层

- [x] 1.1 创建 `cli/commands/capital_flow.py`，定义 `ymos fetch-capital-flow` 命令组（Typer 子模块）
- [x] 1.2 实现 OpenD 连接检测：启动时检测 localhost:11111 是否可连接，失败时输出启动指引
- [x] 1.3 实现 `--ticker TICKER` 单票查询：通过 Futu OpenD SDK 获取资金流数据（主力/散户净流入、经纪商买卖、做空量）
- [x] 1.4 实现 `--from-state` 批量查询：读取 holdings + watchlist 状态机，遍历所有 ticker
- [x] 1.5 实现市场字段归一化：港股/美股/A 股数据字段映射到统一 schema
- [x] 1.6 实现 JSON 输出到 `data/reports/radar/raw/YYYY-MM/`
- [x] 1.7 在 `cli/main.py` 中注册 `fetch-capital-flow` 命令

## 2. Prompt 与分析层

- [x] 2.1 创建 `skills/ymos-radar/prompts/` 目录（如不存在）
- [x] 2.2 编写 `skills/ymos-radar/prompts/p20-capital-anomaly.md`：资金异动分析 prompt，含信号检测规则、强度评级（strong/moderate/weak）、Tier 调整建议
- [x] 2.3 定义资金异动检测阈值：主力连续 3 日净流入 → Tier 1 加分；单日大单净流出 > 1% 流通市值 → Tier 1 警告

## 3. Radar SOP 扩展

- [x] 3.1 更新 `skills/ymos-radar/sop.md`：在价格扫描步骤后新增「资金流扫描」步骤
- [x] 3.2 更新 `skills/ymos-radar/SKILL.md`：新增触发词 `查一下资金流`、`有什么资金异动`；新增资金流扫描在执行步骤中的描述
- [x] 3.3 更新 `skills/ymos-radar/sop.md`：资金异动信号纳入 Tier 1/Tier 2 事件评级逻辑

## 4. Strategy 集成

- [x] 4.1 更新 `skills/ymos-strategy/sop.md`：在 Route A（买入）和 Route B（加仓）中增加资金流确认步骤
- [x] 4.2 更新 P12（p12-referee.md）：增加资金流作为辅助确认因子的说明

## 5. 路由集成

- [x] 5.1 更新 `skills/ymos-core/routing.md`：新增资金流相关路由条目（`查一下资金流` → radar 资金流步骤）

## 6. 测试与验证

- [x] 6.1 验证 OpenD 连接检测正常工作
- [x] 6.2 验证 `uv run ymos fetch-capital-flow --ticker 0700.HK` 能正常返回资金流数据
- [x] 6.3 验证 `uv run ymos fetch-capital-flow --from-state` 批量模式正常工作
- [x] 6.4 验证 P20 prompt 输出格式符合规范（含异动信号、强度、Tier 建议）
- [x] 6.5 验证 radar SOP 中资金流步骤正确串联
