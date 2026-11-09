"""Static regression checks for the five resolved motion-skill instruction conflicts.

These checks validate written contracts and mirror integrity, not runtime FPS.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class MotionSkillConsistencyTests(unittest.TestCase):
    def test_source_skills_have_identical_rebased_mirrors(self):
        for name in ("animate", "animation-performance", "review-animations", "improve-animations"):
            with self.subTest(skill=name):
                main = read(f"skills/{name}/SKILL.md")
                mirror = read(f".agents/skills/{name}/SKILL.md")
                self.assertEqual(main.replace("../../", "../../../"), mirror)

    def test_property_exceptions_not_banned_globally(self):
        for path, expected in (
            ("skills/animate/SKILL.md", "by default, not exclusively"),
            ("skills/review-animations/SKILL.md", "Property cost with justified exceptions"),
            ("skills/animation-performance/SKILL.md", "Conditional/compositor-or-paint"),
            ("skills/animate/RECIPES.md", "intentional exceptions"),
            ("skills/review-animations/STANDARDS.md", "not as an absolute rule"),
            ("skills/improve-animations/AUDIT.md", "Necessary layout animation"),
        ):
            with self.subTest(path=path):
                self.assertIn(expected, read(path))

    def test_acceleration_is_conditional_not_guaranteed(self):
        for path, evidence in (
            ("skills/animate/SKILL.md", "not guaranteed GPU execution"),
            ("skills/animation-performance/SKILL.md", "not a hardware-acceleration guarantee"),
            ("skills/review-animations/SKILL.md", "do not claim guaranteed GPU acceleration"),
            ("skills/animate/RECIPES.md", "hardware acceleration is conditional"),
            ("skills/review-animations/STANDARDS.md", "not automatically hardware-accelerated"),
        ):
            with self.subTest(path=path):
                self.assertIn(evidence.lower(), read(path).lower())

    def test_css_waapi_and_main_thread_are_separated(self):
        for path in ("skills/animate/SKILL.md",
                     "skills/animation-performance/SKILL.md",
                     "skills/review-animations/STANDARDS.md"):
            with self.subTest(path=path):
                text = read(path)
                self.assertIn("WAAPI", text)
                self.assertIn("main thread", text)
                self.assertIn("compositor", text)

    def test_motion_independent_transforms_are_not_blanket_banned(self):
        for path in ("skills/animate/SKILL.md",
                     "skills/animation-performance/SKILL.md",
                     "skills/review-animations/SKILL.md",
                     "skills/review-animations/STANDARDS.md",
                     "skills/improve-animations/AUDIT.md"):
            with self.subTest(path=path):
                text = read(path).lower()
                self.assertIn("motion", text)
                self.assertNotIn("shorthands are not hardware-accelerated", text)
                self.assertNotIn("shorthands are not hardware accelerated", text)

    def test_audit_cannot_automatically_execute_or_activate_review(self):
        audit = read("skills/improve-animations/SKILL.md")
        integration = read("methods/engine-template-adaptation.md")
        review = read("skills/review-animations/SKILL.md")
        self.assertIn("Not supported in this audit skill", audit)
        self.assertIn("no source edits", audit.lower())
        self.assertIn("explicit-only", integration)
        self.assertIn("disable-model-invocation: true", review)
        self.assertIn("его `execute <plan>` отключён", integration)


if __name__ == "__main__":
    unittest.main()
