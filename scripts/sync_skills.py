#!/usr/bin/env python3
"""Generate .agents mirrors, rebasing repository references. Never delete files."""
import argparse
from pathlib import Path

from skill_catalog import ROOT, discover, mirror_bytes


def sync(root=ROOT, check=False):
    root = Path(root).resolve()
    _, errors = discover(root)
    sources = {p.relative_to(root / "skills"): p for p in (root / "skills").rglob("*") if p.is_file()}
    target = root / ".agents/skills"
    if (root / ".agents").is_symlink() or target.is_symlink() or any(p.is_symlink() for p in target.rglob("*")):
        errors.append(".agents/skills must not contain symlinks")
    for path in target.rglob("*"):
        if path.is_file() and path.relative_to(target) not in sources:
            errors.append(f"Orphan mirror file (review manually): {path.relative_to(root)}")
    if errors:
        return errors  # Do not partially write an invalid skill set.
    for rel, source in sources.items():
        destination = target / rel
        expected = mirror_bytes(source, root)
        if not destination.is_file() or destination.read_bytes() != expected:
            if check:
                errors.append(f"Missing or stale mirror: {destination.relative_to(root)}")
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(expected)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read-only comparison")
    args = parser.parse_args()
    errors = sync(check=args.check)
    for error in errors:
        print(f"ERROR {error}")
    print(f"Mirror {'check' if args.check else 'sync'}: {len(errors)} errors")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
