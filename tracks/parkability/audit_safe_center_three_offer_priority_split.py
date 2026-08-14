#!/usr/bin/env python3
"""Exact audit of the safe-center star priority split."""

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
    root_floor, root_rest, root_offer, root_total, root_slack, compensation = z3.Reals(
        "root_floor root_rest root_offer root_total root_slack compensation"
    )
    root_price = prove(
        [root_total == root_rest + root_offer,
         root_slack == root_total - root_floor],
        (root_rest + compensation >= root_floor)
        == (compensation >= root_offer - root_slack),
    )
    base_root, current_root, offer = z3.Reals("base_root current_root offer")
    root_center_strict = prove(
        [current_root >= base_root, offer > current_root],
        offer > base_root,
    )
    assert root_price and root_center_strict

    results = repo / "results"
    theorem = results / "SAFE_CENTER_THREE_OFFER_PRIORITY_SPLIT_REDUCTION_20260813.md"
    star = results / "SAFE_CENTER_THREE_OFFER_RETURN_OR_REJECTION_LEMMA_20260813.md"
    external = results / "ONE_CORE_THREE_HOLE_EXTERNAL_STAR_NORMAL_FORM_20260811.md"
    two_hole = results / "TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "safe-center-three-offer-priority-split-audit-v1",
        "status": "STAR_ROUTES_TO_ROOT_PRICE_OR_EXISTING_EXTERNAL_STAR",
        "nonroot_center_root_holder_price_identity": root_price,
        "root_center_offer_strict_over_base": root_center_strict,
        "routes": {
            "center_not_root": ["root_holder_price", "two_core_two_hole"],
            "center_is_root": [
                "retired_collision_normalization",
                "EFX",
                "one_core_three_hole_external_star",
            ],
        },
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free priority routing; holder-price and inherited external-"
            "star signs remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "star_theorem": str(star.relative_to(repo)),
            "star_theorem_sha256": sha256(star),
            "external_star": str(external.relative_to(repo)),
            "external_star_sha256": sha256(external),
            "two_hole": str(two_hole.relative_to(repo)),
            "two_hole_sha256": sha256(two_hole),
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
        "routes": result["routes"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
