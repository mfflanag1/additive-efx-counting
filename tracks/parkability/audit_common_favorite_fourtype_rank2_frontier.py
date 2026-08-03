#!/usr/bin/env python3
"""Audit the bounded four-type rank-two selection frontier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_common_favorite_mixed_selection_gate import audit_search
except ImportError:
    from anneal import atomic_json
    from audit_common_favorite_mixed_selection_gate import audit_search


SCHEMA = "common-favorite-fourtype-rank2-frontier-audit-v1"


def run(source_paths, output):
    if not source_paths or output.exists():
        raise ValueError("at least one source and a new output are required")
    searches = []
    for path in source_paths:
        payload = json.loads(path.read_text())
        if (
            payload.get("cell_symmetry") is not True
            or payload.get("require_upper_used") is not False
            or payload.get("selected_owner") != 0
            or payload.get("selected_residual_partition")
            != [[1, 2, 3], [4, 5, 6], [7, 8]]
        ):
            raise ValueError("four-type selection-search scope changed")
        searches.append(
            audit_search(
                path,
                "rank_two",
                upper=4,
                require_pairwise_nonproportional_rows=True,
            )
        )
    result = {
        "schema": SCHEMA,
        "status": "FOUR_TYPE_RANK_TWO_GATE_OPEN",
        "n": 4,
        "m": 9,
        "upper": 4,
        "strict_common_favorite": 0,
        "selected_residual_shape": "332",
        "selection_motif": "rank_two",
        "pairwise_nonproportional_rows": True,
        "searches": searches,
        "final_reconstructed_learned_motif_count": searches[-1][
            "reconstructed_learned_motif_count"
        ],
        "claim_boundary": (
            "Every trace profile, seed hash, proto hash, motif census, and "
            "pairwise-nonproportional-row condition is replayed exactly. "
            "An iteration limit or timeout is not a proof of the bounded "
            "rank-two selector and not an EFX-existence theorem."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
