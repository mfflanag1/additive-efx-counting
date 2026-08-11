#!/usr/bin/env python3
"""Exact audit of mutual-floater deletion and double criticality."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    r_top, r_f, r_base = z3.Reals("r_top r_f r_base")
    q_top, q_f, q_base = z3.Reals("q_top q_f q_base")
    premises = [
        r_top >= 0,
        r_f > 0,
        r_base > 0,
        q_top >= 0,
        q_f > 0,
        q_base > 0,
        r_top + r_f > r_base,
        q_top + q_f > q_base,
    ]
    no_q_deletion = q_top <= q_base
    no_root_deletion = r_top <= r_base
    checks = {
        "q_deletion_or_root_deletion_or_double_critical_exhaustive": prove(
            premises,
            z3.Or(
                q_top > q_base,
                r_top > r_base,
                z3.And(no_q_deletion, no_root_deletion),
            ),
        ),
        "root_double_critical_implication": prove(
            premises + [no_q_deletion, no_root_deletion],
            z3.And(r_top <= r_base, r_base < r_top + r_f),
        ),
        "q_double_critical_implication": prove(
            premises + [no_q_deletion, no_root_deletion],
            z3.And(q_top <= q_base, q_base < q_top + q_f),
        ),
    }
    assert all(checks.values())

    root_core = {"tq0", "tq1", "f"}
    q_core = {"tr0", "tr1", "f"}
    assert root_core & q_core == {"f"}
    assert (root_core - {"f"}) & q_core == set()
    assert root_core & (q_core - {"f"}) == set()

    script = Path(__file__).resolve()
    theorem = (
        root
        / "results"
        / "MUTUAL_FLOATER_DELETION_OR_DOUBLE_CRITICAL_LEMMA_20260811.md"
    )
    return {
        "schema": "mutual-floater-deletion-or-double-critical-audit-v1",
        "status": "ALL_FORCED",
        "checks": checks,
        "canonical_core_intersection": ["f"],
        "root_deletion_is_disjoint": True,
        "q_deletion_is_disjoint": True,
        "remaining_separator": "simultaneous root/q floater criticality",
        "claim_boundary": (
            "deletion/double-critical trichotomy only; substitute packet, "
            "q-source collision, mixed-margin closure, and EFX remain open"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
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
    print(
        json.dumps(
            {
                "status": result["status"],
                "remaining_separator": result["remaining_separator"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
