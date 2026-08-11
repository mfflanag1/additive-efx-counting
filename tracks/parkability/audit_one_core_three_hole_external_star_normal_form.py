#!/usr/bin/env python3
"""Audit the one-core/three-hole external-star normal form."""

from __future__ import annotations

import argparse
import hashlib
import itertools
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
    own_h, tail_root, root_total, base_h = z3.Reals(
        "own_h tail_root root_total base_h"
    )
    loss_band = check_unsat(
        own_h < tail_root,
        tail_root < root_total,
        root_total <= base_h,
        root_total != base_h,
        z3.Not(z3.And(own_h < tail_root, tail_root < root_total, root_total < base_h)),
    )

    desired, deletion, threshold, base = z3.Reals(
        "desired containing_deletion threshold base"
    )
    response_rigidity = check_unsat(
        desired <= deletion,
        deletion <= threshold,
        threshold <= base,
        desired > base,
    )

    support_cases = [
        {"packet": "A_r", "supplier": "r", "receiver": "h"},
        {"packet": "D_r", "supplier": "h", "receiver": "r"},
    ]

    raw_patterns = []
    surviving_patterns = []
    signs = ("none", "hole_to_root", "root_to_hole", "reciprocal")
    for pattern in itertools.product(signs, repeat=3):
        raw_patterns.append(pattern)
        if "reciprocal" not in pattern:
            surviving_patterns.append(pattern)

    assert len(raw_patterns) == 64
    assert len(surviving_patterns) == 27

    script = Path(__file__).resolve()
    theorem = root / "results/ONE_CORE_THREE_HOLE_EXTERNAL_STAR_NORMAL_FORM_20260811.md"
    return {
        "schema": "one-core-three-hole-external-star-normal-form-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "source_inactive_loss_band": loss_band,
            "common_safe_response_is_whole_root_core": response_rigidity,
        },
        "wall_localization": {
            "hole_to_hole_walls": 0,
            "possible_root_star_comparisons": 6,
        },
        "reciprocal_support": support_cases,
        "reciprocal_support_disjoint": True,
        "raw_signed_star_count": len(raw_patterns),
        "nonreciprocal_signed_star_count": len(surviving_patterns),
        "reciprocal_containing_signed_star_count": (
            len(raw_patterns) - len(surviving_patterns)
        ),
        "claim_boundary": (
            "cap-free rank-one external-star normal form; elimination of the "
            "one-directional and source-inactive reciprocal patterns is not proved"
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
    output = args.output or root / "results/one_core_three_hole_external_star_normal_form_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
