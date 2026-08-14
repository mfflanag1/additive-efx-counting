#!/usr/bin/env python3
"""Exact QF_LRA audit of the root-facing anchor surplus-band dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    x, delta, d, c, h = z3.Reals("x delta d c h")
    base = [x > 0, delta > 0, d > 0, c > 0, h == x + delta, c == h - d]
    trichotomy = prove(
        base,
        z3.Or(d > x, d < delta, z3.And(d >= delta, d <= x)),
    )
    complement_paid = prove([*base, d < delta], c > x)
    band_blocks_complement = prove([*base, d >= delta], c <= x)
    band_blocks_reselection = prove([*base, d <= x], z3.Not(d > x))
    high_surplus_closes_band = prove(
        [*base, h > 2 * x, d >= delta, d <= x],
        z3.BoolVal(False),
    )
    assert all((trichotomy, complement_paid, band_blocks_complement,
                band_blocks_reselection, high_surplus_closes_band))

    theorem = repo / "results/ROOT_FACING_ANCHOR_SURPLUS_BAND_DICHOTOMY_20260813.md"
    normal_form = repo / "results/RETIRED_PACKET_COLLISION_ATOMIC_NORMAL_FORM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-facing-anchor-surplus-band-audit-v1",
        "status": "ROOT_FACING_SURVIVOR_REDUCED_TO_CLOSED_SURPLUS_BAND",
        "trichotomy_exhaustive": trichotomy,
        "complement_paid_below_delta": complement_paid,
        "band_blocks_complement_strictness": band_blocks_complement,
        "band_blocks_root_reselection": band_blocks_reselection,
        "root_above_twice_base_closes_band": high_surplus_closes_band,
        "surviving_band": "delta <= v_r(D) <= x",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "root-facing scalar and physical split theorem; observer debt and "
            "the surviving loss band remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "normal_form": str(normal_form.relative_to(repo)),
            "normal_form_sha256": sha256(normal_form),
            "z3_version": z3.get_version_string(),
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
        "surviving_band": result["surviving_band"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()

