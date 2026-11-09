"""Static guards for editorial craft instructions. Not a literary quality scorer."""

from pathlib import Path
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class EditorialCraftContractTests(unittest.TestCase):
    def test_editorial_quality_adds_clarity_and_section_necessity(self):
        content = read("methods/editorial-quality.md")
        for fragment in (
            "## Финальная смысловая и языковая вычитка",
            "**Фраза должна читаться с первого раза.**",
            "**Проверка заголовков отдельно от абзацев.**",
            "**Право не создавать раздел.**",
            "Не устанавливать квоты слов",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, content)

    def test_author_and_seo_roles_reject_template_padding(self):
        mapping = {
            "skills/architektonica-idea-lab/SKILL.md": (
                "## От мысли к предметному заголовку",
                "Не заполнять страницу дополнительными мини-идеями",
            ),
            "skills/architektonica-narrative-design/SKILL.md": (
                "## Раздел появляется ради вопроса читателя",
                "Не создавать обязательный",
            ),
            "skills/architektonica-critical-editor/SKILL.md": (
                "## Редактура предложения, заголовка и необязательного блока",
                "**Необязательные секции.**",
            ),
            "skills/architektonica-search-visibility/SKILL.md": (
                "## SEO без пустого объёма",
                "Не добавляй FAQ",
            ),
        }
        for path, fragments in mapping.items():
            with self.subTest(path=path):
                text = read(path)
                for fragment in fragments:
                    self.assertIn(fragment, text)

    def test_publication_copy_is_separate_from_editor_notes(self):
        for path, fragment in (
            ("methods/copy-workflow.md", "одна цельная версия публикационного текста"),
            ("methods/site-voice-and-consistency.md", "## Разделение публикационного и служебного текста"),
            ("AGENTS.md", "не вставлять перечень навыков и служебную самооценку"),
        ):
            with self.subTest(path=path):
                self.assertIn(fragment, read(path))

    def test_approved_homepage_remains_the_voice_reference(self):
        home = read("planning/stage-02/home-page.md")
        self.assertIn("# Комплексные решения для развития компаний", home)
        self.assertTrue(home.startswith("ARCHITEKTONICA – Архитектура решений."))
        self.assertNotIn("\u2014", home)
        self.assertGreater(len(home), 4000)
        # Snapshot of the owner-approved copy, not a model quality metric.
        # Updated after owner's 09.11.2026 approval of the /research main-navigation addition; all other copy remains unchanged.
        raw = home.encode("utf-8")
        git_blob_sha = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        self.assertEqual(git_blob_sha, "7af1bbda754e2a66e466765bba72c5e0ae5b2dfd")
        for rel in (
            "AGENTS.md",
            "PROJECT_SYSTEM_PROMPT.md",
            "methods/editorial-source-boundaries.md",
            "methods/copy-workflow.md",
            "methods/editorial-quality.md",
            "methods/site-voice-and-consistency.md",
            "QUICK_START.md",
            "prompts/ONE_LINE_TASKS.md",
            "prompts/PERPLEXITY_SPACE.md",
            "README.md",
        ):
            with self.subTest(path=rel):
                self.assertIn("planning/stage-02/home-page.md" if not rel.startswith(("methods/", "prompts/")) else "../planning/stage-02/home-page.md", read(rel))
        work_map = read("planning/stage-02/WORK_MAP.md")
        self.assertIn("owner_approved", work_map)

    def test_editorial_rules_do_not_restore_preapproval_drafts_or_conflict(self):
        agents = read("AGENTS.md")
        workflow = read("methods/copy-workflow.md")
        contract = read("methods/editorial-source-boundaries.md")
        voice = read("methods/site-voice-and-consistency.md")
        self.assertIn("одну лучшую цельную редакцию", agents)
        self.assertIn("Единственная каноническая последовательность", workflow)
        self.assertIn("Итоговая сверка голоса и Only", contract)
        self.assertIn("Утверждены главная и «О компании» от 09.11.2026", voice)
        self.assertNotIn("После сброса Stage 02 прежних действующих текстов нет", voice)
        self.assertNotIn("**Новая главная:**", read("QUICK_START.md"))
        for rel in (
            "PROJECT_SYSTEM_PROMPT.md",
            "methods/copy-workflow.md",
            "methods/editorial-source-boundaries.md",
            "methods/editorial-quality.md",
            "skills/architektonica-creative-director/SKILL.md",
            "skills/architektonica-idea-lab/SKILL.md",
            "skills/architektonica-narrative-design/SKILL.md",
            "skills/architektonica-critical-editor/SKILL.md",
        ):
            with self.subTest(path=rel):
                self.assertNotIn(r"\n\n", read(rel))

    def test_skill_mirrors_match_rebased_source(self):
        for name in (
            "architektonica-idea-lab",
            "architektonica-narrative-design",
            "architektonica-critical-editor",
            "architektonica-search-visibility",
        ):
            with self.subTest(name=name):
                source = read(f"skills/{name}/SKILL.md")
                mirror = read(f".agents/skills/{name}/SKILL.md")
                self.assertEqual(source.replace("../../", "../../../"), mirror)


if __name__ == "__main__":
    unittest.main()
