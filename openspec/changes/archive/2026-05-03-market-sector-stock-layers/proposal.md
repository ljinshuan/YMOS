## Why

YMOS 当前以个股为中心，大盘和板块只是 P13 市场洞察中的文字描述（新闻级），没有量化的价格/技术面追踪。投资者决策需要三层上下文：大盘趋势（顺风/逆风）→ 板块趋势（行业资金流向）→ 个股信号。缺少上层判断会导致在逆风板块中追多、或在顺风大盘中过早看空。

CLI 工具层已经具备对任意 ETF（QQQ、SOXX、SPY 等）做价格扫描和技术分析的能力，但没有任何 skill 流程去调用它们。

## What Changes

- 新增「大盘锚点」配置 — 在 preferences.md 或独立状态机中定义用户关注的市场指数 ETF（如美股看 QQQ，A 股看沪深300 ETF）
- 新增「板块-个股映射表」— 维护 `{ticker → sector ETF}` 映射（INTC→SOXX, META→XLK, BABA→KWEB）
- 修改 ymos-radar 流程 — 雷达扫描时自动拉取大盘+板块 ETF 价格和技术面，输出三层联动判断（大盘趋势→板块趋势→个股信号）
- 修改 ymos-market-insight 流程 — 在 P13 分析前增加大盘/板块技术面数据作为量化输入（当前纯靠新闻文字）
- P14 板块猎手升级 — 对持仓涉及的板块自动执行 P14 扫描（当前手动触发）

## Capabilities

### New Capabilities
- `market-sector-mapping`: 板块-个股映射表 + 大盘锚点配置，定义 ticker→sector ETF 映射关系和用户关注的市场指数 ETF
- `multi-layer-signal`: 三层信号联动机制 — 大盘技术面→板块技术面→个股信号的综合判断框架，在雷达和策略流程中提供顺风/逆风过滤

### Modified Capabilities
- `skill-ymos-radar`: 雷达流程增加大盘+板块 ETF 价格扫描和技术分析步骤，桥接报告新增三层信号联动section
- `skill-ymos-market-insight`: P13 分析增加量化技术面数据输入（大盘/板块 ETF 技术指标），不再仅依赖新闻文字

## Impact

- **Skills**: ymos-radar SOP 需增加大盘/板块扫描步骤；ymos-market-insight SOP 需增加技术面数据获取步骤
- **State machine**: preferences.md 或新文件需增加大盘锚点和板块映射配置
- **CLI**: 无新命令，复用现有 `ymos price-scan --symbols` 和 `ymos tech-analysis analyze --symbols`
- **Prompts**: P13 可能需要微调输入格式以接受技术面数据；雷达桥接报告模板需增加三层信号section
- **数据**: 新增 `data/reports/radar/raw/` 下大盘/板块 ETF 价格和技术面 JSON 文件
