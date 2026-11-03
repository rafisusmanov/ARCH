"""Static guards for editorial craft instructions. Not a literary quality scorer."""

from pathlib import Path
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
