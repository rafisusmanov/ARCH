"""Regression guards for current documentation, not a semantic quality score."""
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class CurrentDocumentationTests(unittest.TestCase):
    def test_seo_uses_group_sections_and_current_catalogue(self):
        prefix = "skills/architektonica-search-visibility/references/"
        research = read(prefix + "keyword-serp-research.md")
        self.assertIn("planning/stage-02/public-service-catalogue.json", research)
        self.assertIn("proposed_page_type = group_section", research)
        self.assertIn("84 строки действующих идентификаторов", research)
        self.assertNotIn("detail_candidate", research)
        self.assertNotIn("approved_detail", research)
        self.assertNotIn("17/81", read(prefix + "page-publishing-audit.md"))
        self.assertIn("исторический ID", research)

    def test_public_names_and_navigation_match_owner_decisions(self):
        catalogue = json.loads(read("planning/stage-02/public-service-catalogue.json"))
        ia = read("planning/stage-01/IA_PROPOSAL.md")
        flow = read("planning/stage-02/services-direction-flow.md")
        home = read("planning/stage-02/home-page.md")
        for group in catalogue["groups"]:
            self.assertIn(group["display_title"], ia)
            self.assertIn(group["display_title"], flow)
            self.assertIn(group["display_title"], home)
        for category in catalogue["directions"]:
            self.assertIn(category["display_title"], ia)
        self.assertIn("Проекты · Услуги · Обсудить проект · Кабинет клиента", home)
        self.assertIn("Главное · Компания · Проекты · Услуги · Обсудить проект · Блог", home)
        self.assertNotIn("· Контакты ·", home)
        language = read("references/project/05_Architektonica_Language.md")
        self.assertIn("На первом уровне «искусственный интеллект»", language)
        self.assertNotIn("AI, не ИИ", language)
        self.assertNotIn("Кириллических «ИИ»", language)

    def test_approved_people_have_fact_bank_sources(self):
        about = read("planning/stage-02/about-page.md")
        bank = read("references/project/02_Architektonica_Fact_Bank.md")
        self.assertIn("| S8 |", bank)
        for name in ("Зульфия Усманова", "Люция Жукова"):
            public = about.split("### " + name + "\n", 1)[1].split("\n### ", 1)[0]
            facts = bank.split("### " + name, 1)[1].split("\n### ", 1)[0]
            self.assertIn("`CONFIRMED` Источник: S8", facts)
            for paragraph in public.strip().split("\n\n")[1:]:
                self.assertIn(paragraph, facts)

    def test_historical_catalogue_is_not_a_current_source(self):
        historical = read("references/project/04_Architektonica_Services.md")
        self.assertIn("Исторический источник, не действующий каталог", historical)
        self.assertIn("6 основных направлений / 17 внутренних категорий / 84 услуги", historical)
        self.assertIn("не действующий состав и не текущие статусы", read(
            "planning/stage-02/catalogue-extension-decision-2026-11-10.md"))
