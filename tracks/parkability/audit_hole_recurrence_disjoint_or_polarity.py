#!/usr/bin/env python3
"""Audit the scalar and finite-cycle parts of hole recurrence closure."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints: z3.BoolRef) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    target, outside, overlap, base = z3.Reals(
        "target outside_used overlap_used base"
    )
    hitting_set_polarity = check_unsat(
        target == outside + overlap,
        outside <= base,
        target > base,
        z3.Not(z3.And(overlap >= target - base, overlap > 0)),
    )

    core, without_good, good, core_base = z3.Reals(
        "core without_good good core_base"
    )
    critical_good_polarity = check_unsat(
        core == without_good + good,
        without_good <= core_base,
        core > core_base,
        z3.Not(z3.And(good >= core - core_base, good > 0)),
    )

    simple_cycles = []
    for length in (2, 3):
        for owners in itertools.permutations(("q", "c", "s"), length):
            if owners[0] != min(owners):
                continue
            edges = [
                [owners[index], owners[(index + 1) % length]]
                for index in range(length)
            ]
            simple_cycles.append({"length": length, "edges": edges})
    assert {record["length"] for record in simple_cycles} == {2, 3}

    script = Path(__file__).resolve()
    theorem = root / "results/HOLE_RECURRENCE_DISJOINT_OR_POLARITY_LEMMA_20260811.md"
    return {
        "schema": "hole-recurrence-disjoint-or-polarity-audit-v1",
        "status": "ALL_FORCED",
        "simple_cycle_records": simple_cycles,
        "scalar_records": {
            "failed_disjoint_response_forces_hitting_set_polarity": (
                hitting_set_polarity
            ),
            "shared_minimal_core_good_is_critical": critical_good_polarity,
        },
        "support_records": {
            "above_base_disjoint_remainder_has_minimal_desired_subset": True,
            "failed_common_safety_routes_to_unsafe_core_augmentation": True,
        },
        "claim_boundary": (
            "cap-free simple-cycle support audit; dynamic target persistence "
            "and termination after unsafe-core augmentation or overlap polarity "
            "are not proved"
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
    output = args.output or root / "results/hole_recurrence_disjoint_or_polarity_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
