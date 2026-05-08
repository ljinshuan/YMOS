## 1. Skill 结构创建

- [ ] 1.1 创建 `.claude/skills/ymos-dcf-model/` 目录
- [ ] 1.2 创建 `SKILL.md`，定义触发方式、调用接口、执行步骤
- [ ] 1.3 创建 `sop.md`，定义 DCF 建模的详细操作流程
- [ ] 1.4 创建 `prompts/` 目录和 DCF 相关 prompts
- [ ] 1.5 创建 `templates/` 目录和模板文件

## 2. DCF Prompts 创建

- [ ] 2.1 创建 `prompts/dcf-assumptions.md` — 假设收集 prompt
- [ ] 2.2 创建 `prompts/dcf-cash-flow.md` — 现金流预测 prompt
- [ ] 2.3 创建 `prompts/dcf-wacc.md` — WACC 计算 prompt
- [ ] 2.4 创建 `prompts/dcf-terminal-value.md` — 终值计算 prompt
- [ ] 2.5 创建 `prompts/dcf-sensitivity.md` — 敏感性分析 prompt
- [ ] 2.6 创建 `prompts/dcf-scenarios.md` — 情景分析 prompt

## 3. Excel 模板创建

- [ ] 3.1 创建 Assumptions Sheet 模板
- [ ] 3.2 创建 Free Cash Flow Sheet 模板
- [ ] 3.3 创建 WACC Sheet 模板
- [ ] 3.4 创建 Terminal Value Sheet 模板
- [ ] 3.5 创建 Valuation Sheet 模板
- [ ] 3.6 创建 Sensitivity Sheet 模板
- [ ] 3.7 创建 Scenarios Sheet 模板

## 4. 计算逻辑实现

- [ ] 4.1 实现自由现金流计算逻辑
- [ ] 4.2 实现 CAPM 模型计算
- [ ] 4.3 实现 WACC 汇总计算
- [ ] 4.4 实现永续增长法终值计算
- [ ] 4.5 实现退出倍数法终值计算
- [ ] 4.6 实现现值计算（现金流 + 终值）
- [ ] 4.7 实现企业价值和股权价值计算

## 5. 敏感性分析实现

- [ ] 5.1 实现双变量敏感性表生成
- [ ] 5.2 实现 WACC vs. 永续增长率敏感性
- [ ] 5.3 实现收入增长 vs. 利润率敏感性
- [ ] 5.4 实现条件格式化应用

## 6. 情景分析实现

- [ ] 6.1 实现乐观情景参数生成
- [ ] 6.2 实现悲观情景参数生成
- [ ] 6.3 实现三情景对比计算
- [ ] 6.4 实现概率加权估值计算

## 7. 报告生成

- [ ] 7.1 创建 DCF 报告模板
- [ ] 7.2 实现执行摘要生成
- [ ] 7.3 实现详细假设列表
- [ ] 7.4 实现风险提示生成

## 8. 与现有 Skill 集成

- [ ] 8.1 修改 `ymos-core/prompts/p9-valuation.md`，添加 DCF 选项
- [ ] 8.2 修改 `ymos-research/SKILL.md`，集成 DCF 模型
- [ ] 8.3 修改 `ymos-strategy/SKILL.md`，引用 DCF 估值

## 9. 数据源集成

- [ ] 9.1 实现从数据源获取历史财务数据
- [ ] 9.2 实现行业 Beta 数据获取
- [ ] 9.3 实现无风险利率获取
- [ ] 9.4 实现市场风险溢价获取

## 10. 路由和文档更新

- [ ] 10.1 更新 `ymos-core/routing.md`，添加 DCF 模型入口
- [ ] 10.2 更新 `CLAUDE.md`，添加 ymos-dcf-model skill 说明
- [ ] 10.3 更新 `总入口暗号.md`，添加 DCF 相关暗号

## 11. 测试验证

- [ ] 11.1 测试现金流预测功能
- [ ] 11.2 测试 WACC 计算功能
- [ ] 11.3 测试终值计算功能
- [ ] 11.4 测试敏感性分析
- [ ] 11.5 测试情景分析
- [ ] 11.6 测试 Excel 模型生成
- [ ] 11.7 测试与 ymos-research 集成
- [ ] 11.8 测试与 ymos-strategy 集成

## 12. 完成检查

- [ ] 12.1 验证所有 task 已完成
- [ ] 12.2 验证 Excel 模型公式正确性
- [ ] 12.3 验证计算逻辑与手工计算一致
- [ ] 12.4 测试完整工作流
