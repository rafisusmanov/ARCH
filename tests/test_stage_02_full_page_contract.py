"""Mechanical safeguards for Stage 02 editorial workflow and WEB write boundary.

These checks verify documented contracts, not the literary quality or motion of a page.
"""
from pathlib import Path
import hashlib
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

    def test_legacy_catalogue_is_history_not_public_source(self):
        manifest = json.loads(read("planning/stage-01/catalogue-map.json"))
        source = json.loads(read("references/project/services_catalogue.json"))["services"]
        self.assertEqual(81, len(manifest["services"]))
        self.assertEqual(81, len(source))
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        self.assertNotIn("review", public["source"])
        self.assertNotIn("proposals", public["source"])
        self.assertEqual(
            "planning/stage-02/contact-page.md",
            public["source"]["current_decision"],
        )
        self.assertIn("взаимодействий", read("methods/text-reference-only-digital.md"))
        self.assertIn("дизайн, композицию и пространство", read("AGENTS.md"))

    def test_approved_public_taxonomy_preserves_legacy_ids_and_page_gate(self):
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        manifest = json.loads(read("planning/stage-01/catalogue-map.json"))
        self.assertEqual("owner_approved_taxonomy", public["approval"]["status"])
        self.assertFalse(public["approval"]["web_write_authorized"])
        self.assertEqual((6, 17, 84, 81),
            (len(public["groups"]), len(public["directions"]),
             len(public["services"]), len(public["legacy_id_map"])))
        ids = {s["id"] for s in public["services"]}
        legacy = {s["id"]: s for s in public["legacy_id_map"]}
        self.assertEqual(len(ids), 84)
        self.assertEqual(set(legacy), {s["id"] for s in manifest["services"]})
        self.assertEqual(ids, (set(legacy) -
            {"svc-007", "svc-008", "svc-048", "svc-049", "svc-050", "svc-063", "svc-067", "svc-068"}) |
            {f"svc-{i:03d}" for i in range(82, 93)})
        self.assertEqual({d["id"] for d in public["directions"]},
                         {d["id"] for d in manifest["directions"]})
        self.assertEqual(84, sum(d["count"] for d in public["directions"]))
        self.assertEqual(4, next(d["count"] for d in public["directions"] if d["id"] == "dir-13"))
        self.assertEqual(
            "Прикладные AI-системы и инженерные решения",
            next(d["name"] for d in public["directions"] if d["id"] == "dir-10"))
        self.assertEqual("retired_by_owner", legacy["svc-007"]["role"])
        self.assertIsNone(legacy["svc-007"]["public_service_id"])
        for retired in ("svc-063", "svc-067", "svc-068"):
            self.assertEqual("retired_by_owner", legacy[retired]["role"])
            self.assertIsNone(legacy[retired]["public_service_id"])
        self.assertEqual("svc-006", legacy["svc-008"]["public_service_id"])
        self.assertEqual("merged_alias", legacy["svc-008"]["role"])
        for old in ("svc-048", "svc-049", "svc-050"):
            self.assertEqual("case_reference_only", legacy[old]["role"])
            self.assertIsNone(legacy[old]["public_service_id"])
        self.assertTrue(all(not v["redirect_implemented"] for v in legacy.values()))
        self.assertTrue(all(s["publication_status"] == "copy_not_approved"
                            for s in public["services"]))
        self.assertEqual("overview_copy_owner_approved_detail_copy_not_approved",
                         public["publication_gate"]["status"])
        self.assertEqual(11, public["counts"]["new_service_ids"])
        self.assertEqual(4, public["counts"]["retired_by_owner"])
        self.assertEqual(2, public["counts"]["explicit_scope_groups"])
        self.assertEqual({r["direction_id"] for r in public["direction_capabilities"]},
                         {"dir-05", "dir-10"})
        self.assertTrue(all(len(r["items"]) >= 5 for r in public["direction_capabilities"]))
        self.assertEqual([f"svc-{i:03d}" for i in range(82, 93)],
                         sorted(x["id"] for x in public["services"] if int(x["id"][4:]) >= 82))
        self.assertIn("6/17/87", read("planning/stage-02/catalogue-extension-decision-2026-11-10.md"))

        self.assertIn("svc-008",
            next(s["merged_legacy_ids"] for s in public["services"]
                 if s["id"] == "svc-006"))

    def test_owner_approved_pages_2026_11_12_and_no_repeated_evidence_interrogation(self):
        home = read("planning/stage-02/home-page.md")
        about = read("planning/stage-02/about-page.md")
        work = read("planning/stage-02/WORK_MAP.md")
        self.assertIn("# Создаём цифровые продукты, бренды и решения для бизнеса", home)
        self.assertIn("Посмотреть все 6 направлений и 84 услуги", home)
        self.assertNotIn("Полный каталог включает 81 услугу", home)
        self.assertIn("**Верхняя навигация**", home)
        self.assertIn("# Команда и принципы работы ARCHITEKTONICA", about)
        for name in ("Рафис Усманов", "Ильмир Гайбадуллин", "Зульфия Усманова", "Люция Жукова"):
            self.assertIn(name, about)
        self.assertEqual(work.count("**active_task:**"), 1)
        self.assertIn("**`owner_approved` 12.11.2026**", work)
        for path in (
            "AGENTS.md",
            "methods/editorial-source-boundaries.md",
            "methods/editorial-quality.md",
            "methods/site-voice-and-consistency.md",
            "skills/architektonica-critical-editor/SKILL.md",
            "skills/architektonica-creative-director/SKILL.md",
        ):
            self.assertIn("не допрашивать о доказательности повторно", read(path), path)

    def test_services_overview_approved_but_service_details_not_approved(self):
        page = read("planning/stage-02/services-page.md")
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        work = read("planning/stage-02/WORK_MAP.md")
        self.assertIn("# Услуги для цифровых продуктов, брендов и бизнеса", page)
        self.assertIn("**Обсудить проект**", page)
        self.assertIn("owner_approved 12.11.2026", page)
        self.assertIn("Спецификация UX (служебное приложение", page)
        self.assertEqual(6, len(public["groups"]))
        self.assertEqual(17, len(public["directions"]))
        self.assertEqual(84, len(public["services"]))
        self.assertEqual(
            "overview_copy_owner_approved_detail_copy_not_approved",
            public["publication_gate"]["status"])
        self.assertTrue(all(s["publication_status"] == "copy_not_approved"
                            for s in public["services"]))
        self.assertIn("**`owner_approved` 12.11.2026", work)
        self.assertEqual(1, work.count("**active_task:**"))

    def test_single_active_task_and_clean_sources(self):
        work = read("planning/stage-02/WORK_MAP.md")
        agents = read("AGENTS.md")
        ia = read("planning/stage-01/IA_PROPOSAL.md")
        urls = read("planning/stage-01/JOURNEYS_AND_URLS.md")
        seo = read("planning/stage-01/SEO_NAMING_POLICY.md")
        self.assertEqual(work.count("**active_task:**"), 1)
        self.assertIn("**active_task:** `ARCH-STAGE02-SALES-AND-CX`", work)
        self.assertNotIn("ARCH-CLEANUP-2026-11-10", work)
        self.assertIn("Единственная активная задача", work)
        self.assertIn("overview_copy_owner_approved_detail_copy_not_approved", json.loads(read(
            "planning/stage-02/public-service-catalogue.json"))["publication_gate"]["status"])
        self.assertIn("одна активная задача", agents.lower())
        self.assertIn("84 публичных услуг", ia)
        self.assertIn("84 публичных услуг", urls)
        self.assertIn("84 публичных услуг", seo)
        self.assertIn("public-service-catalogue.json", ia)
        self.assertIn("public-service-catalogue.json", urls)
        self.assertNotIn("SEO и мультиязычное продвижение", seo)
        for rel in (
            "planning/agent-guardrail-evaluation-20261102.md",
            "planning/editorial-system-audit-20261103.md",
            "planning/stage-02/repository-audit-2026-11-09.md",
            "methods/source-audit-and-portfolio-rules.md",
            "references/project/08_Architektonica_Site_Content_Plan.md",
            "planning/stage-02/service-taxonomy-proposal.json",
            "planning/stage-02/service-taxonomy-review.md",
        ):
            self.assertFalse((ROOT / rel).exists(), rel)

    def test_brand_and_communications_approved_page_covers_catalogue(self):
        page = read("planning/stage-02/brand-and-communications-page.md")
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        services = [s for s in public["services"]
                    if s["group_id"] == "brand-and-communications"]
        self.assertEqual(15, len(services))
        self.assertIn("`owner_approved` 20.11.2026", page)
        for service in services:
            title = service["display_title"]
            self.assertIn(f"{title}\n\n{service['plain_summary']}\n\n", page)
            self.assertIn(f"| {service['direction_id']} | {service['id']} | {title} |", page)
        self.assertEqual(9, page.count("**Показатели оценки:**"))
        for section in ("Анатомия бренда", "Бренд в разных средах",
                        "Где аудитория встречается с брендом",
                        "Как развивается информационный повод", "Арктическая Венеция"):
            self.assertIn(section, page)

    def test_immersive_media_approved_page_covers_catalogue(self):
        page = read("planning/stage-02/immersive-media-page.md")
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        services = [s for s in public["services"] if s["group_id"] == "immersive-media"]
        self.assertEqual(16, len(services))
        self.assertIn("`owner_approved` 20.11.2026", page)
        for service in services:
            title = service["display_title"]
            self.assertIn(f"{title}\n\n{service['plain_summary']}\n\n", page)
            self.assertIn(f"| {service['direction_id']} | {service['id']} | {title} |", page)
        for section in ("От зрителя к участнику", "Два способа изменить восприятие пространства",
                        "Из чего складывается цифровой кадр", "A Life Extraordinary",
                        "У пространства есть свой звук"):
            self.assertIn(section, page)

    def test_ai_and_infrastructure_approved_page_covers_catalogue(self):
        page = read("planning/stage-02/ai-and-infrastructure-page.md")
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        services = [s for s in public["services"] if s["group_id"] == "ai-and-infrastructure"]
        self.assertEqual(18, len(services))
        self.assertIn("`owner_approved` 20.11.2026", page)
        for service in services:
            title = service["display_title"]
            self.assertIn(f"{title}\n\n{service['plain_summary']}\n\n", page)
            self.assertIn(f"| {service['direction_id']} | {service['id']} | {title} |", page)
        for section in ("Контур цифровой инфраструктуры", "От гипотезы к работающему решению",
                        "Как проверяется искусственный интеллект до внедрения", "5–6 месяцев",
                        "Работающая система", "Архитектура решения"):
            self.assertIn(section, page)

    def test_sales_and_cx_approved_page_covers_catalogue(self):
        page = read("planning/stage-02/sales-and-cx-page.md")
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        services = [s for s in public["services"] if s["group_id"] == "sales-and-cx"]
        self.assertEqual(7, len(services))
        self.assertIn("`owner_approved` 20.11.2026", page)
        for service in services:
            title = service["display_title"]
            self.assertIn(f"{title}\n\n{service['plain_summary']}\n\n", page)
            self.assertIn(f"| {service['direction_id']} | {service['id']} | {title} |", page)
        for section in ("Управляем всем путём клиента", "ДЕМОНСТРАЦИЯ КЛИЕНТСКОГО СЦЕНАРИЯ",
                        "Воронка продаж", "Коммерческая система в цифрах", "ПРИМЕР ОБРАБОТКИ ОБРАЩЕНИЯ",
                        "Зульфия Усманова", "19+"):
            self.assertIn(section, page)

    def test_client_os_owner_approved_revision_04_is_preserved(self):
        page = read("planning/stage-02/client-workspace-page.md")
        work = read("planning/stage-02/WORK_MAP.md")
        decision = read("references/project/OWNER_DECISION_2026-11-18_CONTACT_CLIENT_OS.md")
        copy = page.split("## Утверждённый публикационный текст\n\n", 1)[1].split("\n\n---\n", 1)[0]
        self.assertEqual(hashlib.sha256(copy.encode("utf-8")).hexdigest(),
                         "f6cc80f021213d0e08cad1f4f06fc144aa14d3a305786ced9cccacdeb1de14bb")
        self.assertEqual(copy.count("## Безопасность и конфиденциальность"), 1)
        self.assertTrue(copy.endswith("**Обсудить проект** · **Посмотреть услуги**"))
        self.assertIn("**`owner_approved` 19.11.2026**", work)
        self.assertIn("активируется только клиентский доступ, а не сама Client OS", decision)

    def test_approved_direction_disclosure_keeps_group_and_direction_distinct(self):
        flow = read("planning/stage-02/services-direction-flow.md")
        work = read("planning/stage-02/WORK_MAP.md")
        public = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        direction = next(d for d in public["directions"] if d["id"] == "dir-04")
        self.assertEqual(direction["count"], 11)
        self.assertEqual(sum(s["direction_id"] == "dir-04" for s in public["services"]), 11)
        self.assertEqual(sum(s["group_id"] == direction["group_id"] for s in public["services"]), 13)
        group = next(g for g in public["groups"] if g["id"] == "digital-products")
        self.assertIn(group["proposed_url"], flow)
        self.assertEqual(direction["proposed_url"], group["proposed_url"] + "#dir-04")
        self.assertEqual(public["architecture"]["total_service_pages"], 7)
        self.assertEqual(len({g["proposed_url"] for g in public["groups"]}), 6)
        self.assertTrue(all(not s["detail_page_candidate"] and s["proposed_surface"] == "group_section"
                            for s in public["services"]))
        self.assertIn("structure_approved", flow)
        self.assertIn("Дословный текст страницы направления утверждается отдельно", flow)
        self.assertIn("services-direction-flow.md", work)

    def test_current_guidance_uses_public_canon_and_cancelled_route(self):
        current_docs = (
            "README.md",
            "planning/stage-02/WORK_MAP.md",
            "planning/stage-02/client-workspace-publication-gate.md",
            "planning/stage-02/research-page.md",
            "methods/engine-field-guide.md",
            "methods/research-evidence-map.md",
            "methods/text-reference-only-digital.md",
            "skills/architektonica-search-visibility/references/site-structure-linking.md",
            "skills/architektonica-ui-ux-expert/references/content-model.md",
        )
        for rel in current_docs:
            with self.subTest(path=rel):
                text = read(rel)
                self.assertNotIn("17 направлений / 81 услугу", text)
                self.assertNotIn("17 направлений / 81 услуга", text)
                self.assertNotIn("блок на `/process`", text)
                self.assertNotIn("ARCH-CLEANUP-2026-11-10", text)
        work = read("planning/stage-02/WORK_MAP.md")
        self.assertIn("`08_Site_Content_Plan` и `09_Engine_Home_Copy` удалены", work)
        self.assertNotIn("08_Site_Content_Plan` сохранён", work)
        self.assertIn("84 публичных услуг", read(
            "skills/architektonica-search-visibility/references/site-structure-linking.md"))
        self.assertIn("svc-008`: одна публичная услуга", read(
            "skills/architektonica-search-visibility/references/site-structure-linking.md"))

    def test_contact_concept_and_client_access_gate(self):
        contact = read("planning/stage-02/contact-page.md")
        decision = read("references/project/OWNER_DECISION_2026-11-18_CONTACT_CLIENT_OS.md")
        work = read("planning/stage-02/WORK_MAP.md")
        self.assertIn("brief_prototype_owner_approved", contact)
        self.assertIn("# Обсудить проект", contact)
        self.assertIn("# Какая задача вас интересует?", contact)
        self.assertIn("https://only.digital/contacts", contact)
        self.assertIn("https://eolabs.ru/en/contact/", contact)
        self.assertIn("Скачиваемый бриф не нужен", contact)
        self.assertIn("Telegram, MAX и корпоративный email", contact)
        self.assertIn("84 индивидуальных мини-брифа", contact)
        self.assertIn("Вопрос о предполагаемом/ориентировочном бюджете проекта исключён полностью", contact)
        self.assertIn("PR #24 слит", work)
        self.assertIn("Доступ к личному кабинету исключительно после подписания договора и поступления предусмотренной договором оплаты", decision)
        self.assertIn("Оба условия обязательны", decision)
        self.assertIn("нет клиентского аккаунта, приглашения, регистрации или доступа к кабинету", decision)
        self.assertIn("не запрашивать повторное подтверждение", decision.lower())
        self.assertIn("Обсудить проект", read("planning/stage-01/IA_PROPOSAL.md"))

    def test_deleted_copy_studio_stays_deleted_and_baseline_intact(self):
        self.assertFalse((ROOT / "skills/copy-studio").exists())
        self.assertFalse((ROOT / ".agents/skills/copy-studio").exists())
        self.assertIn("Copy Studio не существует как актуальный навык", read("AGENTS.md"))
        self.assertIn("6/17/87", read("planning/stage-02/catalogue-extension-decision-2026-11-10.md"))
        self.assertIn("81 услугу", read("references/project/ARCHITEKTONICA_SITE_PLAN_V2.md"))
        self.assertIn("77 JPG", read("methods/web-reference-style-and-depth.md"))


if __name__ == "__main__":
    unittest.main()
