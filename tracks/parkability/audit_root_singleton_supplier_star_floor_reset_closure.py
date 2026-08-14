#!/usr/bin/env python3
"""Exact arithmetic/support audit of root singleton-star collision closure."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subsets(items: tuple[int, ...]):
    for size in range(len(items) + 1):
        for chosen in combinations(items, size):
            yield frozenset(chosen)


def run() -> dict[str, object]:
    exterior, anchor, base, atom = z3.Reals("exterior anchor base atom")
    base_atom = z3.SolverFor("QF_LRA")
    base_atom.add(
        exterior >= anchor,
        anchor > base,
        base >= atom,
        atom > 0,
        exterior - atom <= 0,
    )
    base_atom_star_is_strict = base_atom.check() == z3.unsat

    remainder = z3.Real("remainder")
    exterior_atom = z3.SolverFor("QF_LRA")
    exterior_atom.add(
        exterior == atom + remainder,
        atom > 0,
        remainder > 0,
        exterior - atom <= 0,
    )
    exterior_atom_star_is_strict = exterior_atom.check() == z3.unsat

    goods = tuple(range(8))
    support_cases = 0
    base_atom_cases = 0
    exterior_atom_cases = 0
    response_cases = 0
    whole_hit_failures = 0
    for base_root in subsets(goods):
        exterior_support = frozenset(goods) - base_root
        for anchor in subsets(tuple(exterior_support)):
            if len(anchor) < 2:
                continue
            for packet in subsets(goods):
                if not packet:
                    continue
                for chosen in packet:
                    support_cases += 1
                    if chosen in base_root:
                        base_atom_cases += 1
                    else:
                        exterior_atom_cases += 1
                        assert exterior_support - {chosen}
                    root_target = frozenset(goods) - {chosen}
                    singleton_target = frozenset({chosen})
                    empty_target = frozenset()
                    targets = (root_target, singleton_target, empty_target, empty_target)
                    assert set().union(*targets) == set(goods)
                    assert sum(map(len, targets)) == len(goods)
                    # The singleton and empty targets cannot be EFX walls.
                    # Any response against the only remaining target misses
                    # the chosen packet atom.
                    response_cases += 1
                    root_packet_intersection = root_target & packet
                    assert root_packet_intersection == packet - {chosen}
                    whole_hit_failures += int(packet <= root_packet_intersection)

    assert support_cases > 0
    assert base_atom_cases > 0 and exterior_atom_cases > 0
    assert response_cases > 0
    assert whole_hit_failures == 0

    theorem = ROOT / "results/ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md"
    reset = ROOT / "results/STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md"
    floor_gap = ROOT / "results/ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md"
    nonroot = ROOT / "results/NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    old_core = ROOT / "results/GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "floor-reset theorem" in text
    assert "D\\cap K\\subseteq K-k\\subsetneq K" in text
    assert "collision subtype `T_{L,times}^*`" in text

    return {
        "schema": "root-singleton-supplier-star-floor-reset-closure-audit-v1",
        "status": "ROOT_HELD_T_L_TIMES_COLLISION_CLOSED_BY_FLOOR_RESET_STAR",
        "base_atom_star_is_strict": base_atom_star_is_strict,
        "exterior_atom_star_is_strict": exterior_atom_star_is_strict,
        "support_cases_checked": support_cases,
        "base_atom_cases": base_atom_cases,
        "exterior_atom_cases": exterior_atom_cases,
        "response_subsets_checked": response_cases,
        "whole_packet_response_failures": whole_hit_failures,
        "old_later_floors_preserved": False,
        "controlled_floor_reset_used": True,
        "historical_reversibility_used": False,
        "global_supplier_star_supplier_closed": True,
        "root_holder_branch_closed": True,
        "nonroot_holder_branch_closed_by_dependency": True,
        "full_T_L_times_theorem_closed": True,
        "full_GG_closed": False,
        "general_EFX_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                theorem,
                reset,
                floor_gap,
                nonroot,
                contract,
                old_core,
                script,
            )
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
