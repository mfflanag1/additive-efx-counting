#!/usr/bin/env python3
"""Audit threshold/Hall gate interaction on the two real boundary profiles."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_integer_partition_cegar import supported_partitions
except ImportError:
    from anneal import atomic_json
    from run_integer_partition_cegar import supported_partitions


SCHEMA = "favorite-singleton-hall-boundaries-audit-v1"
EXPECTED = {
    "singleton_only": {
        0: {(False, False): 423, (False, True): 527, (True, True): 16},
        1: {(False, False): 52, (False, True): 897, (True, True): 17},
        2: {
            (False, False): 632,
            (False, True): 295,
            (True, False): 28,
            (True, True): 11,
        },
        3: {
            (False, False): 567,
            (False, True): 359,
            (True, False): 4,
            (True, True): 36,
        },
    },
    "balanced_only": {
        0: {(False, False): 795, (True, False): 171},
        1: {(False, False): 815, (True, False): 151},
        2: {(False, False): 805, (True, False): 161},
        3: {(False, False): 829, (True, False): 137},
    },
}
EXPECTED_WALL_SLACKS = {
    "singleton_only": (
        (-6262, -6255),
        (-76082, -63823),
        (-13136, -12461),
        (-3841, -3881),
    ),
    "balanced_only": (
        (752, 491),
        (572, 581),
        (824, 1031),
        (2129, 2399),
    ),
}


def residual_partitions() -> tuple[tuple[tuple[int, ...], ...], ...]:
    partitions = set()
    for assignment in itertools.product(range(3), repeat=8):
        if set(assignment) != {0, 1, 2}:
            continue
        partitions.add(
            tuple(
                sorted(
                    tuple(
                        good + 1
                        for good, owner in enumerate(assignment)
                        if owner == slot
                    )
                    for slot in range(3)
                )
            )
        )
    return tuple(sorted(partitions))


def load_values(path: Path) -> tuple[tuple[int, ...], ...]:
    source = json.loads(path.read_text())
    raw = source.get("values")
    if raw is None:
        raw = source["trace"][0]["values"]
    return tuple(tuple(row) for row in raw)


def gate_census(
    values: tuple[tuple[int, ...], ...],
    partitions: tuple[tuple[tuple[int, ...], ...], ...],
    owner: int,
) -> Counter[tuple[bool, bool]]:
    residents = tuple(agent for agent in range(4) if agent != owner)
    resident_values = tuple(values[agent] for agent in residents)
    matched = set(supported_partitions(resident_values, list(partitions)))
    result: Counter[tuple[bool, bool]] = Counter()
    for partition in partitions:
        threshold = max(
            sum(values[owner][good] for good in bundle)
            - min(values[owner][good] for good in bundle)
            for bundle in partition
        )
        result[(partition in matched, threshold <= values[owner][0])] += 1
    return result


def named_counts(counts: Counter[tuple[bool, bool]]) -> dict[str, int]:
    return {
        f"hall_{'pass' if hall else 'fail'}_"
        f"threshold_{'pass' if threshold else 'fail'}": count
        for (hall, threshold), count in sorted(counts.items())
    }


def audit(singleton_path: Path, balanced_path: Path) -> dict:
    partitions = residual_partitions()
    if len(partitions) != 966:
        raise AssertionError("the three-bundle residual universe changed")
    cases = {}
    for name, path in (
        ("singleton_only", singleton_path),
        ("balanced_only", balanced_path),
    ):
        values = load_values(path)
        owner_records = {}
        for owner in range(4):
            counts = gate_census(values, partitions, owner)
            if dict(counts) != EXPECTED[name][owner]:
                raise AssertionError((name, owner, counts))
            residual = sorted(values[owner][1:], reverse=True)
            wall_slacks = (
                residual[2] + residual[6] - values[owner][0],
                residual[3] + residual[4] - values[owner][0],
            )
            if wall_slacks != EXPECTED_WALL_SLACKS[name][owner]:
                raise AssertionError((name, owner, wall_slacks))
            owner_records[str(owner)] = {
                **named_counts(counts),
                "canonical_x3_plus_x7_slack": wall_slacks[0],
                "canonical_x4_plus_x5_slack": wall_slacks[1],
            }
        cases[name] = {
            "source": str(path.resolve()),
            "owners": owner_records,
            "both_gates_pass_count": sum(
                EXPECTED[name][owner].get((True, True), 0)
                for owner in range(4)
            ),
            "threshold_pass_count": sum(
                count
                for owner in range(4)
                for (hall, threshold), count in EXPECTED[name][owner].items()
                if threshold
            ),
        }
    if cases["balanced_only"]["threshold_pass_count"] != 0:
        raise AssertionError("balanced boundary gained a passing threshold")
    return {
        "schema": SCHEMA,
        "status": "HALL_BOUNDARY_AUDIT_PASSED",
        "residual_partition_count_per_owner": len(partitions),
        "owner_partition_checks_per_case": 4 * len(partitions),
        "cases": cases,
        "claim": (
            "The balanced-only profile fails the owner threshold on every "
            "residual partition, whereas the singleton-only profile has 80 "
            "owner/partition pairs passing both the threshold and resident "
            "Hall gates."
        ),
        "analytic_interpretation": (
            "The cleanest common-favorite target is now: if every owner "
            "fails the scalar threshold on every residual partition, force "
            "a balanced four-agent Hall matching. Universal threshold "
            "failure implies the canonical per-row rank-sum disjunction "
            "x3+x7>f or x4+x5>f."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--singleton-source",
        type=Path,
        default=Path("results/efx49_common_favorite_real_sparse_session1.json"),
    )
    parser.add_argument(
        "--balanced-source",
        type=Path,
        default=Path("results/efx49_common_favorite_real_shape6111_session1.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.singleton_source, args.balanced_source)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
