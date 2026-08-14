#!/usr/bin/env python3
"""Validate the skills collection against skills/registry.json.

Checks:
  1. Registry integrity: unique valid names, required fields, allowed categories.
  2. Skill directories: skill.md exists with a valid, registry-consistent front matter.
  3. (--strict) README skill tables stay in sync with the registry.

Usage:
    python scripts/validate-skills.py          # registry + skill dirs
    python scripts/validate-skills.py --strict # also check README tables
"""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
REGISTRY_FILE = SKILLS_DIR / "registry.json"
README_FILES = [PROJECT_ROOT / "README.md", PROJECT_ROOT / "README_zh.md"]

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESCRIPTION_LEN = 300
REQUIRED_FIELDS = ["name", "title", "description", "repo", "category"]


def load_registry() -> dict:
    if not REGISTRY_FILE.exists():
        print(f"ERROR: Registry not found at {REGISTRY_FILE}", file=sys.stderr)
        sys.exit(1)
    with REGISTRY_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def parse_front_matter(md_text: str) -> dict:
    """Parse YAML-ish front matter between leading --- markers."""
    if not md_text.startswith("---"):
        return {}
    end = md_text.find("\n---", 3)
    if end == -1:
        return {}
    block = md_text[3:end]
    result = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"\'')
    return result


def validate_registry(registry: dict) -> list[str]:
    errors: list[str] = []
    skills = registry.get("skills", [])
    categories = set(registry.get("categories", {}))

    if not isinstance(skills, list) or not skills:
        errors.append("registry: 'skills' must be a non-empty list")

    seen: set[str] = set()
    for i, skill in enumerate(skills):
        label = f"registry.skills[{i}]"
        for field in REQUIRED_FIELDS:
            if field not in skill or not str(skill[field]).strip():
                errors.append(f"{label}: missing or empty field '{field}'")
        name = skill.get("name", "")
        if name:
            if not NAME_RE.match(name):
                errors.append(f"{label}: invalid name '{name}' (lowercase letters, digits, hyphens)")
            if name in seen:
                errors.append(f"{label}: duplicate name '{name}'")
            seen.add(name)
        if len(str(skill.get("description", ""))) > MAX_DESCRIPTION_LEN:
            errors.append(f"{label}: description too long (> {MAX_DESCRIPTION_LEN} chars)")
        if skill.get("category") not in categories:
            errors.append(f"{label}: unknown category '{skill.get('category')}' (allowed: {sorted(categories)})")
    return errors


def validate_skill_dirs(registry: dict) -> list[str]:
    errors: list[str] = []
    skills = registry.get("skills", [])
    names = {s["name"] for s in skills}

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir() or skill_dir.name == ".git":
            continue
        name = skill_dir.name
        if name not in names:
            errors.append(f"skills/{name}: directory not declared in registry.json")
            continue
        md_path = skill_dir / "skill.md"
        if not md_path.exists():
            errors.append(f"skills/{name}: missing skill.md")
            continue
        fm = parse_front_matter(md_path.read_text(encoding="utf-8", errors="replace"))
        skill = next(s for s in skills if s["name"] == name)
        for key in ("name", "title", "description", "category"):
            if key not in fm or not fm[key].strip():
                errors.append(f"skills/{name}: front matter missing '{key}'")
            elif key == "name" and fm[key] != name:
                errors.append(f"skills/{name}: front matter name '{fm[key]}' != directory name")
            elif key == "category" and fm[key] != skill["category"]:
                errors.append(f"skills/{name}: front matter category '{fm[key]}' != registry '{skill['category']}'")
        if "repoUrl" not in fm:
            errors.append(f"skills/{name}: front matter missing 'repoUrl'")

    for name in names:
        if not (SKILLS_DIR / name).is_dir():
            errors.append(f"registry: skill '{name}' has no directory under skills/")
    return errors


def validate_readme_tables(registry: dict) -> list[str]:
    """Check that every README skill-table row matches the registry."""
    errors: list[str] = []
    names = {s["name"] for s in registry["skills"]}
    row_re = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|")
    for readme in README_FILES:
        if not readme.exists():
            continue
        found = set()
        for line in readme.read_text(encoding="utf-8", errors="replace").splitlines():
            m = row_re.match(line)
            if m:
                found.add(m.group(1))
        for name in sorted(names - found):
            errors.append(f"{readme.name}: skill '{name}' missing from table")
        for name in sorted(found - names):
            errors.append(f"{readme.name}: table lists unknown skill '{name}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the skills collection against registry.json")
    parser.add_argument("--strict", action="store_true", help="Also check README tables stay in sync")
    args = parser.parse_args()

    registry = load_registry()
    checks = [
        ("registry.json integrity", validate_registry(registry)),
        ("skill directories & front matter", validate_skill_dirs(registry)),
    ]
    if args.strict:
        checks.append(("README tables sync", validate_readme_tables(registry)))

    failures = 0
    for title, errors in checks:
        print(f"[{'OK' if not errors else 'FAIL'}] {title}")
        for error in errors:
            print(f"      - {error}")
            failures += 1

    print()
    if failures:
        print(f"Validation FAILED with {failures} problem(s).")
        return 1
    print("Validation PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
