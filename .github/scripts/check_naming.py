#!/usr/bin/env python3
"""Cross-field checks for azure/caf/schema.naming.json that JSON Schema cannot express.

Standard library only. Exit code 1 if any problem is found.
"""
import json
import re
import sys
from collections import Counter

PATH = sys.argv[1] if len(sys.argv) > 1 else "azure/caf/schema.naming.json"


def main() -> int:
    with open(PATH, encoding="utf-8") as fh:
        data = json.load(fh)

    problems: list[str] = []
    resources = data["resources"]

    counts = Counter(r["resourceType"] for r in resources)
    for name, n in sorted(counts.items()):
        if n > 1:
            problems.append(f"resourceType {name!r} appears {n} times")

    known = set(counts)
    for i, r in enumerate(resources):
        where = f"resources[{i}] ({r['resourceType']})"
        if r["minLength"] > r["maxLength"]:
            problems.append(f"{where}: minLength {r['minLength']} > maxLength {r['maxLength']}")
        if r["deprecatedBy"] and r["deprecatedBy"] not in known:
            problems.append(f"{where}: deprecatedBy {r['deprecatedBy']!r} is not a known resourceType")
        if r["validationRegex"]:
            try:
                re.compile(r["validationRegex"])
            except re.error as exc:
                problems.append(f"{where}: validationRegex does not compile: {exc}")

    for p in problems:
        print(f"::error file={PATH}::{p}")
    if problems:
        print(f"{len(problems)} problem(s) found in {PATH}", file=sys.stderr)
        return 1
    print(f"OK: {len(resources)} resources in {PATH} passed cross-field checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
