#!/usr/bin/env python3
"""Read-only integrity checks; not a substitute for editorial or browser review."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import unquote

from skill_catalog import ROOT, discover
from sync_skills import sync

ORIGINAL_AUTHOR_SKILLS = {
    'architektonica-creative-director', 'architektonica-reader-insight',
    'architektonica-idea-lab', 'architektonica-narrative-design',
    'architektonica-psycholinguistic-editor', 'architektonica-critical-editor',
    'architektonica-search-visibility', 'architektonica-engine-mapper',
    'architektonica-portfolio-case-writer',
}
WEB_RESOURCES = {
    'emil-design-eng': [], 'animate': ['RECIPES.md'], 'animation-performance': [],
    'find-animation-opportunities': [], 'improve-animations': ['AUDIT.md', 'PLAN-TEMPLATE.md'],
    'review-animations': ['STANDARDS.md'], 'prototype': ['PICKER.md'],
    'mobile-native': [], 'break-ui': ['CATALOG.md'],
}
# Preservation baseline, not an allowlist: all additional skill folders are validated.
REQUIRED_SKILLS = ORIGINAL_AUTHOR_SKILLS | {'architektonica-ui-ux-expert', 'architektonica-website-qa'} | set(WEB_RESOURCES)
PLAN_PATH = 'references/project/ARCHITEKTONICA_SITE_PLAN_V2.md'
# Full owner-approved v2 baseline, including the final clarification on 2026-10-31.
# Update this digest only alongside an explicitly approved plan revision.
PLAN_SHA256 = '9d9ff918e9af64fb81fe7c6d28348104828784c53b593290c038268af63fe4d7'
POSITIONING_DOCS = [
    'AGENTS.md', 'PROJECT_SYSTEM_PROMPT.md', 'references/project/MASTER_INSTRUCTION.md',
    'references/project/01_Architektonica_Brand_Core.md',
    'references/project/02_Architektonica_Fact_Bank.md',
    'references/project/05_Architektonica_Language.md',
    'references/project/08_Architektonica_Site_Content_Plan.md',
]
CRITICAL = [
    'methods/portfolio-case-workflow.md', 'samples/05_portfolio_from_one_message.md',
    'PROJECT_SYSTEM_PROMPT.md', 'QUICK_START.md', 'methods/research-evidence-map.md',
    'methods/engine-template-adaptation.md', 'methods/ui-ux-pro-max-integration.md',
    'references/research/Architektonica_реестры_исследования.xlsx',
    'references/template/Тексты шаблона Architektonica (Engine).xlsx',
    'third_party/emil-skills-LICENSE', PLAN_PATH,
]
VENDOR_FILES = [
    'LICENSE', 'SKILL.md', 'scripts/search.py', 'scripts/core.py',
    'scripts/design_system.py', 'scripts/reasoning_contract.py',
    'references/pro-rules.md', 'references/quick-reference.md',
    'design-system/token-architecture.md', 'design-system/component-specs.md',
    'design-system/primitive-tokens.md', 'design-system/semantic-tokens.md',
    'design-system/component-tokens.md', 'design-system/states-and-variants.md',
]
ROOT_PREFIXES = ('skills/', '.agents/', 'references/', 'methods/', 'samples/',
                 'scripts/', 'prompts/', 'third_party/', '.github/')

def local_references(text):
    """Literal Markdown links and inline repository paths; not example code/URLs.

    Inline root-prefixed paths resolve locally first, then from the repository.
    Markdown links and ./ ../ references are always relative to their document.
    Generated paths/placeholders in code examples are not asserted to exist.
    """
    text = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*(?:\n|$)', '', text, flags=re.M | re.S)
    for match in re.finditer(r'\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)(?:\s+"[^"]*")?\)', text):
        yield match[1].strip('<>'), False
    for match in re.finditer(r'(?<!`)`([^`\n]+)`(?!`)', text):
        ref = match[1]
        if ref.startswith(('../', './', *ROOT_PREFIXES)) and not re.search(r'[<>*{}|\n]', ref):
            yield ref, ref.startswith(ROOT_PREFIXES)

def check_references(root, path, errors):
    for ref, root_relative in local_references(path.read_text(encoding='utf-8')):
        # Preserve this audit's historical reference to the removed skill.
        # No other document or target is exempt from local-link validation.
        if (path.relative_to(root).as_posix() == 'methods/source-audit-and-portfolio-rules.md'
                and ref == '../skills/architektonica-copy-studio/SKILL.md'):
            continue
        if re.match(r'^[\w+.-]+:', ref) or ref.startswith(('#', '/')):
            continue
        target = unquote(ref.split('#', 1)[0].split('?', 1)[0])
        candidate = path.parent / target
        if root_relative and not candidate.exists():
            candidate = root / target
        candidate = candidate.resolve()
        if not candidate.is_relative_to(root) or not candidate.exists():
            errors.append(f'Broken local reference: {path.relative_to(root)} -> {ref}')

def check_catalogue(root, errors):
    catalogue = json.loads((root / 'references/project/services_catalogue.json').read_text())['services']
    table = (root / 'references/project/Услуги_дополнительный_перечень.md').read_text()
    actual = []
    for line in table.splitlines():
        if line.startswith('| ') and not line.startswith('| Направление'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) == 3:
                actual.append(dict(zip(('direction', 'name', 'scope'), cells)))
    if catalogue != actual:
        errors.append('Canonical catalogue differs from synchronized source table')
    if len(catalogue) != 81 or len({x['direction'] for x in catalogue}) != 17:
        errors.append('Expected 17 directions / 81 services')
    if len({(x['direction'], x['name']) for x in catalogue}) != 81:
        errors.append('Duplicate catalogue entry')
    services = (root / 'references/project/04_Architektonica_Services.md').read_text()
    for item in catalogue:
        if '**' + item['name'] + '**' not in services:
            errors.append('Missing service in Services: ' + item['name'])
    for rel in POSITIONING_DOCS:
        text = (root / rel).read_text()
        if 'ARCHITEKTONICA — Архитектура решений.' not in text or 'Технологии · Дизайн · Бизнес' not in text:
            errors.append('Missing approved positioning: ' + rel)

# The package verifier checks machine-verifiable integrity only. Editorial
# authorship is governed by the single route in engine-template-adaptation.md;
# human-language conflicts require focused editorial review, not regex linting.

def approved_service_id_errors(mapping, expected):
    """Compare all owner-approved ID/direction/name assignments, order-independent."""
    directions = {d['id']: d['name'] for d in mapping['directions']}
    records = sorted((s['id'], s['direction_id'], directions[s['direction_id']], s['name'])
                     for s in mapping['services'])
    rows = [tuple(line.split('\t')) for line in expected.splitlines() if line]
    problems = []
    if (len(records), len(rows)) != (81, 81) or len(set(records)) != 81:
        problems.append('Approved service ID baseline must contain 81 unique records')
    if len(rows) != len(set(rows)) or any(len(row) != 4 for row in rows):
        problems.append('Approved service ID baseline is invalid')
    if records != sorted(rows):
        problems.append('Approved service ID → direction → name assignments changed')
    return problems

def check_approved_service_ids(root, errors):
    mapping = json.loads((root / 'planning/stage-01/catalogue-map.json').read_text(encoding='utf-8'))
    baseline = (root / 'planning/stage-01/approved-service-ids.tsv').read_text(encoding='utf-8')
    errors.extend(approved_service_id_errors(mapping, baseline))

def check_vendor(root, errors):
    vendor = root / 'third_party/ui-ux-pro-max'
    for rel in VENDOR_FILES:
        if not (vendor / rel).is_file():
            errors.append(f'Missing vendor file: {rel}')
    spec = importlib.util.spec_from_file_location('curated_core_validation', vendor / 'scripts/core.py')
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    configs = list(core.CSV_CONFIG.values()) + [
        dict(cfg, **core._STACK_COLS) for cfg in core.STACK_CONFIG.values()
    ]
    configs.append({'file': 'ui-reasoning.csv', 'search_cols': ['UI_Category', 'Decision_Rules']})
    for cfg in configs:
        path = vendor / 'data' / cfg['file']
        try:
            with path.open(encoding='utf-8-sig', newline='') as handle:
                reader = csv.DictReader(handle, strict=True)
                required = set(cfg.get('search_cols', []))
                if not required.issubset(reader.fieldnames or []):
                    errors.append(f'Invalid CSV headers: {cfg["file"]}; missing {sorted(required - set(reader.fieldnames or []))}')
                rows = list(reader)
                if not rows or any(None in row or any(v is None for v in row.values()) for row in rows):
                    errors.append(f'Empty or malformed CSV: {cfg["file"]}')
        except (OSError, UnicodeError, csv.Error) as exc:
            errors.append(f'Invalid vendor CSV {cfg["file"]}: {exc}')
    for path in [vendor / 'LICENSE', root / 'third_party/emil-skills-LICENSE']:
        if not path.is_file() or 'MIT License' not in path.read_text():
            errors.append(f'Missing MIT license: {path.relative_to(root)}')

def verify(root=ROOT):
    root = Path(root).resolve()
    records, errors = discover(root)
    found = {record['name'] for record in records}
    if REQUIRED_SKILLS - found:
        errors.append(f'Missing required skills: {sorted(REQUIRED_SKILLS - found)}')
    errors.extend(sync(root, check=True))
    for name, resources in WEB_RESOURCES.items():
        for resource in resources:
            if not (root / 'skills' / name / resource).is_file():
                errors.append(f'Missing web skill resource: {name}/{resource}')
    for rel in CRITICAL:
        if not (root / rel).is_file():
            errors.append(f'Missing: {rel}')
    for path in root.rglob('*'):
        if any(part in {'.git', '__pycache__', '.venv'} for part in path.parts) or not path.is_file():
            continue
        if path.suffix in {'.md', '.py', '.php', '.js', '.json', '.yml', '.yaml'}:
            text = path.read_text(encoding='utf-8')
            if re.search(r'^(?:<{7}|={7}|>{7})(?: |$)', text, re.M):
                errors.append(f'Unresolved merge marker: {path.relative_to(root)}')
            if path.suffix == '.md':
                check_references(root, path, errors)
    for label, check in [('Catalogue', check_catalogue), ('Approved service IDs', check_approved_service_ids),
                         ('Vendor', check_vendor)]:
        try:
            check(root, errors)
        except (OSError, KeyError, TypeError, ValueError) as exc:
            errors.append(f'{label} validation failed: {exc}')
    plan = root / PLAN_PATH
    if plan.is_file() and hashlib.sha256(plan.read_bytes()).hexdigest() != PLAN_SHA256:
        errors.append('Approved roadmap v2 changed or truncated; review the full owner-approved text')
    return records, list(dict.fromkeys(errors))

def main():
    records, errors = verify()
    print(f'Skills: {len(records)}; baseline: {len(REQUIRED_SKILLS)}; errors: {len(errors)}')
    for error in errors:
        print('ERROR', error)
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
