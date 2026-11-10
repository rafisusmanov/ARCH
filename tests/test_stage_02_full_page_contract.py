"""Mechanical safeguards for Stage 02 editorial workflow and WEB write boundary.

These checks verify documented contracts, not the literary quality or motion of a page.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class Stage02FullPageContractTest(unittest.TestCase):
    def test_full_page_instead_of_card_only(self):
        guide = read("methods/stage-02-full-page-contract.md")
        self.assertIn("Read-only WEB-инвентаризация", guide)
        self.assertIn("Полная содержательная композиция", guide)
        self.assertIn("Шесть обзорных карточек Engine", guide)
        self.assertIn("не менять публикационный текст в Creative и никакие файлы WEB", guide)
        self.assertIn("контракт целой страницы", read("methods/agent-expert-stage-protocol.md"))

    def test_reference_design_is_retain_and_refine(self):
        guide = read("methods/web-reference-style-and-depth.md")
        self.assertIn("77 JPG", guide)
        self.assertIn("5 MP4", guide)
        self.assertIn("воспроизведение, реальные траектории, тайминги и звук не проверены", guide)
        self.assertIn("дорабатывать", guide)
        self.assertIn("Z0 / Дальний план", guide)
        self.assertIn("На каждый внешний материал проверять права", guide)
        self.assertIn("WEB/reference", read("AGENTS.md"))

    def test_only_is_text_and_ux_reference(self):
        guide = read("methods/text-reference-only-digital.md")
        self.assertIn("обязательный разбор целой страницы и UX", guide)
        self.assertIn("не копировать тексты", guide)
        self.assertIn("UX", read("PROJECT_SYSTEM_PROMPT.md"))
        self.assertNotIn("Референс относится к **текстам, не структуре сайта**", read("PROJECT_SYSTEM_PROMPT.md"))

    def test_deleted_copy_studio_stays_deleted_and_baseline_intact(self):
        self.assertFalse((ROOT / "skills/copy-studio").exists())
        self.assertFalse((ROOT / ".agents/skills/copy-studio").exists())
        self.assertIn("Copy Studio не существует как актуальный навык", read("AGENTS.md"))
        self.assertIn("classification_review_pending", read("planning/stage-02/service-taxonomy-review.md"))
        self.assertIn("81 услугу", read("references/project/ARCHITEKTONICA_SITE_PLAN_V2.md"))
        self.assertIn("77 JPG", read("methods/web-reference-style-and-depth.md"))


if __name__ == "__main__":
    unittest.main()
