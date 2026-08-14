#!/usr/bin/env python3
"""Exact audit of protected-floor currentization and support routing."""

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
    d, floor, holder, source = z3.Reals("d floor holder source")
    inactive = z3.SolverFor("QF_LRA")
    inactive.add(
        d > floor,
        d <= holder,
        holder <= source,
        z3.Not(z3.And(d - floor > 0, d - floor <= source - floor)),
    )
    source_inactive_debt_exact = inactive.check() == z3.unsat

    # A subset cannot be current-desired when the entire positive-additive
    # holder target is weakly below the source's current bundle.
    subset_value = z3.Real("subset_value")
    no_current_subset = z3.SolverFor("QF_LRA")
    no_current_subset.add(
        subset_value <= holder,
        holder <= source,
        subset_value > source,
    )
    inactive_excludes_current_subset = no_current_subset.check() == z3.unsat

    e_h, ell_h, zj_h = z3.Reals("e_h ell_h zj_h")
    residual_cancellation = z3.SolverFor("QF_LRA")
    residual_cancellation.add(
        ell_h + zj_h >= ell_h + e_h,
        z3.Not(zj_h >= e_h),
    )
    path_sink_identity_exact = residual_cancellation.check() == z3.unsat

    # Exhaust support geometry, including the empty residual case.
    support_cases = 0
    empty_residual_cases = 0
    for size in range(1, 8):
        holder_support = set(range(size))
        for k_mask in range(1, 1 << size):
            packet = {g for g in holder_support if k_mask & (1 << g)}
            for e_mask in range(1, 1 << size):
                core = {g for g in holder_support if e_mask & (1 << g)}
                if not packet <= core:
                    continue
                residual = holder_support - core
                assert not (residual & packet)
                support_cases += 1
                empty_residual_cases += int(not residual)
    assert support_cases > 0 and empty_residual_cases > 0

    path_hall = run_path_hall()
    assert path_hall["no_path_iff_displayed_hall_cut"]
    theorem = ROOT / "results/PROTECTED_FLOOR_WHOLE_HIT_CURRENTIZATION_OR_PATH_HALL_THEOREM_20260814.md"
    path_theorem = ROOT / "results/FOUR_OWNER_CURRENT_BUNDLE_COMPENSATION_PATH_HALL_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "protected-floor-whole-hit-currentization-or-path-hall-audit-v1",
        "status": "PROTECTED_WHOLE_HIT_REDUCED_TO_SOURCE_INACTIVE_DEBT_OR_CURRENT_PATH_HALL",
        "source_inactive_debt_exact": source_inactive_debt_exact,
        "inactive_excludes_current_subset": inactive_excludes_current_subset,
        "path_sink_identity_exact_with_empty_residual": path_sink_identity_exact,
        "whole_hit_support_cases_checked": support_cases,
        "empty_residual_cases_checked": empty_residual_cases,
        "five_path_cut_reused_exactly": True,
        "remaining_separators": [
            "source_inactive_floor_debt",
            "five_path_current_bundle_hall_cut",
            "other_retired_support_normalization",
        ],
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, path_theorem, contract, script)
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
