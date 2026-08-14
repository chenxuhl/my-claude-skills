# Claude Code 开发技能集合

> 精选的 Claude Code 开发技能集合 —— 由**单一数据源**驱动索引、安装与按需下载。

<!--
  发布到 GitHub 后，将下方徽章中的 OWNER/REPO 替换为实际仓库地址。
  技能数量徽章请与 skills/registry.json 保持同步。
-->
[![CI](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&label=CI)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 24](https://img.shields.io/badge/skills-24-blue)](skills/INDEX.md)

[**English**](./README.md)

---

## 这是什么？

本仓库是 Claude Code 的**技能索引 + 安装器 + 下载器**，而不是技能本体仓库。每个技能默认只携带一个精简的 `skill.md` 模板（仅元数据）；完整内容（参考文档、脚本等）按需从上游仓库下载。

所有内容由**单一数据源**驱动：[`skills/registry.json`](skills/registry.json)。

## 特性

- **单一数据源** —— 一份 registry 驱动模板生成、下载、校验和文档，不再有重复且漂移的技能清单。
- **轻量优先** —— 仓库保持小巧；完整技能内容按需下载（`download-skill.py`）。
- **统一 CLI** —— `python scripts/claude-skills.py <command>` 覆盖列表、状态、生成、校验和下载。
- **来源追溯** —— 每次下载都会写入 `source.json`，记录上游 commit SHA 和时间戳，内容可审计。
- **可校验、有测试** —— CI 运行 registry 校验、单元测试、Python 语法检查、ShellCheck 和 PowerShell 解析检查。
- **跨平台安装** —— Windows 用 PowerShell、macOS/Linux 用 bash，符号链接 → junction → 目录复制逐级降级。

## 快速开始

### 1. 安装技能

```powershell
# Windows（以管理员身份运行 PowerShell）
.\scripts\install.ps1
```

```bash
# macOS/Linux
chmod +x scripts/install.sh
./scripts/install.sh
```

安装脚本会把 `skills/` 目录链接（或复制）到 `~/.claude/skills` —— Claude Code 官方技能目录。在 Claude Code 中运行 `/skills` 验证。

### 2. 用统一 CLI 管理一切

```bash
python scripts/claude-skills.py list        # 列出所有可用技能
python scripts/claude-skills.py status      # 每个技能的状态：template / full / missing
python scripts/claude-skills.py setup       # （重新）从 registry 生成 skill.md 模板
python scripts/claude-skills.py index       # 重新生成 skills/INDEX.md
python scripts/claude-skills.py validate    # 校验 registry 与技能 front matter
python scripts/claude-skills.py validate --strict   # 额外校验 README 表格是否同步
python scripts/claude-skills.py download skill-creator   # 下载单个技能完整内容
python scripts/claude-skills.py download all            # 下载全部技能完整内容
```

> 想用 npm？`npm run` 暴露了同样的命令：`setup`、`setup:index`、`download`、`download:all`、`validate`、`validate:strict`、`test`、`lint`、`install:win`、`install:unix`、`uninstall:win`、`uninstall:unix`。

### 3. 下载完整技能内容（可选）

```bash
python scripts/download-skill.py --list                     # 查看可下载的技能
python scripts/download-skill.py skill-creator              # 下载单个技能
python scripts/download-skill.py all                        # 下载全部
python scripts/download-skill.py skill-creator --force      # 强制覆盖已有内容
```

每次下载都会在 `skills/<name>/source.json` 中记录上游来源：

```json
{
  "skill": "skill-creator",
  "repo": "https://github.com/ComposioHQ/awesome-claude-skills",
  "path": "skill-creator",
  "commit": "9f3c2a1...",
  "downloaded_at": "2026-02-10T12:00:00+00:00"
}
```

## 项目结构

```
self-use-skills/
├── skills/
│   ├── registry.json          # 全部 24 个技能的单一数据源
│   ├── INDEX.md               # 自动生成的技能索引（setup-skills.py --index）
│   └── <skill-name>/          # 每个技能一个目录
│       ├── skill.md           # 模板（元数据）或已下载的完整技能
│       └── source.json        # 下载时写入的来源追溯
├── scripts/
│   ├── claude-skills.py       # 统一 CLI 入口
│   ├── setup-skills.py        # 从 registry 生成 skill.md 模板 + INDEX.md
│   ├── download-skill.py      # 按上游仓库分组下载完整内容
│   ├── validate-skills.py     # registry + front matter + README 同步校验
│   ├── install.ps1 / install.sh
│   └── uninstall.ps1 / uninstall.sh
├── tests/                     # 零依赖 unittest 测试套件
├── .github/workflows/ci.yml   # 校验、测试、语法检查
├── package.json               # npm 脚本别名
├── LICENSE
└── README.md / README_zh.md
```

## 包含的技能

按分类组织。权威清单在 [`skills/registry.json`](skills/registry.json) —— 本表格由 `validate-skills.py --strict` 检查同步。

### development · 开发实践

| 技能 | 作用 | 仓库 |
|------|------|------|
| `finishing-a-development-branch` | 通过清晰选项引导开发任务收尾并处理工作流 | [obra/superpowers](https://github.com/obra/superpowers) |
| `move-code-quality-skill` | 按官方 Move Book 2024 质量清单检查 Move 包 | [1NickPappas/move-code-quality-skill](https://github.com/1NickPappas/move-code-quality-skill) |
| `software-architecture` | Clean Architecture、SOLID 等设计模式与最佳实践 | [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) |
| `subagent-driven-development` | 为每个任务分派独立子代理，迭代间设代码审查检查点 | [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) |
| `test-driven-development` | 先写测试再写实现，驱动功能开发与 bug 修复 | [obra/superpowers](https://github.com/obra/superpowers) |
| `using-git-worktrees` | 通过智能目录选择和安全验证创建隔离的 Git 工作树 | [obra/superpowers](https://github.com/obra/superpowers) |

### frontend · 前端与可视化

| 技能 | 作用 | 仓库 |
|------|------|------|
| `artifacts-builder` | 用现代前端技术构建复杂多组件 HTML 资产 | [anthropics/skills](https://github.com/anthropics/skills) |
| `d3js-visualization` | 生成 D3 图表和交互式数据可视化 | [chrisvoncsefalvay/claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill) |

### integration · 服务集成

| 技能 | 作用 | 仓库 |
|------|------|------|
| `aws-skills` | AWS 开发：CDK 最佳实践与无服务器架构模式 | [zxkane/aws-skills](https://github.com/zxkane/aws-skills) |
| `connect` | 接入 1000+ 服务：邮件、Issue、消息、数据库 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `langsmith-fetch` | 获取并分析 LangSmith Studio 执行轨迹，调试代理 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `mcp-builder` | 用 Python/TypeScript 创建高质量 MCP 服务器 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `reddit-fetch` | WebFetch 被封时用 Gemini CLI 获取 Reddit 内容 | [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) |

### productivity · 效率工具

| 技能 | 作用 | 仓库 |
|------|------|------|
| `changelog-generator` | 把技术性 Git 提交转成用户友好的发布说明 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `claude-code-terminal-title` | 给每个 Claude-Code 终端窗口动态设置标题 | [bluzername/claude-code-terminal-title](https://github.com/bluzername/claude-code-terminal-title) |
| `jules` | 把编码任务交给 Google Jules AI 代理 | [sanjay3290/ai-skills](https://github.com/sanjay3290/ai-skills) |
| `prompt-engineering` | 经典提示工程技巧与 Anthropic 最佳实践 | [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) |
| `skill-creator` | 手把手打造高效的 Claude 技能 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `skill-seekers` | 几分钟把文档网站变成 Claude AI 技能 | [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) |

### testing · 测试与调试

| 技能 | 作用 | 仓库 |
|------|------|------|
| `ffuf-web-fuzzing` | 集成 ffuf 模糊测试工具并分析漏洞结果 | [jthack/ffuf_claude_skill](https://github.com/jthack/ffuf_claude_skill) |
| `ios-simulator` | 与 iOS 模拟器交互，测试和调试 iOS 应用 | [conorluddy/ios-simulator-skill](https://github.com/conorluddy/ios-simulator-skill) |
| `playwright-browser-automation` | 由模型调用的 Playwright 自动化测试 | [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) |
| `pypict-claude-skill` | 用 PICT 成对组合测试设计全面测试用例 | [omkamal/pypict-claude-skill](https://github.com/omkamal/pypict-claude-skill) |
| `webapp-testing` | 用 Playwright 测试本地 Web 应用并抓取截图 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |

## 添加新技能

1. 在 [`skills/registry.json`](skills/registry.json) 中新增条目（`name`、`title`、`description`、`description_en`、`repo`、`path`、`category`）。
2. 重新生成模板和索引：
   ```bash
   python scripts/setup-skills.py --index
   ```
3. 在上方 README 表格（中英两份）中补充对应行，然后运行：
   ```bash
   python scripts/validate-skills.py --strict
   ```
4. 跑测试并提交：`python -m unittest discover -s tests -v`

## 校验与测试

```bash
python scripts/validate-skills.py            # registry + 技能 front matter
python scripts/validate-skills.py --strict   # + README 表格同步
python -m unittest discover -s tests -v      # 单元测试（无第三方依赖）
python -m py_compile scripts/*.py            # 语法检查
```

CI（`.github/workflows/ci.yml`）在每次 push/PR 时运行以上全部检查，外加 ShellCheck 和 PowerShell 解析器。

## 路线图

- [ ] 发布到 GitHub 并启用 CI 徽章
- [ ] 从 registry 自动生成 README 技能表（去掉手工同步）
- [ ] `download` 支持稀疏检出，适配超大上游仓库
- [ ] 支持 Claude Code 插件/Agent 打包规范（`SKILL.md` 约定）
- [ ] 增加更新检查：上游 commit 与 `source.json` 不一致时提醒

## 常见问题

**Q: 为什么每个技能默认只有 skill.md 模板？**
A: 为了让本仓库保持轻量、可审查。完整内容（参考文档、脚本）通过 `download-skill.py` 按需下载，每次下载都会在 `source.json` 中留痕。

**Q: 如何验证技能是否正确安装？**
A: 在 Claude Code 中运行 `/skills`，或在本仓库运行 `python scripts/claude-skills.py status`。

**Q: 符号链接创建失败怎么办？**
A: Windows 下创建符号链接需要管理员权限。安装脚本会自动降级为 junction，再降级为目录复制。注意：复制安装不会自动同步本仓库后续的改动。

**Q: `skills/INDEX.md` 是什么？**
A: 由 registry 自动生成的按分类技能索引（`setup-skills.py --index`），请勿手工编辑。

## 许可证

[MIT](./LICENSE)

## 贡献

参见 [CONTRIBUTING.md](./CONTRIBUTING.md)。
