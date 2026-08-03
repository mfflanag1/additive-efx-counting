#!/usr/bin/env python3
"""Aggregate dual-Z3 candidates for all eleven all-distinct patterns."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_bottom_pair_pattern_selector_cegar import (
        CANONICAL_PATTERNS,
        goods_pattern,
        multiplicity_signature,
    )
except ImportError:
    from anneal import atomic_json
    from run_bottom_pair_pattern_selector_cegar import (
        CANONICAL_PATTERNS,
        goods_pattern,
        multiplicity_signature,
    )


SCHEMA = "all-distinct-dual-z3-candidates-audit-v1"
EXPECTED_PARTITIONS = {
    9: 282,
    10: 288,
    11: 303,
    12: 318,
    13: 315,
    14: 300,
    15: 315,
    16: 330,
    17: 330,
    18: 345,
    19: 360,
}


def load(path):
    return json.loads(path.read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index_results(paths, encoding):
    indexed = {}
    for path in paths:
        payload = load(path)
        pattern_index = payload.get("pattern_index")
        if pattern_index in indexed:
            raise AssertionError(f"duplicate {encoding} pattern")
        if not (
            pattern_index in EXPECTED_PARTITIONS
            and payload.get("schema")
            == "bottom-pattern-conversion-selector-lra-v1"
            and payload.get("status") == "UNSAT_CANDIDATE"
            and payload.get("solver_status") == "unsat"
            and payload.get("threshold_encoding") == encoding
            and payload.get("agent_bottom_pairs")
            == [list(pair) for pair in goods_pattern(pattern_index)]
            and payload.get("distinct_conversion_partition_count")
            == EXPECTED_PARTITIONS[pattern_index]
            and payload.get("pool_size") == EXPECTED_PARTITIONS[pattern_index]
        ):
            raise AssertionError(f"invalid {encoding} theorem candidate")
        indexed[pattern_index] = (path, payload)
    if set(indexed) != set(EXPECTED_PARTITIONS):
        raise AssertionError(f"missing {encoding} all-distinct pattern")
    return indexed


def run(census_path, cardinal_paths, sorting_paths, output):
    census = load(census_path)
    distinct_indices = tuple(
        index
        for index, pattern in enumerate(CANONICAL_PATTERNS)
        if multiplicity_signature(pattern) == (1, 1, 1, 1)
    )
    if distinct_indices != tuple(EXPECTED_PARTITIONS):
        raise AssertionError("all-distinct canonical pattern indices changed")
    if not (
        census.get("status") == "BOTTOM_PAIR_PATTERN_CENSUS_AUDITED"
        and census.get("canonical_pattern_count") == 20
        and census.get("multiplicity_census", {}).get("1+1+1+1") == 11
    ):
        raise AssertionError("bottom-pair census changed")
    cardinal = index_results(cardinal_paths, "cardinal")
    sorting = index_results(sorting_paths, "sorting")
    for pattern_index in distinct_indices:
        if (
            cardinal[pattern_index][1].get("symmetry_encoding")
            != sorting[pattern_index][1].get("symmetry_encoding")
        ):
            raise AssertionError("dual encodings use different symmetry cuts")

    result = {
        "schema": SCHEMA,
        "status": "ALL_DISTINCT_DUAL_Z3_CANDIDATES",
        "canonical_pattern_indices": list(distinct_indices),
        "canonical_pattern_count": len(distinct_indices),
        "conversion_partition_counts": {
            str(index): EXPECTED_PARTITIONS[index]
            for index in distinct_indices
        },
        "total_cardinal_solve_seconds": sum(
            cardinal[index][1]["elapsed_seconds"] for index in distinct_indices
        ),
        "total_sorting_solve_seconds": sum(
            sorting[index][1]["elapsed_seconds"] for index in distinct_indices
        ),
        "census": {
            "path": str(census_path),
            "sha256": sha256(census_path),
        },
        "sources": {
            str(index): {
                "cardinal": str(cardinal[index][0]),
                "cardinal_sha256": sha256(cardinal[index][0]),
                "sorting": str(sorting[index][0]),
                "sorting_sha256": sha256(sorting[index][0]),
            }
            for index in distinct_indices
        },
        "claim_boundary": (
            "These are dual Z3 theorem candidates. Independent cvc5/CPC "
            "checking is required before promoting the eleven-case class."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--cardinal", action="append", type=Path, required=True)
    parser.add_argument("--sorting", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.census,
                tuple(args.cardinal),
                tuple(args.sorting),
                args.output,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
