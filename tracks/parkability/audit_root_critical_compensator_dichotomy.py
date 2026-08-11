#!/usr/bin/env python3
"""Audit the root-critical compensator dichotomy."""

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
    rh, ra, rw, rl = z3.Reals("r_H r_A r_W r_L")
    rg, rk = z3.Reals("r_g r_K")
    dl, dg, dk = z3.Reals("d_L d_g d_K")
    delta = rh - ra

    support_identity = check_unsat(
        ra + rw == rh + rl,
        z3.Not(delta == rw - rl),
    )
    compensator_preserves_root = check_unsat(
        rh >= ra,
        rk >= rg - delta,
        z3.Not(rh - rg + rk >= ra),
    )
    optimality_forces_opposite_order = check_unsat(
        dl + dg - dk <= dl,
        z3.Not(dk >= dg),
    )
    no_compensator_beats_old_residual = check_unsat(
        ra + rw == rh + rl,
        rl < rg - delta,
        z3.Not(rg > rw),
    )
    old_residual_membership_impossible = check_unsat(
        rg > rw,
        rw >= rg,
    )

    support_cases = []
    for origin in ("A", "W"):
        compatible = origin == "A"
        support_cases.append({
            "critical_good_origin": origin,
            "compatible_with_r_g_gt_r_W": compatible,
        })

    script = Path(__file__).resolve()
    theorem = root / "results/ROOT_CRITICAL_COMPENSATOR_DICHOTOMY_LEMMA_20260811.md"
    return {
        "schema": "root-critical-compensator-dichotomy-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "support_identity": support_identity,
            "compensator_preserves_root_constraint": compensator_preserves_root,
            "maximality_forces_opposite_row_order": optimality_forces_opposite_order,
            "no_compensator_beats_old_residual": no_compensator_beats_old_residual,
            "old_residual_membership_is_impossible": old_residual_membership_impossible,
        },
        "support_cases": support_cases,
        "claim_boundary": (
            "cap-free compensator/no-compensator dichotomy; the strict "
            "compensator dependency terminates through the separately audited "
            "alternating-frontier lemma, while its resulting handoffs remain open"
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
    output = args.output or root / "results/root_critical_compensator_dichotomy_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
