"""Executable integration checks for the locally shipped search package."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / 'third_party/ui-ux-pro-max'
sys.path.insert(0, str(VENDOR / 'scripts'))
import core
from design_system import generate_design_system


class SearchTests(unittest.TestCase):
    def cli(self, *args, script=None, cwd=None):
        return subprocess.run([sys.executable, '-B', str(script or VENDOR / 'scripts/search.py'), *args],
                              cwd=cwd, capture_output=True, text=True)

    def test_every_shipped_domain_and_stack_returns_relevant_data(self):
        probes = {'style': 'Minimalism', 'color': 'SaaS', 'chart': 'comparison',
                  'landing': 'hero-features-cta', 'product': 'SaaS', 'ux': 'focus not obscured',
                  'typography': 'editorial', 'icons': 'hamburger menu navigation',
                  'gsap': 'scroll', 'react': 'render', 'web': 'focus'}
        stacks = {'react': 'accessibility semantic', 'nextjs': 'App Router',
                  'astro': 'Islands Architecture', 'html-tailwind': 'accessibility semantic',
                  'threejs': 'dispose geometry', 'laravel': 'Blade components'}
        self.assertEqual(set(core.CSV_CONFIG), set(probes))
        self.assertEqual(set(core.STACK_CONFIG), set(stacks))
        for domain, query in probes.items():
            with self.subTest(domain=domain):
                result = core.search(query, domain)
                self.assertNotIn('error', result)
                self.assertGreater(result['count'], 0, result)
        for stack, query in stacks.items():
            with self.subTest(stack=stack):
                result = core.search_stack(query, stack)
                self.assertNotIn('error', result)
                self.assertGreater(result['count'], 0, result)

    def test_unknown_domain_is_not_a_style_result(self):
        result = core.search('modern', 'google-fonts')
        self.assertIn('error', result)
        self.assertNotIn('results', result)
        auto = core.search('popular google fonts')
        self.assertIn(auto['domain'], core.CSV_CONFIG)
        self.assertNotEqual(auto.get('runner_up_domain'), 'google-fonts')

    def test_search_and_design_system_work_outside_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.cli('Minimalism', '--domain', 'style', '--json', cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertGreater(json.loads(result.stdout)['count'], 0)
            result = self.cli('premium corporate portfolio', '--design-system', '--motion', '4',
                              '--variance', '6', '--density', '3', '--json', cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)['design_system'])
            self.assertEqual(list(Path(directory).iterdir()), [], 'Read-only generation wrote files')

    def test_empty_result_is_distinct_from_corrupt_corpus(self):
        result = self.cli('zzzznotacorpuswordzzzz', '--domain', 'style', '--json')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['count'], 0)
        with tempfile.TemporaryDirectory() as directory:
            vendor = Path(directory) / 'vendor'
            shutil.copytree(VENDOR, vendor, ignore=shutil.ignore_patterns('__pycache__'))
            (vendor / 'data/icons.csv').unlink()
            result = self.cli('hamburger menu', '--domain', 'icons', '--json', script=vendor / 'scripts/search.py')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('error', json.loads(result.stdout))

    def test_incompatible_flags_are_not_silently_ignored(self):
        for flags in [('--domain', 'style', '--stack', 'react'),
                      ('--domain', 'style', '--design-system'), ('--motion', '3'),
                      ('--design-system', '--page', 'home')]:
            with self.subTest(flags=flags):
                result = self.cli('modern', *flags)
                self.assertEqual(result.returncode, 2)
                self.assertIn('error:', result.stderr)

    def test_design_system_fails_before_persisting_incomplete_data(self):
        with tempfile.TemporaryDirectory() as directory:
            vendor = Path(directory) / 'vendor'
            output = Path(directory) / 'output'
            shutil.copytree(VENDOR, vendor, ignore=shutil.ignore_patterns('__pycache__'))
            path = vendor / 'data/ui-reasoning.csv'
            original = path.read_bytes()
            for corrupt in (None, b'Wrong,Columns\na,b\n'):
                with self.subTest(corrupt=corrupt):
                    if corrupt is None:
                        path.unlink()
                    else:
                        path.write_bytes(corrupt)
                    result = self.cli('premium corporate', '--design-system', '--persist',
                                      '--output-dir', str(output), '--json', script=vendor / 'scripts/search.py')
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn('error', json.loads(result.stdout))
                    self.assertFalse(output.exists())
            path.write_bytes(original)

    def test_persist_preserves_existing_master_and_page(self):
        with tempfile.TemporaryDirectory() as directory:
            kwargs = dict(project_name='../../review', persist=True, page='../home', output_dir=directory)
            result = generate_design_system('premium corporate', **kwargs)
            files = [Path(path) for path in result['persistence']['created_files']]
            self.assertEqual(len(files), 2)
            for path in files:
                self.assertTrue(path.resolve().is_relative_to(Path(directory).resolve()))
                path.write_text('OWNER APPROVED')
            result = generate_design_system('playful colorful', **kwargs)
            self.assertEqual(result['persistence']['status'], 'skipped_exists')
            self.assertTrue(all(path.read_text() == 'OWNER APPROVED' for path in files))

    def test_persist_rejects_symlink_escape_before_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            output = base / 'output'
            outside = base / 'outside'
            output.mkdir()
            outside.mkdir()
            (output / 'design-system').symlink_to(outside, target_is_directory=True)
            result = None
            from design_system import persist_design_system
            with self.assertRaisesRegex(ValueError, 'outside the selected output directory'):
                persist_design_system({'project_name': 'example'}, output_dir=str(output))
            self.assertEqual(list(outside.iterdir()), [], 'must not write through an escaped symlink')
