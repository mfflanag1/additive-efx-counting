#!/usr/bin/env python3
"""Independent integer replay of the signed-return margin fork."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    bound = 64
    cases = 0
    proper_cases = 0
    equality_cases = 0
    failures: list[tuple[int, int, int]] = []
    for plus in range(1, bound + 1):
        for minus in range(0, plus):
            delta = plus - minus
            for packet in range(1, plus + 1):
                cases += 1
                post_margin = delta - packet + minus
                if packet < plus:
                    proper_cases += 1
                    if post_margin != plus - packet or post_margin <= 0:
                        failures.append((plus, minus, packet))
                else:
                    equality_cases += 1
                    if post_margin != 0:
                        failures.append((plus, minus, packet))

    assert cases > 0
    assert proper_cases > 0 and equality_cases > 0
    assert failures == []

    theorem = ROOT / "results/ROOT_CRITICAL_OLD_ANCHOR_SIGNED_RETURN_OR_BLOCKER_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-critical-old-anchor-signed-return-or-blocker-independent-v1",
        "status": "INDEPENDENT_SIGNED_RETURN_MARGIN_REPLAY_PASSED",
        "integer_bound": bound,
        "cases_checked": cases,
        "proper_cases": proper_cases,
        "equality_cases": equality_cases,
        "failures": len(failures),
        "imports_primary_audit": False,
        "imports_z3": False,
        "repeated_blocker_well_foundedness_proved": False,
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
