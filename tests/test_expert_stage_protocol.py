"""Verify seven-stage coverage and real document links, without pinning prose."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "methods/agent-expert-stage-protocol.md"


class ExpertStageProtocolTests(unittest.TestCase):
    def test_protocol_has_seven_ordered_stage_rows_and_approved_plan(self):
        body = PROTOCOL.read_text(encoding="utf-8")
        stage_rows = re.findall(r"^\|\s*(0[1-7])\s*[—–-]", body, flags=re.M)
        stage_rows += re.findall(
            r"<tr\b[^>]*>\s*<td\b[^>]*>\s*(0[1-7])\s*[—–-]", body, flags=re.I)
        self.assertEqual(stage_rows, [f"{number:02d}" for number in range(1, 8)])
        self.assertIn("ARCHITEKTONICA_SITE_PLAN_V2.md", body)
        self.assertTrue((ROOT / "references/project/ARCHITEKTONICA_SITE_PLAN_V2.md").is_file())

    def test_agent_entry_points_link_to_protocol(self):
        for path in ("AGENTS.md", "PROJECT_SYSTEM_PROMPT.md"):
            with self.subTest(path=path):
                self.assertIn("methods/agent-expert-stage-protocol.md",
                              (ROOT / path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
