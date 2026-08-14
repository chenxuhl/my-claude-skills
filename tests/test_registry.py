"""Registry integrity tests against the single source of truth."""

import json
import re
import unittest
from pathlib import Path

from helpers import load_script

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = PROJECT_ROOT / "skills" / "registry.json"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESCRIPTION_LEN = 300

validate_skills = load_script("validate_skills", "validate-skills.py")


class TestRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with REGISTRY_FILE.open(encoding="utf-8") as f:
            cls.registry = json.load(f)
        cls.skills = cls.registry["skills"]

    def test_registry_file_exists_and_is_valid_json(self):
        self.assertTrue(REGISTRY_FILE.exists())
        self.assertIsInstance(self.registry, dict)

    def test_has_version_and_skills(self):
        self.assertTrue(self.registry.get("version"))
        self.assertIsInstance(self.skills, list)
        self.assertGreaterEqual(len(self.skills), 20)

    def test_names_are_unique_and_valid(self):
        names = [s["name"] for s in self.skills]
        self.assertEqual(len(names), len(set(names)), "duplicate skill names")
        for name in names:
            self.assertRegex(name, NAME_RE, f"invalid name: {name}")

    def test_required_fields_present(self):
        for skill in self.skills:
            for field in ("name", "title", "description", "repo", "category"):
                self.assertTrue(str(skill.get(field, "")).strip(), f"{skill['name']}: missing '{field}'")

    def test_categories_are_declared(self):
        declared = set(self.registry.get("categories", {}))
        for skill in self.skills:
            self.assertIn(skill["category"], declared, f"{skill['name']}: unknown category")

    def test_description_length(self):
        for skill in self.skills:
            self.assertLessEqual(len(skill["description"]), MAX_DESCRIPTION_LEN, skill["name"])

    def test_registry_passes_validator(self):
        errors = validate_skills.validate_registry(self.registry)
        self.assertEqual(errors, [], f"registry errors: {errors}")

    def test_every_skill_has_english_summary(self):
        for skill in self.skills:
            self.assertTrue(str(skill.get("description_en", "")).strip(), f"{skill['name']}: missing description_en")


if __name__ == "__main__":
    unittest.main()
