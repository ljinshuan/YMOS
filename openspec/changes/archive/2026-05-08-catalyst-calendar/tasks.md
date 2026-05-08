## 1. Skill 结构创建

- [x] 1.1 创建 `.claude/skills/ymos-catalyst-calendar/` 目录
- [x] 1.2 创建 `SKILL.md`，定义触发方式、调用接口、执行步骤
- [x] 1.3 创建 `sop.md`，定义催化剂日历的详细操作流程
- [x] 1.4 创建 `templates/` 目录和模板文件

## 2. 模板文件创建

- [x] 2.1 创建 `templates/catalyst-calendar.md` 日历主模板
- [x] 2.2 创建 `templates/weekly-preview.md` 每周预览模板
- [x] 2.3 定义事件数据结构和格式

## 3. CLI 工具实现

- [x] 3.1 实现 `ymos catalyst-calendar add` 添加事件
- [x] 3.2 实现 `ymos catalyst-calendar list` 查看日历
- [x] 3.3 实现 `ymos catalyst-calendar weekly` 生成每周预览
- [x] 3.4 实现 `ymos catalyst-calendar export` 导出 Excel
- [x] 3.5 实现 `ymos catalyst-calendar fetch-earnings` 抓取财报日期

## 4. 数据抓取功能

- [x] 4.1 实现富途 API 财报日期抓取
- [x] 4.2 实现 Yahoo Finance 财报日期抓取（兜底）
- [x] 4.3 实现多市场日期标准化处理
- [x] 4.4 实现日期去重和验证逻辑

## 5. Excel 导出功能

- [x] 5.1 集成 openpyxl 库
- [x] 5.2 实现日历视图 Sheet（按日期排序）
- [x] 5.3 实现按标的分组 Sheet
- [x] 5.4 实现按影响等级排序 Sheet

## 6. 与现有 Skill 集成

- [x] 6.1 修改 `ymos-radar/SKILL.md`，添加日历集成
- [x] 6.2 修改 `ymos-strategy/SKILL.md`，添加催化剂读取
- [x] 6.3 修改 `ymos-thesis-tracker/SKILL.md`（待创建），添加催化剂关联

## 7. 路由更新

- [x] 7.1 更新 `ymos-core/routing.md`，添加催化剂日历入口
- [x] 7.2 定义催化剂日历的触发词和调用链路

## 8. 文档更新

- [x] 8.1 更新 `CLAUDE.md`，添加 ymos-catalyst-calendar skill 说明
- [x] 8.2 更新 `总入口暗号.md`，添加催化剂日历相关暗号
- [x] 8.3 在 skill 中添加使用示例和最佳实践

## 9. 测试验证

- [x] 9.1 测试手动添加事件功能
- [x] 9.2 测试财报日期抓取（A股/港股/美股）
- [x] 9.3 测试日历视图和筛选
- [x] 9.4 测试每周预览生成
- [x] 9.5 测试 Excel 导出
- [x] 9.6 测试与 ymos-radar/strategy 的集成

## 10. 完成检查

- [x] 10.1 验证所有 task 已完成
- [x] 10.2 验证数据结构完整性
- [x] 10.3 测试完整工作流
