#!/usr/bin/env python3
"""Audit a strict counterexample to fixed-host lexicographic floor selection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_normal_form_boundaries import audit_branch
    from .decide_distinct_half_pair_cover import (
        favorite_pair_balanced_universe,
        supported_efx_states,
    )
    from .search_distinct_half_lex_floor import lex_failure
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_normal_form_boundaries import audit_branch
    from decide_distinct_half_pair_cover import (
        favorite_pair_balanced_universe,
        supported_efx_states,
    )
    from search_distinct_half_lex_floor import lex_failure


SCHEMA = "distinct-half-fixed-host-lex-boundary-audit-v1"
VALUES = (
    (43, 27, 29, 42, 35, 38, 39, 15, 8),
    (36, 22, 35, 13, 17, 31, 6, 7, 25),
    (39, 29, 20, 23, 34, 27, 4, 2, 19),
    (47, 27, 34, 10, 46, 26, 23, 32, 38),
)


def audit() -> dict:
    branch = audit_branch(VALUES)
    universe = favorite_pair_balanced_universe()
    failure = lex_failure(VALUES, universe)
    if failure is None:
        raise AssertionError("fixed-host lexicographic boundary disappeared")
    expected = {
        "host": 2,
        "priority_order": [0, 3, 1, 2],
        "partition": [[0, 3], [1, 5, 6], [2, 7], [4, 8]],
        "matching": [0, 2, 1, 3],
        "utilities": [85, 42, 60, 84],
    }
    if any(failure[key] != value for key, value in expected.items()):
        raise AssertionError("fixed-host lexicographic witness changed")
    supported = supported_efx_states(VALUES, universe)
    if not supported:
        raise AssertionError("selection-rule boundary lost complete EFX")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_FIXED_HOST_LEX_BOUNDARY_AUDIT_PASSED",
        "values": [list(row) for row in VALUES],
        "branch_audit": branch,
        "target_partition_count": len(universe),
        "fixed_host_lexicographic_failure": failure,
        "favorite_pair_balanced_efx_partition_count": len(supported),
        "literal_complete_efx_allocation_count": (
            independent.count_complete_efx0(VALUES)
        ),
        "interpretation": (
            "Fixing the triple owner, placing it last, and maximizing the "
            "owner-floor utility vector can select a non-EFX state even in "
            "strict generic position. The profile still has complete EFX."
        ),
        "limitation": (
            "This refutes only the fixed-host lexicographic conversion; it "
            "does not refute a host-changing alternating exchange."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
