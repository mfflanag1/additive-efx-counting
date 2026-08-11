#!/usr/bin/env python3
"""Audit the root-preserving two-hole selector lemma."""

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
    ra, rw, rh, rl, rg = z3.Reals("r_A r_W r_H r_L r_g")
    dl, dg = z3.Reals("d_L d_g")

    root_is_envy_free = check_unsat(
        ra > rw,
        rh + rl == ra + rw,
        rh >= ra,
        z3.Not(rh > rl),
    )

    root_criticality = check_unsat(
        dg > 0,
        z3.Implies(rh - rg >= ra, dl + dg <= dl),
        z3.Not(rh - rg < ra),
    )

    polarity_identity = check_unsat(
        rh + rl == ra + rw,
        rg > rh - ra,
        z3.Not(rg > rw - rl),
    )

    theorem = root / "results/ROOT_PRESERVING_TWO_HOLE_SELECTOR_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-preserving-two-hole-selector-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "root_is_envy_free": root_is_envy_free,
            "failed_selector_forces_root_criticality": root_criticality,
            "root_criticality_equals_residual_deficit_polarity": polarity_identity,
        },
        "claim_boundary": (
            "cap-free root-preserving selector dichotomy; conversion of the "
            "root-critical good into a closing transfer is not proved"
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
    output = args.output or root / "results/root_preserving_two_hole_selector_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
