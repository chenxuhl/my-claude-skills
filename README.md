# my-claude-skills

> `choose-skill` 路由层：**小需求走 Matt 不让模型滑进重流程仪式；大需求在 Matt ticket 流和 superpowers 全流程间二选一**。

## 为什么这样组合

**起点**：装了 superpowers 之后，发现它太重——每个小请求默认走 brainstorming→writing-plans→subagent-driven-development 仪式，改个 typo 也要三步流程，token 在仪式上烧光。

**解决**：装 Matt skills 作为小需求的主力（每步做完即停、不自动链式），让 `choose-skill` 在路由层把 L1/L2 锁死给 Matt——superpowers 进不来。大需求（L3）不排斥 superpowers：它在 L3 是和 Matt ticket 流并列的合法选项，按工作形状选。

| 维度 | mattpocock/skills | obra/superpowers |
|------|-------------------|------------------|
| 角色 | L1/L2 主力，L3 选项之一 | L3 选项之一，L1/L2 进不来 |
| 哲学 | 小、易改、可组合；每步做完即停 | 完整方法论；spec→plan→subagent→review，agent 可自主工作数小时 |
| 何时用 | 改 typo / 单技能任务 / ticket 逐个交付的大功能 | 要 agent 长时间自主/并行/隔离 worktree 的大需求 |
| 重叠 | tdd / diagnosing-bugs / code-review / grill-me | test-driven-development / systematic-debugging / requesting-code-review / brainstorming |

## 组合的优势

| 基线 | 失败模式 | 本组合如何解决 |
|------|----------|----------------|
| **单用 superpowers** | 每个小请求都走重仪式，typo 也要三步流程，token 烧光 | `choose-skill` 把 L1/L2 锁给 Matt——superpowers 进不来；只有大需求（L3）才可能选它 |
| **单用 Matt** | 超大任务缺 subagent 自主执行、worktree 隔离、并行分派 | L3 档保留 superpowers 全流程作为合法选项，用户按工作形状选 |
| **两套都装、无路由** | 60+ 技能平铺，小任务也会误触 superpowers 重流程 | `choose-skill` 三件事：①L1/L2/L3 复杂度路由 ②L1/L2 重叠区走 Matt、superpowers 进不来 ③分档前必须 announce `choose-skill: L{n} — {reason}`，用户可一词否决 |

**一句话**：superpowers 太重不是卸载它（大需求要用），而是用 `choose-skill` 把它关在 L3 门里——小需求 Matt 直接管够，大需求才可能让 superpowers 出来，且和 Matt ticket 流并列二选一，不是默认项。

## 路由层：choose-skill

[`skills/choose-skill/SKILL.md`](skills/choose-skill/SKILL.md) 是复杂度路由器，在调用任何工程技能之前先分档：

- **L1 · 直接做** —— 单点修改、事实问题。不调任何技能。
- **L2 · 单个 Matt 技能** —— ≤3 文件、目标已清晰。每步做完停，等用户确认下一跳。superpowers 不进此档。
- **L3 · 两条路二选一** —— >3 文件/多模块/多会话。**先确认再进入**：
  - **Matt ticket 流**：`to-spec` → `to-tickets` → `implement` per ticket → `code-review`（含 `wayfinder`/`improve-codebase-architecture`）
  - **superpowers 全流程**：`brainstorming` → `using-git-worktrees` → `writing-plans` → `subagent-driven-development` → `requesting-code-review` → `finishing-a-development-branch`
  - **按形状选**：要 ticket 逐个交付 → Matt；要 agent 长时间自主/并行 → superpowers；犹豫 → Matt（更易中断转向）

核心原则：**偏向下限**。两档之间犹豫时选低的；现实证明更重可以中途升级，但已烧在仪式上的 token 退不回来。分档前必须 announce `choose-skill: L{n} — {reason}`，用户可一词否决。

体感差异：
- **改 typo** → 不再被模型带进 brainstorming→plan 仪式，L1 直接改完
- **调一个难复现 bug** → 自动走 Matt 的 `diagnosing-bugs`，不会误触 superpowers 的 `systematic-debugging` 重复跑
- **做一个跨模块大功能** → L3 档打开，按形状选：要逐个 ticket 交付走 Matt `to-spec→to-tickets→implement`；要 agent 自主数小时走 superpowers 全流程

结构化数据（两源元信息、路由规则、重叠去重表、bias 原则）在 [`skills/registry.json`](skills/registry.json)。具体路由表见 SKILL.md 的 Step 2。

## 安装

三步配置完，之后 `choose-skill` 在每次工程请求前自动分档。命令标注了运行位置：**会话内**（在 Claude Code 会话输入）vs **终端**（在外部 shell 跑）。

```bash
# 1. superpowers —— 提供 L3 重型流程
#    运行位置：会话内
/plugin install superpowers@claude-plugins-official

# 2. mattpocock —— 提供 L2 轻量技能（两种哲学，二选一）
#    运行位置：终端
claude plugins install mattpocock-skills     # 托管只读，自动更新
# 或
npx skills@latest add mattpocock/skills      # 拷贝可编辑，手动 npx skills update
```

```bash
# 3. 路由层（本仓库核心）—— 把 SKILL.md 复制到你的 skills 目录
#    运行位置：终端，在本仓库根目录下
# macOS / Linux:
mkdir -p ~/.claude/skills/choose-skill && cp skills/choose-skill/SKILL.md ~/.claude/skills/choose-skill/SKILL.md
# Windows (PowerShell):
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\choose-skill" | Out-Null; Copy-Item "skills\choose-skill\SKILL.md" "$env:USERPROFILE\.claude\skills\choose-skill\SKILL.md"
```

两套都装会触发重叠——这恰好是 `choose-skill` 的价值所在：路由层已内建重叠区二选一规则（默认用 Matt 版本），无需手工剪裁。

## License

MIT
