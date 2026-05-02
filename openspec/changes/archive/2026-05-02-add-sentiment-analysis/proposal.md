## Why

YMOS 目前缺乏市场情绪维度的分析能力。投资决策中，散户/社区情绪是重要的反向指标（极端看多往往是顶部信号，极端看空往往是底部信号）。富途已提供成熟的评论情绪分析能力（评论抓取 + 多空情绪分布 + temperature score），用户本地已安装 OpenD 客户端，可以直接复用。

## What Changes

- 新增 `skills/ymos-sentiment/` skill，支持对单个或多个股票进行评论情绪分析
- 新增 CLI 命令 `ymos fetch-sentiment`，通过富途 OpenD 网关获取股票评论数据
- 新增 P-series prompt（P19-comment-sentiment），用于结构化情绪分析输出
- 情绪分析结果可被 ymos-strategy 和 ymos-radar 引用，作为辅助决策维度
- 在 `skills/ymos-core/routing.md` 中新增情绪分析路由入口

## Capabilities

### New Capabilities
- `comment-sentiment`: 评论情绪抓取与多空分析能力，支持港股/美股/A股，输出 bullish/bearish/neutral 百分比 + temperature score + 关键观点摘要

### Modified Capabilities
- `ymos-strategy`: 在策略分析路由中增加情绪维度参考（作为 P12 纪律审查前的辅助输入）
- `ymos-radar`: 在投资雷达中增加情绪异动信号检测（情绪极端值预警）

## Impact

- **新增文件**: `skills/ymos-sentiment/` (SKILL.md, sop.md, prompts/p19-comment-sentiment.md), `cli/commands/sentiment.py`
- **修改文件**: `cli/main.py` (注册新命令), `skills/ymos-core/routing.md` (新增路由)
- **依赖**: 需要本地运行富途 OpenD 客户端（用户已安装）
- **数据源**: 富途评论数据 API（通过 OpenD 网关）
