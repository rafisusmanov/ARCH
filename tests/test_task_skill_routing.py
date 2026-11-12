"""Canonical routing regression: missing skills, sources, explicit-only safety, read traces.

Synthetic traces here verify parser and gate behavior, NOT that an AI actually read
sources or that independent human review took place.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_catalog import discover
from task_skill_router import (
    STAGES, audit_read_trace, expected_for_task, load_matrix,
    make_plan, verify_matrix,
)

FIXTURES = ROOT / "tests/fixtures/skill-evaluation-cases.json"


class TaskSkillRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_matrix(ROOT)
        cls.records, cls.discovery_errors = discover(ROOT)

    def check(self, matrix):
        return verify_matrix(ROOT, matrix=matrix, records=self.records)[1]

    def test_canonical_matrix_is_valid_and_covers_every_discovered_skill(self):
        self.assertEqual(self.discovery_errors, [])
        self.assertEqual(self.check(self.matrix), [])
        self.assertEqual({t["stage"] for t in self.matrix["tasks"]}, STAGES)
        self.assertGreaterEqual(len(self.matrix["tasks"]), 20)
        present = {
            skill for t in self.matrix["tasks"]
            for skill in (
                t["required_skills"] + t["explicit_only_skills"]
                + [c["skill"] for c in t["conditional_skills"]]
            )
        }
        self.assertEqual(present, {record["name"] for record in self.records})

    def test_fixtures_have_exact_route_and_required_skills(self):
        tasks = {t["id"]: t for t in self.matrix["tasks"]}
        fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
        self.assertEqual(len(fixtures), len({f["id"] for f in fixtures}))
        covered = set()
        for fixture in fixtures:
            with self.subTest(case=fixture["id"]):
                route = fixture.get("routing_task_id")
                self.assertIn(route, tasks)
                covered.add(tasks[route]["stage"])
                self.assertEqual(set(tasks[route]["required_skills"]), set(fixture["skills"]))
                self.assertFalse(set(fixture["skills"]) & {"prototype", "review-animations"})
                self.assertTrue(fixture.get("must_check"))
        self.assertEqual(covered, STAGES)

    def test_missing_required_skill_is_rejected(self):
        matrix = copy.deepcopy(self.matrix)
        route = next(t for t in matrix["tasks"] if t["id"] == "content.services-overview")
        route["required_skills"].remove("architektonica-critical-editor")
        self.assertTrue(any("skills differ from required_skills" in e for e in self.check(matrix)))

    def test_high_risk_required_roles_cannot_be_removed_together_with_fixture(self):
        # Independent regression invariant: not another view of the fixture itself.
        critical = {
            "content.public-page": {"architektonica-critical-editor"},
            "content.services-overview": {
                "architektonica-critical-editor", "architektonica-ui-ux-expert"
            },
            "dev.forms-integration": {"architektonica-website-qa", "break-ui"},
            "qa.site": {"architektonica-website-qa", "mobile-native"},
            "release.beget": {"architektonica-website-qa", "architektonica-search-visibility"},
        }
        routes = {x["id"]: x for x in self.matrix["tasks"]}
        for ident, required in critical.items():
            with self.subTest(task=ident):
                self.assertTrue(required <= set(routes[ident]["required_skills"]))

    def test_explicit_only_behavioral_cases_require_user_request(self):
        fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cases = {x["id"]: x for x in fixtures}
        self.assertEqual(cases["motion-variants-explicit"]["explicit_requested_skills"], ["prototype"])
        self.assertEqual(cases["stage-04-review-explicit"]["explicit_requested_skills"], ["review-animations"])
        for case in fixtures:
            explicit = case.get("explicit_requested_skills", [])
            if explicit:
                route = next(x for x in self.matrix["tasks"] if x["id"] == case["routing_task_id"])
                self.assertTrue(set(explicit) <= set(route["explicit_only_skills"]))

    def test_conditional_skills_have_a_real_trigger(self):
        base = make_plan(ROOT, self.matrix, "content.public-page")
        extra = make_plan(ROOT, self.matrix, "content.public-page", conditions=["new_concept"])
        self.assertNotIn("skills/architektonica-idea-lab/SKILL.md", base["skill_paths_to_read"])
        self.assertIn("skills/architektonica-idea-lab/SKILL.md", extra["skill_paths_to_read"])

    def test_unknown_source_and_unknown_skill_fail(self):
        for field, value, signal in (
            ("required_sources", "methods/THIS_DOES_NOT_EXIST.md", "missing/unsafe source"),
            ("required_skills", "skill-that-does-not-exist", "unknown skill"),
        ):
            with self.subTest(field=field):
                matrix = copy.deepcopy(self.matrix)
                matrix["tasks"][0][field].append(value)
                self.assertTrue(any(signal in error for error in self.check(matrix)))

    def test_restricted_activation_is_never_silent(self):
        restricted = {r["name"] for r in self.records if r["activation"] == "explicit-only"}
        self.assertEqual(restricted, {"prototype", "review-animations"})
        for task in self.matrix["tasks"]:
            self.assertFalse(restricted.intersection(task["required_skills"]))
            self.assertFalse(restricted.intersection(c["skill"] for c in task["conditional_skills"]))
        with self.assertRaisesRegex(ValueError, "explicit user invocation required"):
            make_plan(ROOT, self.matrix, "design.variants")
        with self.assertRaisesRegex(ValueError, "explicit user invocation required"):
            make_plan(ROOT, self.matrix, "motion.review-explicit")
        plan = make_plan(ROOT, self.matrix, "design.variants", user_requested_explicit=["prototype"])
        self.assertIn("skills/prototype/SKILL.md", plan["skill_paths_to_read"])
        with self.assertRaisesRegex(ValueError, "not permitted"):
            make_plan(ROOT, self.matrix, "design.page", user_requested_explicit=["prototype"])

    def test_unknown_tasks_and_conditions_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unlisted task"):
            make_plan(ROOT, self.matrix, "stage04.made-up-task")
        with self.assertRaisesRegex(ValueError, "unknown conditions"):
            make_plan(ROOT, self.matrix, "content.public-page", conditions=["made_up_condition"])

    def mock_trace(self, task_id, *, conditions=None, explicit=None):
        conditions, explicit = conditions or [], explicit or []
        plan = make_plan(ROOT, self.matrix, task_id, conditions, explicit)
        paths = plan["skill_paths_to_read"] + plan["source_paths_to_read"]
        return {
            "task_id": task_id,
            "conditions": conditions,
            "explicit_user_request": explicit,
            "events": [
                {
                    "type": "file_read",
                    "origin": "tool_log",
                    "tool_call_id": f"SYNTHETIC-TEST-{i}",
                    "path": path,
                    "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
                }
                for i, path in enumerate(paths)
            ],
        }

    def test_synthetic_read_log_completeness_and_missing_gate(self):
        trace = self.mock_trace("content.services-overview")
        self.assertEqual(audit_read_trace(ROOT, self.matrix, trace), [])
        trace["events"].pop(0)
        err = audit_read_trace(ROOT, self.matrix, trace)
        self.assertTrue(any("missing actual source-read records" in x for x in err))

    def test_tampered_or_self_reported_trace_fails(self):
        trace = self.mock_trace("qa.site")
        trace["events"][0]["sha256"] = "0" * 64
        self.assertTrue(any("sha256" in x for x in audit_read_trace(ROOT, self.matrix, trace)))
        trace = self.mock_trace("qa.site")
        trace["events"][0]["origin"] = "self_report"
        self.assertTrue(any("only tool_log" in x for x in audit_read_trace(ROOT, self.matrix, trace)))

    def test_missing_task_metadata_fails(self):
        matrix = copy.deepcopy(self.matrix)
        del matrix["tasks"][0]["deliverable"]
        self.assertTrue(any("missing" in e for e in self.check(matrix)))


if __name__ == "__main__":
    unittest.main()
