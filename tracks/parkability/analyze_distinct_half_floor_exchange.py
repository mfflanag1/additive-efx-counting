#!/usr/bin/env python3
"""Analyze lexicographic owner-floor states at a distinct-half boundary."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
except ImportError:
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe


SCHEMA = "distinct-half-floor-exchange-analysis-v1"
N = 4
FAVORITE = 0


def bundle_value(row, bundle) -> int:
    return sum(row[good] for good in bundle)


def floor_matchings(values, partition):
    return tuple(
        matching
        for matching in itertools.permutations(range(N))
        if all(
            bundle_value(values[observer], partition[matching[observer]])
            >= values[observer][FAVORITE]
            for observer in range(N)
        )
    )


def efx_violations(values, partition, matching):
    violations = []
    for observer in range(N):
        own = bundle_value(values[observer], partition[matching[observer]])
        for target_bundle, target in enumerate(partition):
            if target_bundle == matching[observer]:
                continue
            for removed in target:
                remainder = bundle_value(
                    values[observer],
                    tuple(good for good in target if good != removed),
                )
                if remainder > own:
                    violations.append({
                        "observer": observer,
                        "target_bundle": target_bundle,
                        "removed_good": removed,
                        "own_value": own,
                        "remainder_value": remainder,
                    })
    return violations


def run(session_path: Path) -> dict:
    source = json.loads(session_path.read_text())
    values = tuple(tuple(row) for row in source["trace"][0]["values"])
    universe = favorite_pair_balanced_universe()
    states_by_host = {host: [] for host in range(N)}
    floor_allocation_count = 0
    efx_floor_allocation_count = 0
    for partition in universe:
        triple_index = next(
            index for index, bundle in enumerate(partition) if len(bundle) == 3
        )
        for matching in floor_matchings(values, partition):
            floor_allocation_count += 1
            host = matching.index(triple_index)
            utilities = tuple(
                bundle_value(values[observer], partition[matching[observer]])
                for observer in range(N)
            )
            violations = efx_violations(values, partition, matching)
            if not violations:
                efx_floor_allocation_count += 1
            states_by_host[host].append(
                (utilities, partition, matching, violations)
            )

    priority_records = []
    for host in range(N):
        for prefix in itertools.permutations(
            observer for observer in range(N) if observer != host
        ):
            order = prefix + (host,)
            states = states_by_host[host]
            if not states:
                priority_records.append({
                    "host": host,
                    "priority_order": list(order),
                    "state_exists": False,
                })
                continue
            best = max(
                states,
                key=lambda state: tuple(state[0][observer] for observer in order),
            )
            utilities, partition, matching, violations = best
            favorite_bundle_index = next(
                index
                for index, bundle in enumerate(partition)
                if FAVORITE in bundle
            )
            favorite_owner = matching.index(favorite_bundle_index)
            absorption = []
            for violation in violations:
                observer = violation["observer"]
                if violation["target_bundle"] != matching[host]:
                    continue
                old_bundle = partition[matching[observer]]
                left_behind = violation["removed_good"]
                candidate = old_bundle + (left_behind,)
                slack = (
                    bundle_value(values[host], candidate)
                    - values[host][FAVORITE]
                )
                absorption.append({
                    "envier": observer,
                    "envier_owns_favorite_pair": observer == favorite_owner,
                    "left_behind": left_behind,
                    "host_absorption_bundle": list(candidate),
                    "host_floor_slack": slack,
                })
            priority_records.append({
                "host": host,
                "priority_order": list(order),
                "state_exists": True,
                "partition": [list(bundle) for bundle in partition],
                "matching": list(matching),
                "utilities": list(utilities),
                "efx": not violations,
                "violation_count": len(violations),
                "triple_absorption": absorption,
            })

    efx_lex_count = sum(record.get("efx", False) for record in priority_records)
    return {
        "schema": SCHEMA,
        "source": str(session_path.resolve()),
        "values": [list(row) for row in values],
        "target_partition_count": len(universe),
        "floor_allocation_count": floor_allocation_count,
        "efx_floor_allocation_count": efx_floor_allocation_count,
        "priority_record_count": len(priority_records),
        "efx_lexicographic_record_count": efx_lex_count,
        "priority_records": priority_records,
        "interpretation": (
            "Descriptive exact analysis of lexicographically maximal "
            "favorite-pair owner-floor states at one adversarial boundary; "
            "it is not a universal theorem."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.session)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
