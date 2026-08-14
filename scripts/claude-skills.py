#!/usr/bin/env python3
"""claude-skills — unified CLI for managing the Claude Code skills collection.

Usage:
    python scripts/claude-skills.py list                 # list available skills
    python scripts/claude-skills.py status               # per-skill install status
    python scripts/claude-skills.py setup [--force] [--index]
    python scripts/claude-skills.py index                # regenerate skills/INDEX.md
    python scripts/claude-skills.py validate [--strict]
    python scripts/claude-skills.py download <name|all> [--force]
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
REGISTRY_FILE = SKILLS_DIR / "registry.json"


def load_script(module_name: str, filename: str):
    """Load a sibling script module so we can reuse its main()/functions."""
    path = SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script(filename: str, argv: list[str]) -> int:
    """Run a sibling script with a substituted argv."""
    module = load_script(filename.replace(".py", "").replace("-", "_"), filename)
    old_argv = sys.argv
    sys.argv = ["claude-skills"] + argv
    try:
        return module.main()
    finally:
        sys.argv = old_argv


def load_registry() -> dict:
    with REGISTRY_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def cmd_status() -> int:
    registry = load_registry()
    skills = registry["skills"]
    print(f"Skills collection: {len(skills)} skills, registry v{registry.get('version', '?')}\n")
    print(f"{'skill':32} {'status':10} category")
    print("-" * 60)
    for skill in sorted(skills, key=lambda s: s["name"]):
        name = skill["name"]
        skill_dir = SKILLS_DIR / name
        md = skill_dir / "skill.md"
        if not md.exists():
            status = "MISSING"
        else:
            content = md.read_text(encoding="utf-8", errors="replace")
            has_refs = (skill_dir / "references").exists() and any((skill_dir / "references").iterdir())
            has_scripts = (skill_dir / "scripts").exists() and any((skill_dir / "scripts").iterdir())
            if has_refs or has_scripts:
                status = "FULL"
            elif "此技能的完整内容需要从官方仓库获取" in content:
                status = "template"
            else:
                status = "custom"
        print(f"{name:32} {status:10} {skill['category']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="claude-skills", description="Manage the Claude Code skills collection")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all available skills")
    sub.add_parser("status", help="Show per-skill status (template/full/missing)")

    p_setup = sub.add_parser("setup", help="Generate skill.md templates from registry.json")
    p_setup.add_argument("-f", "--force", action="store_true")
    p_setup.add_argument("--index", action="store_true")

    sub.add_parser("index", help="Regenerate skills/INDEX.md")

    p_validate = sub.add_parser("validate", help="Validate the collection against registry.json")
    p_validate.add_argument("--strict", action="store_true")

    p_download = sub.add_parser("download", help="Download full skill content")
    p_download.add_argument("skill", nargs="?", help="Skill name or 'all'")
    p_download.add_argument("-f", "--force", action="store_true")
    p_download.add_argument("-l", "--list", action="store_true")

    args = parser.parse_args()

    if args.command == "list":
        return run_script("download-skill.py", ["--list"])
    if args.command == "status":
        return cmd_status()
    if args.command == "setup":
        argv = ["setup"] + (["--force"] if args.force else []) + (["--index"] if args.index else [])
        return run_script("setup-skills.py", argv)
    if args.command == "index":
        return run_script("setup-skills.py", ["--index"])
    if args.command == "validate":
        argv = ["validate"] + (["--strict"] if args.strict else [])
        return run_script("validate-skills.py", argv)
    if args.command == "download":
        argv = ["download"]
        if args.list:
            argv.append("--list")
        elif args.skill:
            argv.append(args.skill)
        if args.force:
            argv.append("--force")
        return run_script("download-skill.py", argv)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
