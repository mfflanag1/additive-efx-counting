#!/usr/bin/env python3
"""Enumerate exact ordinary/current response relations of the radius-3 no-go."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_radius_three_exchange_no_go import (
    BASE,
    GOODS,
    OWNERS,
    REASSEMBLY,
    SPLIT,
    total,
    tail,
)


SUPPORT = {
    "r": ("a0", "a1", "h"),
    "q": ("j", "k", "q0"),
    "d": ("m", "gq", "gr"),
    "s": ("l", "e"),
    "charity": ("p",),
}


def relation(values, allocation, floor):
    floor_u = {owner: total(values, owner, floor[owner]) for owner in OWNERS}
    records = []
    for target, target_goods in allocation.items():
        for size in range(1, len(target_goods) + 1):
            for subset in itertools.combinations(target_goods, size):
                safe = all(tail(values, observer, subset) <= floor_u[observer]
                           for observer in OWNERS)
                if not safe:
                    continue
                for source in OWNERS:
                    if total(values, source, subset) > floor_u[source]:
                        records.append({
                            "source": source,
                            "target": target,
                            "subset": list(subset),
                        })
    return records


def maximum_matching(records):
    edges = {(record["source"], record["target"]) for record in records}
    best = ()
    for size in range(1, len(OWNERS) + 1):
        for chosen in itertools.combinations(sorted(edges), size):
            if len({source for source, _ in chosen}) != size:
                continue
            if len({target for _, target in chosen}) != size:
                continue
            best = chosen
    return [list(edge) for edge in best]


def run(source: Path, iteration: int):
    payload = json.loads(source.read_text())
    record = next(record for record in payload["rounds"] if record["iteration"] == iteration)
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in record["values"].items()
    }
    states = {"support": SUPPORT, "split": SPLIT, "reassembly": REASSEMBLY}
    result = {}
    for name, allocation in states.items():
        ordinary = relation(values, allocation, BASE)
        current = relation(values, allocation, allocation)
        union = ordinary + current
        result[name] = {
            "ordinary_base_floor": ordinary,
            "current_floor": current,
            "ordinary_maximum_matching": maximum_matching(ordinary),
            "current_maximum_matching": maximum_matching(current),
            "mixed_maximum_matching": maximum_matching(union),
        }
    return {
        "schema": "fixed-u-no-go-response-relation-analysis-v1",
        "source": f"results/{source.name}",
        "source_iteration": iteration,
        "states": result,
        "claim_boundary": (
            "descriptive exact subset-response census under base and same-state floors; "
            "it does not assert which GG response records are reachable or selected"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--iteration", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.iteration)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        name: {
            "ordinary_edges": len(state["ordinary_base_floor"]),
            "current_edges": len(state["current_floor"]),
            "ordinary_rank": len(state["ordinary_maximum_matching"]),
            "current_rank": len(state["current_maximum_matching"]),
            "mixed_rank": len(state["mixed_maximum_matching"]),
        }
        for name, state in result["states"].items()
    }, indent=2))


if __name__ == "__main__":
    main()
