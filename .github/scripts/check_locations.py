#!/usr/bin/env python3
"""Cross-field checks for azure/caf/schema.locations.json that JSON Schema cannot express.

Standard library only. Exit code 1 if any problem is found.
"""
import json
import sys
from collections import defaultdict

PATH = sys.argv[1] if len(sys.argv) > 1 else "azure/caf/schema.locations.json"


def main() -> int:
    with open(PATH, encoding="utf-8") as fh:
        locations = json.load(fh)["locations"]

    by_abbr: dict[str, list[str]] = defaultdict(list)
    for region, abbr in locations.items():
        by_abbr[abbr].append(region)

    problems = [
        f"abbreviation {abbr!r} is used by multiple regions: {', '.join(sorted(regions))}"
        for abbr, regions in sorted(by_abbr.items())
        if len(regions) > 1
    ]

    for p in problems:
        print(f"::error file={PATH}::{p}")
    if problems:
        print(f"{len(problems)} problem(s) found in {PATH}", file=sys.stderr)
        return 1
    print(f"OK: {len(locations)} locations in {PATH} passed cross-field checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
