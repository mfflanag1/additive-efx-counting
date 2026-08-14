#!/usr/bin/env python3
"""Exact graph audit of the two-source hard topology and debt map."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cycle_length(mapping: tuple[int, int, int]) -> int:
    for start in range(3):
        seen: dict[int, int] = {}
        node = start
        step = 0
        while node not in seen:
            seen[node] = step
            node = mapping[node]
            step += 1
        length = step - seen[node]
        if length in (2, 3):
            return length
    raise AssertionError("self-loop-free finite map has no nontrivial cycle")


def run() -> dict[str, object]:
    # With sources a,b and non-source t, the only possible edges are a->t
    # and b->t. Non-source means at least one is present; the double-edge
    # case is the Pareto-closing CGM branch.
    source_graphs = []
    for a_to_t, b_to_t in product((False, True), repeat=2):
        if not (a_to_t or b_to_t):
            continue
        source_graphs.append(
            {
                "a_to_t": a_to_t,
                "b_to_t": b_to_t,
                "pareto_closing": a_to_t and b_to_t,
                "surviving_single_edge": a_to_t ^ b_to_t,
            }
        )
    assert len(source_graphs) == 3
    assert sum(case["pareto_closing"] for case in source_graphs) == 1
    assert sum(case["surviving_single_edge"] for case in source_graphs) == 2

    # The champion of t is a, b, or both after b->a and t->b are forced.
    hard_champion_patterns = (
        ("b->a", "t->b", "a->t"),
        ("b->a", "t->b", "b->t"),
        ("b->a", "t->b", "a->t", "b->t"),
    )

    debt_maps = []
    cycle_counts = {2: 0, 3: 0}
    for mapping in product(range(3), repeat=3):
        if any(mapping[i] == i for i in range(3)):
            continue
        length = cycle_length(mapping)
        cycle_counts[length] += 1
        debt_maps.append({"map": list(mapping), "cycle_length": length})
    assert len(debt_maps) == 8
    assert cycle_counts == {2: 6, 3: 2}

    theorem = ROOT / "results/TWO_SOURCE_ROOT_THRESHOLD_DEBT_DERANGEMENT_THEOREM_20260814.md"
    source = ROOT / "results/EXTERIOR_DOMINANCE_THREE_AGENT_SOURCE_REDUCTION_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    theorem_text = theorem.read_text()
    assert "exactly one ordinary edge" in theorem_text
    assert "directed map `j -> d(j)`" in theorem_text
    assert "not yet a release-compatible PI cycle" in theorem_text

    return {
        "schema": "two-source-root-threshold-debt-derangement-audit-v1",
        "status": "TWO_SOURCE_FACE_REDUCED_TO_SINGLE_EDGE_HARD_CHAMPIONS_CYCLIC_DEBT",
        "two_source_graphs_checked": len(source_graphs),
        "double_edge_pareto_closing_graphs": 1,
        "single_edge_surviving_graphs": 2,
        "hard_champion_patterns": [list(pattern) for pattern in hard_champion_patterns],
        "self_loop_free_debt_maps_checked": len(debt_maps),
        "debt_cycle_counts": {str(k): v for k, v in cycle_counts.items()},
        "all_debt_maps_have_nontrivial_cycle": True,
        "debt_cycle_is_release_compatible_pi": False,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, source, contract, script)
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
