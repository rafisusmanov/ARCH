#!/usr/bin/env python3
"""ARCH task routing: validate catalogue, prepare work, inspect supplied read traces.

Static CI verifies the declared routing and integrity of references. Trace checks
verify completeness of a *supplied* external tool log; they cannot authenticate
log origin or prove that a model understood the material.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml

from skill_catalog import ROOT, UniqueKeyLoader, discover

MATRIX = "methods/task-skill-matrix.yaml"
STAGES = {f"{i:02d}" for i in range(1, 8)}
TASK_RE = re.compile(r"^[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$")
CONDITION_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SITE_PRINCIPLE = "Сайт должен быть понятен без чтения. Интересен при просмотре. И содержателен при углублении."
PRIORITY_CHECKS = ("understand_without_reading", "interesting_when_viewing", "depth_on_demand")
SERVICE_ROUTES = {"content.services-overview", "content.service-detail", "ia.service-taxonomy"}
FIELDS = {
    "id", "stage", "description", "required_skills", "conditional_skills",
    "explicit_only_skills", "required_sources", "deliverable",
    "acceptance_checks", "stop_conditions",
}


def safe_path(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return None
    target = (Path(root) / path).resolve()
    if not target.is_relative_to(Path(root).resolve()):
        return None
    return target


def load_matrix(root=ROOT):
    path = Path(root) / MATRIX
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UniqueKeyLoader)


def _unique_strings(values, name, errors, required=True):
    if not isinstance(values, list) or (required and not values):
        errors.append(f"{name}: expected {'nonempty ' if required else ''}list")
        return []
    if any(not isinstance(v, str) or not v.strip() for v in values):
        errors.append(f"{name}: invalid string")
        return []
    if len(values) != len(set(values)):
        errors.append(f"{name}: duplicate values")
    return values


def verify_matrix(root=ROOT, matrix=None, records=None):
    root = Path(root)
    errors = []
    if matrix is None:
        try:
            matrix = load_matrix(root)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            return None, [f"matrix cannot be read: {exc}"]
    if not isinstance(matrix, dict):
        return None, ["matrix: expected YAML mapping"]
    if records is None:
        records, errors_from_discover = discover(root)
        errors.extend(errors_from_discover)
    names = {s["name"] for s in records}
    restricted = {s["name"] for s in records if s["activation"] == "explicit-only"}
    if matrix.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    ids = matrix.get("stage_ids")
    if not isinstance(ids, list) or set(ids) != STAGES or len(ids) != 7:
        errors.append("stage_ids must contain exactly stages 01..07")
    stages = matrix.get("stages")
    if not isinstance(stages, dict) or set(stages) != STAGES:
        errors.append("stages must cover 01..07")
    elif any(not isinstance(x, dict) or not str(x.get("label", "")).strip() for x in stages.values()):
        errors.append("stages require nonempty labels")
    policy = matrix.get("policy")
    if not isinstance(policy, dict) or not all(policy.get(k) for k in (
        "unlisted_task", "source_missing", "explicit_only",
        "evidence_without_tool_trace", "owner_approval",
    )):
        errors.append("policy: mandatory fail-closed behavior missing")
    compat = policy.get("compatibility", {}) if isinstance(policy, dict) else {}
    if not isinstance(compat, dict) or compat.get("live_catalogue") != "6/17/84" or not str(compat.get("legacy_ids", "")).startswith("81"):
        errors.append("policy: current public catalogue/legacy compatibility missing")
    priority = policy.get("priority_gate", {}) if isinstance(policy, dict) else {}
    if priority != {"source": "AGENTS.md", "principle": SITE_PRINCIPLE,
                    "required_checks": list(PRIORITY_CHECKS), "failure": "BLOCK_PROPOSAL_AND_REVISE"}:
        errors.append("policy: mandatory site-principle gate missing or changed")
    for source in ("AGENTS.md", "PROJECT_SYSTEM_PROMPT.md"):
        target = root / source
        if not target.is_file() or SITE_PRINCIPLE not in "\n".join(target.read_text(encoding="utf-8").splitlines()[:12]):
            errors.append(f"priority principle must appear at the start of {source}")
    tasks = matrix.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return matrix, errors + ["tasks: nonempty list required"]
    seen_ids, covered, used_stages = set(), set(), set()
    for i, task in enumerate(tasks):
        prefix = f"tasks[{i}]"
        if not isinstance(task, dict):
            errors.append(f"{prefix}: not a mapping")
            continue
        missing = FIELDS - set(task)
        unknown = set(task) - FIELDS - {"explicit_trigger_required"}
        if missing or unknown:
            errors.append(f"{prefix}: missing {sorted(missing)}, extra {sorted(unknown)}")
        ident = task.get("id")
        if not isinstance(ident, str) or not TASK_RE.fullmatch(ident):
            errors.append(f"{prefix}: invalid id")
        elif ident in seen_ids:
            errors.append(f"{prefix}: duplicate id {ident}")
        else:
            seen_ids.add(ident)
        stage = task.get("stage")
        if stage not in STAGES:
            errors.append(f"{prefix}: invalid stage {stage!r}")
        else:
            used_stages.add(stage)
        for field in ("description", "deliverable"):
            if not isinstance(task.get(field), str) or not task[field].strip():
                errors.append(f"{prefix}: missing {field}")
        required = _unique_strings(task.get("required_skills"), prefix + ".required_skills", errors)
        explicit = _unique_strings(task.get("explicit_only_skills"), prefix + ".explicit_only_skills", errors, False)
        if task.get("explicit_trigger_required", False) is not False and task.get("explicit_trigger_required") is not True:
            errors.append(f"{prefix}: explicit_trigger_required must be boolean")
        if task.get("explicit_trigger_required") is True and not explicit:
            errors.append(f"{prefix}: explicit_trigger_required needs an explicit-only skill")
        if set(required) & restricted:
            errors.append(f"{prefix}: explicit-only skill cannot be required automatically")
        if any(s not in names for s in required + explicit):
            errors.append(f"{prefix}: unknown skill in required/explicit set")
        if set(explicit) - restricted:
            errors.append(f"{prefix}: explicit_only_skills must have disable-model-invocation true")
        cond = task.get("conditional_skills")
        conditional_names = []
        conditions = set()
        if not isinstance(cond, list):
            errors.append(f"{prefix}: conditional_skills must be a list")
        else:
            for c in cond:
                if not isinstance(c, dict) or set(c) != {"when", "skill"}:
                    errors.append(f"{prefix}: condition needs only when/skill")
                    continue
                when, skill = c["when"], c["skill"]
                if not isinstance(when, str) or not CONDITION_RE.fullmatch(when) or when in conditions:
                    errors.append(f"{prefix}: invalid or duplicate condition")
                else:
                    conditions.add(when)
                if skill not in names or skill in restricted:
                    errors.append(f"{prefix}: missing or explicit-only conditional skill")
                conditional_names.append(skill)
        if set(required) & (set(explicit) | set(conditional_names)):
            errors.append(f"{prefix}: skill appears as required and conditional/explicit")
        covered.update(required)
        covered.update(explicit)
        covered.update(conditional_names)
        sources = _unique_strings(task.get("required_sources"), prefix + ".required_sources", errors)
        for p in sources:
            target = safe_path(root, p)
            if not target or not target.is_file():
                errors.append(f"{prefix}: missing/unsafe source {p}")
        _unique_strings(task.get("acceptance_checks"), prefix + ".acceptance_checks", errors)
        _unique_strings(task.get("stop_conditions"), prefix + ".stop_conditions", errors)
        if "missing_required_source" not in task.get("stop_conditions", []):
            errors.append(f"{prefix}: must stop on missing_required_source")
    if used_stages != STAGES:
        errors.append(f"tasks do not cover stages {sorted(STAGES - used_stages)}")
    if covered != names:
        errors.append(f"skill coverage mismatch: missing={sorted(names-covered)}, unknown={sorted(covered-names)}")
    for ident in ("content.next-task", "content.services-overview", "content.service-detail"):
        route = next((t for t in tasks if isinstance(t, dict) and t.get("id") == ident), {})
        required = {"architektonica-ui-ux-expert", "architektonica-critical-editor"}
        criteria = {"progressive_disclosure", "no_flat_catalogue", "no_automatic_detail_pages"}
        sources = {"planning/stage-01/IA_PROPOSAL.md", "planning/stage-02/public-service-catalogue.json",
                   "planning/stage-02/services-page-acceptance.md", "planning/stage-02/WORK_MAP.md"}
        for field, expected in (("required_skills", required), ("acceptance_checks", criteria),
                                ("required_sources", sources)):
            if (not isinstance(route.get(field), list)
                    or any(not isinstance(item, str) for item in route[field])
                    or not expected.issubset(route[field])):
                errors.append(f"{ident}: mandatory service disclosure gate missing {field}")
    if not errors and Path(root).resolve() == ROOT.resolve():
        errors.extend(verify_fixture_bindings(root, matrix))
    return matrix, list(dict.fromkeys(errors))



def verify_fixture_bindings(root, matrix):
    """Behavioral evaluation prompts must match canonical required skills."""
    path = Path(root) / "tests/fixtures/skill-evaluation-cases.json"
    try:
        fixtures = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"evaluation fixtures unreadable: {exc}"]
    errors = []
    if not isinstance(fixtures, list):
        return ["evaluation fixtures must be a list"]
    tasks = {t["id"]: t for t in matrix["tasks"] if isinstance(t, dict) and "id" in t}
    seen = set()
    stages = set()
    for case in fixtures:
        if not isinstance(case, dict):
            errors.append("fixture entry must be a mapping")
            continue
        ident = case.get("id")
        route = case.get("routing_task_id")
        if not isinstance(ident, str) or ident in seen:
            errors.append(f"fixture has missing or duplicate id {ident!r}")
        seen.add(ident)
        if route not in tasks:
            errors.append(f"fixture {ident}: unknown routing_task_id {route!r}")
            continue
        task = tasks[route]
        stages.add(task["stage"])
        if not isinstance(case.get("skills"), list) or set(case["skills"]) != set(task["required_skills"]):
            errors.append(f"fixture {ident}: skills differ from required_skills for {route}")
        explicit_selected = case.get("explicit_requested_skills", [])
        if not isinstance(explicit_selected, list):
            errors.append(f"fixture {ident}: explicit_requested_skills must be list")
        elif set(explicit_selected) - set(task["explicit_only_skills"]):
            errors.append(f"fixture {ident}: explicit skill not permitted by route")
        elif task.get("explicit_trigger_required") and not explicit_selected:
            errors.append(f"fixture {ident}: missing explicit invocation for explicit-only task")
        if not isinstance(case.get("must_check"), list) or not case["must_check"]:
            errors.append(f"fixture {ident}: must_check missing")
    if stages != STAGES:
        errors.append(f"behavioral fixtures lack stages {sorted(STAGES-stages)}")
    return errors

def task_by_id(matrix, task_id):
    return next((t for t in matrix["tasks"] if t["id"] == task_id), None)


def expected_for_task(task, conditions=(), user_requested_explicit=()):
    defined = {c["when"]: c["skill"] for c in task["conditional_skills"]}
    unknown = set(conditions) - defined.keys()
    if unknown:
        raise ValueError(f"unknown conditions: {sorted(unknown)}")
    permitted = set(task["explicit_only_skills"])
    unauthorized = set(user_requested_explicit) - permitted
    if task.get("explicit_trigger_required", False) and not set(user_requested_explicit):
        raise ValueError("explicit user invocation required; task cannot start automatically")
    if unauthorized:
        raise ValueError(f"explicit-only skills not permitted by this task: {sorted(unauthorized)}")
    return (
        set(task["required_skills"])
        | {defined[c] for c in conditions}
        | set(user_requested_explicit)
    )


def make_plan(root, matrix, task_id, conditions=(), user_requested_explicit=()):
    task = task_by_id(matrix, task_id)
    if not task:
        raise ValueError(f"unlisted task {task_id}: BLOCK_AND_ROUTE_FOR_REVIEW")
    chosen = expected_for_task(task, conditions, user_requested_explicit)
    skill_paths = [f"skills/{name}/SKILL.md" for name in sorted(chosen)]
    return {
        "task_id": task_id,
        "stage": task["stage"],
        "conditions": list(conditions),
        "explicit_user_request": list(user_requested_explicit),
        "priority_gate": matrix["policy"]["priority_gate"],
        "source_paths_to_read": list(dict.fromkeys(["AGENTS.md", "PROJECT_SYSTEM_PROMPT.md"] + task["required_sources"])),
        "skill_paths_to_read": skill_paths,
        "deliverable": task["deliverable"],
        "acceptance_checks": list(dict.fromkeys(list(PRIORITY_CHECKS) + task["acceptance_checks"])),
        "stop_conditions": ["site_principle_failed"] + task["stop_conditions"],
        "approval": "NOT APPROVED until owner explicitly accepts this deliverable",
        "trace_authentication": "Tool-call records must be independently supplied; self-report does not prove reads.",
    }


def check_proposal(root, matrix, proposal):
    """Fail closed on missing/contradictory decision metadata; NOT a semantic model evaluator."""
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    task = proposal.get("task_id")
    if not task_by_id(matrix, task):
        return ["unlisted proposal task"]
    errors = []
    if not isinstance(proposal.get("decision"), str) or not proposal["decision"].strip():
        errors.append("decision is required")
    checks = proposal.get("principle_checks")
    if not isinstance(checks, dict) or set(checks) != set(PRIORITY_CHECKS):
        errors.append("all three site-principle checks are required")
    else:
        for key in PRIORITY_CHECKS:
            check = checks[key]
            if (not isinstance(check, dict) or check.get("verdict") != "PASS"
                    or not isinstance(check.get("reason"), str) or not check["reason"].strip()):
                errors.append(f"{key}: explicit PASS and concrete reason required; revise proposal")
    scope = proposal.get("scope")
    if scope not in ("services", "other"):
        errors.append("scope must be services or other")
    if task in SERVICE_ROUTES and scope != "services":
        errors.append("service route requires service scope")
    if scope != "services":
        if "service_plan" in proposal:
            errors.append("service plan must use services scope")
        return errors
    plan = proposal.get("service_plan")
    if not isinstance(plan, dict):
        return errors + ["service scope requires service_plan"]
    catalogue = json.loads((Path(root) / "planning/stage-02/public-service-catalogue.json").read_text(encoding="utf-8"))
    public = {s["id"] for s in catalogue["services"]}
    candidates = {s["id"] for s in catalogue["services"] if s["detail_page_candidate"]}
    ids = _unique_strings(plan.get("service_ids"), "service_ids", errors)
    selected = set(ids)
    if selected - public:
        errors.append("unknown/excluded public service ID")
    if plan.get("coverage") not in ("all", "selected"):
        errors.append("service coverage must be all or selected")
    elif plan["coverage"] == "all" and selected != public:
        errors.append("all coverage must include exactly the current public catalogue")
    if task == "content.services-overview" and plan.get("coverage") != "all":
        errors.append("overview requires full coverage")
    if task == "content.service-detail" and (plan.get("coverage") != "selected" or len(selected) != 1):
        errors.append("service-detail requires exactly one selected service")
    if plan.get("disclosure") != "progressive_on_demand":
        errors.append("services must use progressive on-demand disclosure")
    expanded = _unique_strings(plan.get("default_expanded_ids"), "default_expanded_ids", errors, False)
    if set(expanded) - selected:
        errors.append("expanded services outside selected scope")
    if len(selected) > 1 and set(expanded) == selected:
        errors.append("flat full-detail catalogue is forbidden")
    pages = plan.get("detail_page_candidates")
    if not isinstance(pages, list):
        return errors + ["detail_page_candidates must be an explicit list (may be empty)"]
    seen = set()
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("id"), str):
            errors.append("invalid detail-page candidate")
            continue
        sid = page["id"]
        if sid in seen or sid not in selected or sid not in candidates:
            errors.append(f"{sid}: separate detail requires an existing eligible candidate; no automatic pages")
        seen.add(sid)
        if not isinstance(page.get("reason"), str) or not page["reason"].strip():
            errors.append(f"{sid}: independent reader need and content justification required")
        if page.get("status") != "proposed_not_approved":
            errors.append(f"{sid}: candidate is not an owner-approved page")
    return errors


def audit_read_trace(root, matrix, trace):
    """Check evidence completeness, NOT authenticity of supplied tool records."""
    if not isinstance(trace, dict):
        return ["trace: JSON object required"]
    task_id = trace.get("task_id")
    task = task_by_id(matrix, task_id)
    if not task:
        return ["trace: task is absent from matrix"]
    conditions = trace.get("conditions", [])
    explicit = trace.get("explicit_user_request", [])
    if not isinstance(conditions, list) or not isinstance(explicit, list):
        return ["trace: conditions and explicit_user_request must be arrays"]
    try:
        plan = make_plan(root, matrix, task_id, conditions, explicit)
    except ValueError as exc:
        return [str(exc)]
    wanted = set(plan["skill_paths_to_read"] + plan["source_paths_to_read"])
    events = trace.get("events")
    if not isinstance(events, list):
        return ["trace: events array required"]
    observed, errors = set(), []
    for i, event in enumerate(events):
        if not isinstance(event, dict):
            errors.append(f"events[{i}]: object expected")
            continue
        if event.get("type") != "file_read" or event.get("origin") != "tool_log":
            errors.append(f"events[{i}]: only tool_log file_read evidence accepted")
            continue
        path = event.get("path")
        target = safe_path(root, path)
        if target is None or not target.is_file():
            errors.append(f"events[{i}]: unsafe or nonexistent path")
            continue
        sha = event.get("sha256")
        if not isinstance(sha, str) or sha != hashlib.sha256(target.read_bytes()).hexdigest():
            errors.append(f"events[{i}]: sha256 does not match {path}")
            continue
        if not event.get("tool_call_id"):
            errors.append(f"events[{i}]: tool_call_id required")
            continue
        observed.add(path)
    missing = wanted - observed
    if missing:
        errors.append(f"missing actual source-read records: {sorted(missing)}")
    explicit_paths = {f"skills/{s}/SKILL.md" for s in ("prototype", "review-animations")}
    unexpected = (observed & explicit_paths) - set(plan["skill_paths_to_read"])
    if unexpected:
        errors.append(f"explicit-only read without user request: {sorted(unexpected)}")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "plan", "audit", "preflight"))
    parser.add_argument("--task", help="Exact registered task id")
    parser.add_argument("--condition", action="append", default=[], help="Active condition; repeatable")
    parser.add_argument("--explicit", action="append", default=[], help="User explicitly invoked skill; repeatable")
    parser.add_argument("--trace", type=Path, help="JSON tool-read trace for audit")
    parser.add_argument("--proposal", type=Path, help="JSON decision record for preflight")
    args = parser.parse_args(argv)
    matrix, errors = verify_matrix()
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    if args.command == "validate":
        print(json.dumps({"status": "STRUCTURE_PASS", "tasks": len(matrix["tasks"]),
                          "stages": 7, "catalogue": "dynamic"}, ensure_ascii=False))
        return 0
    try:
        if args.command == "preflight":
            if args.proposal is None:
                raise ValueError("preflight requires --proposal")
            proposal = json.loads(args.proposal.read_text(encoding="utf-8"))
            err = check_proposal(ROOT, matrix, proposal)
            print(json.dumps({"status": "FAIL" if err else "PROPOSAL_STRUCTURE_PASS",
                              "errors": err, "note": "Structure only; reasons and actual UX require critical review, not self-certified PASS."}, ensure_ascii=False, indent=2))
            return bool(err)
        if args.command == "plan":
            result = make_plan(ROOT, matrix, args.task, args.condition, args.explicit)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.trace is None:
            raise ValueError("audit requires --trace from exported tool events")
        trace = json.loads(args.trace.read_text(encoding="utf-8"))
        err = audit_read_trace(ROOT, matrix, trace)
        print(json.dumps({"status": "TRACE_COVERAGE_UNAUTHENTICATED" if not err else "FAIL",
                          "errors": err,
                          "note": "Supplied log origin is NOT cryptographically authenticated; human QA remains necessary."},
                         ensure_ascii=False, indent=2))
        return bool(err)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
