#!/usr/bin/env python3
"""Independent QF_LRA audit of nested-core exhaustion."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/NESTED_DESIRED_CORE_EXHAUSTS_SAFE_TARGET_LEMMA_20260814.md"
BOUNDED = ROOT / "results/allocated_e_form0_anchor_charity_bypass_audit.json"


def run(output: Path):
    floor, core, residual_without_g, g = z3.Reals(
        "floor core residual_without_g g"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        floor >= 0,
        core > floor,
        residual_without_g >= 0,
        g > 0,
        # Common safety after deleting the chosen residual good.
        core + residual_without_g <= floor,
    )
    status = str(solver.check())
    assert status == "unsat"

    p, empty = z3.Reals("p empty")
    singleton = z3.SolverFor("QF_LRA")
    singleton.add(p > 0, empty == 0, z3.Not(p > empty))
    singleton_status = str(singleton.check())
    assert singleton_status == "unsat"

    bounded = json.loads(BOUNDED.read_text())
    assert bounded["status"] == "UNSAT_ANCHOR_CHARITY_PARKED_BYPASS"
    assert bounded["deletion_minimal_unsat_core"] == ["p_parked_for_q"]

    result = {
        "schema": "nested-desired-core-exhausts-safe-target-audit-v1",
        "status": "CAP_FREE_NESTED_CORE_EXHAUSTION_PROVED",
        "proper_residual_negation_status": status,
        "positive_singleton_desire_negation_status": singleton_status,
        "bounded_form0_core_replayed": True,
        "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
        "bounded_audit_sha256": hashlib.sha256(BOUNDED.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Cap-free for a desired core nested in a whole target common-safe "
            "at the same floor. The universal fixed-U predicate does not "
            "currently provide whole-target safety."
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
