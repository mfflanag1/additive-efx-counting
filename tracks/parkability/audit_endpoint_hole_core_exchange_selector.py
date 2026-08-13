#!/usr/bin/env python3
"""Exact audit of the endpoint hole/core-exchange selector."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def subsets(goods: frozenset[str]):
    ordered = sorted(goods)
    for mask in range(1 << len(ordered)):
        yield frozenset(
            ordered[index] for index in range(len(ordered)) if mask >> index & 1
        )


def local_separator_witness() -> dict:
    goods = frozenset({"p0", "p1", "a0", "a1", "r"})
    P = frozenset({"p0", "p1"})
    A = frozenset({"a0", "a1"})
    R = frozenset({"r"})
    tenth = Fraction(1, 10)
    rows = {
        "hole": {"p0": Fraction(6), "p1": Fraction(6),
                 "a0": tenth, "a1": tenth, "r": tenth},
        "middle": {"p0": Fraction(6), "p1": Fraction(6),
                   "a0": Fraction(6), "a1": Fraction(6), "r": tenth},
        "observer_a": {good: tenth for good in goods},
        "observer_b": {good: tenth for good in goods},
    }
    base = {agent: Fraction(10) for agent in rows}
    floor_hole = Fraction(10)
    floor_middle = Fraction(10)

    def value(agent: str, bundle: frozenset[str]) -> Fraction:
        return sum((rows[agent][good] for good in bundle), Fraction(0))

    def threshold(agent: str, bundle: frozenset[str]) -> Fraction:
        if len(bundle) <= 1:
            return Fraction(0)
        return value(agent, bundle) - min(rows[agent][good] for good in bundle)

    desired = [
        H for H in subsets(A)
        if value("middle", H) > base["middle"]
        and all(threshold(agent, H) <= base[agent] for agent in rows)
    ]
    assert desired == [A]
    feasible = []
    successful = []
    for H, K in itertools.product(desired, subsets(P)):
        hole_bundle = (P - K) | H
        middle_bundle = R | (A - H) | K
        if value("middle", middle_bundle) < floor_middle:
            continue
        record = {
            "H": sorted(H), "K": sorted(K),
            "hole_value": str(value("hole", hole_bundle)),
            "middle_value": str(value("middle", middle_bundle)),
        }
        feasible.append(record)
        if value("hole", hole_bundle) >= floor_hole:
            successful.append(record)
    assert feasible
    assert not successful
    assert all(
        Fraction(record["hole_value"]) < floor_hole for record in feasible
    )
    assert value("hole", P) >= floor_hole
    assert all(value("hole", P - {good}) < floor_hole for good in P)
    assert value("middle", A | R) >= floor_middle
    assert all(value("middle", (A | R) - {good}) < floor_middle for good in A)
    assert all(threshold(agent, A) <= base[agent] for agent in rows)
    assert all(threshold(agent, P) <= base[agent] for agent in rows)
    return {
        "goods": sorted(goods),
        "P": sorted(P), "A_2": sorted(A), "R_2": sorted(R),
        "valuations": {
            agent: {good: str(number) for good, number in row.items()}
            for agent, row in rows.items()
        },
        "base_utilities": {agent: str(number) for agent, number in base.items()},
        "hole_floor": str(floor_hole),
        "middle_floor": str(floor_middle),
        "desired_core_count": len(desired),
        "middle_feasible_exchange_count": len(feasible),
        "successful_exchange_count": len(successful),
        "middle_feasible_exchanges": feasible,
        "hole_packet_inclusion_minimal": True,
        "middle_core_inclusion_minimal_for_floor": True,
        "separator": "hole",
    }


def run(root: Path) -> dict:
    p, b0, h, k, a, r, b2 = z3.Reals("p b0 h k a r b2")
    symbolic = {
        "success_pays_hole": prove([p - k + h >= b0], p - k + h >= b0),
        "success_pays_middle": prove([r + a - h + k >= b2], r + a - h + k >= b2),
        "hole_failure_separator": prove(
            [p >= b0, p - k + h < b0], k - h > p - b0
        ),
        "middle_exhaustion_separator": prove(
            [a + r >= b2, a - h + r + p < b2], h > a + r + p - b2
        ),
        "pool_conservation": prove([], (p - k + h) + (r + a - h + k) == p + r + a),
    }
    assert all(symbolic.values())
    witness = local_separator_witness()
    script = Path(__file__).resolve()
    theorem = root / "results/ENDPOINT_HOLE_CORE_EXCHANGE_SELECTOR_LEMMA_20260813.md"
    return {
        "schema": "endpoint-hole-core-exchange-selector-audit-v1",
        "status": "EXACT_TRICHOTOMY_WITH_LOCAL_HOLE_SEPARATOR",
        "symbolic_checks": symbolic,
        "local_positive_rational_separator": witness,
        "smallest_remaining_operation": (
            "eliminate the hole/middle two-row separator using an anchored GG "
            "inequality, priority-valid floor sacrifice, or an outside packet"
        ),
        "claim_boundary": (
            "cap-free selector and local countermodel only; not a globally "
            "lex-maximal GG countermodel"
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
    print(json.dumps({"status": result["status"], "smallest": result["smallest_remaining_operation"]}, indent=2))


if __name__ == "__main__":
    main()
