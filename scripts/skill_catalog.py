#!/usr/bin/env python3
"""Discover skills from disk; list metadata/resources without invoking any skill."""
import argparse
import json
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys rather than silently replacing activation flags."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError(f"duplicate or non-string YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError("missing or unclosed YAML frontmatter")
    data = yaml.load(match[1], Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    for key in ("name", "description"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"{key} must be a non-empty string")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["name"]):
        raise ValueError("name must use lowercase letters, digits and single hyphens")
    if data["name"] != path.parent.name:
        raise ValueError("name differs from directory name")
    for key in ("disable-model-invocation", "user-invocable"):
        if key in data and type(data[key]) is not bool:
            raise ValueError(f"{key} must be a YAML boolean")
    return data


def discover(root=ROOT):
    root = Path(root).resolve()
    records, errors = [], []
    if not (root / "skills").is_dir() or (root / "skills").is_symlink():
        return [], ["skills must be a real directory in the repository"]
    for directory in sorted((root / "skills").iterdir()):
        if not directory.is_dir():
            continue
        path = directory / "SKILL.md"
        try:
            if directory.is_symlink() or any(p.is_symlink() for p in directory.rglob("*")):
                raise ValueError("skill trees must not contain symlinks")
            data = frontmatter(path)
            records.append({
                "name": data["name"], "description": data["description"],
                "activation": "explicit-only" if data.get("disable-model-invocation", False) else "by-task",
                "disable-model-invocation": data.get("disable-model-invocation", False),
                "user-invocable": data.get("user-invocable", True),
                "path": str(path.relative_to(root)),
                "resources": [str(p.relative_to(root)) for p in sorted(directory.rglob("*"))
                              if p.is_file() and p != path],
            })
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    return records, errors


def mirror_bytes(source, root=ROOT):
    """Rebase external ../ references; local recipes and sibling skills stay local."""
    root = Path(root).resolve()
    source = Path(source).resolve()
    destination = root / ".agents" / source.relative_to(root)
    data = source.read_bytes()
    if source.suffix != ".md":
        return data

    def rebase(match):
        import os
        anchor = (source.parent / match[0]).resolve()
        if not anchor.is_relative_to(root):
            return match[0]  # The reference validator reports escaping paths.
        if anchor.is_relative_to(root / "skills"):
            anchor = root / ".agents" / anchor.relative_to(root)
        return os.path.relpath(anchor, destination.parent).replace(os.sep, "/").rstrip("/") + "/"

    return re.sub(r"(?<![\w./])(?:\.\./)+", rebase, data.decode("utf-8")).encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    records, errors = discover()
    if args.json:
        print(json.dumps({"skills": records, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        for item in records:
            print(f"{item['name']} [{item['activation']}] — {item['description']}")
            print(f"  Read: {item['path']}")
            for path in item["resources"]:
                print(f"  Resource: {path}")
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"Discovered: {len(records)}; errors: {len(errors)}")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
