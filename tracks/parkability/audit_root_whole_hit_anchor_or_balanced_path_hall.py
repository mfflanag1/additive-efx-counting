#!/usr/bin/env python3
"""Exact QF_LRA audit of the root anchor/balanced-band theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .audit_four_owner_current_bundle_compensation_path_hall import (
        run as run_path_hall,
    )
except ImportError:  # direct script replay
    from audit_four_owner_current_bundle_compensation_path_hall import (
        run as run_path_hall,
    )


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    x, delta, d, ell = z3.Reals("x delta d ell")
    common = [x > 0, delta > 0, d > 0, ell > 0, d + ell == x + delta]

    lower_d = z3.SolverFor("QF_LRA")
    lower_d.add(*common, ell < x, d <= delta)
    response_side_strictly_above_surplus = lower_d.check() == z3.unsat

    lower_ell = z3.SolverFor("QF_LRA")
    lower_ell.add(*common, d < x, ell <= delta)
    complement_strictly_above_surplus = lower_ell.check() == z3.unsat

    anchor_partition = z3.SolverFor("QF_LRA")
    anchor_partition.add(
        *common,
        z3.Not(z3.Or(d > x, ell > x, z3.And(d <= x, ell <= x))),
    )
    root_value_partition_exhaustive = anchor_partition.check() == z3.unsat

    zj, pi = z3.Reals("zj pi")
    sink = z3.SolverFor("QF_LRA")
    sink.add(*common, pi == d - delta, ell + zj - x != zj - pi)
    sink_margin_identity_exact = sink.check() == z3.unsat

    price_positive = z3.SolverFor("QF_LRA")
    price_positive.add(*common, d > delta, d < x, pi == d - delta, pi <= 0)
    discounted_price_positive = price_positive.check() == z3.unsat

    path = run_path_hall()
    assert path["no_path_iff_displayed_hall_cut"]
    assert all((
        response_side_strictly_above_surplus,
        complement_strictly_above_surplus,
        root_value_partition_exhaustive,
        sink_margin_identity_exact,
        discounted_price_positive,
    ))

    theorem = ROOT / "results/ROOT_WHOLE_HIT_ANCHOR_OR_BALANCED_PATH_HALL_THEOREM_20260814.md"
    path_theorem = ROOT / "results/FOUR_OWNER_CURRENT_BUNDLE_COMPENSATION_PATH_HALL_THEOREM_20260814.md"
    minimal_anchor = ROOT / "results/MINIMAL_SAFE_ROOT_ANCHOR_OR_ATOMWISE_CORE_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-whole-hit-anchor-or-balanced-path-hall-audit-v1",
        "status": "ROOT_WHOLE_HIT_REDUCED_TO_ANCHOR_OR_BALANCED_FIVE_PATH_CUT",
        "root_value_partition_exhaustive": root_value_partition_exhaustive,
        "response_side_strictly_above_surplus": response_side_strictly_above_surplus,
        "complement_strictly_above_surplus": complement_strictly_above_surplus,
        "sink_margin_identity_exact": sink_margin_identity_exact,
        "discounted_price_positive": discounted_price_positive,
        "strict_sink_test": "v_r(Z_j)>v_r(D)-delta",
        "root_equality_boundary_retained": True,
        "five_path_cut_reused_exactly": True,
        "remaining_separator": "balanced_root_band_and_discounted_five_path_hall_cut",
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, path_theorem, minimal_anchor, script)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
