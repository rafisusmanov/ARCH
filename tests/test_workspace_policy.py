"""Structural owner-decision references and permission controls.

A natural-language regex cannot reliably establish or disprove policy consistency.
The owner decision is authoritative; semantic conflicts need human PR review.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "references/project/OWNER_DECISION_2026-11-02_CLIENT_WORKSPACE.md"
OWNER_FILENAME = OWNER.name
ENTRYPOINTS = ("AGENTS.md", "PROJECT_SYSTEM_PROMPT.md", "README.md",
               "methods/agent-expert-stage-protocol.md")
ROLES = ("creative-director", "critical-editor",
         "ui-ux-expert", "portfolio-case-writer")

class WorkspacePolicyTests(unittest.TestCase):
    def test_owner_decision_is_present_and_reachable(self):
        self.assertTrue(OWNER.is_file())
        self.assertTrue(OWNER.read_text(encoding="utf-8").strip())
        for path in ENTRYPOINTS:
            with self.subTest(path=path):
                self.assertIn(OWNER_FILENAME, (ROOT / path).read_text(encoding="utf-8"))

    def test_active_editors_link_to_authoritative_decision(self):
        for role in ROLES:
            for folder in ("skills", ".agents/skills"):
                with self.subTest(role=role, folder=folder):
                    path = ROOT / folder / ("architektonica-" + role) / "SKILL.md"
                    self.assertTrue(path.is_file())
                    self.assertIn(OWNER_FILENAME, path.read_text(encoding="utf-8"))

    def test_workspace_page_and_gate_refer_to_owner_decision(self):
        page = ROOT / "planning/stage-02/client-workspace-page.md"
        gate = ROOT / "planning/stage-02/client-workspace-publication-gate.md"
        self.assertTrue(page.is_file())
        self.assertTrue(gate.is_file())
        self.assertIn("methods/client-workspace-integration.md",
                      (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("client-workspace-page.md", OWNER.read_text(encoding="utf-8"))

    def test_stage_01_approval_is_separate_from_stage_02_draft(self):
        data = json.loads((ROOT / "planning/stage-01/catalogue-map.json").read_text(encoding="utf-8"))
        self.assertTrue(data["owner_approval"].strip())
        self.assertEqual(len(data["services"]), 81)
        self.assertEqual(len(data["directions"]), 17)
        page = (ROOT / "planning/stage-02/client-workspace-page.md").read_text(encoding="utf-8")
        self.assertTrue(page.strip())

    def test_guardrail_exercises_are_not_claimed_as_passed(self):
        body = (ROOT / "planning/agent-guardrail-evaluation-20261102.md").read_text(encoding="utf-8")
        for number in range(1, 6):
            label = f"| G{number:02d} |"
            row = next((line for line in body.splitlines() if line.startswith(label)), None)
            self.assertIsNotNone(row, label)
            self.assertIn("NOT RUN", row)

    def test_ci_uses_read_only_repository_permissions(self):
        workflow = (ROOT / ".github/workflows/verify-skills.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)

if __name__ == "__main__":
    unittest.main()