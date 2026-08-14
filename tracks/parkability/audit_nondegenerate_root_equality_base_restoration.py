#!/usr/bin/env python3
"""Exact set/value audit of nondegenerate root equality restoration."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subsets(universe: frozenset[int]):
    ordered = tuple(sorted(universe))
    for size in range(len(ordered) + 1):
        for chosen in combinations(ordered, size):
            yield frozenset(chosen)


def run(repo: Path) -> dict:
    # Nondegeneracy supplies the implication from equal values to equal
    # physical bundles. Audit the remaining set-theoretic uniqueness without
    # importing the theorem implementation.
    universe = frozenset(range(6))
    cases = 0
    equality_cases = 0
    uniqueness = True
    base_crossing = True
    base_crossing_cases = 0
    for base in subsets(universe):
        for current in subsets(universe):
            for transferred in subsets(current):
                outside = universe - current
                for returned in subsets(outside):
                    cases += 1
                    post = (current - transferred) | returned
                    if post != base:
                        continue
                    equality_cases += 1
                    uniqueness &= transferred == current - base
                    uniqueness &= returned == base - current
                    for packet in subsets(current):
                        if not transferred <= packet:
                            continue
                        retained = packet - transferred
                        base_crossing_cases += 1
                        base_crossing &= retained == (packet & base)

    current_value, base_value, plus_value, minus_value, delta = z3.Reals(
        "current_value base_value plus_value minus_value delta"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        current_value == base_value + delta,
        current_value - base_value == plus_value - minus_value,
        z3.Not(plus_value - minus_value == delta),
    )
    signed_surplus_identity = solver.check() == z3.unsat
    t_value, u_value, r_value = z3.Reals("t_value u_value r_value")
    price_solver = z3.SolverFor("QF_LRA")
    price_solver.add(
        r_value == t_value - delta,
        u_value > 0,
        z3.Not(r_value < t_value + u_value - delta),
    )
    retained_positive_makes_full_underpayment = price_solver.check() == z3.unsat
    assert (uniqueness and base_crossing and signed_surplus_identity
            and retained_positive_makes_full_underpayment)

    theorem = repo / "results/NONDEGENERATE_ROOT_EQUALITY_BASE_RESTORATION_LEMMA_20260814.md"
    strict = repo / "results/STRICT_ROOT_OVERPAYMENT_SACRIFICE_OR_EQUALITY_HALL_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "nondegenerate-root-equality-base-restoration-audit-v1",
        "status": "ROOT_EQUALITY_COLLAPSES_TO_UNIQUE_BASE_RESTORATION",
        "physical_cases_checked": cases,
        "base_restoration_cases_checked": equality_cases,
        "transfer_equals_current_minus_base": uniqueness,
        "return_equals_base_minus_current": uniqueness,
        "base_crossing_cases_checked": base_crossing_cases,
        "retained_packet_equals_packet_intersect_base": base_crossing,
        "signed_surplus_identity": signed_surplus_identity,
        "retained_positive_makes_full_payment_strictly_larger": (
            retained_positive_makes_full_underpayment
        ),
        "remaining_separator": (
            "base_crossing_restoration_hitting_cut_or_root_payment_deficiency"
        ),
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "exact set/value audit under bundle nondegeneracy; base-support "
            "hitting cut and full theorem remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "strict_equality_theorem": str(strict.relative_to(repo)),
            "strict_equality_theorem_sha256": sha256(strict),
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
        "remaining_separator": result["remaining_separator"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
