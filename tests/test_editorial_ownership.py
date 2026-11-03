"""Check editorial routing resources, sources and mirrors; not Russian wording."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_catalog import mirror_bytes

SKILLS = ROOT / "skills"
DIRECTOR = SKILLS / "architektonica-creative-director" / "SKILL.md"
PORTFOLIO = SKILLS / "architektonica-portfolio-case-writer" / "SKILL.md"
VOICE = ROOT / "methods/site-voice-and-consistency.md"
ROUTING = ROOT / "methods/engine-template-adaptation.md"

class EditorialOwnershipTests(unittest.TestCase):
    def test_single_main_author_and_case_handoff_link(self):
        route = ROUTING.read_text(encoding="utf-8")
        portfolio = PORTFOLIO.read_text(encoding="utf-8")
        self.assertIn("главный исполнитель", route)
        self.assertIn("Portfolio Case Writer", route)
        self.assertNotIn("copy-studio", route)
        # Portfolio author checks factual sources; word choice remains editorial.
        self.assertIn("02_Architektonica_Fact_Bank.md", portfolio)
        self.assertIn("03_Architektonica_Case_Studies.md", portfolio)

    def test_authors_resolve_canonical_voice(self):
        self.assertTrue(VOICE.is_file())
        for skill in (DIRECTOR, PORTFOLIO):
            with self.subTest(skill=skill.parent.name):
                reference = skill.parent / "../../methods/site-voice-and-consistency.md"
                self.assertTrue(reference.resolve().samefile(VOICE))
                self.assertIn("../../methods/site-voice-and-consistency.md",
                              skill.read_text(encoding="utf-8"))

    def test_editorial_skill_mirrors_use_generator(self):
        for skill in (DIRECTOR, PORTFOLIO):
            with self.subTest(skill=skill.parent.name):
                mirror = ROOT / ".agents" / skill.relative_to(ROOT)
                self.assertTrue(mirror.is_file())
                self.assertEqual(mirror.read_bytes(), mirror_bytes(skill, ROOT))

if __name__ == "__main__":
    unittest.main()