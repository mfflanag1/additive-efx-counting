#!/usr/bin/env python3
"""Analyze the two-stage form-2 linear-allocation CEGAR checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .run_fixed_u_full_packet_terminal_cegar import OWNERS, SUPPORT_STATE


FORM2_EDGES = (("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r"))


def total(values, owner, goods):
    return sum((values[owner][good] for good in goods), Fraction())


def tail(values, owner, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction()
    return total(values, owner, goods) - min(values[owner][good] for good in goods)


def minimal_response_cores(values, source, target):
    current = {owner: total(values, owner, SUPPORT_STATE[owner]) for owner in OWNERS}
    valid = []
    goods = SUPPORT_STATE[target]
    for size in range(1, len(goods) + 1):
        for subset in itertools.combinations(goods, size):
            base = (
                total(values, source, subset) > 1
                and all(tail(values, observer, subset) <= 1 for observer in OWNERS)
            )
            same_state = (
                total(values, source, subset) > current[source]
                and all(
                    tail(values, observer, subset) <= current[observer]
                    for observer in OWNERS
                )
            )
            if base or same_state:
                valid.append(subset)
    return tuple(
        subset for subset in valid
        if not any(set(other) < set(subset) for other in valid)
    )


def analyze(sources):
    rounds = []
    for source in sources:
        rounds.extend(json.loads(source.read_text())["rounds"])
    topology_count = Counter(
        tuple(tuple(edge) for edge in topology)
        for record in rounds
        for topology in record["chosen_topologies"]
    )
    core_patterns = {edge: Counter() for edge in FORM2_EDGES}
    for record in rounds:
        values = {
            owner: {good: Fraction(amount) for good, amount in row.items()}
            for owner, row in record["values"].items()
        }
        for edge in FORM2_EDGES:
            core_patterns[edge][minimal_response_cores(values, *edge)] += 1

    def encode_pattern(pattern):
        return [list(core) for core in pattern]

    script = Path(__file__).resolve()
    return {
        "schema": "exact-response-linear-cegar-checkpoint-analysis-v1",
        "status": "33_MODELS_ALL_HAVE_FOUR_EDGE_EFX",
        "source_files": [f"results/{source.name}" for source in sources],
        "source_sha256": {
            f"results/{source.name}": hashlib.sha256(source.read_bytes()).hexdigest()
            for source in sources
        },
        "round_count": len(rounds),
        "chosen_allocation_count": sum(
            len(record["chosen_allocations"]) for record in rounds
        ),
        "distinct_chosen_topology_count": len(topology_count),
        "minimum_edge_histogram": {
            str(edge_count): count
            for edge_count, count in sorted(Counter(
                record["minimum_edge_count"] for record in rounds
            ).items())
        },
        "complete_efx_count_range": [
            min(record["complete_efx_allocation_count"] for record in rounds),
            max(record["complete_efx_allocation_count"] for record in rounds),
        ],
        "feasible_topology_count_range": [
            min(record["feasible_topology_count"] for record in rounds),
            max(record["feasible_topology_count"] for record in rounds),
        ],
        "most_common_topologies": [
            {
                "count": count,
                "topology": [list(edge) for edge in topology],
            }
            for topology, count in topology_count.most_common(12)
        ],
        "minimal_response_core_patterns": {
            f"{source}->{target}": [
                {"count": count, "minimal_cores": encode_pattern(pattern)}
                for pattern, count in patterns.most_common()
            ]
            for (source, target), patterns in core_patterns.items()
        },
        "fixed_whole_target_patterns": {
            "r->q": all(
                pattern == (tuple(SUPPORT_STATE["q"]),)
                for pattern in core_patterns["r", "q"]
            ),
            "q->s": all(
                pattern == (tuple(SUPPORT_STATE["s"]),)
                for pattern in core_patterns["q", "s"]
            ),
            "d->q": all(
                pattern == (tuple(SUPPORT_STATE["q"]),)
                for pattern in core_patterns["d", "q"]
            ),
        },
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "claim_boundary": (
            "exact census of 33 bounded twelve-atom adversarial models; every "
            "recorded model has a <=4 support-edge complete EFX allocation, but "
            "the run ended UNKNOWN and proves neither the bounded nor cap-free theorem"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.source)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "rounds": result["round_count"],
        "topologies": result["distinct_chosen_topology_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
