"""Structural SEO/GEO/AEO checks, not a textual lint or a live SEO audit."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_catalog import discover, mirror_bytes

BASE = ROOT / "skills/architektonica-search-visibility"
REFS = ["keyword-serp-research.md", "site-structure-linking.md",
        "geo-aeo-content-evidence.md", "page-publishing-audit.md", "EXTERNAL_SOURCES.md"]


class SearchVisibilityMethodsTests(unittest.TestCase):
    def test_required_references_exist_and_skill_is_discoverable(self):
        main = (BASE / "SKILL.md").read_text(encoding="utf-8")
        for name in REFS:
            self.assertTrue((BASE / "references" / name).is_file(), name)
            self.assertIn(f"references/{name}", main)
        records, errors = discover(ROOT)
        self.assertFalse(errors)
        self.assertIn(BASE.name, {item["name"] for item in records})
        # No arbitrary global skill count: new valid skills are allowed.

    def test_mirror_matches_generator_not_an_exact_text_substitution(self):
        original = BASE / "SKILL.md"
        mirrored = ROOT / ".agents/skills/architektonica-search-visibility/SKILL.md"
        self.assertEqual(mirrored.read_bytes(), mirror_bytes(original, ROOT))

    def test_external_sources_have_traceable_commit_pins(self):
        sources = (BASE / "references/EXTERNAL_SOURCES.md").read_text(encoding="utf-8")
        urls = re.findall(r"https://github\.com/[^)\s]+", sources)
        pinned = [url for url in urls if re.search(r"/(?:tree|blob)/[0-9a-f]{40}(?:/|$)", url)]
        self.assertGreaterEqual(len(pinned), 2, "Keep traceable pinned upstream sources")
        self.assertIn("LICENSE", sources)


if __name__ == "__main__":
    unittest.main()
