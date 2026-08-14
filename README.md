# my-claude-skills

A curated index of 24 Claude Code skills, installable and downloadable on demand.

## What

Each skill ships as a directory under `skills/`; full content (references, scripts) is fetched from upstream repos with `scripts/skills.py download`. The single source of truth is [`skills/registry.json`](skills/registry.json).

## Install

```powershell
# Windows (admin)
.\scripts\install.ps1
```

```bash
# macOS/Linux
./scripts/install.sh
```

Links `skills/` into `~/.claude/skills` (falls back to junction, then copy on Windows). Verify with `/skills` inside Claude Code.

## Use

```bash
python scripts/skills.py list                    # list all skills
python scripts/skills.py status                  # per-skill status: template / full / missing
python scripts/skills.py download skill-creator  # download one skill's full content
python scripts/skills.py download all            # download everything
```

Each download records provenance in `skills/<name>/source.json` (upstream commit SHA + timestamp).

## Skills

24 skills across 5 categories. See [`skills/registry.json`](skills/registry.json) for the authoritative list with descriptions and upstream repos — it is the single source of truth, no separate index to keep in sync.

## License

MIT
