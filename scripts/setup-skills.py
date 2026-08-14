#!/usr/bin/env python3
"""Skills Setup Script - Generate skill.md templates and INDEX.md from registry.json.

Usage:
    python scripts/setup-skills.py            # generate/refresh skill templates
    python scripts/setup-skills.py --index    # also regenerate skills/INDEX.md
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
REGISTRY_FILE = SKILLS_DIR / "registry.json"

# Marker used to detect "template-only" skill.md files. download-skill.py relies
# on this exact string to decide whether a skill has real content or not.
TEMPLATE_MARKER = "此技能的完整内容需要从官方仓库获取"

# Allowed front matter keys, in output order.
FRONT_MATTER_KEYS = ["name", "title", "description", "category", "repoUrl"]


def load_registry() -> dict:
    """Load and validate the skills registry (single source of truth)."""
    if not REGISTRY_FILE.exists():
        print(f"ERROR: Registry not found at {REGISTRY_FILE}", file=sys.stderr)
        sys.exit(1)
    with REGISTRY_FILE.open(encoding="utf-8") as f:
        registry = json.load(f)
    if not registry.get("skills"):
        print("ERROR: Registry contains no skills.", file=sys.stderr)
        sys.exit(1)
    return registry


def build_repo_url(skill: dict) -> str:
    """Build a clickable GitHub URL for a skill."""
    return skill["repo"]


def skill_template(skill: dict) -> str:
    """Generate the skill.md template content for one skill."""
    repo_url = build_repo_url(skill)
    category = skill["category"]
    title = skill["title"]
    description = skill["description"]
    name = skill["name"]

    content = f"""---
name: {name}
title: {title}
description: {description}
category: {category}
repoUrl: {repo_url}
---

# {title}

> {description}

## 来源

- 仓库: {repo_url}

## 类别

`{category}`

## 说明

{TEMPLATE_MARKER} 运行以下命令下载完整技能：

```bash
python scripts/download-skill.py {name}
```
"""
    return content


def has_full_content(skill_dir: Path) -> bool:
    """Return True if the skill directory already contains downloaded content."""
    for sub in ("references", "scripts"):
        d = skill_dir / sub
        if d.exists() and any(d.iterdir()):
            return True
    return False


def create_skill(skill: dict, force: bool = False) -> str:
    """Create or refresh one skill directory. Returns a status message."""
    skill_path = SKILLS_DIR / skill["name"]
    skill_path.mkdir(exist_ok=True)
    skill_md = skill_path / "skill.md"

    if has_full_content(skill_path) and not force:
        return f"[SKIP] {skill['name']}: has downloaded content (use --force to overwrite template)"

    skill_md.write_text(skill_template(skill), encoding="utf-8")
    return f"[OK]   {skill['name']} -> {skill_md.relative_to(PROJECT_ROOT)}"


def generate_index(registry: dict) -> Path:
    """Generate skills/INDEX.md grouped by category."""
    categories = registry.get("categories", {})
    skills = registry["skills"]

    lines = [
        "# 技能索引（Skills Index）",
        "",
        "> 本文件由 `python scripts/setup-skills.py --index` 从 `skills/registry.json` 自动生成，请勿手工编辑。",
        "",
        f"共 {len(skills)} 个技能，{len(categories)} 个分类。",
        "",
    ]

    for cat_key, cat_desc in categories.items():
        cat_skills = [s for s in skills if s["category"] == cat_key]
        if not cat_skills:
            continue
        lines.append(f"## {cat_key} · {cat_desc}")
        lines.append("")
        lines.append("| 技能 | 说明 | 仓库 |")
        lines.append("|------|------|------|")
        for s in sorted(cat_skills, key=lambda x: x["name"]):
            lines.append(f"| `{s['name']}` | {s['description']} | [{s['repo']}]({s['repo']}) |")
        lines.append("")

    index_path = SKILLS_DIR / "INDEX.md"
    index_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return index_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate skill.md templates and INDEX.md from registry.json")
    parser.add_argument("--index", action="store_true", help="Also regenerate skills/INDEX.md")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite skill.md even for skills with downloaded content")
    args = parser.parse_args()

    registry = load_registry()
    print(f"Loading registry: {REGISTRY_FILE.relative_to(PROJECT_ROOT)}")
    print(f"Found {len(registry['skills'])} skills\n")

    for skill in registry["skills"]:
        print(create_skill(skill, force=args.force))

    if args.index:
        index_path = generate_index(registry)
        print(f"\n[OK]   index -> {index_path.relative_to(PROJECT_ROOT)}")

    print("\nNote: Run 'python scripts/download-skill.py <skill-name>' to download full content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
