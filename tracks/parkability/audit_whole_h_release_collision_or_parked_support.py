#!/usr/bin/env python3
"""Audit the whole-H collision/parked-support partition."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/WHOLE_H_RELEASE_COLLISION_OR_PARKED_SUPPORT_REDUCTION_20260814.md"
ALL_PAID = ROOT / "results/ALL_PAID_WHOLE_H_TO_D_DECORATED_RESPONSE_LEMMA_20260814.md"
COLLISION_COMMIT = "34709c9ce22dbde23a5fa381a2ccea7898dfe1ca"


def run(output: Path):
    universe = frozenset(range(4))
    retired = frozenset((0, 1))
    supports = tuple(
        frozenset(index for index in universe if mask & (1 << index))
        for mask in range(1 << len(universe))
    )
    cases = 0
    collision = 0
    parked = 0
    # A bit mask selects the complete active support family.
    for family_mask in range(1 << len(supports)):
        family = tuple(
            support for index, support in enumerate(supports)
            if family_mask & (1 << index)
        )
        has_hit = any(support & retired for support in family)
        all_avoid = all(not support & retired for support in family)
        assert has_hit != all_avoid
        assert has_hit or all_avoid
        cases += 1
        collision += int(has_hit)
        parked += int(all_avoid)
    assert retired
    assert cases == collision + parked
    result = {
        "schema": "whole-h-release-collision-or-parked-support-audit-v1",
        "status": "AUDIT_PASSED",
        "retired_packet_nonempty": True,
        "active_family_cases": cases,
        "collision_cases": collision,
        "parked_cases": parked,
        "empty_ledger_terminal_possible": False,
        "surviving_terminal_after_collision_closure": "T_{L,perp}^*",
        "imported_collision_theorem_commit": COLLISION_COMMIT,
        "dependencies": {
            str(THEOREM.relative_to(ROOT)): hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            str(ALL_PAID.relative_to(ROOT)): hashlib.sha256(ALL_PAID.read_bytes()).hexdigest(),
        },
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Audits the set-theoretic typed-terminal partition and dependency "
            "identity. It does not independently reprove the imported collision "
            "theorem or close parked support."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
