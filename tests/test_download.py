"""Tests for the downloader (scripts/download-skill.py) — pure logic only, no network."""

import json
import unittest
from pathlib import Path

from helpers import load_script, workspace_tmp

download_skill = load_script("download_skill", "download-skill.py")
setup_skills = load_script("setup_skills", "setup-skills.py")


def sample_registry():
    return {
        "skills": [
            {"name": "alpha", "title": "A", "description": "d", "repo": "https://github.com/u/r1", "path": "skills/alpha", "category": "development"},
            {"name": "beta", "title": "B", "description": "d", "repo": "https://github.com/u/r1", "path": "skills/beta", "category": "development"},
            {"name": "gamma", "title": "G", "description": "d", "repo": "https://github.com/u/r2", "path": "", "category": "testing"},
        ]
    }


class TestGrouping(unittest.TestCase):
    def test_group_by_repo_clones_each_repo_once(self):
        groups = download_skill.group_by_repo(sample_registry())
        self.assertEqual(set(groups.keys()), {"https://github.com/u/r1", "https://github.com/u/r2"})
        self.assertEqual(len(groups["https://github.com/u/r1"]), 2)
        self.assertEqual(len(groups["https://github.com/u/r2"]), 1)


class TestTemplateDetection(unittest.TestCase):
    def test_template_only_detection(self):
        with workspace_tmp() as tmp:
            skill_dir = Path(tmp) / "s"
            skill_dir.mkdir()
            # No skill.md -> treated as template-only (needs download)
            self.assertTrue(download_skill.is_template_only(skill_dir))
            # Template skill.md -> template-only
            (skill_dir / "skill.md").write_text(setup_skills.skill_template(sample_registry()["skills"][0]), encoding="utf-8")
            self.assertTrue(download_skill.is_template_only(skill_dir))
            # Real content -> not template-only
            (skill_dir / "skill.md").write_text("---\nname: alpha\n---\nreal content", encoding="utf-8")
            self.assertFalse(download_skill.is_template_only(skill_dir))


class TestCopyTree(unittest.TestCase):
    def test_copy_tree_excludes_git_and_cache(self):
        with workspace_tmp() as tmp:
            root = Path(tmp)
            src = root / "src"
            dst = root / "dst"
            (src / ".git").mkdir(parents=True)
            (src / ".git" / "HEAD").write_text("x", encoding="utf-8")
            (src / "__pycache__").mkdir()
            (src / "__pycache__" / "x.pyc").write_text("x", encoding="utf-8")
            (src / "skill.md").write_text("hello", encoding="utf-8")
            (src / "references").mkdir()
            (src / "references" / "r.md").write_text("r", encoding="utf-8")

            download_skill.copy_tree(src, dst)

            self.assertTrue((dst / "skill.md").exists())
            self.assertTrue((dst / "references" / "r.md").exists())
            self.assertFalse((dst / ".git").exists())
            self.assertFalse((dst / "__pycache__").exists())


class TestExtractSkill(unittest.TestCase):
    def test_extract_writes_source_json_and_content(self):
        with workspace_tmp() as tmp:
            root = Path(tmp)
            clone = root / "clone"
            (clone / "skills" / "alpha").mkdir(parents=True)
            (clone / "skills" / "alpha" / "skill.md").write_text("real", encoding="utf-8")
            (clone / "skills" / "alpha" / "references").mkdir()
            (clone / "skills" / "alpha" / "references" / "a.md").write_text("r", encoding="utf-8")

            old_skills_dir = download_skill.SKILLS_DIR
            download_skill.SKILLS_DIR = root / "skills_out"
            try:
                skill = sample_registry()["skills"][0]
                ok = download_skill.extract_skill(clone, skill, force=True)
                self.assertTrue(ok)

                out_dir = download_skill.SKILLS_DIR / "alpha"
                self.assertTrue((out_dir / "skill.md").exists())
                self.assertTrue((out_dir / "references" / "a.md").exists())

                source = json.loads((out_dir / "source.json").read_text(encoding="utf-8"))
                self.assertEqual(source["skill"], "alpha")
                self.assertEqual(source["repo"], "https://github.com/u/r1")
                self.assertIn("commit", source)
                self.assertIn("downloaded_at", source)
            finally:
                download_skill.SKILLS_DIR = old_skills_dir

    def test_download_unknown_skill_fails_fast(self):
        result = download_skill.download_skills(["does-not-exist"], force=False)
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
