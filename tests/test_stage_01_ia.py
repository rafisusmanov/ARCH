"""Stage-01 approved IA: immutable 17/81 identities and routes, mutable Stage-02 statuses.

Run: python3 -m unittest discover -s tests -v
These are structural checks, NOT owner approval or browser verification.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'references/project/services_catalogue.json'
MAP = ROOT / 'planning/stage-01/catalogue-map.json'


class Stage01IATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(SRC.read_text(encoding='utf-8'))['services']
        cls.mapping = json.loads(MAP.read_text(encoding='utf-8'))

    def test_no_lost_or_invented_services(self):
        data = self.mapping
        self.assertEqual(data['stage'], '01')
        self.assertIn('Owner confirmed Stage 01 IA 2026-11-01', data['owner_approval'])
        self.assertEqual(len(data['directions']), 17)
        self.assertEqual(len(data['services']), 81)
        canon = [(x['direction'], x['name']) for x in self.source]
        by_id = {x['id']: x for x in data['directions']}
        self.assertEqual(
            sorted(canon),
            sorted((by_id[x['direction_id']]['name'], x['name'])
                   for x in data['services'])
        )

    def test_approved_service_id_mapping_is_immutable(self):
        """Pin 81 ID-to-direction-to-name assignments as approved on 01.11.2026.

        Changes to this baseline require an explicit architecture decision.
        """
        baseline = (ROOT / 'planning/stage-01/approved-service-ids.tsv').read_text(
            encoding='utf-8')
        dirs = {d['id']: d['name'] for d in self.mapping['directions']}
        rows = ['\t'.join((s['id'], s['direction_id'],
                           dirs[s['direction_id']], s['name']))
                for s in sorted(self.mapping['services'], key=lambda x: x['id'])]
        self.assertEqual('\n'.join(rows) + '\n', baseline)
        self.assertEqual(len(rows), 81)

    def test_groups_17_and_urls_unique_and_anchored(self):
        data = self.mapping
        directions, groups, services = data['directions'], data['groups'], data['services']
        grouped = [name for group in groups for name in group['direction_names']]
        self.assertEqual(len(groups), 6)
        self.assertEqual(len(grouped), 17)
        self.assertEqual(set(grouped), {d['name'] for d in directions})
        self.assertEqual(len(set(grouped)), len(grouped))
        self.assertEqual(len({d['id'] for d in directions}), 17)
        self.assertEqual(len({d['proposed_url'] for d in directions}), 17)
        self.assertEqual(len({s['id'] for s in services}), 81)
        self.assertEqual(len({s['proposed_destination'] for s in services}), 81)
        self.assertEqual({s['proposed_surface'] for s in services},
                         {'detail_candidate', 'direction_section'})
        self.assertEqual(sum(s['proposed_surface'] == 'detail_candidate' for s in services), 13)
        group_ids = {g['id'] for g in groups}
        direction_by_id = {d['id']: d for d in directions}
        for d in directions:
            self.assertIn(d['group_id'], group_ids)
            self.assertTrue(d['proposed_url'].startswith('/services/'))
            self.assertEqual(d['count'],
                             sum(s['direction_id'] == d['id'] for s in services))
        for s in services:
            with self.subTest(service=s['id']):
                self.assertIn(s['direction_id'], direction_by_id)
                direction_url = direction_by_id[s['direction_id']]['proposed_url']
                self.assertTrue(s['proposed_destination'].startswith(direction_url))
                if s['proposed_surface'] == 'direction_section':
                    self.assertEqual(s['proposed_destination'], f"{direction_url}#{s['id']}")
                    self.assertIsNone(s['proposed_detail_slug'])
                else:
                    self.assertTrue(s['proposed_destination'].startswith(direction_url + '/'))
                    self.assertTrue(s['proposed_detail_slug'])
                # Stage-02 editorial states may advance without reopening approved IA.
                self.assertIn(s['publication_status'], {
                    'not_approved', 'draft', 'in_review', 'approved', 'published', 'archived'
                })
                self.assertIn(s['locale_status']['ru'], {
                    'needs_stage_02_copy', 'draft', 'in_review', 'approved', 'published', 'archived'
                })
                self.assertIn(s['locale_status']['en'], {
                    'not_translated', 'draft', 'in_review', 'approved', 'published', 'archived'
                })

    def test_stage_boundaries_are_explicit(self):
        a = (ROOT / 'planning/stage-01/IA_PROPOSAL.md').read_text(encoding='utf-8')
        b = (ROOT / 'planning/stage-01/JOURNEYS_AND_URLS.md').read_text(encoding='utf-8')
        for needle in ('approval: owner-approved', '17 направлений', '81', '/careers', '/services'):
            self.assertIn(needle, a)
        for needle in ('W1-A1', 'W1-A2', 'W1-P', '/project', '/contact?service=svc-NNN'):
            self.assertIn(needle, b)


    def test_independent_careers_and_search_naming(self):
        a = (ROOT / 'planning/stage-01/IA_PROPOSAL.md').read_text(encoding='utf-8')
        b = (ROOT / 'planning/stage-01/JOURNEYS_AND_URLS.md').read_text(encoding='utf-8')
        seo = (ROOT / 'planning/stage-01/SEO_NAMING_POLICY.md').read_text(encoding='utf-8')
        self.assertIn('/careers', a)
        self.assertIn('/careers/<vacancy-slug>', a)
        self.assertIn('/careers', b)
        self.assertIn('JobPosting', b)
        self.assertTrue(seo.strip(), 'SEO naming policy must not be empty')
        self.assertEqual(self.mapping['seo_naming_policy'], 'planning/stage-01/SEO_NAMING_POLICY.md')
        self.assertEqual(self.mapping['careers_route'], '/careers')
        self.assertEqual(len(self.mapping['services']), 81)
