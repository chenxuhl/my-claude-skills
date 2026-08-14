# Claude Code Dev Skills Collection

> A curated collection of Claude Code development skills — indexed, installed and downloaded from a single source of truth.

<!-- Keep the skills count badge in sync with skills/registry.json. -->
[![CI](https://img.shields.io/github/actions/workflow/status/chenxuhl/self-use-skills/ci.yml?branch=main&label=CI)](https://github.com/chenxuhl/self-use-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 24](https://img.shields.io/badge/skills-24-blue)](skills/INDEX.md)

[**中文文档**](./README_zh.md)

---

## What is this?

This repository is a **skill index + installer + downloader** for Claude Code, not a collection of skill bodies. Every skill ships as a minimal `skill.md` template (metadata only); full content (references, scripts, docs) is downloaded on demand from the upstream repositories.

Everything is driven by a **single source of truth**: [`skills/registry.json`](skills/registry.json).

## Features

- **Single source of truth** — one registry drives templates, downloads, validation and docs. No more duplicated, drifting skill lists.
- **Lightweight by design** — the repo stays small; full skill content is fetched on demand (`download-skill.py`).
- **Unified CLI** — `python scripts/claude-skills.py <command>` covers listing, status, setup, validation and downloads.
- **Provenance tracking** — every download writes `source.json` with the upstream commit SHA and timestamp, so content is auditable.
- **Validated & tested** — CI runs registry validation, unit tests, Python syntax checks, ShellCheck and PowerShell parser checks.
- **Cross-platform installers** — PowerShell for Windows, bash for macOS/Linux, with symlink → junction → copy fallback.

## Quick Start

### 1. Install the skills

```powershell
# Windows (run PowerShell as Administrator)
.\scripts\install.ps1
```

```bash
# macOS/Linux
chmod +x scripts/install.sh
./scripts/install.sh
```

This links (or copies, if you lack permissions) the `skills/` directory into `~/.claude/skills`, Claude Code's official skills directory. Verify with `/skills` inside Claude Code.

### 2. Manage everything through the CLI

```bash
python scripts/claude-skills.py list        # list all available skills
python scripts/claude-skills.py status      # per-skill status: template / full / missing
python scripts/claude-skills.py setup       # (re)generate skill.md templates from the registry
python scripts/claude-skills.py index       # regenerate skills/INDEX.md
python scripts/claude-skills.py validate    # check registry + skill front matter
python scripts/claude-skills.py validate --strict   # also check README tables are in sync
python scripts/claude-skills.py download skill-creator   # fetch full content for one skill
python scripts/claude-skills.py download all            # fetch full content for every skill
```

> Need npm instead? `npm run` exposes the same commands: `setup`, `setup:index`, `download`, `download:all`, `validate`, `validate:strict`, `test`, `lint`, `install:win`, `install:unix`, `uninstall:win`, `uninstall:unix`.

### 3. Download full skill content (optional)

```bash
python scripts/download-skill.py --list                     # what can be downloaded
python scripts/download-skill.py skill-creator              # one skill
python scripts/download-skill.py all                        # everything
python scripts/download-skill.py skill-creator --force      # overwrite existing content
```

Each download records the upstream source in `skills/<name>/source.json`:

```json
{
  "skill": "skill-creator",
  "repo": "https://github.com/ComposioHQ/awesome-claude-skills",
  "path": "skill-creator",
  "commit": "9f3c2a1...",
  "downloaded_at": "2026-02-10T12:00:00+00:00"
}
```

## Project Structure

```
self-use-skills/
├── skills/
│   ├── registry.json          # SINGLE SOURCE OF TRUTH for all 24 skills
│   ├── INDEX.md               # auto-generated skill index (setup-skills.py --index)
│   └── <skill-name>/          # one directory per skill
│       ├── skill.md           # template (metadata) or downloaded full skill
│       └── source.json        # provenance, written on download
├── scripts/
│   ├── claude-skills.py       # unified CLI entry point
│   ├── setup-skills.py        # generate skill.md templates + INDEX.md from registry
│   ├── download-skill.py      # fetch full content, grouped per upstream repo
│   ├── validate-skills.py     # registry + front matter + README sync checks
│   ├── install.ps1 / install.sh
│   └── uninstall.ps1 / uninstall.sh
├── tests/                     # zero-dependency unittest suite
├── .github/workflows/ci.yml   # validation, tests, syntax checks
├── package.json               # npm script aliases
├── LICENSE
└── README.md / README_zh.md
```

## Included Skills

Grouped by category. The authoritative list lives in [`skills/registry.json`](skills/registry.json) — this table is checked by `validate-skills.py --strict`.

### development · 开发实践

| Skill | Description | Source |
|-------|-------------|--------|
| `finishing-a-development-branch` | Guide the finishing of a development task with clear options and workflows | [obra/superpowers](https://github.com/obra/superpowers) |
| `move-code-quality-skill` | Check Move packages against the official Move Book 2024 quality checklist | [1NickPappas/move-code-quality-skill](https://github.com/1NickPappas/move-code-quality-skill) |
| `software-architecture` | Design patterns: Clean Architecture, SOLID, software design best practices | [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) |
| `subagent-driven-development` | Dispatch independent subagents per task with review checkpoints | [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) |
| `test-driven-development` | Write tests before implementation to drive features and bug fixes | [obra/superpowers](https://github.com/obra/superpowers) |
| `using-git-worktrees` | Create isolated Git worktrees with safe validation | [obra/superpowers](https://github.com/obra/superpowers) |

### frontend · 前端与可视化

| Skill | Description | Source |
|-------|-------------|--------|
| `artifacts-builder` | Build complex multi-component Claude.ai HTML artifacts with modern web tech | [anthropics/skills](https://github.com/anthropics/skills) |
| `d3js-visualization` | Generate D3 charts and interactive data visualizations | [chrisvoncsefalvay/claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill) |

### integration · 服务集成

| Skill | Description | Source |
|-------|-------------|--------|
| `aws-skills` | AWS development with CDK best practices and serverless patterns | [zxkane/aws-skills](https://github.com/zxkane/aws-skills) |
| `connect` | Connect Claude to any app — email, issues, messages, databases, 1000+ services | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `langsmith-fetch` | Fetch and analyze LangSmith Studio execution traces to debug agents | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `mcp-builder` | Build high-quality MCP servers in Python or TypeScript | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `reddit-fetch` | Fetch Reddit content via Gemini CLI when WebFetch is blocked | [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) |

### productivity · 效率工具

| Skill | Description | Source |
|-------|-------------|--------|
| `changelog-generator` | Turn technical Git commits into user-friendly release notes | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `claude-code-terminal-title` | Set a dynamic title on each Claude-Code terminal window | [bluzername/claude-code-terminal-title](https://github.com/bluzername/claude-code-terminal-title) |
| `jules` | Delegate coding tasks to Google Jules AI agent | [sanjay3290/ai-skills](https://github.com/sanjay3290/ai-skills) |
| `prompt-engineering` | Classic prompt engineering techniques and Anthropic best practices | [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) |
| `skill-creator` | Step-by-step guide to building effective Claude skills | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| `skill-seekers` | Turn any documentation website into a Claude AI skill in minutes | [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) |

### testing · 测试与调试

| Skill | Description | Source |
|-------|-------------|--------|
| `ffuf-web-fuzzing` | Integrate the ffuf web fuzzer to run fuzzing and analyze results | [jthack/ffuf_claude_skill](https://github.com/jthack/ffuf_claude_skill) |
| `ios-simulator` | Interact with the iOS Simulator to test and debug iOS apps | [conorluddy/ios-simulator-skill](https://github.com/conorluddy/ios-simulator-skill) |
| `playwright-browser-automation` | Model-invoked Playwright automation for testing web apps | [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) |
| `pypict-claude-skill` | Design comprehensive test cases with PICT pairwise testing | [omkamal/pypict-claude-skill](https://github.com/omkamal/pypict-claude-skill) |
| `webapp-testing` | Test local web apps with Playwright, capture screenshots | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |

## Adding a New Skill

1. Add an entry to [`skills/registry.json`](skills/registry.json) (`name`, `title`, `description`, `description_en`, `repo`, `path`, `category`).
2. Regenerate templates and the index:
   ```bash
   python scripts/setup-skills.py --index
   ```
3. Add the row to the README tables above (English + Chinese), then run:
   ```bash
   python scripts/validate-skills.py --strict
   ```
4. Run the tests and commit: `python -m unittest discover -s tests -v`

## Validation & Testing

```bash
python scripts/validate-skills.py            # registry + skill front matter
python scripts/validate-skills.py --strict   # + README table sync
python -m unittest discover -s tests -v      # unit tests (no third-party deps)
python -m py_compile scripts/*.py            # syntax check
```

CI (`.github/workflows/ci.yml`) runs all of the above plus ShellCheck and the PowerShell parser on every push/PR.

## Roadmap

- [ ] Publish to GitHub and enable CI badges
- [ ] Auto-generate README skill tables from the registry (drop manual sync)
- [ ] `download` with sparse support for very large upstream repos
- [ ] Support Claude Code plugin/agent packaging (`SKILL.md` conventions)
- [ ] Add update checks: notify when an upstream commit differs from `source.json`

## FAQ

**Q: Why does each skill ship with only a `skill.md` template?**
A: To keep this repo light and reviewable. Full content (references, scripts, docs) is downloaded on demand with `download-skill.py`, and every download is traced in `source.json`.

**Q: How do I verify the skills are installed?**
A: Run `/skills` inside Claude Code, or `python scripts/claude-skills.py status` from this repo.

**Q: Symbolic link creation fails?**
A: On Windows, creating symlinks needs Administrator rights. The installer falls back to a junction, then to a full directory copy. Note: a copied installation won't auto-reflect later changes to this repo.

**Q: What is `skills/INDEX.md`?**
A: A category-grouped skill index auto-generated from the registry (`setup-skills.py --index`). Don't edit it by hand.

## License

[MIT](./LICENSE)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
