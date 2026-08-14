#!/usr/bin/env python3
"""Exact QF_LRA audit of safe-center return or rejection."""

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
    center_base, center_offer, center_threshold = z3.Reals(
        "center_base center_offer center_threshold"
    )
    leaf_floor, leaf_offer_threshold, center_bundle_leaf, rho = z3.Reals(
        "leaf_floor leaf_offer_threshold center_bundle_leaf rho"
    )
    center_protected = prove(
        [center_offer > center_base, center_threshold <= center_base],
        center_offer > center_threshold,
    )
    leaf_protected = prove(
        [rho >= leaf_floor, rho >= leaf_offer_threshold,
         center_bundle_leaf >= rho],
        z3.And(center_bundle_leaf >= leaf_floor,
               center_bundle_leaf >= leaf_offer_threshold),
    )
    trichotomy = prove(
        [],
        z3.Or(center_bundle_leaf >= rho, center_bundle_leaf < rho),
    )
    assert all((center_protected, leaf_protected, trichotomy))

    results = repo / "results"
    theorem = results / "SAFE_CENTER_THREE_OFFER_RETURN_OR_REJECTION_LEMMA_20260813.md"
    star = results / "TARGET_ENVELOPE_PROTECTED_PAIR_OR_SAME_SOURCE_STAR_LEMMA_20260813.md"
    two_hole = results / "TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "safe-center-three-offer-return-or-rejection-audit-v1",
        "status": "SAFE_CENTER_STAR_ENTERS_TWO_HOLE_OR_THREE_ROW_REJECTION",
        "center_pays_safe_return_bundle": center_protected,
        "leaf_pays_floor_and_offer": leaf_protected,
        "return_or_rejection_exhaustive": trichotomy,
        "surviving_separator": (
            "v_h(U_s) < max(F_h,tau_h(O_h)) for all three leaves"
        ),
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "exact protected center-return test; the three-row rejection and "
            "downstream two-hole collisions remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "star_theorem": str(star.relative_to(repo)),
            "star_theorem_sha256": sha256(star),
            "two_hole_theorem": str(two_hole.relative_to(repo)),
            "two_hole_theorem_sha256": sha256(two_hole),
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
        "surviving_separator": result["surviving_separator"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()

