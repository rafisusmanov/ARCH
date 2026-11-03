"""Validate evaluation-case fixtures without freezing their number or skill count.

The fixtures are prompts for human evaluation, not independent model runs.
"""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_catalog import discover

CASES = ROOT / "tests/fixtures/skill-evaluation-cases.json"
BASELINE = {"home", "service", "case-uncertain", "microcopy", "immersive-scene"}

def fixture_errors(cases, records):
    """Return structural problems only; quality of a response needs human review."""
    available = {record["name"] for record in records}
    explicit_only = {record["name"] for record in records
                     if record["activation"] == "explicit-only"}
    problems = []
    if not isinstance(cases, list):
        return ["Cases must be a list"]
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or any(not isinstance(i, str) or not i.strip() for i in ids):
        problems.append("Every case needs a nonempty ID")
    if len(set(ids)) != len(ids):
        problems.append("Duplicate evaluation-case ID")
    if not BASELINE.issubset(ids):
        problems.append("Missing baseline evaluation cases")
    for case in cases:
        if not isinstance(case, dict):
            continue
        ident = case.get("id", "<unnamed>")
        if not isinstance(case.get("task"), str) or not case["task"].strip():
            problems.append(f"{ident}: missing task")
        skills = case.get("skills")
        if not isinstance(skills, list) or not skills or any(not isinstance(s, str) for s in skills):
            problems.append(f"{ident}: needs valid selected skills")
        else:
            if set(skills) - available:
                problems.append(f"{ident}: unknown skill")
            if set(skills) & explicit_only:
                problems.append(f"{ident}: explicit-only skill selected without user invocation")
        checks = case.get("must_check")
        if not isinstance(checks, list) or not checks or any(not isinstance(c, str) or not c.strip() for c in checks):
            problems.append(f"{ident}: missing evaluation criteria")
    return problems

class SkillEvaluationFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(CASES.read_text(encoding="utf-8"))
        cls.records, cls.discovery_errors = discover(ROOT)

    def test_baseline_cases_are_valid_but_extra_cases_are_allowed(self):
        self.assertFalse(self.discovery_errors)
        self.assertEqual(fixture_errors(self.cases, self.records), [])

    def test_additional_single_skill_case_is_legal_but_unsafe_cases_fail(self):
        extended = self.cases + [{
            "id": "new-valid-scenario",
            "task": "Напиши корректный текст по предоставленным фактам.",
            "skills": ["architektonica-creative-director"],
            "must_check": ["source-facts"],
        }]
        self.assertEqual(fixture_errors(extended, self.records), [])
        self.assertTrue(fixture_errors(extended + [extended[-1]], self.records))
        invalid = [dict(item) for item in self.cases]
        invalid[0]["skills"] = ["nonexistent-skill"]
        self.assertIn("home: unknown skill", fixture_errors(invalid, self.records))

    def test_human_rubric_and_analytics_contract_remain_available(self):
        rubric = ROOT / "methods/skill-effectiveness-evaluation.md"
        analytics = ROOT / "methods/site-analytics-contract.md"
        self.assertTrue(rubric.is_file())
        self.assertTrue(analytics.is_file())
        self.assertIn("lead_confirmed", analytics.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()