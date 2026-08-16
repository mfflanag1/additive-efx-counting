#!/usr/bin/env python3
"""Exact replay of Pareto-conditioned bounded Nash rescues."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

try:
    from .analyze_partial_state_potentials import enumerate_states
    from .anneal import atomic_json
    from .anneal_lexmax_all_orders import load_values
    from .fast_count import FastParkability
except ImportError:
    from analyze_partial_state_potentials import enumerate_states
    from anneal import atomic_json
    from anneal_lexmax_all_orders import load_values
    from fast_count import FastParkability


SCHEMA = "partial-pareto-radius-rescue-audit-v1"
DEFAULT_SOURCES = (
    "results/adaptive_seed_trace92_i5.json",
    "results/adaptive_seed_trace93_i7117.json",
    "results/adaptive_seed_trace93_i7244.json",
    "results/adaptive_seed_trace93_i9744.json",
    "results/lexmax_all_orders_anneal_4x9_seed92.json",
    "results/lexmax_all_orders_anneal_4x9_seed93.json",
    "results/lexmax_partial_counterexample_4x9.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner_vector(state: dict, m: int) -> tuple[int | None, ...]:
    owner: list[int | None] = [None] * m
    for agent, mask in enumerate(state["masks"]):
        for good in range(m):
            if mask & (1 << good):
                owner[good] = agent
    return tuple(owner)


def public_state(state: dict, m: int) -> dict:
    return {
        "floater": state["floater"],
        "base_owner": list(owner_vector(state, m)),
        "utilities": list(state["utilities"]),
        "utility_product": math.prod(state["utilities"]),
        "insertable_hosts": list(state["insertable_hosts"]),
    }


def exact_rescue_audit(values, radius: int) -> dict:
    if type(radius) is not int or radius < 0:
        raise ValueError("radius must be a nonnegative integer")
    states = enumerate_states(values)
    m = len(values[0])
    by_utilities: dict[tuple[int, ...], list[dict]] = {}
    for state in states:
        by_utilities.setdefault(state["utilities"], []).append(state)
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
        if not any(
            state["insertable_hosts"] for state in by_utilities[utilities]
        )
    ]
    products = {
        utilities: math.prod(utilities) for utilities in by_utilities
    }
    maximum_product = max(products.values())
    maximum_product_vectors = [
        utilities
        for utilities, product in products.items()
        if product == maximum_product
    ]
    blocked_maximum_product = (
        max(products[utilities] for utilities in blocked)
        if blocked
        else None
    )
    records = []
    for utilities in blocked:
        blocked_product = math.prod(utilities)
        best_rescue = None
        strongest_target = None
        for state in by_utilities[utilities]:
            source_owner = owner_vector(state, m)
            for target in states:
                if target["floater"] != state["floater"]:
                    continue
                target_owner = owner_vector(target, m)
                distance = sum(
                    left != right
                    for left, right in zip(source_owner, target_owner)
                )
                if distance > radius:
                    continue
                target_product = math.prod(target["utilities"])
                target_insertable = bool(target["insertable_hosts"])
                target_record = {
                    **public_state(target, m),
                    "distance": distance,
                    "moves": [
                        {
                            "good": good,
                            "from": left,
                            "to": right,
                        }
                        for good, (left, right) in enumerate(
                            zip(source_owner, target_owner)
                        )
                        if left != right
                    ],
                }
                if strongest_target is None or (
                    target_product,
                    target_insertable,
                    -distance,
                ) > (
                    strongest_target["utility_product"],
                    bool(strongest_target["insertable_hosts"]),
                    -strongest_target["distance"],
                ):
                    strongest_target = target_record
                if not (
                    target_product > blocked_product
                    or (target_product == blocked_product and target_insertable)
                ):
                    continue
                if best_rescue is None or (
                    distance,
                    -target_product,
                    not target_insertable,
                ) < (
                    best_rescue["distance"],
                    -best_rescue["utility_product"],
                    not bool(best_rescue["insertable_hosts"]),
                ):
                    best_rescue = target_record
        records.append(
            {
                "utilities": list(utilities),
                "utility_product": blocked_product,
                "realization_count": len(by_utilities[utilities]),
                "representative": public_state(by_utilities[utilities][0], m),
                "strongest_bounded_target": strongest_target,
                "strongest_bounded_product_surplus": (
                    strongest_target["utility_product"] - blocked_product
                ),
                "bounded_rescue": best_rescue,
            }
        )
    rescued = sum(record["bounded_rescue"] is not None for record in records)
    return {
        "eligible_base_count": len(states),
        "distinct_utility_vector_count": len(by_utilities),
        "pareto_frontier_utility_vector_count": len(frontier),
        "blocked_pareto_frontier_utility_vector_count": len(blocked),
        "maximum_product": maximum_product,
        "maximum_product_vector_count": len(maximum_product_vectors),
        "maximum_product_has_insertable_realization": any(
            state["insertable_hosts"]
            for utilities in maximum_product_vectors
            for state in by_utilities[utilities]
        ),
        "blocked_pareto_maximum_product": blocked_maximum_product,
        "blocked_pareto_to_maximum_product_ratio": (
            blocked_maximum_product / maximum_product
            if blocked_maximum_product is not None
            else None
        ),
        "rescue_radius": radius,
        "blocked_pareto_frontier_with_bounded_rescue_count": rescued,
        "blocked_pareto_frontier_without_bounded_rescue_count": (
            len(blocked) - rescued
        ),
        "blocked_pareto_rescues": records,
    }


def audit(sources: list[Path], radius: int) -> dict:
    records = []
    for source in sources:
        values = load_values(source)
        exact = exact_rescue_audit(values, radius)
        vectorized = FastParkability(4, len(values[0])).partial_pareto_landscape(
            values,
            rescue_radius=radius,
        )
        compared_keys = (
            "eligible_base_count",
            "distinct_utility_vector_count",
            "pareto_frontier_utility_vector_count",
            "blocked_pareto_frontier_utility_vector_count",
            "blocked_pareto_frontier_with_bounded_rescue_count",
            "blocked_pareto_frontier_without_bounded_rescue_count",
            "maximum_product",
            "maximum_product_vector_count",
            "maximum_product_has_insertable_realization",
            "blocked_pareto_maximum_product",
        )
        if any(exact[key] != vectorized[key] for key in compared_keys):
            raise AssertionError("vectorized Pareto rescue landscape disagrees")
        records.append(
            {
                "source": str(source),
                "source_sha256": sha256(source),
                "values": values,
                "exact_audit": exact,
            }
        )
    distance_histogram = {}
    for record in records:
        for rescue in record["exact_audit"]["blocked_pareto_rescues"]:
            bounded = rescue["bounded_rescue"]
            if bounded is None:
                continue
            key = str(bounded["distance"])
            distance_histogram[key] = distance_histogram.get(key, 0) + 1
    unresolved = sum(
        record["exact_audit"][
            "blocked_pareto_frontier_without_bounded_rescue_count"
        ]
        for record in records
    )
    return {
        "schema": SCHEMA,
        "status": (
            "UNRESCUED_BLOCKED_PARETO_VECTOR_FOUND"
            if unresolved
            else "ALL_FROZEN_BLOCKED_PARETO_VECTORS_RESCUED"
        ),
        "meaning": (
            "This is an exact audit of a fixed finite profile list, not a "
            "proof of the radius-rescue conjecture or complete additive EFX."
        ),
        "conjecture": (
            "Every all-realizations-blocked Pareto-maximal eligible utility "
            "vector has a same-floater eligible rival within four good-owner "
            "changes that has larger Nash product, or equal product and an "
            "insertion."
        ),
        "implication": (
            "The conjecture would imply maximum-Nash completion and therefore "
            "complete EFX for four additive agents."
        ),
        "rescue_radius": radius,
        "source_count": len(records),
        "blocked_pareto_vector_count": sum(
            record["exact_audit"][
                "blocked_pareto_frontier_utility_vector_count"
            ]
            for record in records
        ),
        "unrescued_blocked_pareto_vector_count": unresolved,
        "minimum_rescue_distance_histogram": distance_histogram,
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append")
    parser.add_argument("--radius", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sources = args.source or [Path(path) for path in DEFAULT_SOURCES]
    result = audit(sources, args.radius)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
