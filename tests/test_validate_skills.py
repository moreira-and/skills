import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_skills.py"
VALID_DESCRIPTION = (
    "Checks skill metadata and local references for catalog contributors. "
    "Use when adding or reviewing an Agent Skill."
)


class ValidateSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.skills_dir = Path(self.temporary_directory.name) / "skills"
        self.skills_dir.mkdir()

    def add_skill(self, name="catalog-check", description=VALID_DESCRIPTION, body="Follow the review steps."):
        skill_dir = self.skills_dir / name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n{body}\n",
            encoding="utf-8",
        )
        return skill_dir

    def validate(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--skills-dir", str(self.skills_dir)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_accepts_valid_skill(self):
        self.add_skill()
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validated 1 skill(s).", result.stdout)

    def test_empty_catalog_is_valid_without_placeholder(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No skills found", result.stdout)

    def test_requires_valid_frontmatter_and_required_fields(self):
        skill = self.add_skill()
        (skill / "SKILL.md").write_text("# Instructions\n", encoding="utf-8")
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing YAML frontmatter", result.stderr)

    def test_rejects_mismatched_and_duplicate_names(self):
        self.add_skill(name="first-skill")
        self.add_skill(name="second-skill")
        for skill in (self.skills_dir / "first-skill", self.skills_dir / "second-skill"):
            file = skill / "SKILL.md"
            file.write_text(file.read_text(encoding="utf-8").replace(f"name: {skill.name}", "name: same-skill"), encoding="utf-8")
        result = self.validate()
        self.assertIn("must match directory", result.stderr)
        self.assertIn("duplicate skill name", result.stderr)

    def test_requires_description_activation_cue_and_length(self):
        self.add_skill(description="A generic skill.")
        result = self.validate()
        self.assertIn("at least 30 characters", result.stderr)
        self.assertIn("explicit phrase 'Use when'", result.stderr)

    def test_rejects_missing_local_reference(self):
        self.add_skill(body="Read [the guide](references/missing.md).")
        result = self.validate()
        self.assertIn("does not exist", result.stderr)

    def test_scripts_require_usage_and_dependency_documentation(self):
        skill = self.add_skill()
        scripts = skill / "scripts"
        scripts.mkdir()
        (scripts / "check.py").write_text("print('ok')\n", encoding="utf-8")
        result = self.validate()
        self.assertIn("scripts/README.md is required", result.stderr)
        (scripts / "README.md").write_text(
            "### scripts/check.py\n\nUsage: `python scripts/check.py`\n",
            encoding="utf-8",
        )
        result = self.validate()
        self.assertIn("needs a Dependencies: entry", result.stderr)


if __name__ == "__main__":
    unittest.main()
