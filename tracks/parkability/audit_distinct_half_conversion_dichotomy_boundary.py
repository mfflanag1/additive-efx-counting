#!/usr/bin/env python3
"""Audit the one-repair boundary of the distinct-half conversion dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import N, audit_branch, build_state_graph
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_pair_cover import balanced_state_universe
    from .run_distinct_half_conversion_dichotomy_cegar import (
        FAVORITE,
        repair_holds,
        repair_universe,
    )
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import N, audit_branch, build_state_graph
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_pair_cover import balanced_state_universe
    from run_distinct_half_conversion_dichotomy_cegar import (
        FAVORITE,
        repair_holds,
        repair_universe,
    )


SCHEMA = "distinct-half-conversion-dichotomy-boundary-audit-v1"


def has_perfect_matching(graph):
    return any(
        all(graph[agent][matching[agent]] for agent in range(N))
        for matching in itertools.permutations(range(N))
    )


def audit(source_path):
    source = json.loads(source_path.read_text())
    values = tuple(tuple(map(int, row)) for row in source["values"])
    representatives = audit_branch(values)

    favorite_pair_universe, _ = build_state_graph()
    favorite_pair_ranks = tuple(
        matching_rank(feasible_graph(values, partition))
        for partition in favorite_pair_universe
    )
    balanced_universe = tuple(balanced_state_universe())
    balanced_graphs = tuple(
        feasible_graph(values, partition) for partition in balanced_universe
    )
    balanced_ranks = tuple(map(matching_rank, balanced_graphs))
    balanced_perfect = tuple(
        partition
        for partition, graph in zip(balanced_universe, balanced_graphs)
        if has_perfect_matching(graph)
    )
    favorite_triple_cells = Counter(
        tuple(
            good
            for good in next(
                bundle for bundle in partition if FAVORITE in bundle
            )
            if good != FAVORITE
        )
        for partition in balanced_perfect
    )
    repairs = tuple(
        partition
        for partition in repair_universe()
        if repair_holds(values, partition)
    )
    parked_goods = (1, 2)
    residual_goods = tuple(
        good for good in range(len(values[0])) if good not in (FAVORITE, *parked_goods)
    )
    common_bottom = all(
        set(parked_goods)
        == set(sorted(range(1, len(row)), key=lambda good: row[good])[:2])
        for row in values
    )
    universal_pair_acceptors = tuple(
        observer
        for observer, row in enumerate(values)
        if all(
            row[left] + row[right]
            >= row[FAVORITE] + max(row[good] for good in parked_goods)
            for left, right in itertools.combinations(residual_goods, 2)
        )
    )

    labeled_shapes = Counter()
    favorite_bundles = Counter()
    for assignment in itertools.product(range(N), repeat=len(values[0])):
        if not independent.is_complete_efx0(values, assignment):
            continue
        bundles = tuple(
            tuple(good for good, owner in enumerate(assignment) if owner == agent)
            for agent in range(N)
        )
        shape = tuple(sorted(map(len, bundles), reverse=True))
        labeled_shapes[shape] += 1
        favorite_bundles[bundles[assignment[FAVORITE]]] += 1

    if (
        representatives != (3, 4, 5, 6)
        or sum(rank == N for rank in favorite_pair_ranks) != 0
        or Counter(balanced_ranks) != Counter({1: 320, 2: 359, 3: 566, 4: 15})
        or len(balanced_perfect) != 15
        or favorite_triple_cells != Counter({(1, 2): 15})
        or len(repairs) != 1
        or not common_bottom
        or universal_pair_acceptors != (0, 2, 3)
        or labeled_shapes != Counter({(3, 2, 2, 2): 252})
        or independent.count_complete_efx0(values) != 252
    ):
        raise AssertionError("conversion-dichotomy boundary census changed")
    if set(favorite_bundles) != {(0, 1, 2)}:
        raise AssertionError("favorite triple changed")

    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_CONVERSION_DICHOTOMY_BOUNDARY_AUDIT_PASSED",
        "source": str(source_path.resolve()),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "values": [list(row) for row in values],
        "half_favorite_representatives": list(representatives),
        "favorite_pair_partition_count": len(favorite_pair_universe),
        "favorite_pair_efx_partition_count": 0,
        "balanced_matching_rank_histogram": {
            str(rank): count for rank, count in sorted(Counter(balanced_ranks).items())
        },
        "balanced_efx_partition_count": len(balanced_perfect),
        "favorite_triple_pairing_cell_counts": [
            {"parked_goods": list(goods), "efx_pairing_count": count}
            for goods, count in sorted(favorite_triple_cells.items())
        ],
        "all_fifteen_pairings_work_for_parked_goods": [1, 2],
        "parked_goods_are_common_bottom_pair": common_bottom,
        "agents_accepting_every_pair_of_the_other_six_goods": list(
            universal_pair_acceptors
        ),
        "common_favorite_triple_in_every_balanced_efx_partition": [0, 1, 2],
        "common_low_triple_repair_count": len(repairs),
        "unique_common_low_triple_repair": [list(bundle) for bundle in repairs[0]],
        "literal_complete_efx_allocation_count": sum(labeled_shapes.values()),
        "literal_complete_efx_shape_census": {"3+2+2+2": 252},
        "interpretation": (
            "This is a knife-edge positive boundary for the replacement "
            "dichotomy: favorite-pair EFX is absent, but exactly one "
            "common-low triple repair survives."
        ),
        "limitation": (
            "The profile has 252 complete EFX allocations and is neither a "
            "dichotomy counterexample nor an additive EFX counterexample."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "results/efx49_distinct_half_conversion_dichotomy_anneal_session1.json"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
