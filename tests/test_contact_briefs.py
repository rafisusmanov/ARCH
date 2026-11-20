"""Documented, owner-approved prototype v9: catalogue and question integrity.

This is not a browser, production form, or API integration test.
"""
from collections import Counter
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "planning/stage-02"


def read_briefs():
    groups = Counter()
    rows = {}
    group = None
    text = (STAGE / "contact-briefs.tsv").read_text(encoding="utf-8")
    if "\ufffd" in text:
        raise ValueError("Damaged UTF-8 in contact briefs")
    for line in text.splitlines():
        if line.startswith("# Group: "):
            group = line.removeprefix("# Group: ")
        if not line or line.startswith("#"):
            continue
        number, label, description, *questions = line.split("|")
        service = "svc-" + number
        if service in rows:
            raise ValueError(f"Duplicate service {service}")
        rows[service] = (label, description, questions)
        groups[group] += 1
    return groups, rows


class ContactBriefsTest(unittest.TestCase):
    def test_exact_public_coverage_and_group_counts(self):
        groups, rows = read_briefs()
        catalogue = json.loads((STAGE / "public-service-catalogue.json").read_text())
        self.assertEqual({s["id"] for s in catalogue["services"]}, set(rows))
        self.assertEqual(84, len(rows))
        self.assertEqual([12, 4, 19, 18, 16, 15], list(groups.values()))
        self.assertTrue(all(label and description for label, description, _ in rows.values()))

    def test_questions_options_and_conditions(self):
        _, rows = read_briefs()
        for service, (_, _, questions) in rows.items():
            with self.subTest(service=service):
                self.assertLessEqual(4, len(questions))
                self.assertLessEqual(len(questions), 6)
                available = []
                for i, question in enumerate(questions):
                    if question.startswith("?"):
                        condition, question = question[1:].split(":", 1)
                        n, value = condition.split("=", 1)
                        self.assertLess(int(n), i)
                        self.assertIn(value, available[int(n)])
                    multi = question.startswith("+")
                    label, *opts = question.lstrip("+").split("~")
                    self.assertTrue(label.strip())
                    self.assertTrue(all(o.strip("!").strip() for o in opts))
                    self.assertEqual(len(opts), len(set(o.lstrip("!") for o in opts)))
                    if multi:
                        self.assertGreaterEqual(len(opts), 2)
                    if any(o.startswith("!") for o in opts):
                        self.assertTrue(multi)
                    self.assertNotIn("Пока не знаю", opts)
                    self.assertNotIn("Свой вариант", opts)
                    self.assertNotIn("бюджет", label.lower())
                    available.append([o.lstrip("!") for o in opts])

    def test_public_labels_match_catalogue(self):
        _, rows = read_briefs()
        catalogue = json.loads((STAGE / "public-service-catalogue.json").read_text(encoding="utf-8"))
        self.assertEqual({s["id"]: s["display_title"] for s in catalogue["services"]},
                         {service: row[0] for service, row in rows.items()})

    def test_marketing_regression_and_exclusive_ranges(self):
        _, rows = read_briefs()
        marketing = rows["svc-004"][2][0]
        self.assertTrue(marketing.startswith("+"))
        self.assertIn("Привлечение клиентов", marketing)
        self.assertIn("Увеличение продаж", marketing)
        self.assertIn("Выход на новый рынок", marketing)
        ranges = rows["svc-089"][2][1]
        self.assertFalse(ranges.startswith("+"))
        self.assertEqual(["До 50", "51–500", "501–5000", "Более 5000"], ranges.split("~")[1:])
        self.assertTrue(rows["svc-084"][2][0].startswith("+"))
        self.assertTrue(rows["svc-046"][2][0].startswith("+"))

    def test_approved_v9_artifact_matches_master(self):
        _, rows = read_briefs()
        path = STAGE / "contact-prototype/ARCHITEKTONICA-brief-v9.html"
        html = path.read_bytes().decode("ascii")
        payload = re.search(r'<script type="application/json" id="brief-data">([\s\S]*?)</script>', html)
        self.assertIsNotNone(payload)
        groups = json.loads(payload[1])
        self.assertNotIn("\ufffd", json.dumps(groups, ensure_ascii=False))
        self.assertEqual([12, 4, 19, 18, 16, 15], [len(g["services"]) for g in groups])
        self.assertEqual("Видео, анимация, визуализация, виртуальные пространства и звук", groups[4]["desc"])
        services = {"svc-" + s["id"]: s for g in groups for s in g["services"]}
        catalogue = json.loads((STAGE / "public-service-catalogue.json").read_text(encoding="utf-8"))
        self.assertEqual({s["id"]: (s["display_title"], s["search_aliases"]) for s in catalogue["services"]},
                         {service: (s["name"], s["aliases"]) for service, s in services.items()})
        self.assertEqual(set(rows), set(services))
        self.assertEqual(344, sum(len(s["questions"]) for s in services.values()))
        for service, (name, desc, questions) in rows.items():
            with self.subTest(service=service):
                s = services[service]
                self.assertEqual((name, desc), (s["name"], s["desc"]))
                expected = []
                for i, raw in enumerate(questions):
                    condition = None
                    if raw.startswith("?"):
                        expr, raw = raw[1:].split(":", 1)
                        index, value = expr.split("=", 1)
                        condition = {"n": int(index), "v": value}
                    multi = raw.startswith("+")
                    label, *opts = raw.lstrip("+").split("~")
                    expected.append({"i": i, "label": label, "multi": multi,
                                     "exclusive": [o[1:] for o in opts if o.startswith("!")],
                                     "opts": [o.lstrip("!") for o in opts], "condition": condition})
                self.assertEqual(expected, s["questions"])


if __name__ == "__main__":
    unittest.main()
