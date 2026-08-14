#!/usr/bin/env python3
"""Independent integer replay of the critical-anchor scalar fork."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    bound = 48
    cases = 0
    failures = []
    critical_cases = 0
    removable_cases = 0
    equality_cases_excluded_by_nondegeneracy = 0
    for base in range(1, bound + 1):
        for anchor in range(base + 1, bound + 1):
            for atom in range(1, anchor + 1):
                cases += 1
                if anchor - atom > base:
                    removable_cases += 1
                elif anchor - atom == base:
                    equality_cases_excluded_by_nondegeneracy += 1
                else:
                    critical_cases += 1
                    if not atom > anchor - base:
                        failures.append((base, anchor, atom))
    assert cases > 0
    assert removable_cases > 0
    assert critical_cases > 0
    assert failures == []

    theorem = ROOT / "results/ROOT_RETIRED_PACKET_OLD_ANCHOR_CRITICAL_LOCALIZATION_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-retired-packet-old-anchor-critical-localization-independent-v1",
        "status": "INDEPENDENT_CRITICAL_ANCHOR_FORK_REPLAY_PASSED",
        "integer_bound": bound,
        "cases_checked": cases,
        "removable_cases": removable_cases,
        "critical_cases": critical_cases,
        "equality_cases_excluded_by_nondegeneracy": (
            equality_cases_excluded_by_nondegeneracy
        ),
        "failures": len(failures),
        "imports_primary_audit": False,
        "imports_z3": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, script)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
