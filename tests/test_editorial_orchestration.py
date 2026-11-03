"""Editorial ownership is an approved working rule, not a literal-phrase CI gate.

Text quality and role decisions require actual editorial review, not keyword counting.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ROUTE = ROOT / "methods/engine-template-adaptation.md"

class EditorialRoutingTests(unittest.TestCase):
    def test_role_map_references_real_available_skills(self):
        body = ROUTE.read_text(encoding="utf-8")
        mentioned = re.findall(r"^\|\s*`([a-z][a-z0-9-]+)`\s*\|", body, re.M)
        mentioned += re.findall(
            r"<tr\b[^>]*>\s*<td\b[^>]*>\s*`([a-z][a-z0-9-]+)`\s*</td>",
            body, re.I)
        self.assertTrue(mentioned, "Expected a skill routing table")
        for name in mentioned:
            with self.subTest(name=name):
                self.assertTrue((SKILLS / name / "SKILL.md").is_file())

    def test_deleted_copy_studio_does_not_return(self):
        body = ROUTE.read_text(encoding="utf-8")
        self.assertNotIn("copy-studio", body)

    def test_main_author_and_case_role_exist(self):
        for name in ("architektonica-creative-director", "architektonica-portfolio-case-writer"):
            with self.subTest(name=name):
                self.assertTrue((SKILLS / name / "SKILL.md").is_file())

if __name__ == "__main__":
    unittest.main()
