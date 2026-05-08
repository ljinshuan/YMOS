## 1. Skill 结构创建

- [x] 1.1 创建 `.claude/skills/ymos-thesis-tracker/` 目录
- [x] 1.2 创建 `SKILL.md`，定义触发方式、调用接口、执行步骤
- [x] 1.3 创建 `sop.md`，定义论点追踪的详细操作流程
- [x] 1.4 创建 `templates/` 目录和模板文件

## 2. 模板文件创建

- [x] 2.1 创建 `templates/thesis-tracker.md` 论点追踪主模板
- [x] 2.2 创建 `templates/thesis-tracker-mini.md` 简化版模板（用于快速查看）
- [x] 2.3 在模板中定义：论点陈述、支柱、风险、记分卡、更新日志、催化剂日历等结构

## 3. Skill 核心逻辑实现

- [x] 3.1 实现论点初始化流程（输入论点陈述、支柱、风险等）
- [x] 3.2 实现记分卡生成和更新逻辑
- [x] 3.3 实现更新日志记录格式
- [x] 3.4 实现置信度管理和趋势追踪
- [x] 3.5 实现催化剂关联功能
- [x] 3.6 实现论点验证检查逻辑

## 4. 与现有 Skill 集成

- [x] 4.1 修改 `ymos-research/SKILL.md`，添加论点初始化选项
- [x] 4.2 修改 `ymos-strategy/SKILL.md`，添加论点置信度读取逻辑
- [x] 4.3 修改 `ymos-radar/SKILL.md`，添加论点更新提示

## 5. 路由更新

- [x] 5.1 更新 `ymos-core/routing.md`，添加论点追踪入口
- [x] 5.2 在 routing.md 中定义论点追踪的触发词和调用链路

## 6. 文档更新

- [x] 6.1 更新 `CLAUDE.md`，添加 ymos-thesis-tracker skill 说明
- [x] 6.2 更新 `总入口暗号.md`，添加论点追踪相关暗号
- [x] 6.3 在 skill 中添加使用示例和最佳实践

## 7. 测试验证

- [x] 7.1 测试论点初始化流程
- [x] 7.2 测试记分卡更新功能
- [x] 7.3 测试更新日志记录
- [x] 7.4 测试置信度变化追踪
- [x] 7.5 测试催化剂关联和预警
- [x] 7.6 测试与 ymos-research/strategy/radar 的集成

## 8. 完成检查

- [x] 8.1 验证所有 task 已完成
- [x] 8.2 运行 `ymos state validate` 检查状态机
- [x] 8.3 测试完整工作流（从研究到策略到追踪）
