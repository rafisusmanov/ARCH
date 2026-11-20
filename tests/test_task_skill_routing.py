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
    STAGES, PRIORITY_CHECKS, SITE_PRINCIPLE, audit_read_trace, check_proposal, expected_for_task, load_matrix,
    make_plan, verify_matrix,
    validate_service_architecture,
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
        self.assertTrue(any("mandatory service disclosure gate" in e for e in self.check(matrix)))

    def test_high_risk_required_roles_cannot_be_removed_together_with_fixture(self):
        # Independent regression invariant: not another view of the fixture itself.
        critical = {
            "content.public-page": {"architektonica-critical-editor"},
            "content.services-overview": {
                "architektonica-critical-editor", "architektonica-ui-ux-expert"
            },
            "content.next-task": {"architektonica-ui-ux-expert", "architektonica-critical-editor"},
            "content.service-detail": {"architektonica-ui-ux-expert", "architektonica-critical-editor"},
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

    def test_all_plans_begin_with_priority_gate(self):
        for task in self.matrix["tasks"]:
            plan = make_plan(ROOT, self.matrix, task["id"],
                             user_requested_explicit=task["explicit_only_skills"] if task.get("explicit_trigger_required") else [])
            self.assertEqual(plan["source_paths_to_read"][:2], ["AGENTS.md", "PROJECT_SYSTEM_PROMPT.md"])
            self.assertEqual(plan["priority_gate"]["principle"], SITE_PRINCIPLE)
            self.assertEqual(plan["acceptance_checks"][:3], list(PRIORITY_CHECKS))
            self.assertIn("site_principle_failed", plan["stop_conditions"])

    def test_disclosure_policy_cannot_be_removed(self):
        for ident in ("content.next-task", "content.service-detail", "content.services-overview"):
            matrix = copy.deepcopy(self.matrix)
            route = next(t for t in matrix["tasks"] if t["id"] == ident)
            route["acceptance_checks"].remove("no_automatic_detail_pages")
            self.assertTrue(any("mandatory service disclosure gate" in e for e in self.check(matrix)))
        matrix = copy.deepcopy(self.matrix)
        del matrix["policy"]["priority_gate"]
        self.assertTrue(any("mandatory site-principle gate" in e for e in self.check(matrix)))

    def service_proposal(self):
        catalogue = json.loads((ROOT / "planning/stage-02/public-service-catalogue.json").read_text(encoding="utf-8"))
        return {
            "task_id": "content.next-task",
            "decision": "Выбрать модель краткого содержания направлений и глубины по запросу",
            "scope": "services",
            "principle_checks": {
                "understand_without_reading": {"verdict": "PASS", "reason": "Визуальные группы и названия направлений"},
                "interesting_when_viewing": {"verdict": "PASS", "reason": "Различимые карточки направлений и удобный выбор"},
                "depth_on_demand": {"verdict": "PASS", "reason": "Услуга раскрывается в выбранном направлении"}
            },
            "service_plan": {
                "coverage": "all",
                "service_ids": [s["id"] for s in catalogue["services"]],
                "group_page_ids": [g["id"] for g in catalogue["groups"]],
                "disclosure": "progressive_on_demand",
                "default_expanded_ids": [],
                "detail_page_candidates": []
            }
        }

    def test_observed_next_task_failure_and_corrected_control(self):
        # The observed response omitted any justification of the disclosure model.
        # This record describes that omission, not a claim of authenticated tool logs.
        observed = {"task_id": "content.next-task", "scope": "services",
                    "decision": "Детальные страницы услуг: разработать контент всех 17 направлений и 84 услуг"}
        errors = check_proposal(ROOT, self.matrix, observed)
        self.assertTrue(any("all three site-principle checks" in e for e in errors))
        self.assertTrue(any("requires service_plan" in e for e in errors))
        corrected = self.service_proposal()
        self.assertEqual(len(corrected["service_plan"]["service_ids"]), 84)
        self.assertEqual(check_proposal(ROOT, self.matrix, corrected), [])
        all_pages = copy.deepcopy(corrected)
        all_pages["service_plan"]["detail_page_candidates"] = [
            {"id": sid, "reason": "Every catalogue entry receives a page", "status": "proposed_not_approved"}
            for sid in all_pages["service_plan"]["service_ids"]
        ]
        errors = check_proposal(ROOT, self.matrix, all_pages)
        self.assertTrue(any("standalone service pages forbidden" in e for e in errors))

    def test_preflight_rejects_flat_catalogue_ineligible_pages_and_omissions(self):
        for field, value, signal in (
            ("default_expanded_ids", self.service_proposal()["service_plan"]["service_ids"], "flat full-detail"),
            ("service_ids", ["svc-001"], "exactly the current public catalogue"),
            ("service_ids", ["svc-007"], "unknown/excluded"),
            ("disclosure", "all_visible", "progressive on-demand"),
            ("group_page_ids", [f"dir-{i:02d}" for i in range(1,18)], "no category pages"),
            ("detail_page_candidates", [{"id": "svc-001", "reason": "Specific need", "status": "approved"}], "standalone service pages forbidden"),
        ):
            with self.subTest(field=field, signal=signal):
                record = self.service_proposal()
                record["service_plan"][field] = value
                self.assertTrue(any(signal in e for e in check_proposal(ROOT, self.matrix, record)))
        record = self.service_proposal()
        record["service_plan"]["detail_page_candidates"] = [
            {"id": "svc-001", "reason": "Distinct reader question requiring an explanation", "status": "proposed_not_approved"}
        ]
        self.assertTrue(any("standalone service pages forbidden" in e for e in check_proposal(ROOT, self.matrix, record)))
        record["principle_checks"]["depth_on_demand"]["verdict"] = "FAIL"
        self.assertTrue(any("depth_on_demand" in e for e in check_proposal(ROOT, self.matrix, record)))

    def test_service_route_cannot_bypass_scope_gate(self):
        record = self.service_proposal()
        record["task_id"] = "content.service-detail"
        self.assertTrue(any("exactly one" in e for e in check_proposal(ROOT, self.matrix, record)))
        record["scope"] = "other"
        del record["service_plan"]
        self.assertTrue(any("requires service scope" in e for e in check_proposal(ROOT, self.matrix, record)))

    def test_seven_page_architecture_cannot_regress_to_17_pages(self):
        catalogue = json.loads((ROOT / "planning/stage-02/public-service-catalogue.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_service_architecture(catalogue), [])
        catalogue["directions"][0]["proposed_url"] = "/services/branding"
        self.assertTrue(any("category must be an anchor" in e for e in validate_service_architecture(catalogue)))
        catalogue["architecture"]["direction_pages"] = 17
        self.assertTrue(any("exactly seven pages" in e for e in validate_service_architecture(catalogue)))

    def test_digital_products_page_requires_all_13_services(self):
        catalogue = json.loads((ROOT / "planning/stage-02/public-service-catalogue.json").read_text(encoding="utf-8"))
        record = self.service_proposal()
        record["task_id"] = "content.public-page"
        plan = record["service_plan"]
        plan["coverage"] = "selected"
        plan["group_page_ids"] = ["digital-products"]
        plan["service_ids"] = [s["id"] for s in catalogue["services"] if s["direction_id"] == "dir-04"]
        self.assertEqual(len(plan["service_ids"]), 11)
        self.assertTrue(any("all services of one main direction" in e for e in check_proposal(ROOT, self.matrix, record)))
        plan["service_ids"] = [s["id"] for s in catalogue["services"] if s["group_id"] == "digital-products"]
        self.assertEqual(len(plan["service_ids"]), 13)
        self.assertEqual(check_proposal(ROOT, self.matrix, record), [])


if __name__ == "__main__":
    unittest.main()
