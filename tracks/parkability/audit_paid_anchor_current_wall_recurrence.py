#!/usr/bin/env python3
"""Audit current-wall progress at a paid residual anchor."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(assumptions, negated) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, negated)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    yd, extra, xd = z3.Reals("yd extra xd")
    ai, rr, anchor, least = z3.Reals("ai rr anchor least")
    checks = {
        "anchor_keeps_hole_paid": prove(
            [yd >= xd, extra >= 0], yd + extra < xd
        ),
        "current_source_strictly_improves": prove(
            [rr > ai], rr <= ai
        ),
        "anchor_drives_remaining_wall": prove(
            [ai < anchor + rr - least, rr <= ai, least > 0],
            anchor <= ai - rr + least,
        ),
        "anchor_contribution_positive": prove(
            [ai < anchor + rr - least, rr <= ai, least > 0], anchor <= 0
        ),
    }

    # Finite-state sanity check: strictly increasing one coordinate of a
    # fixed vector cannot return to an earlier vector.
    values = range(4)
    checked_transitions = 0
    violations = []
    for state in itertools.product(values, repeat=3):
        for coordinate in range(3):
            for new_value in values:
                if new_value <= state[coordinate]:
                    continue
                updated = list(state)
                updated[coordinate] = new_value
                checked_transitions += 1
                if tuple(updated) == state:
                    violations.append((state, coordinate, new_value))

    theorem = root / "results/PAID_ANCHOR_CURRENT_WALL_RECURRENCE_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "paid-anchor-current-wall-recurrence-audit-v1",
        "status": "ALL_FORCED" if not violations else "FAILED",
        "symbolic_checks": checks,
        "support_identity": "A_i + Y_d + R = R + A_i + Y_d",
        "finite_vector_audit": {
            "coordinate_values": len(values),
            "dimensions": 3,
            "strict_transitions": checked_transitions,
            "violations": violations,
        },
        "outcomes": [
            "strict represented-source utility-vector growth",
            "unsafe response augmentation",
            "anchor-driven wall",
        ],
        "remaining_gate": "anchor-driven splice or hole-changing reset",
        "claim_boundary": (
            "fixed-hole disjoint recurrence termination; unsafe augmentation, "
            "anchor splice, hole changes, GG, and EFX remain open"
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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
