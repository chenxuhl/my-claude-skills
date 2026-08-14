# Contributing

Thanks for helping make this collection better! This is a personal project, but well-structured contributions are very welcome.

## Development setup

```bash
# 1. Verify the collection is healthy
python scripts/validate-skills.py --strict

# 2. Run the test suite (zero third-party dependencies)
python -m unittest discover -s tests -v

# 3. Syntax-check everything
python -m py_compile scripts/*.py
```

## Adding or updating a skill

1. **Edit the registry** — `skills/registry.json` is the single source of truth. Every change goes there first:
   ```json
   {
     "name": "my-skill",
     "title": "My Skill",
     "description": "一句中文描述",
     "description_en": "One-line English description",
     "repo": "https://github.com/owner/repo",
     "path": "skills/my-skill",
     "category": "development"
   }
   ```
   - `name`: lowercase letters, digits and hyphens only; must be unique.
   - `path`: path inside the upstream repo (empty string = repo root). Do **not** include `tree/` or `blob/` prefixes — those are web URLs, not repo paths.
   - `category`: one of `development`, `frontend`, `integration`, `productivity`, `testing` (add a new one only if it genuinely doesn't fit).

2. **Regenerate templates & index**:
   ```bash
   python scripts/setup-skills.py --index
   ```

3. **Keep the READMEs in sync** — add the row to the skill tables in both `README.md` and `README_zh.md`. CI enforces this with `validate-skills.py --strict`.

4. **Add tests if you touched the scripts** — see `tests/` (plain `unittest`, no third-party deps).

## Git conventions

- Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.
- Keep changes focused; one logical change per commit.
- Update `CHANGELOG.md` under an "Unreleased" section when relevant.

## Pull request checklist

- [ ] `python scripts/validate-skills.py --strict` passes
- [ ] `python -m unittest discover -s tests -v` passes
- [ ] README (EN + ZH) skill tables match the registry
- [ ] No secrets or local paths committed (mind `.claude/settings.local.json`)
