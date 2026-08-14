#!/usr/bin/env python3
"""Download full skill content from official repositories.

Reads skill metadata from skills/registry.json (single source of truth),
clones each upstream repository once per run, extracts the requested skill
directories, and records provenance (commit SHA + timestamp) in source.json.

Usage:
    python scripts/download-skill.py <skill-name>   # download one skill
    python scripts/download-skill.py all            # download every skill
    python scripts/download-skill.py --list         # list available skills
    python scripts/download-skill.py <name> --force # overwrite existing content
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
REGISTRY_FILE = SKILLS_DIR / "registry.json"

# Must stay in sync with scripts/setup-skills.py
TEMPLATE_MARKER = "此技能的完整内容需要从官方仓库获取"

# Directories that must never be copied out of a clone.
EXCLUDE_DIRS = {".git", ".github", "node_modules", "__pycache__"}


def load_registry() -> dict:
    if not REGISTRY_FILE.exists():
        print(f"ERROR: Registry not found at {REGISTRY_FILE}", file=sys.stderr)
        sys.exit(1)
    with REGISTRY_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def check_git() -> bool:
    if shutil.which("git") is None:
        print("ERROR: 'git' not found on PATH. Git is required to download skills.", file=sys.stderr)
        return False
    return True


def group_by_repo(registry: dict) -> dict:
    """Group skills by upstream repository URL so each repo is cloned once."""
    groups: dict[str, list] = {}
    for skill in registry["skills"]:
        groups.setdefault(skill["repo"], []).append(skill)
    return groups


def run_git(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run a git command safely. Never raises — OSError maps to a 127 result."""
    try:
        return subprocess.run(
            ["git", *args],
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:  # git missing or blocked by the environment
        return subprocess.CompletedProcess(
            ["git", *args], 127, stdout="", stderr=f"cannot run git: {exc}"
        )


def clone_repo(repo_url: str, dest: Path) -> str | None:
    """Shallow-clone a repository into dest. Returns the HEAD commit SHA."""
    print(f"  Cloning {repo_url} ...")
    result = run_git(["clone", "--depth", "1", repo_url, str(dest)])
    if result.returncode != 0:
        print(f"  ERROR: clone failed: {result.stderr.strip()}", file=sys.stderr)
        return None
    sha_result = run_git(["rev-parse", "HEAD"], cwd=dest)
    if sha_result.returncode == 0:
        return sha_result.stdout.strip()
    return None


def is_template_only(skill_dir: Path) -> bool:
    """True if the skill directory contains only the setup-generated template."""
    md = skill_dir / "skill.md"
    if not md.exists():
        return True
    return TEMPLATE_MARKER in md.read_text(encoding="utf-8", errors="replace")


def copy_tree(src: Path, dst: Path) -> None:
    """Copy src tree into dst, excluding EXCLUDE_DIRS."""
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


def extract_skill(clone_dir: Path, skill: dict, force: bool) -> bool:
    """Copy one skill out of a fresh clone. Returns success."""
    name = skill["name"]
    skill_dir = SKILLS_DIR / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    repo_path = (skill.get("path") or "").strip().strip("/")
    source_dir = clone_dir / repo_path if repo_path else clone_dir
    if not source_dir.exists():
        print(f"  WARNING: path '{repo_path}' not found in repository, using repo root instead.")
        source_dir = clone_dir

    # Decide whether we may overwrite an existing skill.md.
    has_real_content = not is_template_only(skill_dir)
    if has_real_content and not force:
        response = input(f"  Skill '{name}' already has content. Overwrite? (y/N): ")
        if response.lower() != "y":
            print(f"  [SKIP] {name}")
            return False

    copy_tree(source_dir, skill_dir)

    # Keep our template metadata if upstream has no skill.md of its own.
    if not (source_dir / "skill.md").exists() and not (skill_dir / "skill.md").exists():
        print(f"  WARNING: upstream '{name}' has no skill.md; template retained.")

    # Record provenance.
    sha = None
    sha_result = run_git(["rev-parse", "HEAD"], cwd=clone_dir)
    if sha_result.returncode == 0:
        sha = sha_result.stdout.strip()
    source_info = {
        "skill": name,
        "repo": skill["repo"],
        "path": repo_path,
        "commit": sha,
        "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (skill_dir / "source.json").write_text(
        json.dumps(source_info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  [OK] {name} -> {skill_dir.relative_to(PROJECT_ROOT)} (commit {sha or 'unknown'})")
    return True


def download_skills(names: list[str] | None, force: bool) -> int:
    registry = load_registry()
    registry_skills = {s["name"]: s for s in registry["skills"]}

    if names is None:
        targets = list(registry_skills.values())
    else:
        unknown = [n for n in names if n not in registry_skills]
        if unknown:
            print(f"ERROR: unknown skill(s): {', '.join(unknown)}", file=sys.stderr)
            return 1
        targets = [registry_skills[n] for n in names]

    if not check_git():
        return 1

    groups = group_by_repo(registry)
    workdir = Path(tempfile.mkdtemp(prefix="claude-skills-dl-"))
    success = 0
    try:
        for repo_url, skills in groups.items():
            wanted = [s for s in skills if s["name"] in {t["name"] for t in targets}]
            if not wanted:
                continue
            clone_dir = workdir / f"repo-{groups[repo_url][0]['name']}"
            sha = clone_repo(repo_url, clone_dir)
            if sha is None:
                continue
            for skill in wanted:
                if extract_skill(clone_dir, skill, force):
                    success += 1
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    print(f"\nDownloaded {success}/{len(targets)} skills successfully.")
    return 0 if success == len(targets) else 1


def list_skills() -> int:
    registry = load_registry()
    for skill in sorted(registry["skills"], key=lambda s: s["name"]):
        print(f"  {skill['name']:32} [{skill['category']:12}] {skill['repo']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Download full skill content from official repositories")
    parser.add_argument("skill", nargs="?", help="Skill name to download, or 'all'")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite existing content")
    parser.add_argument("-l", "--list", action="store_true", help="List all available skills")
    args = parser.parse_args()

    if args.list:
        return list_skills()
    if not args.skill:
        parser.print_help()
        return 1
    if args.skill == "all":
        return download_skills(None, args.force)
    return download_skills([args.skill], args.force)


if __name__ == "__main__":
    sys.exit(main())
