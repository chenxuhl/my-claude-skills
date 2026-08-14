# my-claude-skills

> mattpocock × superpowers 组合最佳实践：用 `choose-skill` 做复杂度路由，让两个数据源各司其职、重叠区二选一，**匹配工作量而非放大工作量**。

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

## 组合的优势（对比三个基线）

| 基线 | 失败模式 | 本组合如何解决 |
|------|----------|----------------|
| **单用 mattpocock** | 遇到大计划只能手动拼流水线，缺 subagent 自主执行、并行分派、worktree 隔离 | L3 直接连 superpowers：`subagent-driven-development` + `dispatching-parallel-agents` + `using-git-worktrees` 让 agent 连续工作数小时不偏航 |
| **单用 superpowers** | 每个请求默认走 brainstorming→plan→subagent 仪式，typo 也要三步流程，token 在仪式上烧光 | `choose-skill` 在最前端分档：L1 直接做，L2 单个 Matt 技能做完即停。**偏向下限**——工作够轻就别调重型流程 |
| **两套都装、无路由** | 60+ 技能平铺，重叠 4 项会被模型重复触发（`tdd` 和 `test-driven-development` 各跑一遍），agent 选错档无提示 | `choose-skill` 做三件事：①L1/L2/L3 复杂度路由 ②重叠区二选一（默认用 Matt 的）③模型分档前必须 announce `choose-skill: L{n} — {reason}`，用户可一词否决 |

**一句话总结**：单用任一数据源要么太轻（Matt 应付不了大计划）要么太重（superpowers 对小任务是过度流程化）；无路由地两套同装则是技能堆砌 + 重复触发。本组合用 `choose-skill` 把两个数据源剪裁成**按工作量自动匹配档位**的单一系统，让小任务走轻流程、大任务走重流程、重叠区不重复。

## 路由层：choose-skill

[`skills/choose-skill/SKILL.md`](skills/choose-skill/SKILL.md) 是复杂度路由器，在调用任何工程技能之前先分档：

- **L1 · 直接做** —— 单点修改、事实问题。不调任何技能。
- **L2 · 单个 Matt 技能** —— ≤3 文件、目标已清晰。每步做完停，等用户确认下一跳。
- **L3 · superpowers 全流程** —— >3 文件/多模块/多会话。**先确认再进入**：brainstorming → writing-plans → subagent-driven-development → review。

核心原则：**偏向下限**。两档之间犹豫时选低的；现实证明更重可以中途升级，但已烧在仪式上的 token 退不回来。

结构化数据（两源元信息、路由规则、重叠去重表）在 [`skills/registry.json`](skills/registry.json)。

## 安装

三步配置完，之后 `choose-skill` 在每次工程请求前自动分档：

```bash
# 1. superpowers（托管、自动更新）——提供 L3 重型流程
/plugin install superpowers@claude-plugins-official

# 2. mattpocock（两种哲学，二选一）——提供 L2 轻量技能
claude plugins install mattpocock-skills     # 托管只读，自动更新
# 或
npx skills@latest add mattpocock/skills      # 拷贝可编辑，手动 npx skills update

# 3. 路由层（本仓库核心）
cp skills/choose-skill/SKILL.md ~/.claude/skills/choose-skill/SKILL.md
```

两套都装会触发重叠——这恰好是 `choose-skill` 的价值所在：路由层已内建重叠区二选一规则（默认用 Matt 版本），无需手工剪裁。

## 使用

路由层装好后，在任何工程请求之前让 agent 先跑 `choose-skill` 分档。具体路由表见 [`skills/choose-skill/SKILL.md`](skills/choose-skill/SKILL.md) 的 Step 2。

体感差异：
- **改 typo** → 不再被模型带进 brainstorming→plan 仪式，L1 直接改完
- **调一个难复现 bug** → 自动走 Matt 的 `diagnosing-bugs`（先建红反馈环），不会误触 superpowers 的 `systematic-debugging` 重复跑
- **做一个跨模块大功能** → 模型先 announce `L3`，等你确认才进入 superpowers 全流程，不会静默起跳重型流程

结构化数据（两源元信息、路由规则、重叠去重表）在 [`skills/registry.json`](skills/registry.json)。

## License

MIT
