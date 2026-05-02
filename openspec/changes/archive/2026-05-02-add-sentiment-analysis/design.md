## Context

YMOS 目前有 9 个 skill，覆盖从 onboarding 到策略分析的全流程，但缺少市场情绪维度。Futu SkillHub 已提供成熟的评论情绪分析能力（评论抓取 → 多空分布 → temperature score → 关键观点摘要）。用户本地已安装 Futu OpenD 客户端，可通过 OpenAPI 网关获取数据。

YMOS 的架构是 `skills/ → data/ → cli/`，数据获取通过 `cli/commands/` 下的 Typer 子模块实现，每个模块注册为 `ymos <command>` 命令。新能力需要遵循这一模式。

## Goals / Non-Goals

**Goals:**
- 新增 `skills/ymos-sentiment/` skill，支持单股票和多股票评论情绪分析
- 新增 CLI 命令 `ymos fetch-sentiment`，通过 Futu OpenD 获取评论数据并输出结构化 JSON
- 新增 P19-comment-sentiment prompt，用于 LLM 对评论数据的深度分析
- 情绪分析结果可被 ymos-strategy 和 ymos-radar 引用为辅助维度
- 触发词：「看一下 [ticker] 的情绪」「[ticker] 多空怎么样」「分析一下市场情绪」

**Non-Goals:**
- 不实现实时情绪监控推送（batch 模式即可）
- 不自建评论爬虫（完全复用 Futu 数据源）
- 不做情绪预测或情绪交易策略（只做当前情绪快照）

## Decisions

### 1. 新建独立 skill vs 扩展 radar

**选择：新建 `ymos-sentiment` 独立 skill**

理由：情绪分析与雷达的价格扫描在数据源、输出格式、使用场景上差异较大。雷达是定期批量扫描，情绪是按需查询。独立 skill 可以单独触发，也可以被其他 skill 引用，符合 YMOS 的 skill 解耦原则。

替代方案：将情绪分析作为 radar 的子步骤——会导致 radar 职责膨胀，且情绪分析无法独立使用。

### 2. Prompt 编号与位置

**选择：P19-comment-sentiment，放在 `skills/ymos-sentiment/prompts/` 下**

理由：P1-P18 已被占用。P19 紧跟现有编号体系。由于该 prompt 仅被 ymos-sentiment 使用，按 YMOS 规范应放在 skill 内部而非 ymos-core。

### 3. 数据获取方式

**选择：通过 Futu 搜索 API（HTTP）直接获取评论数据，不需要 OpenD**

理由：Futu 的评论情绪分析属于 Search Skill 类别，使用 `ai-news-search.futunn.com` HTTP 端点，无需 OpenD 网关。CLI 命令通过 HTTP 直接调用搜索端点获取评论，LLM 在本地做情绪分类和结构化输出。这是 Futu Skill 体系中唯一不需要 OpenD 的能力。

替代方案：通过 OpenD TCP 网关获取——OpenD 主要用于行情/交易类 API，评论搜索走 HTTP 更直接。

### 4. 与 strategy/radar 的集成方式

**选择：松耦合——情绪数据作为可选输入，由 strategy/radar 在需要时主动读取**

理由：情绪数据不是每次策略分析都需要的（如持有检查 Route C），也不应强制阻塞 radar 流程。通过文件输出（`data/reports/sentiment/`）实现松耦合，其他 skill 可按需读取最新的情绪报告。

## Risks / Trade-offs

- **[搜索 API 不可达]** → CLI 检测网络连接，无法访问 `ai-news-search.futunn.com` 时给出明确提示
- **[评论数据为空]** → 小市值/冷门股票可能无评论数据，返回空结果时提示用户
- **[情绪分析延迟]** → 评论抓取 + LLM 分析需要时间，文档说明预计耗时（单股票 ~30s）
- **[Futu API 限流]** → 批量查询时加入间隔，避免触发频率限制
