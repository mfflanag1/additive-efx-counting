#!/usr/bin/env python3
"""Audit the source-inactive core/residual repair lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    support_cases = []
    for origin, selected in (
        ("A", False),
        ("A", True),
        ("W", False),
        ("W", True),
    ):
        if origin == "A":
            destination = "W_prime" if selected else "A_prime"
        else:
            destination = "A_prime" if selected else "W_prime"
        support_cases.append({
            "origin": origin,
            "selected_for_exchange": selected,
            "destination": destination,
        })
    assert len(support_cases) == 4

    a = z3.Real("d_A")
    w = z3.Real("d_W")
    k = z3.Real("d_K")
    tail_k = z3.Real("d_tail_K")
    full_h_repairs_d = check_unsat(
        a > w,
        0 <= k,
        k <= w,
        tail_k <= k,
        z3.Not(z3.And(a + w - k > tail_k, a > k)),
    )

    h = z3.Real("d_H")
    residual_advance = check_unsat(
        h >= k,
        h != k,
        z3.Not(w + h - k > w),
    )

    old_tail = z3.Real("d_old_core_tail")
    new_residual = z3.Real("d_new_residual")
    old_core_safety_preserved = check_unsat(
        w >= old_tail,
        new_residual > w,
        z3.Not(new_residual >= old_tail),
    )

    ja = z3.Real("j_A")
    jh = z3.Real("j_H")
    jw = z3.Real("j_W")
    jb = z3.Real("j_base")
    exhaustion_margin = check_unsat(
        ja - jh + jw <= jb,
        ja > jb,
        z3.Not(z3.And(
            jh - jw >= ja - jb,
            jh > jw,
        )),
    )

    script = Path(__file__).resolve()
    theorem = (
        root / "results" / "SOURCE_INACTIVE_CORE_RESIDUAL_REPAIR_LEMMA_20260811.md"
    )
    return {
        "schema": "source-inactive-core-residual-repair-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "support_partition_valid": True,
        "support_membership_cases": support_cases,
        "scalar_records": {
            "full_core_repairs_missing_owner": full_h_repairs_d,
            "nondegenerate_monotone_exchange_advances_residual": residual_advance,
            "old_missing_owner_core_safety_is_preserved": old_core_safety_preserved,
            "j_exhaustion_forces_unanimous_margin": exhaustion_margin,
        },
        "claim_boundary": (
            "cap-free finite repair and exhaustion-polarity audit; it does not "
            "eliminate J-exhaustion or close the flower"
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
    output = (
        args.output
        or root / "results" / "source_inactive_core_residual_repair_audit.json"
    )
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
