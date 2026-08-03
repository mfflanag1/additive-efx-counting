#!/usr/bin/env python3
"""Exact coordinate descent for singleton support in a rank-one repair cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        in_cell,
        in_rank_one_cell,
        repair_partitions,
        singleton_partitions,
        supporting_singletons,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from optimize_common_favorite_rank1_bridge_singletons_cpsat import (
        in_cell,
        in_rank_one_cell,
        repair_partitions,
        singleton_partitions,
        supporting_singletons,
    )


SCHEMA = "common-favorite-rank1-bridge-singleton-local-search-v1"


def support_count_below(values, universe, ceiling):
    count = 0
    for partition in universe:
        if supporting_singletons(values, (partition,)):
            count += 1
            if count >= ceiling:
                return count
    return count


def run(source_path, repair_family, upper, hamming_two, output_path):
    if upper < 1 or output_path.exists():
        raise ValueError("a positive cap and new output path are required")
    source = json.loads(source_path.read_text())
    raw_values = source.get("best_values", source.get("values"))
    values = core.validate_values(
        raw_values,
        expected_n=4,
        expected_m=9,
        lower=1,
        upper=upper,
    )
    blocked = repair_partitions(repair_family)
    universe = singleton_partitions()
    if not in_cell(values, blocked):
        raise ValueError("source profile does not block the selected repair family")

    current = values
    current_score = len(supporting_singletons(current, universe))
    sequence = [current_score]
    rounds = []
    while True:
        best_score = current_score
        best_values = None
        examined = 0
        premise_pass = 0
        repair_pass = 0
        for observer in range(4):
            for good in range(9):
                for value in range(1, upper + 1):
                    if value == current[observer][good]:
                        continue
                    examined += 1
                    candidate_rows = [list(row) for row in current]
                    candidate_rows[observer][good] = value
                    candidate = tuple(tuple(row) for row in candidate_rows)
                    if not in_rank_one_cell(candidate):
                        continue
                    premise_pass += 1
                    if not in_cell(candidate, blocked):
                        continue
                    repair_pass += 1
                    score = support_count_below(candidate, universe, best_score)
                    if score < best_score or (
                        score == best_score
                        and best_values is not None
                        and candidate > best_values
                    ):
                        best_score = score
                        best_values = candidate
        rounds.append({
            "search": "hamming_one",
            "score_before": current_score,
            "examined_neighbor_count": examined,
            "rank_one_premise_neighbor_count": premise_pass,
            "repair_blocking_neighbor_count": repair_pass,
            "best_strictly_lower_score": (
                best_score if best_score < current_score else None
            ),
        })
        if best_values is None or best_score >= current_score:
            if not hamming_two:
                break
            coordinates = tuple(itertools.product(range(4), range(9)))
            best_score = current_score
            best_values = None
            examined = 0
            premise_pass = 0
            repair_pass = 0
            for (left_observer, left_good), (
                right_observer,
                right_good,
            ) in itertools.combinations(coordinates, 2):
                for left_value in range(1, upper + 1):
                    if left_value == current[left_observer][left_good]:
                        continue
                    for right_value in range(1, upper + 1):
                        if right_value == current[right_observer][right_good]:
                            continue
                        examined += 1
                        candidate_rows = [list(row) for row in current]
                        candidate_rows[left_observer][left_good] = left_value
                        candidate_rows[right_observer][right_good] = right_value
                        candidate = tuple(tuple(row) for row in candidate_rows)
                        if not in_rank_one_cell(candidate):
                            continue
                        premise_pass += 1
                        if not in_cell(candidate, blocked):
                            continue
                        repair_pass += 1
                        score = support_count_below(
                            candidate,
                            universe,
                            best_score,
                        )
                        if score < best_score or (
                            score == best_score
                            and best_values is not None
                            and candidate > best_values
                        ):
                            best_score = score
                            best_values = candidate
            rounds.append({
                "search": "hamming_two",
                "score_before": current_score,
                "examined_neighbor_count": examined,
                "rank_one_premise_neighbor_count": premise_pass,
                "repair_blocking_neighbor_count": repair_pass,
                "best_strictly_lower_score": (
                    best_score if best_score < current_score else None
                ),
            })
            if best_values is None or best_score >= current_score:
                break
        current = best_values
        current_score = best_score
        sequence.append(current_score)

    result = {
        "schema": SCHEMA,
        "status": (
            "ZERO_SINGLETON_LOCAL_WITNESS"
            if current_score == 0
            else "HAMMING_TWO_LOCAL_MINIMUM"
            if hamming_two
            else "ONE_COORDINATE_LOCAL_MINIMUM"
        ),
        "n": 4,
        "m": 9,
        "domain": f"positive integers in [1,{upper}]",
        "upper": upper,
        "repair_family": repair_family,
        "repair_partition_count": len(blocked),
        "hamming_two": hamming_two,
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "singleton_support_count_sequence": sequence,
        "final_singleton_support_count": current_score,
        "values": [list(row) for row in current],
        "rounds": rounds,
        "claim_boundary": (
            "This certifies only the recorded local neighborhood. "
            "A positive local minimum is not a global lower bound."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--repair-family",
        choices=("bridge30", "bridge45"),
        default="bridge45",
    )
    parser.add_argument("--upper", type=int, default=6)
    parser.add_argument("--hamming-two", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.source,
        args.repair_family,
        args.upper,
        args.hamming_two,
        args.output,
    )


if __name__ == "__main__":
    main()
