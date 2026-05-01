## Why

YMOS 当前的指令路由完全依赖 `routing.md` 中的手动关键词映射和用户对 skill 体系的熟悉程度。当用户说出自然语言（如"最近美联储加息对 NIO 影响大吗"），系统无法自动判断应该走 P8 → P3 → P2 链条。参考 FinceptTerminal 的 SuperAgent 意图路由设计，引入自动意图识别层，降低使用门槛。

## What Changes

- 在 ymos-core 中新增"意图识别"prompt 模块，定义 7-9 种投资意图分类
- 每种意图映射到最优的 skill → prompt 链条
- 在 `总入口暗号.md` 路由表中增加意图识别层：先分类意图，再路由到具体 skill
- 支持复合意图（如"分析 NIO 并看看要不要加仓"→ 研究 + 策略两步链）
- 保持用户可以直接用触发词绕过意图识别

## Capabilities

### New Capabilities
- `intent-routing`: 意图识别 prompt 模块，定义意图分类体系、映射规则、复合意图处理

### Modified Capabilities
- `ymos-core`: 更新 routing.md 增加意图识别层，新增意图分类 prompt

## Impact

- 新增文件：`skills/ymos-core/prompts/intent-classifier.md`
- 修改文件：`skills/ymos-core/routing.md`、`总入口暗号.md`
- 无 CLI 代码变更，纯 prompt/路由层改动
- 向后兼容：用户仍可直接用触发词
