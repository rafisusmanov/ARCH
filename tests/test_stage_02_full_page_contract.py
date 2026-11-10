"""Mechanical safeguards for Stage 02 editorial workflow and WEB write boundary.

These checks verify documented contracts, not the literary quality or motion of a page.
"""
from pathlib import Path
import json
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
        self.assertIn("Дорабатывать дизайн", guide)
        self.assertIn("Z0 / Дальний план", guide)
        self.assertIn("На каждый внешний материал проверять права", guide)
        self.assertIn("WEB/reference", read("AGENTS.md"))

    def test_only_is_text_and_ux_reference(self):
        guide = read("methods/text-reference-only-digital.md")
        self.assertIn("обязательный разбор целой страницы и UX", guide)
        self.assertIn("Не копировать тексты", guide)
        self.assertIn("UX", read("PROJECT_SYSTEM_PROMPT.md"))
        self.assertNotIn("Референс относится к **текстам, не структуре сайта**", read("PROJECT_SYSTEM_PROMPT.md"))

    def test_services_taxonomy_audits_every_legacy_id_without_changing_source(self):
        proposal = json.loads(read("planning/stage-02/service-taxonomy-proposal.json"))
        source = json.loads(read("references/project/services_catalogue.json"))["services"]
        manifest = json.loads(read("planning/stage-01/catalogue-map.json"))["services"]
        self.assertEqual(81, len(proposal["services"]))
        self.assertEqual(81, len(source))
        self.assertEqual(81, len(manifest))
        self.assertEqual(
            [x["id"] for x in manifest],
            [x["id"] for x in proposal["services"]],
        )
        self.assertEqual(
            [x["name"] for x in source],
            [x["legacy_name"] for x in proposal["services"]],
        )
        self.assertEqual(
            {"retain": 27, "clarify": 50, "merge_candidate": 1, "case_candidate": 3},
            proposal["count_by_action"],
        )
        self.assertEqual(
            [f"svc-{i:03d}" for i in (48, 49, 50)],
            [x["id"] for x in proposal["services"] if x["action"] == "case_candidate"],
        )
        self.assertEqual(
            ["svc-008"],
            [x["id"] for x in proposal["services"] if x["action"] == "merge_candidate"],
        )
        self.assertEqual("proposal_unapproved", proposal["status"])
        self.assertIn("77", read("planning/stage-02/service-taxonomy-review.md"))
        self.assertIn("взаимодействий", read("methods/text-reference-only-digital.md"))
        self.assertIn("дизайн, композицию и пространство", read("AGENTS.md"))

    def test_deleted_copy_studio_stays_deleted_and_baseline_intact(self):
        self.assertFalse((ROOT / "skills/copy-studio").exists())
        self.assertFalse((ROOT / ".agents/skills/copy-studio").exists())
        self.assertIn("Copy Studio не существует как актуальный навык", read("AGENTS.md"))
        self.assertIn("audited_proposal_pending_owner_approval", read("planning/stage-02/service-taxonomy-review.md"))
        self.assertIn("81 услугу", read("references/project/ARCHITEKTONICA_SITE_PLAN_V2.md"))
        self.assertIn("77 JPG", read("methods/web-reference-style-and-depth.md"))


if __name__ == "__main__":
    unittest.main()
