#!/usr/bin/env python3
"""Exact audit of the desire-free root complete-pool reduction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    x, delta, d, ell, pool, pi = z3.Reals("x delta d ell pool pi")
    base = [x > 0, delta > 0, d > 0, ell >= 0, d + ell == x + delta]

    balanced_d = z3.SolverFor("QF_LRA")
    balanced_d.add(*base, ell < x, d <= delta)
    d_above_surplus = balanced_d.check() == z3.unsat

    balanced_l = z3.SolverFor("QF_LRA")
    balanced_l.add(*base, d < x, ell <= delta)
    l_above_surplus = balanced_l.check() == z3.unsat

    margin = z3.SolverFor("QF_LRA")
    margin.add(*base, pi == d - delta, ell + pool - x != pool - pi)
    pool_margin_identity_exact = margin.check() == z3.unsat

    strict = z3.SolverFor("QF_LRA")
    strict.add(*base, pi == d - delta, pool > pi, ell + pool <= x)
    strict_pool_is_root_strict = strict.check() == z3.unsat

    equality = z3.SolverFor("QF_LRA")
    equality.add(*base, pi == d - delta, pool == pi, ell + pool != x)
    equality_pool_is_root_base = equality.check() == z3.unsat

    assert all((
        d_above_surplus,
        l_above_surplus,
        pool_margin_identity_exact,
        strict_pool_is_root_strict,
        equality_pool_is_root_base,
    ))
    theorem = ROOT / "results/ROOT_SAFE_WHOLE_HIT_COMPLETE_POOL_REDUCTION_THEOREM_20260814.md"
    nonroot = ROOT / "results/NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md"
    strict_pool = ROOT / "results/ROOT_WHOLE_HIT_GLOBAL_SACRIFICE_POOL_OR_UNDERPAYMENT_THEOREM_20260814.md"
    scalar = ROOT / "results/RETIRED_PACKET_BIROW_CUT_SCALAR_REALIZABILITY_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-safe-whole-hit-complete-pool-reduction-audit-v1",
        "status": "ALL_TYPED_SAFE_WHOLE_HITS_REDUCED_TO_ROOT_POOL_UNDERPAYMENT_OR_EQUALITY",
        "response_side_above_surplus": d_above_surplus,
        "complement_side_above_surplus": l_above_surplus,
        "pool_margin_identity_exact": pool_margin_identity_exact,
        "strict_pool_is_root_strict": strict_pool_is_root_strict,
        "equality_pool_is_root_base": equality_pool_is_root_base,
        "current_desire_required": False,
        "arbitrary_recipient_allowed": False,
        "named_typed_recipient_required": True,
        "typed_branches_unified": [
            "strict_capture",
            "equality_capture",
            "base_floor_source_inactive",
        ],
        "remaining_separator": "complete_compatible_pool_underpayment_or_root_equality",
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, nonroot, strict_pool, scalar, script)
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
