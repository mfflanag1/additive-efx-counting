#!/usr/bin/env python3
"""Audit the strict two-core/Tutte distinct-half boundary."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .anneal_distinct_half_rank_augmentation import Landscape
    from .audit_distinct_half_rank_augmentation import N, audit_branch
except ImportError:
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_rank_augmentation import Landscape
    from audit_distinct_half_rank_augmentation import N, audit_branch


SCHEMA = "distinct-half-two-core-boundary-audit-v1"
FAVORITE = 0
VALUES = (
    (100, 6, 1, 72, 60, 90, 44, 61, 55),
    (100, 10, 1, 51, 85, 66, 45, 60, 77),
    (100, 1, 2, 77, 72, 47, 91, 76, 73),
    (100, 1, 7, 57, 70, 61, 84, 63, 65),
)


def literal_census():
    counts = Counter()
    for assignment in itertools.product(range(N), repeat=len(VALUES[0])):
        if not independent.is_complete_efx0(VALUES, assignment):
            continue
        bundles = tuple(
            tuple(good for good, owner in enumerate(assignment) if owner == agent)
            for agent in range(N)
        )
        counts[
            (
                tuple(sorted(map(len, bundles), reverse=True)),
                bundles[assignment[FAVORITE]],
            )
        ] += 1
    return counts


def audit():
    representatives = audit_branch(VALUES)
    landscape = Landscape("balanced").audit(VALUES)
    labeled = literal_census()
    expected_key = ((3, 2, 2, 2), (0, 1, 2))
    expected_two_core = [
        {
            "low_goods": [1, 2],
            "core_agents": [2, 3],
            "bad_edge_count": 1,
        }
    ]
    if (
        representatives != (3, 4, 6, 5)
        or any(len(set(row)) != len(row) for row in VALUES)
        or landscape["matching_rank_histogram"]
        != {"1": 294, "2": 347, "3": 604, "4": 15}
        or landscape["favorite_pair_perfect_partition_count"] != 0
        or landscape["favorite_triple_perfect_partition_count"] != 15
        or landscape["maximum_favorite_triple_cell_count"] != 15
        or landscape["full_favorite_triple_cell_count"] != 1
        or landscape["maximum_three_observer_cell_slack"] != -7
        or landscape["robust_low_pair_count"] != 0
        or landscape["two_core_tutte_low_pairs"] != expected_two_core
        or labeled != Counter({expected_key: 270})
    ):
        raise AssertionError("two-core boundary census changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_TWO_CORE_BOUNDARY_AUDIT_PASSED",
        "values": [list(row) for row in VALUES],
        "strict_common_favorite": True,
        "distinct_item_values_per_row": True,
        "half_favorite_representatives": list(representatives),
        "balanced_matching_rank_histogram": landscape[
            "matching_rank_histogram"
        ],
        "favorite_pair_efx_partition_count": 0,
        "favorite_triple_efx_partition_count": 15,
        "full_favorite_triple_cell_count": 1,
        "favorite_triple_cell": [0, 1, 2],
        "best_three_universal_observer_slack": landscape[
            "maximum_three_observer_cell_slack"
        ],
        "three_universal_observer_strengthening_holds": False,
        "two_core_tutte_witnesses": expected_two_core,
        "common_low_triple_repair_partition_count": landscape[
            "common_low_triple_repair_partition_count"
        ],
        "literal_complete_efx_allocation_count": sum(labeled.values()),
        "literal_complete_efx_shape_census": {
            "3+2+2+2_favorite_triple_0_1_2": labeled[expected_key],
        },
        "interpretation": (
            "Three universal pair acceptors are not forced. The surviving "
            "structure has exactly two universal acceptors and a one-edge "
            "outsider-rejection graph, so the two-core/Tutte corollary "
            "makes all 15 pairings EFX-supporting."
        ),
        "limitation": (
            "This is a boundary for a sufficient selection lemma, not an "
            "additive EFX counterexample or a proof of the selection lemma."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
