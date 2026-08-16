#!/usr/bin/env python3
"""Scan stored profiles for a blocked Pareto-maximal eligible utility vector."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
    from .fast_count import FastParkability
    from .scan_partial_nash_potential import matrices
except ImportError:
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json
    from fast_count import FastParkability
    from scan_partial_nash_potential import matrices


SCHEMA = "partial-pareto-completion-corpus-scan-v1"


def exact_audit(values) -> dict:
    states = enumerate_states(values)
    by_utilities = {}
    for state in states:
        utilities = state["utilities"]
        record = by_utilities.setdefault(
            utilities,
            {
                "realization_count": 0,
                "insertable_realization_count": 0,
                "representative": None,
            },
        )
        record["realization_count"] += 1
        record["insertable_realization_count"] += int(
            bool(state["insertable_hosts"])
        )
        if record["representative"] is None:
            owner: list[int | None] = [None] * len(values[0])
            for agent, mask in enumerate(state["masks"]):
                for good in range(len(values[0])):
                    if mask & (1 << good):
                        owner[good] = agent
            record["representative"] = {
                "floater": state["floater"],
                "base_owner": owner,
                "insertable_hosts": list(state["insertable_hosts"]),
            }
    frontier = [
        utilities
        for utilities in by_utilities
        if not any(
            other != utilities
            and all(
                other[agent] >= utilities[agent]
                for agent in range(len(values))
            )
            for other in by_utilities
        )
    ]
    blocked = [
        utilities
        for utilities in frontier
        if by_utilities[utilities]["insertable_realization_count"] == 0
    ]
    products = {
        utilities: product
        for utilities in frontier
        for product in [
            utilities[0] * utilities[1] * utilities[2] * utilities[3]
        ]
    }
    maximum_product = max(products.values())
    maximum_product_vectors = [
        utilities
        for utilities in frontier
        if products[utilities] == maximum_product
    ]
    return {
        "eligible_base_count": len(states),
        "distinct_utility_vector_count": len(by_utilities),
        "pareto_frontier_utility_vector_count": len(frontier),
        "blocked_pareto_frontier_utility_vector_count": len(blocked),
        "blocked_vectors": [
            {
                "utilities": list(utilities),
                **by_utilities[utilities],
                "utility_product": products[utilities],
                "frontier_vector_count_with_larger_product": sum(
                    product > products[utilities] for product in products.values()
                ),
            }
            for utilities in blocked
        ],
        "maximum_product": maximum_product,
        "maximum_product_vector_count": len(maximum_product_vectors),
        "maximum_product_vectors": [
            {
                "utilities": list(utilities),
                **by_utilities[utilities],
            }
            for utilities in maximum_product_vectors
        ],
        "maximum_product_has_insertable_realization": any(
            by_utilities[utilities]["insertable_realization_count"] > 0
            for utilities in maximum_product_vectors
        ),
    }


def run(directory: Path, max_goods: int, output: Path) -> dict:
    evaluators = {}
    seen = set()
    records = []
    exact_counterexamples = []
    paths = sorted(directory.glob("*.json"))
    for position, path in enumerate(paths, 1):
        for value_key, values in matrices(path):
            n = len(values)
            m = len(values[0])
            if n != 4 or m > max_goods or values in seen:
                continue
            seen.add(values)
            if (n, m) not in evaluators:
                evaluators[(n, m)] = FastParkability(n, m)
            evaluator = evaluators[(n, m)]
            landscape = evaluator.partial_pareto_landscape(values)
            record = {
                "source": str(path),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "value_key": value_key,
                "n": n,
                "m": m,
                "values_sha256": hashlib.sha256(
                    json.dumps(values, separators=(",", ":")).encode()
                ).hexdigest(),
                **{
                    key: landscape[key]
                    for key in (
                        "eligible_base_count",
                        "distinct_utility_vector_count",
                        "pareto_frontier_utility_vector_count",
                        "insertable_pareto_frontier_utility_vector_count",
                        "blocked_pareto_frontier_utility_vector_count",
                    )
                },
            }
            records.append(record)
            if landscape["blocked_pareto_frontier_utility_vector_count"]:
                exact = exact_audit(values)
                if exact["blocked_pareto_frontier_utility_vector_count"]:
                    exact_counterexamples.append(
                        {
                            **record,
                            "values": [list(row) for row in values],
                            "exact_audit": exact,
                        }
                    )
            if position % 100 == 0:
                print(
                    f"files={position}/{len(paths)} profiles={len(records)}",
                    flush=True,
                )
    result = {
        "schema": SCHEMA,
        "status": (
            "BLOCKED_PARETO_VECTOR_FOUND"
            if exact_counterexamples
            else "NO_COUNTEREXAMPLE_IN_CORPUS"
        ),
        "conjecture": (
            "Every Pareto-maximal utility vector realized by an eligible "
            "one-floater EFX state has at least one insertable realization."
        ),
        "meaning": (
            "A counterexample refutes only the Pareto completion selector; "
            "absence from this finite corpus is not a theorem. Every reported "
            "counterexample is independently replayed by exact enumeration."
        ),
        "directory": str(directory),
        "json_file_count": len(paths),
        "distinct_profile_count": len(records),
        "max_goods": max_goods,
        "profile_count_with_blocked_pareto_vector": sum(
            record["blocked_pareto_frontier_utility_vector_count"] > 0
            for record in records
        ),
        "total_pareto_frontier_utility_vector_count": sum(
            record["pareto_frontier_utility_vector_count"] for record in records
        ),
        "exact_counterexamples": exact_counterexamples,
        "profile_records": records,
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path("results"))
    parser.add_argument("--max-goods", type=int, default=9)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.directory.is_dir() or args.max_goods < 1:
        parser.error("a valid directory and positive goods bound are required")
    run(args.directory, args.max_goods, args.output)


if __name__ == "__main__":
    main()
