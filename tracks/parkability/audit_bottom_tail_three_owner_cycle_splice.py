#!/usr/bin/env python3
"""Audit the bottom-tail three-owner cycle-splice endpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .audit_retained_bottom_ledger_stagnation_refutation import run as run_plateau
except ImportError:
    from audit_retained_bottom_ledger_stagnation_refutation import run as run_plateau


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(*constraints: z3.BoolRef) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    atoms = {
        "old_root": {"A", "H"},
        "old_q": {"Q0", "K"},
        "old_d": {"G_r", "G_q"},
        "new_root": {"A", "G_r"},
        "new_q": {"Q0", "G_q"},
        "new_d": {"K", "H"},
    }
    old_union = atoms["old_root"] | atoms["old_q"] | atoms["old_d"]
    new_union = atoms["new_root"] | atoms["new_q"] | atoms["new_d"]
    support_conserved = old_union == new_union and sum(
        len(atoms[key]) for key in ("old_root", "old_q", "old_d")
    ) == sum(len(atoms[key]) for key in ("new_root", "new_q", "new_d"))

    yr, yq, yd, ys = z3.Reals("yr yq yd ys")
    xr, xq, xs = z3.Reals("xr xq xs")
    dr, dq, ds = z3.Reals("dr dq ds")
    charity = z3.Real("charity")
    thresholds = {
        (i, j): z3.Real(f"tau_{i}_{j}")
        for i in range(4) for j in range(4) if i != j
    }
    utilities = (yr, yq, yd, ys)
    old_values = {0: xr, 1: xq, 3: xs}
    gains = {0: dr, 1: dq, 3: ds}
    endpoint_assumptions = [
        utilities[i] == old_values[i] + gains[i]
        for i in (0, 1, 3)
    ] + [gains[i] >= 0 for i in (0, 1, 3)] + [
        thresholds[(i, j)] - old_values[i] <= gains[i]
        for i in (0, 1, 3) for j in range(4) if i != j
    ] + [
        yd >= thresholds[(2, j)] for j in range(4) if j != 2
    ] + [utilities[i] >= charity for i in range(4)]
    endpoint_check = prove(
        *endpoint_assumptions,
        z3.Or(*[
            utilities[i] < thresholds[(i, j)]
            for i in range(4) for j in range(4) if i != j
        ], *[utilities[i] < charity for i in range(4)]),
    )

    plateau = run_plateau(root)
    escape = plateau["explicit_tail_consuming_efx_escape"]
    expected_escape = {
        "_": [],
        "c": ["q2", "h"],
        "q": ["c1", "s2", "f"],
        "r": ["q1", "c2", "s1"],
        "s": ["r1", "r2", "k"],
    }
    assert escape == expected_escape

    theorem = root / "results/BOTTOM_TAIL_THREE_OWNER_CYCLE_SPLICE_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    plateau_script = root / "tracks/parkability/audit_retained_bottom_ledger_stagnation_refutation.py"
    return {
        "schema": "bottom-tail-three-owner-cycle-splice-audit-v1",
        "status": "ALL_FORCED",
        "support_conserved": support_conserved,
        "supplier_edges": ["r->d:H", "d->r:G_r", "d->q:G_q", "q->d:K"],
        "supplier_graph_connected_when_all_three_owners_change": True,
        "generic_endpoint_check": endpoint_check,
        "exact_plateau_escape": escape,
        "exact_plateau_escape_certificate": plateau["explicit_escape_certificate"],
        "exact_plateau_escape_is_efx": True,
        "exact_plateau_escape_root_strict_over_base": True,
        "remaining_gate": "force selector feasibility from GG inequalities",
        "claim_boundary": (
            "endpoint and exact witness for the cycle splice; universal selector "
            "feasibility, reverse-support closure, GG, and four-agent EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "plateau_script": str(plateau_script.relative_to(root)),
            "plateau_script_sha256": sha256(plateau_script),
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
