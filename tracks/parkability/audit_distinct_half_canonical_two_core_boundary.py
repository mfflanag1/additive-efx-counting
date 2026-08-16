#!/usr/bin/env python3
"""Audit the strict boundary refuting canonical two-core selection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .anneal_distinct_half_rank_augmentation import Landscape
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .run_distinct_half_two_core_cegar import two_core_witnesses
except ImportError:
    import independent
    from anneal import atomic_json
    from anneal_distinct_half_rank_augmentation import Landscape
    from audit_distinct_half_rank_augmentation import audit_branch
    from run_distinct_half_two_core_cegar import two_core_witnesses


SCHEMA = "distinct-half-canonical-two-core-boundary-audit-v1"
VALUES = (
    (100, 52, 51, 66, 67, 7, 1, 85, 50),
    (100, 81, 86, 59, 63, 1, 2, 70, 90),
    (100, 54, 53, 59, 82, 8, 1, 80, 78),
    (100, 86, 80, 60, 78, 9, 3, 65, 85),
)


def audit():
    representatives = audit_branch(VALUES)
    landscape = Landscape("balanced").audit(VALUES)
    witnesses = two_core_witnesses(VALUES)
    canonical_witnesses = two_core_witnesses(VALUES, "canonical")
    literal_count = independent.count_complete_efx0(VALUES)
    expected_witnesses = [
        {
            "low_goods": [5, 6],
            "core_agents": [1, 3],
            "bad_edges": [[1, 2]],
        }
    ]
    if (
        representatives != (1, 2, 3, 4)
        or any(len(set(row)) != len(row) for row in VALUES)
        or landscape["matching_rank_histogram"]
        != {"1": 261, "2": 406, "3": 578, "4": 15}
        or landscape["favorite_pair_perfect_partition_count"] != 0
        or landscape["favorite_triple_perfect_partition_count"] != 15
        or landscape["full_favorite_triple_cell_count"] != 1
        or landscape["common_low_triple_repair_partition_count"] != 6
        or witnesses != expected_witnesses
        or canonical_witnesses
        or literal_count != 288
    ):
        raise AssertionError("canonical two-core boundary census changed")
    return {
        "schema": SCHEMA,
        "status": "CANONICAL_TWO_CORE_SELECTION_REFUTED",
        "values": [list(row) for row in VALUES],
        "strict_common_favorite": True,
        "distinct_item_values_per_row": True,
        "half_favorite_representatives": list(representatives),
        "matching_rank_histogram": landscape["matching_rank_histogram"],
        "favorite_pair_efx_partition_count": 0,
        "favorite_triple_efx_partition_count": 15,
        "full_favorite_triple_cell_count": 1,
        "common_low_triple_repair_partition_count": 6,
        "canonical_two_core_tutte_witnesses": canonical_witnesses,
        "all_two_core_tutte_witnesses": witnesses,
        "literal_complete_efx_allocation_count": literal_count,
        "interpretation": (
            "The two low goods in a forced two-core/Tutte witness need not "
            "be half-favorite representatives, and the core need not be "
            "their complementary agents. The unrestricted two-core target "
            "survives exactly once at low goods 5 and 6."
        ),
        "limitation": (
            "This refutes only the six-cell canonical strengthening. It is "
            "a positive EFX profile and does not refute unrestricted "
            "two-core selection or additive EFX."
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
