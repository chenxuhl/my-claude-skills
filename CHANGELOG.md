# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Unified CLI: `python scripts/claude-skills.py` (`list` / `status` / `setup` / `index` / `validate` / `download`)
- Skill validator: `scripts/validate-skills.py` (registry integrity, skill front matter, README table sync with `--strict`)
- Unit test suite under `tests/` (25 tests, zero third-party dependencies)
- GitHub Actions CI: validation, tests, Python syntax, ShellCheck, PowerShell parser
- Provenance tracking: every download writes `skills/<name>/source.json` (upstream commit SHA + timestamp)
- Repository hygiene: `LICENSE` (MIT), `CONTRIBUTING.md`, `.editorconfig`, `.markdownlint.json`, `.gitattributes`
- `skills/INDEX.md` auto-generated skill index

### Changed
- **Single source of truth**: introduced `skills/registry.json`; both `setup-skills.py` and `download-skill.py` now read from it (previously two drifting lists)
- `download-skill.py` rewritten: groups skills by upstream repo (one clone per repo), no `shell=True`, temp dirs outside the project root, robust git invocation
- Skill categories consolidated from 14 to 5 (`development` / `frontend` / `integration` / `productivity` / `testing`)
- `install.ps1` / `install.sh`: robust title extraction (no crash on missing front matter)
- `package.json`: fixed broken `install` script, added `test` / `lint` / `validate` / `download` aliases
- README (EN + ZH): badges, CLI docs, corrected installation docs, roadmap, FAQ

### Fixed
- `.gitignore` now excludes `.temp/` (downloader clone scratch space) and `tests/_tmp/`
- Skill template marker string is now shared between `setup-skills.py` and `download-skill.py` (no more magic-string drift)

## [1.0.0] - 2026-02-10

### Added
- Initial release: 24 curated Claude Code skills as lightweight `skill.md` templates
- Cross-platform installers (PowerShell / bash) with symlink → junction → copy fallback
- On-demand full-content downloader `scripts/download-skill.py`
