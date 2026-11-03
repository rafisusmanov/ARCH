"""Reproduce missed YAML, mirror, future-skill and document integrity failures."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from skill_catalog import discover
from sync_skills import sync
from verify_package import check_references


class HistoricalReferenceTests(unittest.TestCase):
    def test_only_exact_audit_reference_is_exempt(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            audit = root / 'methods/source-audit-and-portfolio-rules.md'
            audit.parent.mkdir()
            ref = '../skills/architektonica-copy-studio/SKILL.md'
            audit.write_text(f'[historical]({ref})\n')
            errors = []
            check_references(root, audit, errors)
            self.assertEqual(errors, [])
            for document, target in (
                (audit, '../skills/architektonica-copy-studio/OTHER.md'),
                (audit, '../skills/missing/SKILL.md'),
                (audit.with_name('other-audit.md'), ref),
            ):
                with self.subTest(document=document.name, target=target):
                    document.write_text(f'[missing]({target})\n')
                    errors = []
                    check_references(root, document, errors)
                    self.assertEqual(len(errors), 1)
                    self.assertIn('Broken local reference:', errors[0])


class RepositoryFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.venv'))

    def run_tool(self, name, *args):
        return subprocess.run([sys.executable, '-B', str(self.root / 'scripts' / name), *args],
                              cwd=self.temp.name, capture_output=True, text=True)

    def assert_invalid(self, diagnostic):
        result = self.run_tool('verify_package.py')
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(diagnostic, result.stdout, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)


class DiscoveryTests(RepositoryFixture):
    def test_new_unprefixed_skill_is_discovered_and_validated(self):
        folder = self.root / 'skills/new-editorial-skill'
        folder.mkdir()
        (folder / 'SKILL.md').write_text('---\nname: new-editorial-skill\ndescription: Editorial testing\n---\nRead [recipe](RECIPE.md).\n')
        (folder / 'RECIPE.md').write_text('Read `../../methods/editorial-quality.md`.\n')
        self.assertFalse(sync(self.root))
        result = self.run_tool('skill_catalog.py', '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        record = next(x for x in json.loads(result.stdout)['skills'] if x['name'] == folder.name)
        self.assertEqual(record['resources'], ['skills/new-editorial-skill/RECIPE.md'])
        self.assertEqual(self.run_tool('verify_package.py').returncode, 0)
        (folder / 'RECIPE.md').write_text('Read [missing](MISSING.md).\n')
        self.assertFalse(sync(self.root))
        self.assert_invalid('Broken local reference: skills/new-editorial-skill/RECIPE.md')

    def test_invalid_yaml_and_typed_metadata_are_rejected(self):
        path = self.root / 'skills/architektonica-ui-ux-expert/SKILL.md'
        prefix = '---\nname: architektonica-ui-ux-expert\n'
        variants = [
            prefix + 'description: invalid: colon\n---\n',
            prefix + 'description: [not, text]\n---\n',
            prefix + 'description: ok\ndisable-model-invocation: "true"\n---\n',
            prefix + 'description: ok\ndisable-model-invocation: true\ndisable-model-invocation: false\n---\n',
            prefix + 'description: unclosed\n',
            '---\nname: somebody-else\ndescription: ok\n---\n',
        ]
        for text in variants:
            with self.subTest(text=text):
                path.write_text(text)
                self.assert_invalid('skills/architektonica-ui-ux-expert/SKILL.md')

    def test_mirror_rebases_external_paths_but_keeps_local_recipe(self):
        folder = self.root / 'skills/new-test-skill'
        folder.mkdir()
        (folder / 'SKILL.md').write_text('---\nname: new-test-skill\ndescription: Test\n---\n'
                                      '[facts](../../references/project/02_Architektonica_Fact_Bank.md)\n'
                                      '`../animate/RECIPES.md`\n[local](LOCAL.md)\n')
        (folder / 'LOCAL.md').write_text('Local recipe\n')
        self.assertFalse(sync(self.root))
        mirrored = self.root / '.agents/skills/new-test-skill/SKILL.md'
        self.assertIn('../../../references/project/', mirrored.read_text())
        self.assertIn('../animate/RECIPES.md', mirrored.read_text())
        self.assertIn('[local](LOCAL.md)', mirrored.read_text())
        self.assertEqual(self.run_tool('verify_package.py').returncode, 0)
        # A byte-for-byte copy was the original bug.
        mirrored.write_bytes((folder / 'SKILL.md').read_bytes())
        self.assert_invalid('Broken local reference: .agents/skills/new-test-skill/SKILL.md')

    def test_orphan_mirror_is_reported_without_deletion(self):
        extra = self.root / '.agents/skills/animate/EXTRA.md'
        extra.write_text('Unreviewed content')
        self.assert_invalid('Orphan mirror file')
        result = self.run_tool('sync_skills.py')
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(extra.exists())

    def test_missing_local_markdown_link_is_detected(self):
        with (self.root / 'QUICK_START.md').open('a') as handle:
            handle.write('\n[missing](methods/missing.md)\n')
        self.assert_invalid('Broken local reference: QUICK_START.md')

    def test_missing_vendor_csv_cannot_disappear_from_validation(self):
        for rel in ('icons.csv', 'charts.csv', 'stacks/laravel.csv'):
            with self.subTest(csv=rel):
                path = self.root / 'third_party/ui-ux-pro-max/data' / rel
                original = path.read_bytes()
                path.unlink()
                self.assert_invalid('Invalid vendor CSV ' + rel)
                path.write_bytes(original)

    def test_corrupt_csv_headers_fail(self):
        (self.root / 'third_party/ui-ux-pro-max/data/icons.csv').write_text('Wrong,Columns\na,b\n')
        self.assert_invalid('Invalid CSV headers: icons.csv')

    def test_roadmap_complete_body_is_guarded(self):
        path = self.root / 'references/project/ARCHITEKTONICA_SITE_PLAN_V2.md'
        text = path.read_text()
        # Keep all stage headings but remove a later requirement.
        path.write_text(text.replace('- Подготовить резервное копирование и механизм отката.\n', ''))
        self.assert_invalid('Approved roadmap v2 changed or truncated')

    def test_symlink_resource_does_not_get_mirrored(self):
        path = self.root / 'skills/animate/ESCAPE.md'
        path.symlink_to(self.root / 'README.md')
        self.assert_invalid('skill trees must not contain symlinks')


class WebsiteQaIntegrationTests(RepositoryFixture):
    def test_website_qa_skill_is_discovered_and_mirrored(self):
        records, errors = discover(ROOT)
        self.assertFalse(errors)
        names = {r['name'] for r in records}
        self.assertIn('architektonica-website-qa', names)
        self.assertIn('architektonica-ui-ux-expert', names)
        self.assertEqual(self.run_tool('verify_package.py').returncode, 0)

    def test_website_qa_checklist_is_required(self):
        (self.root / 'skills/architektonica-website-qa/references/QA_CHECKLIST.md').unlink()
        self.assert_invalid('Broken local reference: skills/architektonica-website-qa/SKILL.md')
