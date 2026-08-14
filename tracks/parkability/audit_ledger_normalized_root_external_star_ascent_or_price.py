#!/usr/bin/env python3
"""Exact audit of root external-star ascent or holder-price reduction."""

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
    old_root, hole_remainder, new_root = z3.Reals(
        "old_root hole_remainder new_root"
    )
    strict_ascent = prove(
        [hole_remainder > old_root, new_root == hole_remainder],
        new_root > old_root,
    )

    x, delta, d, c, a = z3.Reals("x delta d c a")
    split = [x > 0, delta > 0, a == x + delta, c == a - d]
    trichotomy = prove(
        split,
        z3.Or(d > x, d < delta, z3.And(d >= delta, d <= x)),
    )
    controlled_release = prove([*split, d < delta], c > x)
    band_price_nonnegative = prove(
        [*split, d >= delta, d <= x],
        z3.And(d - delta >= 0, d - delta <= x - delta),
    )
    proper_root_source_excluded = prove(
        [a > 0, d >= 0, d < a],
        z3.Not(d > a),
    )
    assert all((strict_ascent, trichotomy, controlled_release,
                band_price_nonnegative, proper_root_source_excluded))

    results = repo / "results"
    theorem = results / "LEDGER_NORMALIZED_ROOT_EXTERNAL_STAR_ASCENT_OR_PRICE_THEOREM_20260813.md"
    external = results / "ONE_CORE_THREE_HOLE_EXTERNAL_STAR_NORMAL_FORM_20260811.md"
    priority = results / "SAFE_CENTER_THREE_OFFER_PRIORITY_SPLIT_REDUCTION_20260813.md"
    price = results / "ROOT_FACING_HOLDER_PRICE_DUALITY_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "ledger-normalized-root-external-star-ascent-or-price-audit-v1",
        "status": "EXTERNAL_STAR_SIGNS_ROUTE_TO_ASCENT_RANK_OR_ROOT_PRICE",
        "root_to_hole_strict_ascent": strict_ascent,
        "hole_to_root_trichotomy": trichotomy,
        "controlled_release_below_delta": controlled_release,
        "band_price_nonnegative_and_bounded": band_price_nonnegative,
        "proper_subcore_not_current_root_desired": proper_root_source_excluded,
        "finite_potential": "strict v_r(A) ascent over finite root bundles",
        "remaining_separator": "retired collision / holder price",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free external-star sign reduction; holder payment and "
            "downstream collision closure remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "external_star": str(external.relative_to(repo)),
            "external_star_sha256": sha256(external),
            "priority_split": str(priority.relative_to(repo)),
            "priority_split_sha256": sha256(priority),
            "root_price": str(price.relative_to(repo)),
            "root_price_sha256": sha256(price),
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
        "finite_potential": result["finite_potential"],
        "remaining_separator": result["remaining_separator"],
    }, indent=2))


if __name__ == "__main__":
    main()

