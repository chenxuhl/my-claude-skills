# my-claude-skills

> mattpocock × superpowers 组合最佳实践：用 `choose-skill` 做复杂度路由，让两个数据源各司其职、重叠区二选一。

## 为什么组合

两个数据源不是二选一，而是互补：

| 维度 | mattpocock/skills | obra/superpowers |
|------|-------------------|------------------|
| 技能数 | ~18（engineering 为主） | 14（开发协作） |
| 定位 | L2 轻量层 | L3 重型层 |
| 哲学 | 小、易改、可组合；每步做完即停 | 完整方法论；spec→plan→subagent→review，agent 可自主工作数小时 |
| 擅长 | issue 驱动流水线、架构深挖、研究 | 大计划自主实现、并行多 agent 分派、设计头脑风暴 |
| 重叠 | tdd / diagnosing-bugs / code-review / grill-me | test-driven-development / systematic-debugging / requesting-code-review / brainstorming |

重叠区有 4 个技能做同一件事——**二选一，不要两个都跑**。

## 路由层：choose-skill

[`skills/choose-skill/SKILL.md`](skills/choose-skill/SKILL.md) 是复杂度路由器，在调用任何工程技能之前先分档：

- **L1 · 直接做** —— 单点修改、事实问题。不调任何技能。
- **L2 · 单个 Matt 技能** —— ≤3 文件、目标已清晰。每步做完停，等用户确认下一跳。
- **L3 · superpowers 全流程** —— >3 文件/多模块/多会话。**先确认再进入**：brainstorming → writing-plans → subagent-driven-development → review。

核心原则：**偏向下限**。两档之间犹豫时选低的；现实证明更重可以中途升级，但已烧在仪式上的 token 退不回来。

结构化数据（两源元信息、路由规则、重叠去重表）在 [`skills/registry.json`](skills/registry.json)。

## 安装

```bash
# superpowers（托管、自动更新）
/plugin install superpowers@claude-plugins-official

# mattpocock（两种哲学，二选一）
claude plugins install mattpocock-skills     # 托管只读，自动更新
# 或
npx skills@latest add mattpocock/skills      # 拷贝可编辑，手动 npx skills update
```

两个都装会触发重叠——`choose-skill` 已在路由层处理去重，按它的 L2 默认规则用 Matt 的版本。

## 使用

把 `skills/choose-skill/SKILL.md` 放进你的 `~/.claude/skills/choose-skill/`。然后在任何工程请求之前，让 agent 先跑 `choose-skill` 分档。具体路由表见该 SKILL.md 的 Step 2。

## License

MIT
