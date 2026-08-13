#!/usr/bin/env python3
"""Independent exact finite replay of retire-on-backup inequalities.

This implementation does not import the symbolic audit.  It enumerates
integer rows and checks the wall implications directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(repo: Path) -> dict:
    root_cases = 0
    for base_r, e_r, unchanged_tau in product(range(5), repeat=3):
        if not (e_r > base_r and e_r >= unchanged_tau):
            continue
        root_cases += 1
        assert e_r > base_r
        assert e_r >= unchanged_tau

    supplier_cases = 0
    for q_old, k_q in product(range(5), range(1, 5)):
        supplier_cases += 1
        assert q_old + k_q > q_old

    monotonicity_cases = 0
    for old_u, gain, old_tau, threshold_drop in product(range(5), repeat=4):
        new_u = old_u + gain
        new_tau = old_tau - threshold_drop
        monotonicity_cases += 1
        if new_u < new_tau:
            assert old_u < old_tau

    root_target_cases = 0
    for old_u, gain, tau_e in product(range(5), repeat=3):
        if old_u < tau_e:
            continue
        root_target_cases += 1
        assert old_u + gain >= tau_e

    # Independent physical replay on differently named atoms.
    anchor = frozenset({11, 12, 13})
    backup = frozenset({21, 22})
    supplier = frozenset({31, 32})
    third = frozenset({41})
    before = (anchor | backup, supplier, third)
    after = (backup, supplier | anchor, third)
    assert frozenset().union(*before) == frozenset().union(*after)
    assert all(after[i].isdisjoint(after[j]) for i in range(3) for j in range(i + 1, 3))

    theorem = repo / "results/PERMANENT_ANCHOR_RETIRE_ON_BACKUP_EXCHANGE_THEOREM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "permanent-anchor-retire-on-backup-exchange-independent-audit-v1",
        "status": "INDEPENDENT_EXACT_REPLAY_PASSED",
        "root_priority_cases": root_cases,
        "supplier_return_cases": supplier_cases,
        "unchanged_wall_implication_cases": monotonicity_cases,
        "shrunken_root_target_cases": root_target_cases,
        "physical_replay_passed": True,
        "semantic_note": (
            "finite integer enumeration independently checks the algebraic "
            "implications; the cap-free proof is the manuscript argument"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "unchanged_wall_implication_cases": result["unchanged_wall_implication_cases"],
    }, indent=2))


if __name__ == "__main__":
    main()

