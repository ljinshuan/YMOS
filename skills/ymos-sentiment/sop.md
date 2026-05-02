# ymos-sentiment SOP

## 场景 A：单只股票情绪分析

1. 解析 ticker（如 "看一下 NVDA 的情绪" → ticker = NVDA）
2. 运行 CLI 获取数据：
   ```bash
   uv run ymos fetch-sentiment --ticker NVDA
   ```
3. 读取输出的 JSON 文件，提取评论列表
4. 读取 `skills/ymos-sentiment/prompts/p19-comment-sentiment.md`
5. 将评论数据按 P19 prompt 格式喂给 LLM
6. 将 LLM 输出保存为报告：`data/reports/sentiment/YYYY-MM/情绪分析_YYYY-MM-DD.md`
7. 向用户展示情绪摘要（一句话结论 + 多空百分比 + temperature score）

## 场景 B：多只股票情绪对比

1. 解析多个 ticker（如 "看一下腾讯、苹果、比亚迪的情绪" → [0700.HK, AAPL, BYD]）
2. 逐个运行 `uv run ymos fetch-sentiment --ticker TICKER`
3. 对每只股票分别运行 P19 prompt 分析
4. 输出对比表格：

   | 股票 | 情绪 | 看多% | 看空% | 中性% | Temperature |
   |------|------|-------|-------|-------|-------------|

5. 保存完整报告到 `data/reports/sentiment/YYYY-MM/情绪分析_YYYY-MM-DD.md`

## 场景 C：全持仓+关注列表情绪扫描

1. 读取 `data/state/holdings.md` 和 `data/state/watchlist.md` 提取所有 ticker
2. 运行批量获取：
   ```bash
   uv run ymos fetch-sentiment --from-state
   ```
3. 对每个 ticker 的评论数据运行 P19 分析
4. 按情绪极端程度排序（最看多 → 最看空）
5. 对极端情绪（bullish > 80% 或 bearish > 70%）标注 Tier 1 预警
6. 保存报告，向用户展示预警列表

## 数据源说明

| 数据源 | 需要 | 说明 |
|--------|------|------|
| Futu 搜索 API | 网络访问 `ai-news-search.futunn.com` | HTTP 直接调用，但可能需要认证 |
| Futu OpenD | `futu-api` SDK + OpenD 运行 | 通过 localhost:11111 TCP 网关获取 |

两种数据源自动回退：先尝试 HTTP API，失败后尝试 OpenD。

## 输出格式

情绪分析报告 Markdown 结构：

```markdown
# [TICKER] 情绪分析 YYYY-MM-DD

## 一句话结论
[LLM 生成的总结]

## 情绪分布
- 看多: XX%
- 看空: XX%
- 中性: XX%
- Temperature Score: XX/100

## 关键看多观点
1. ...
2. ...
3. ...

## 关键看空观点
1. ...
2. ...
3. ...

## 预警
[如有极端情绪，在此标注]

---
数据来源：Futu 社区评论 | 仅供参考，不构成投资建议
```
