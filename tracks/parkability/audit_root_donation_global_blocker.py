#!/usr/bin/env python3
"""Audit the scalar and comparison localization of root donation blockers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints: z3.BoolRef) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    base, packet, target_tail = z3.Reals("donor_base packet target_tail")
    donor_slack_polarity = check_unsat(
        packet > 0,
        base - packet < target_tail,
        target_tail <= base,
        z3.Not(packet > base - target_tail),
    )

    old_tail, new_tail, observer_base = z3.Reals(
        "old_root_tail new_root_tail observer_base"
    )
    enlarged_root_polarity = check_unsat(
        old_tail <= observer_base,
        observer_base < new_tail,
        z3.Not(new_tail > old_tail),
    )

    charity = z3.Real("donor_charity")
    charity_slack_polarity = check_unsat(
        packet > 0,
        base - packet < charity,
        charity <= base,
        z3.Not(packet > base - charity),
    )

    script = Path(__file__).resolve()
    theorem = root / "results/ROOT_DONATION_GLOBAL_BLOCKER_LEMMA_20260811.md"
    return {
        "schema": "root-donation-global-blocker-audit-v1",
        "status": "ALL_FORCED",
        "wall_localization": {
            "root_observer_failure": "impossible",
            "unchanged_observer_targets": ["enlarged_root_only"],
            "donor_targets": ["enlarged_root", "unchanged_owner", "charity"],
        },
        "scalar_records": {
            "donor_unchanged_target_exhausts_slack": donor_slack_polarity,
            "unchanged_observer_sees_strict_root_threshold_increase": (
                enlarged_root_polarity
            ),
            "donor_charity_failure_exhausts_slack": charity_slack_polarity,
        },
        "claim_boundary": (
            "cap-free one-edge global blocker localization; compensating-packet "
            "selection and dependency-path termination are not proved"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results/root_donation_global_blocker_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
