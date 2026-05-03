## 1. 状态机基础：大盘锚点 + 板块映射

- [x] 1.1 创建 `data/state/market_anchors.md` 默认模板（美股 QQQ、A 股 000300.SS、港股 2800.HK），更新 `ymos init dirs` 命令自动生成
- [x] 1.2 创建 `data/state/sector_mapping.md` 模板（Markdown 表格：Ticker、名称、板块名称、板块 ETF、市场），基于当前持仓（SOXL→SOXX、META→XLK、INTC→SOXX、CRDO→SOXX、BABA→KWEB）初始化
- [x] 1.3 验证 `ymos price-scan --symbols QQQ,SOXX,XLK,KWEB,000300.SS,2800.HK` 和 `ymos tech-analysis analyze --symbols QQQ,SOXX,XLK,KWEB` 可正常执行

## 2. Radar SOP 修改：大盘+板块扫描步骤

- [x] 2.1 修改 `.claude/skills/ymos-radar/sop.md`，在「价格扫描」步骤前插入「大盘+板块 ETF 扫描」步骤：读取 market_anchors.md → price-scan 大盘 ETF → tech-analysis 大盘 ETF → 读取 sector_mapping.md → price-scan 板块 ETF → tech-analysis 板块 ETF
- [x] 2.2 修改 `.claude/skills/ymos-radar/sop.md`，在综合分析步骤中增加「三层信号联动」判断逻辑：大盘 verdict → 板块 verdict → 顺风/逆风/分化标记
- [x] 2.3 修改 `.claude/skills/ymos-radar/sop.md`，增加 P14 自动触发条件：板块 ETF verdict 为偏多或偏空时触发 P14 板块猎手
- [x] 2.4 修改 `.claude/skills/ymos-radar/SKILL.md`，更新执行步骤描述和产出物列表，增加大盘/板块 ETF 数据文件

## 3. Radar 桥接报告模板更新

- [x] 3.1 在雷达桥接报告模板中增加「三层信号联动」section，展示：大盘锚点 verdict 表 → 板块 ETF verdict 表 → 持仓个股的三层联动汇总表（Ticker | 大盘风向 | 板块风向 | 个股信号 | 综合判断）

## 4. Market Insight SOP 修改：注入技术面数据

- [x] 4.1 修改 `.claude/skills/ymos-market-insight/sop.md`，在 P13 分析前增加大盘技术面数据获取步骤：读取 market_anchors.md → tech-analysis 大盘 ETF → 将 verdict 注入 P13 输入上下文
- [x] 4.2 修改 `.claude/skills/ymos-market-insight/SKILL.md`，更新执行步骤和产出物描述

## 5. Target Mgmt 联动：新增持仓时建议映射

- [x] 5.1 修改 `.claude/skills/ymos-target-mgmt/sop/action-a-watch.md`，在「关注」流程中增加板块映射建议步骤：基于 ticker 市场和行业信息建议板块 ETF → 用户确认 → 写入 sector_mapping.md
- [x] 5.2 修改 `.claude/skills/ymos-target-mgmt/sop/action-c-remove.md` 和 `action-d-liquidate.md`，在「移除」或「清仓」流程中增加清理 sector_mapping.md 对应条目的步骤

## 6. 验证与端到端测试

- [x] 6.1 验证：运行 `ymos init dirs` 确认 market_anchors.md 和 sector_mapping.md 自动生成
- [x] 6.2 验证：手动运行 `ymos price-scan --symbols QQQ,SOXX,XLK,KWEB` 和 `ymos tech-analysis analyze --symbols QQQ,SOXX,XLK,KWEB`，确认 ETF 数据获取和技术分析输出正常
- [x] 6.3 端到端：触发「跑一下投资雷达」，确认雷达报告中包含三层信号联动 section 和 P14 触发（如板块信号显著）
- [x] 6.4 端到端：触发「跑一下市场洞察」，确认报告中包含大盘 ETF 技术面量化数据
