"""Tests for the validator (scripts/validate-skills.py)."""

import json
import unittest
from pathlib import Path

from helpers import load_script, workspace_tmp

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = PROJECT_ROOT / "skills" / "registry.json"

validate_skills = load_script("validate_skills", "validate-skills.py")


class TestFrontMatter(unittest.TestCase):
    def test_parse_front_matter_basic(self):
        md = "---\nname: demo\ntitle: Demo Skill\ndescription: desc\ncategory: testing\n---\n# Body"
        fm = validate_skills.parse_front_matter(md)
        self.assertEqual(fm["name"], "demo")
        self.assertEqual(fm["category"], "testing")

    def test_parse_front_matter_missing(self):
        self.assertEqual(validate_skills.parse_front_matter("# no front matter"), {})


class TestRegistryValidation(unittest.TestCase):
    def setUp(self):
        with REGISTRY_FILE.open(encoding="utf-8") as f:
            self.registry = json.load(f)

    def test_real_registry_passes(self):
        self.assertEqual(validate_skills.validate_registry(self.registry), [])

    def test_duplicate_and_invalid_names_detected(self):
        bad = {
            "categories": {"development": "d"},
            "skills": [
                {"name": "dup", "title": "t", "description": "d", "repo": "https://x", "category": "development"},
                {"name": "dup", "title": "t", "description": "d", "repo": "https://x", "category": "development"},
                {"name": "Bad_Name!", "title": "t", "description": "d", "repo": "https://x", "category": "development"},
            ],
        }
        errors = validate_skills.validate_registry(bad)
        self.assertEqual(len(errors), 2)

    def test_missing_field_and_unknown_category_detected(self):
        bad = {
            "categories": {"development": "d"},
            "skills": [{"name": "ok", "title": "", "repo": "https://x", "category": "nope"}],
        }
        errors = validate_skills.validate_registry(bad)
        self.assertTrue(any("description" in e for e in errors))
        self.assertTrue(any("category" in e for e in errors))


class TestSkillDirs(unittest.TestCase):
    def test_missing_directories_reported(self):
        with workspace_tmp() as tmp:
            old_dir = validate_skills.SKILLS_DIR
            validate_skills.SKILLS_DIR = Path(tmp)
            try:
                registry = {"skills": [{"name": "ghost-skill"}]}
                errors = validate_skills.validate_skill_dirs(registry)
                self.assertTrue(any("ghost-skill" in e for e in errors))
            finally:
                validate_skills.SKILLS_DIR = old_dir


class TestReadmeSync(unittest.TestCase):
    def test_readme_rows_matched(self):
        with workspace_tmp() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "| 技能 | 作用 | 地址 |\n|---|---|---|\n| `alpha` | x | [link](https://x) |\n| `beta` | y | [link](https://y) |\n",
                encoding="utf-8",
            )
            old_files = validate_skills.README_FILES
            validate_skills.README_FILES = [readme]
            try:
                registry = {
                    "skills": [
                        {"name": "alpha"},
                        {"name": "beta"},
                        {"name": "gamma"},  # missing from table
                    ]
                }
                errors = validate_skills.validate_readme_tables(registry)
                self.assertTrue(any("gamma" in e for e in errors))
            finally:
                validate_skills.README_FILES = old_files


if __name__ == "__main__":
    unittest.main()
