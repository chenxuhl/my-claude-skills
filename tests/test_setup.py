"""Tests for the skill.md template generator (scripts/setup-skills.py)."""

import json
import unittest
from pathlib import Path

from helpers import load_script, workspace_tmp

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = PROJECT_ROOT / "skills" / "registry.json"

setup_skills = load_script("setup_skills", "setup-skills.py")
download_skill = load_script("download_skill", "download-skill.py")


class TestTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with REGISTRY_FILE.open(encoding="utf-8") as f:
            cls.registry = json.load(f)
        cls.skill = cls.registry["skills"][0]

    def test_template_has_full_front_matter(self):
        content = setup_skills.skill_template(self.skill)
        for key in ("name", "title", "description", "category", "repoUrl"):
            self.assertIn(f"{key}: ", content, f"missing front matter key: {key}")
        self.assertTrue(content.startswith("---\n"))

    def test_template_contains_marker_shared_with_downloader(self):
        content = setup_skills.skill_template(self.skill)
        self.assertIn(setup_skills.TEMPLATE_MARKER, content)
        self.assertEqual(
            setup_skills.TEMPLATE_MARKER,
            download_skill.TEMPLATE_MARKER,
            "template marker must stay in sync between setup and download scripts",
        )

    def test_template_repo_url_is_repo_root(self):
        content = setup_skills.skill_template(self.skill)
        self.assertIn(self.skill["repo"], content)

    def test_has_full_content_detection(self):
        with workspace_tmp() as tmp:
            skill_dir = Path(tmp) / "demo"
            skill_dir.mkdir()
            self.assertFalse(setup_skills.has_full_content(skill_dir))
            (skill_dir / "references").mkdir()
            (skill_dir / "references" / "a.md").write_text("x", encoding="utf-8")
            self.assertTrue(setup_skills.has_full_content(skill_dir))

    def test_generate_index(self):
        with workspace_tmp() as tmp:
            old_skills_dir = setup_skills.SKILLS_DIR
            setup_skills.SKILLS_DIR = Path(tmp)
            try:
                index_path = setup_skills.generate_index(self.registry)
                text = index_path.read_text(encoding="utf-8")
                for skill in self.registry["skills"]:
                    self.assertIn(f"`{skill['name']}`", text)
                self.assertIn("自动生成", text)
            finally:
                setup_skills.SKILLS_DIR = old_skills_dir


if __name__ == "__main__":
    unittest.main()
