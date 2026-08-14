#!/usr/bin/env python3
"""Manage the skills collection: list, download, status.

One registry (skills/registry.json), one script. That's it.

Usage:
    python scripts/skills.py list
    python scripts/skills.py status
    python scripts/skills.py download <name|all> [--force]
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
REGISTRY = SKILLS_DIR / "registry.json"
EXCLUDE_DIRS = {".git", ".github", "node_modules", "__pycache__"}


def load_registry():
    with REGISTRY.open(encoding="utf-8") as f:
        return json.load(f)


def has_full_content(skill_dir: Path) -> bool:
    """A skill has real content if it has non-empty references/ or scripts/."""
    for sub in ("references", "scripts"):
        d = skill_dir / sub
        if d.exists() and any(d.iterdir()):
            return True
    return False


def cmd_list(reg):
    for s in sorted(reg["skills"], key=lambda x: x["name"]):
        print(f"  {s['name']:32} [{s['category']}]  {s['repo']}")
    return 0


def cmd_status(reg):
    print(f"{len(reg['skills'])} skills, registry v{reg.get('version', '?')}\n")
    print(f"{'skill':32} {'status':9} category")
    print("-" * 55)
    for s in sorted(reg["skills"], key=lambda x: x["name"]):
        d = SKILLS_DIR / s["name"]
        if not (d / "skill.md").exists():
            status = "MISSING"
        elif has_full_content(d):
            status = "full"
        else:
            status = "template"
        print(f"{s['name']:32} {status:9} {s['category']}")
    return 0


def clone(repo_url, dest):
    r = subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, str(dest)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if r.returncode != 0:
        print(f"  ERROR cloning {repo_url}: {r.stderr.strip()}", file=sys.stderr)
        return None
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(dest),
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def copy_tree(src, dst):
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in EXCLUDE_DIRS:
            continue
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, ignore=shutil.ignore_patterns(*EXCLUDE_DIRS))
        else:
            shutil.copy2(item, target)


def cmd_download(reg, names, force):
    by_name = {s["name"]: s for s in reg["skills"]}
    if names is None:
        targets = list(by_name.values())
    else:
        bad = [n for n in names if n not in by_name]
        if bad:
            print(f"ERROR: unknown skill(s): {', '.join(bad)}", file=sys.stderr)
            return 1
        targets = [by_name[n] for n in names]

    if shutil.which("git") is None:
        print("ERROR: git not found on PATH", file=sys.stderr)
        return 1

    # group by repo: one clone per upstream repo
    by_repo = {}
    for s in targets:
        by_repo.setdefault(s["repo"], []).append(s)

    workdir = Path(tempfile.mkdtemp(prefix="skills-dl-"))
    ok = 0
    try:
        for repo_url, skills in by_repo.items():
            clone_dir = workdir / repo_url.replace("/", "_").replace(":", "_")
            sha = clone(repo_url, clone_dir)
            if sha is None:
                continue
            for s in skills:
                src = clone_dir / (s.get("path") or "").strip("/")
                if not src.exists():
                    print(f"  WARNING: path '{s.get('path')}' not found, using repo root")
                    src = clone_dir
                dst = SKILLS_DIR / s["name"]
                dst.mkdir(parents=True, exist_ok=True)
                if has_full_content(dst) and not force:
                    print(f"  [SKIP] {s['name']} (has content, use --force)")
                    continue
                copy_tree(src, dst)
                (dst / "source.json").write_text(json.dumps({
                    "skill": s["name"], "repo": repo_url,
                    "path": s.get("path", ""), "commit": sha,
                    "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(f"  [OK] {s['name']} ({sha[:7]})")
                ok += 1
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    print(f"\nDownloaded {ok}/{len(targets)}.")
    return 0 if ok == len(targets) else 1


def main():
    p = argparse.ArgumentParser(prog="skills", description="Manage the skills collection")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="List all skills")
    sub.add_parser("status", help="Per-skill status (template/full/missing)")
    d = sub.add_parser("download", help="Download full skill content")
    d.add_argument("skill", nargs="?", help="Skill name or 'all'")
    d.add_argument("-f", "--force", action="store_true")
    args = p.parse_args()

    reg = load_registry()
    if args.cmd == "list":
        return cmd_list(reg)
    if args.cmd == "status":
        return cmd_status(reg)
    if args.cmd == "download":
        if not args.skill:
            p.print_help()
            return 1
        names = None if args.skill == "all" else [args.skill]
        return cmd_download(reg, names, args.force)


if __name__ == "__main__":
    sys.exit(main())
