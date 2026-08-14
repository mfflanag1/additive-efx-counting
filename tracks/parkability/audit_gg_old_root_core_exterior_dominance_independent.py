#!/usr/bin/env python3
"""Independent finite replay of the old-root-core contradiction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    # This implementation imports neither z3 nor the primary audit.  It
    # exhausts positive integer candidates for the four scalar quantities.
    tested = 0
    feasible = []
    bound = 32
    for atom in range(1, bound + 1):
        for outside in range(1, bound + 1):
            if not atom > outside:
                continue
            for old_core in range(1, outside + 1):
                for base in range(1, bound + 1):
                    tested += 1
                    if old_core > base >= atom:
                        feasible.append((atom, outside, old_core, base))
    assert tested > 0
    assert feasible == []

    theorem = ROOT / "results/GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md"
    resolution = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_RESOLUTION_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "gg-old-root-core-exterior-dominance-independent-audit-v1",
        "status": "INDEPENDENT_INTEGER_REPLAY_UNSAT",
        "integer_bound": bound,
        "ordered_candidates_checked": tested,
        "feasible_chains": len(feasible),
        "imports_primary_audit": False,
        "imports_z3": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, resolution, script)
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
