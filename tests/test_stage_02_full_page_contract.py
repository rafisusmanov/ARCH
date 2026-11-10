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
        self.assertEqual("owner_approved_taxonomy_2026-11-10", proposal["status"])
        self.assertIn("77", read("planning/stage-02/service-taxonomy-review.md"))
        self.assertIn("взаимодействий", read("methods/text-reference-only-digital.md"))
        self.assertIn("дизайн, композицию и пространство", read("AGENTS.md"))

    def test_approved_public_taxonomy_preserves_legacy_ids_and_page_gate(self):
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        manifest = json.loads(read("planning/stage-01/catalogue-map.json"))
        self.assertEqual("owner_approved_taxonomy", public["approval"]["status"])
        self.assertFalse(public["approval"]["web_write_authorized"])
        self.assertEqual((6, 17, 77, 81),
            (len(public["groups"]), len(public["directions"]),
             len(public["services"]), len(public["legacy_id_map"])))
        ids = {s["id"] for s in public["services"]}
        legacy = {s["id"]: s for s in public["legacy_id_map"]}
        self.assertEqual(len(ids), 77)
        self.assertEqual(set(legacy), {s["id"] for s in manifest["services"]})
        self.assertEqual(ids, set(legacy) -
            {"svc-008", "svc-048", "svc-049", "svc-050"})
        self.assertEqual({d["id"] for d in public["directions"]},
                         {d["id"] for d in manifest["directions"]})
        self.assertEqual(77, sum(d["count"] for d in public["directions"]))
        self.assertEqual(
            "Прикладные AI-системы и инженерные решения",
            next(d["name"] for d in public["directions"] if d["id"] == "dir-10"))
        self.assertEqual("svc-006", legacy["svc-008"]["public_service_id"])
        self.assertEqual("merged_alias", legacy["svc-008"]["role"])
        for old in ("svc-048", "svc-049", "svc-050"):
            self.assertEqual("case_reference_only", legacy[old]["role"])
            self.assertIsNone(legacy[old]["public_service_id"])
        self.assertTrue(all(not v["redirect_implemented"] for v in legacy.values()))
        self.assertTrue(all(s["publication_status"] == "copy_not_approved"
                            for s in public["services"]))
        self.assertEqual("full_page_copy_not_approved",
                         public["publication_gate"]["status"])
        self.assertIn("svc-008",
            next(s["merged_legacy_ids"] for s in public["services"]
                 if s["id"] == "svc-006"))

    def test_deleted_copy_studio_stays_deleted_and_baseline_intact(self):
        self.assertFalse((ROOT / "skills/copy-studio").exists())
        self.assertFalse((ROOT / ".agents/skills/copy-studio").exists())
        self.assertIn("Copy Studio не существует как актуальный навык", read("AGENTS.md"))
        self.assertIn("owner_approved_taxonomy_2026-11-10", read("planning/stage-02/service-taxonomy-review.md"))
        self.assertIn("81 услугу", read("references/project/ARCHITEKTONICA_SITE_PLAN_V2.md"))
        self.assertIn("77 JPG", read("methods/web-reference-style-and-depth.md"))


if __name__ == "__main__":
    unittest.main()
