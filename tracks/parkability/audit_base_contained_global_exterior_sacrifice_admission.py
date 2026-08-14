#!/usr/bin/env python3
"""Exact support/value audit of global-exterior root sacrifice."""

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
    x, exterior, atom = z3.Reals("x exterior atom")
    margin = z3.SolverFor("QF_LRA")
    margin.add(x > 0, exterior > atom, x - atom + exterior <= x)
    strict_margin_exact = margin.check() == z3.unsat

    own, singleton_value = z3.Reals("own singleton_value")
    singleton = z3.SolverFor("QF_LRA")
    singleton.add(own >= 0, singleton_value > 0, own < singleton_value - singleton_value)
    singleton_target_never_strongly_envied = singleton.check() == z3.unsat

    support_cases = 0
    whole_hits = 0
    singleton_packet_zero_hits = 0
    universe = tuple(range(7))
    for base_root in subsets(universe):
        exterior_support = frozenset(universe) - base_root
        if not base_root or not exterior_support:
            continue
        for packet in subsets(tuple(base_root)):
            if not packet:
                continue
            for good in packet:
                root_target = (base_root - {good}) | exterior_support
                singleton_target = frozenset({good})
                assert root_target | singleton_target == frozenset(universe)
                assert root_target.isdisjoint(singleton_target)
                root_hit = root_target & packet
                assert root_hit == packet - {good}
                whole_hits += int(packet <= root_hit)
                if len(packet) == 1:
                    singleton_packet_zero_hits += int(not root_hit)
                support_cases += 1

    assert support_cases > 0
    assert whole_hits == 0
    assert singleton_packet_zero_hits > 0

    theorem = ROOT / "results/BASE_CONTAINED_GLOBAL_EXTERIOR_SACRIFICE_ADMISSION_THEOREM_20260814.md"
    conditional = ROOT / "results/BASE_CONTAINED_RETIRED_PACKET_EXTERIOR_DONATION_SPLIT_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "global supplier-star sacrifice operation" in theorem_text
    assert "base-contained exterior-dominance face" in theorem_text

    return {
        "schema": "base-contained-global-exterior-sacrifice-admission-audit-v1",
        "status": "STRICT_GLOBAL_EXTERIOR_SACRIFICE_ADMITTED_DOMINANCE_REMAINS",
        "strict_margin_exact": strict_margin_exact,
        "singleton_target_never_strongly_envied": singleton_target_never_strongly_envied,
        "support_cases_checked": support_cases,
        "root_target_whole_packet_hits": whole_hits,
        "singleton_packet_zero_hit_cases": singleton_packet_zero_hits,
        "other_retired_labels_recorded": True,
        "exterior_dominance_closed": False,
        "global_multilabel_well_foundedness_proved": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, conditional, contract, script)
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
