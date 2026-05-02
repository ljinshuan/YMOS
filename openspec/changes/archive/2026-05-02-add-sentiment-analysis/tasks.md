## 1. CLI 数据获取层

- [x] 1.1 创建 `cli/commands/sentiment.py`，定义 `ymos fetch-sentiment` 命令组（Typer 子模块）
- [x] 1.2 实现 `--ticker TICKER` 单票查询功能：HTTP 调用 `ai-news-search.futunn.com/stock_feed`，输出 JSON
- [x] 1.3 实现 `--from-state` 批量查询：读取 holdings + watchlist 状态机，遍历所有 ticker 逐个查询
- [x] 1.4 实现 `--output-dir` 参数：JSON 文件输出到 `data/reports/sentiment/raw/YYYY-MM/`
- [x] 1.5 添加网络错误处理：API 不可达时输出明确错误提示
- [x] 1.6 在 `cli/main.py` 中注册 `fetch-sentiment` 命令

## 2. Skill 文档层

- [x] 2.1 创建 `skills/ymos-sentiment/` 目录结构：SKILL.md、sop.md、prompts/
- [x] 2.2 编写 SKILL.md frontmatter（name: ymos-sentiment, depends_on: [ymos-core], description 含触发词）
- [x] 2.3 编写 SKILL.md body：触发、前置条件、执行步骤、产出物、边界
- [x] 2.4 编写 sop.md：详细执行步骤（单票/多票/全持仓三种场景）
- [x] 2.5 编写 `prompts/p19-comment-sentiment.md`：结构化情绪分析 prompt，输出 bullish/bearish/neutral 百分比 + temperature score + key takes

## 3. 路由集成

- [x] 3.1 在 `skills/ymos-core/routing.md` 新增 ymos-sentiment 路由条目（触发词 → skill → prompt → output）
- [x] 3.2 在 intent-classifier（`skills/ymos-core/prompts/intent-classifier.md`）中新增 `sentiment-check` 意图分类

## 4. 现有 Skill 扩展

- [x] 4.1 更新 `skills/ymos-strategy/sop.md`：在 P5（FOMO Killer）和 P12（Referee）步骤中增加可选的情绪数据引用
- [x] 4.2 更新 `skills/ymos-radar/sop.md`：在信号检测环节增加情绪极端值预警逻辑（bullish > 80% 或 bearish > 70%）

## 5. 测试与验证

- [x] 5.1 验证 `uv run ymos fetch-sentiment fetch --ticker 0700.HK` 能正常返回数据（30 posts）
- [x] 5.2 验证 `uv run ymos fetch-sentiment fetch --ticker NVDA` 正常返回（30 posts）
- [x] 5.3 验证 SKILL.md 触发词已加入 routing.md 和 intent-classifier
- [x] 5.4 验证 P19 prompt 输出格式符合规范
