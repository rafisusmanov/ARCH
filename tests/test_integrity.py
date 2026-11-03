"""Regression checks for integration guards in the actual verifier."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from skill_catalog import mirror_bytes
class IntegrityTests(unittest.TestCase):
 def check_mutation(self, mutate):
  with tempfile.TemporaryDirectory() as temp:
   target=Path(temp)/'repo'
   shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('.git','__pycache__','.venv'))
   mutate(target)
   return subprocess.run(['python3','scripts/verify_package.py'],cwd=target,capture_output=True,text=True)
 def test_new_skill_mirror_loss(self):
  self.assertNotEqual(self.check_mutation(lambda r:(r/'.agents/skills/architektonica-ui-ux-expert/SKILL.md').unlink()).returncode,0)
 def test_vendored_ui_engine_loss(self):
  self.assertNotEqual(self.check_mutation(lambda r:(r/'third_party/ui-ux-pro-max/scripts/search.py').unlink()).returncode,0)
 def test_original_author_skill_loss(self):
  self.assertNotEqual(self.check_mutation(lambda r:(r/'skills/architektonica-creative-director/SKILL.md').unlink()).returncode,0)
 def test_deleted_copy_studio_is_not_required(self):
  result=self.check_mutation(lambda r:None)
  self.assertEqual(result.returncode,0)
  self.assertNotIn('copy-studio',result.stdout)
 def test_current_package(self):
  self.assertEqual(self.check_mutation(lambda r:None).returncode,0)
 def test_catalogue_loss(self):
  def mutate(r):
   import json
   p=r/'references/project/services_catalogue.json';v=json.loads(p.read_text());v['services'].pop();p.write_text(json.dumps(v))
  self.assertNotEqual(self.check_mutation(mutate).returncode,0)
 def test_merge_conflict(self):
  self.assertNotEqual(self.check_mutation(lambda r:(r/'README.md').write_text(chr(60)*7+' HEAD\n')).returncode,0)
 def test_web_recipe_loss(self):
  self.assertNotEqual(self.check_mutation(lambda r:(r/'.agents/skills/animate/RECIPES.md').unlink()).returncode,0)

class CuratedUiUxTests(unittest.TestCase):
 def test_cli_only_offers_installed_catalogs(self):
  import importlib.util, sys
  from pathlib import Path
  scripts=ROOT/'third_party/ui-ux-pro-max/scripts'
  sys.path.insert(0,str(scripts))
  try:
   import core
   for name, cfg in core.CSV_CONFIG.items():
    self.assertTrue((core.DATA_DIR/cfg['file']).is_file(), name)
   for name, cfg in core.STACK_CONFIG.items():
    self.assertTrue((core.DATA_DIR/cfg['file']).is_file(), name)
   self.assertNotIn('google-fonts',core.CSV_CONFIG)
   self.assertNotIn('vue',core.STACK_CONFIG)
  finally:
   sys.path.remove(str(scripts))

 def test_engine_source_is_template_not_architecture(self):
  for path in ['AGENTS.md','PROJECT_SYSTEM_PROMPT.md','methods/engine-template-adaptation.md','skills/architektonica-ui-ux-expert/SKILL.md']:
   self.assertIn('Engine', (ROOT/path).read_text(encoding='utf-8'))
  self.assertTrue((ROOT/'references/project/ARCHITEKTONICA_SITE_PLAN_V2.md').is_file())
 def test_new_skill_mirror(self):
  self.assertEqual(mirror_bytes(ROOT/'skills/architektonica-ui-ux-expert/SKILL.md'),(ROOT/'.agents/skills/architektonica-ui-ux-expert/SKILL.md').read_bytes())

class EngineDepthWorkflowTests(unittest.TestCase):
 def test_workflow_order_and_depth(self):
  guide=(ROOT/'methods/engine-template-adaptation.md').read_text(encoding='utf-8')
  self.assertTrue(guide.strip())
  self.assertIn('ARCHITEKTONICA_SITE_PLAN_V2.md', guide)
  self.assertIn('z-index',guide)
  self.assertIn('prefers-reduced-motion',guide)
 def test_activation_restrictions_are_exposed(self):
  from skill_catalog import discover
  records, errors = discover(ROOT)
  self.assertFalse(errors)
  metadata={item['name']:item for item in records}
  for name in ['review-animations','prototype']:
   self.assertEqual(metadata[name]['activation'],'explicit-only')
   self.assertIs(metadata[name]['disable-model-invocation'],True)