"""Narrow instruction regressions, not a literary-quality or agent-behavior scorer."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUTHOR_FILES = sorted((ROOT / 'skills').glob('architektonica-*/SKILL.md'))
BENCHMARK = ROOT / 'methods/text-reference-only-digital.md'
CONTRACT = ROOT / 'methods/editorial-source-boundaries.md'
RETIRED = (
    '06_Architektonica_Reference_Texts.md',
    '07_Architektonica_Copy_Registry.md',
    '08_Architektonica_Site_Content_Plan.md',
    '09_Engine_Home_Copy.md',
)
# Actual former directives. These guards intentionally cover known regressions,
# rather than claiming regex can decide whether every instruction is consistent.
LEGACY_RULES = {
    'skills/architektonica-creative-director/SKILL.md': (
        'Невозможно переставить имена клиентов',
        'она построена на реальных работах',
        '«Нас интересует, что происходит дальше» — существующая концептуальная гипотеза',
    ),
    'skills/architektonica-idea-lab/SKILL.md': (
        'смысловые ходы на основе реальных проектов',
        'одну сцепку с реальным проектом',
        'для каждого запиши тезис, мини-сцену',
    ),
    'skills/architektonica-search-visibility/SKILL.md': (
        'услуги — на конкретные работы',
        'У нефтяной платформы появились достопримечательности',
    ),
    'QUICK_START.md': ('Возьми только реальные проекты.',),
    'prompts/ONE_LINE_TASKS.md': ('покажи компанию через реальные работы',),
    'skills/architektonica-ui-ux-expert/SKILL.md': ('Сцены опираться на реальные кейсы.',),
    'methods/editorial-source-boundaries.md': ('полезна последовательность:',),
    'methods/engine-template-adaptation.md': ('портфолио.  у каждой публикации',),
    'methods/site-voice-and-consistency.md': (
        'Brand Core, Language, Reference Texts + этот файл',
        'готовые/утверждённые соседние страницы и реестр',
        'Будущему жителю нужно выбрать квартиру',
    ),
    'skills/architektonica-search-visibility/references/geo-aeo-content-evidence.md': (
        'этапы/артефакты/ограничения → релевантная проверенная работа →',
    ),
}


def known_regressions(rel, text):
    return [fragment for fragment in LEGACY_RULES.get(rel, ()) if fragment in text]


def section(text, title):
    return text.split('## ' + title + '\n', 1)[1].split('\n## ', 1)[0]


class EditorialInstructionTests(unittest.TestCase):
    def test_known_legacy_directives_do_not_return(self):
        for rel in LEGACY_RULES:
            with self.subTest(path=rel):
                self.assertEqual(known_regressions(rel, (ROOT / rel).read_text()), [])

    def test_guards_reject_each_original_directive_when_reintroduced(self):
        # Mutation probes: reintroducing any former bug must be observable.
        for rel, fragments in LEGACY_RULES.items():
            current = (ROOT / rel).read_text()
            for fragment in fragments:
                with self.subTest(path=rel, fragment=fragment):
                    self.assertEqual(known_regressions(rel, current + '\n' + fragment), [fragment])

    def test_authors_do_not_route_to_reset_copy_sources(self):
        for path in AUTHOR_FILES:
            with self.subTest(path=path.name, skill=path.parent.name):
                for name in RETIRED:
                    self.assertNotIn(name, path.read_text())
        narrative = (ROOT / 'skills/architektonica-narrative-design/SKILL.md').read_text()
        self.assertIn('planning/stage-01/IA_PROPOSAL.md', narrative)
        self.assertIn('planning/stage-02/WORK_MAP.md', narrative)

    def test_entry_points_route_to_same_editorial_contract(self):
        for rel in ('AGENTS.md', 'PROJECT_SYSTEM_PROMPT.md', 'README.md', 'QUICK_START.md',
                    'methods/copy-workflow.md', 'methods/editorial-quality.md',
                    'methods/site-voice-and-consistency.md', 'methods/engine-template-adaptation.md'):
            with self.subTest(path=rel):
                self.assertIn('editorial-source-boundaries.md', (ROOT / rel).read_text())

    def test_search_and_production_steps_have_no_duplicate_or_missing_numbers(self):
        for path, title, count in (
            (ROOT / 'skills/architektonica-search-visibility/SKILL.md', 'Что делать', 8),
            (CONTRACT, 'Производственный порядок текста', 9),
        ):
            with self.subTest(path=str(path)):
                numbers = [int(n) for n in re.findall(r'^(\d+)\. ', section(path.read_text(), title), re.M)]
                self.assertEqual(numbers, list(range(1, count + 1)))

    def test_benchmark_preserves_exact_brand_record_without_home_copy(self):
        body = BENCHMARK.read_text()
        blocks = re.findall(r'```text\n(.*?)\n```', body, re.S)
        self.assertEqual(blocks, ['ARCHITEKTONICA — Архитектура решений.\nТехнологии · Дизайн · Бизнес'])
        self.assertNotIn('ARCHITEKTONICA. Архитектура решений.', body)
        self.assertNotIn('**Первый экран.**', body)

    def test_case_writer_keeps_factual_case_route_and_sample_boundary(self):
        text = (ROOT / 'skills/architektonica-portfolio-case-writer/SKILL.md').read_text()
        self.assertIn('03_Architektonica_Case_Studies.md', text)
        self.assertIn('02_Architektonica_Fact_Bank.md', text)
        self.assertIn('историческими учебными иллюстрациями', text)

    def test_old_workspace_insertions_are_explicitly_historical(self):
        body = (ROOT / 'methods/client-workspace-integration.md').read_text()
        self.assertIn('## Исторические учебные вставки: не источник нового Stage 02', body)
        self.assertNotIn('## Редакционные вставки для Stage 02', body)
        self.assertIn('Если нет предметной пользы, не добавлять', body)


class EditorialEvaluationProtocolTests(unittest.TestCase):
    def test_all_seven_scenarios_are_defined_but_not_claimed_executed(self):
        data = json.loads((ROOT / 'tests/fixtures/editorial-regression-cases.json').read_text())
        self.assertEqual(data['literary_quality'], 'human_review_required')
        self.assertEqual(data['status'], 'NOT RUN')
        self.assertEqual([c['id'] for c in data['cases']], list('ABCDEFG'))
        for case in data['cases']:
            with self.subTest(case=case['id']):
                self.assertTrue(case['task'].strip())
                self.assertGreaterEqual(len(case['must_check']), 3)
                self.assertTrue(all(isinstance(c, str) and c.strip() for c in case['must_check']))
                self.assertIs(case['expected_repository_writes'], False)
                self.assertEqual(case['status'], 'NOT RUN')

    def test_evaluation_requires_separate_reviewer_and_explicit_write_permission(self):
        body = (ROOT / 'methods/editorial-regression-evaluation.md').read_text()
        self.assertIn('Редактор, не писавший ответ', body)
        self.assertIn('Самопроверку автора записывать отдельно', body)
        self.assertIn('отдельного явного разрешения владельца', body)
        self.assertIn('A не выполнять: отметить NOT RUN', body)
        self.assertIn('Автоматические', (ROOT / 'methods/editorial-quality.md').read_text())


if __name__ == '__main__':
    unittest.main()
