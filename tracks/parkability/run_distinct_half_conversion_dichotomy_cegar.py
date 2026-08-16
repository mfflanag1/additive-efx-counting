#!/usr/bin/env python3
"""Exact CEGAR for favorite-pair EFX versus common-low triple repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

import z3

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import half_matching
    from .decide_distinct_half_hall_layers import add_branch
    from .decide_distinct_half_pair_cover import (
        balanced_state_universe,
        favorite_pair_balanced_universe,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import audit_threshold_failure
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import half_matching
    from decide_distinct_half_hall_layers import add_branch
    from decide_distinct_half_pair_cover import (
        balanced_state_universe,
        favorite_pair_balanced_universe,
    )
    from lra_master import ParkabilityLRAMaster
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import audit_threshold_failure
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
    )


SCHEMA = "distinct-half-conversion-dichotomy-cegar-v1"
N = 4
M = 9
FAVORITE = 0


def repair_universe():
    result = tuple(
        partition
        for partition in balanced_state_universe()
        if len(next(bundle for bundle in partition if FAVORITE in bundle)) == 3
    )
    if len(result) != 420:
        raise AssertionError("favorite-triple repair universe changed")
    return result


def repair_holds(values, partition):
    favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
    low_goods = tuple(good for good in favorite_bundle if good != FAVORITE)
    pairs = tuple(bundle for bundle in partition if bundle != favorite_bundle)
    return all(
        all(
            sum(row[good] for good in pair)
            >= row[FAVORITE] + max(row[good] for good in low_goods)
            for pair in pairs
        )
        for row in values
    )


def add_repair_obstruction(master, partition):
    favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
    low_goods = tuple(good for good in favorite_bundle if good != FAVORITE)
    pairs = tuple(bundle for bundle in partition if bundle != favorite_bundle)
    master.solver.add(
        z3.Or(
            *(
                master._sum(observer, pair)
                < (
                    master.values[observer][FAVORITE]
                    + master.values[observer][low_good]
                )
                for observer in range(N)
                for pair in pairs
                for low_good in low_goods
            )
        )
    )


def select_survivors(survivors, limit, kind, strategy):
    if strategy == "first" or len(survivors) <= limit:
        return survivors[:limit]
    primary_counts = Counter()
    secondary_counts = Counter()
    selected = []
    remaining = list(survivors)
    while remaining and len(selected) < limit:
        def keys(partition):
            favorite_bundle = next(
                bundle for bundle in partition if FAVORITE in bundle
            )
            if kind == "pair":
                primary = next(
                    good for good in favorite_bundle if good != FAVORITE
                )
                secondary = next(
                    bundle for bundle in partition if len(bundle) == 3
                )
            else:
                primary = tuple(
                    good for good in favorite_bundle if good != FAVORITE
                )
                secondary = tuple(
                    sorted(bundle for bundle in partition if bundle != favorite_bundle)
                )
            return primary, secondary

        chosen = min(
            remaining,
            key=lambda partition: (
                primary_counts[keys(partition)[0]],
                secondary_counts[keys(partition)[1]],
                partition,
            ),
        )
        remaining.remove(chosen)
        primary, secondary = keys(chosen)
        primary_counts[primary] += 1
        secondary_counts[secondary] += 1
        selected.append(chosen)
    return tuple(selected)


def load_values(path):
    payload = json.loads(path.read_text())
    raw = payload.get("values")
    if raw is None:
        raw = payload["trace"][-1]["values"]
    values = core.validate_values(raw, expected_n=N, expected_m=M, lower=1)
    representatives = half_matching(values)
    if representatives is None:
        raise ValueError(f"seed {path} has no half-favorite matching")
    old_to_new = {FAVORITE: FAVORITE}
    for observer, good in enumerate(representatives):
        old_to_new[good] = observer + 1
    remaining_old = [
        good for good in range(1, M) if good not in representatives
    ]
    for new_good, old_good in enumerate(remaining_old, start=N + 1):
        old_to_new[old_good] = new_good
    return tuple(
        tuple(
            row[next(old for old, new in old_to_new.items() if new == new_good)]
            for new_good in range(M)
        )
        for row in values
    )


def run(result_path, smt2_path, seed_paths, resume_paths, time_limit,
        max_iterations, add_partitions, add_repairs, encoding, preload_all,
        integer_upper, threshold_encoding, selection):
    pair_universe = tuple(favorite_pair_balanced_universe())
    triples = repair_universe()
    master = ParkabilityLRAMaster(N, M, integer_upper=integer_upper)
    if threshold_encoding == "cardinal":
        add_branch(master, None)
    else:
        master.add_strict_favorite_pattern((FAVORITE,) * N)
        for observer in range(N):
            master.solver.add(
                2 * master.values[observer][observer + 1]
                > master.values[observer][FAVORITE]
            )
        add_universal_threshold_failure(master)
    pair_pool = set()
    repair_pool = set()

    if preload_all:
        for partition in pair_universe:
            master.add_partition_obstruction(partition, encoding=encoding)
            pair_pool.add(partition)
        for partition in triples:
            add_repair_obstruction(master, partition)
            repair_pool.add(partition)

    for seed_path in seed_paths:
        values = load_values(seed_path)
        for partition in supported_partitions(values, list(pair_universe)):
            if partition not in pair_pool:
                master.add_partition_obstruction(partition, encoding=encoding)
                pair_pool.add(partition)
        for partition in triples:
            if partition not in repair_pool and repair_holds(values, partition):
                add_repair_obstruction(master, partition)
                repair_pool.add(partition)

    for resume_path in resume_paths:
        resume = json.loads(resume_path.read_text())
        if resume.get("favorite_pair_pool") is not None:
            pair_states = tuple(
                tuple(tuple(bundle) for bundle in partition)
                for partition in resume["favorite_pair_pool"]
            )
            repair_states = tuple(
                tuple(tuple(bundle) for bundle in partition)
                for partition in resume["common_low_triple_repair_pool"]
            )
            for partition in pair_states:
                if partition not in pair_pool:
                    master.add_partition_obstruction(partition, encoding=encoding)
                    pair_pool.add(partition)
            for partition in repair_states:
                if partition not in repair_pool:
                    add_repair_obstruction(master, partition)
                    repair_pool.add(partition)
            continue
        resume_selection = resume.get("survivor_selection", "first")
        if resume_selection != selection:
            raise ValueError("resume selection does not match current selection")
        for trace_entry in resume.get("trace", []):
            values = core.validate_values(
                trace_entry["values"], expected_n=N, expected_m=M, lower=1
            )
            pair_survivors = tuple(
                partition
                for partition in supported_partitions(values, list(pair_universe))
                if partition not in pair_pool
            )
            repair_survivors = tuple(
                partition
                for partition in triples
                if partition not in repair_pool and repair_holds(values, partition)
            )
            for partition in select_survivors(
                pair_survivors, add_partitions, "pair", selection
            ):
                master.add_partition_obstruction(partition, encoding=encoding)
                pair_pool.add(partition)
            for partition in select_survivors(
                repair_survivors, add_repairs, "repair", selection
            ):
                add_repair_obstruction(master, partition)
                repair_pool.add(partition)

    trace = []
    started = time.time()
    status = "ITERATION_LIMIT"
    raw_status = None
    reason_unknown = None
    result_values = None
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit)
        raw_status = solved.raw_status
        if solved.status == "UNSAT":
            status = "UNSAT_CANDIDATE"
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            reason_unknown = solved.reason_unknown
            break
        values = core.validate_values(
            solved.values,
            expected_n=N,
            expected_m=M,
            lower=1,
        )
        audit_threshold_failure(values)
        pair_survivors = tuple(
            partition
            for partition in supported_partitions(values, list(pair_universe))
            if partition not in pair_pool
        )
        repair_survivors = tuple(
            partition
            for partition in triples
            if partition not in repair_pool and repair_holds(values, partition)
        )
        trace.append({
            "iteration": iteration,
            "pair_pool_before": len(pair_pool),
            "repair_pool_before": len(repair_pool),
            "favorite_pair_efx_survivors": len(pair_survivors),
            "common_low_triple_repair_survivors": len(repair_survivors),
            "values": [list(row) for row in values],
        })
        print(
            f"iteration={iteration} pairs={len(pair_survivors)} "
            f"repairs={len(repair_survivors)} "
            f"pools={len(pair_pool)}/{len(repair_pool)}",
            flush=True,
        )
        if not pair_survivors and not repair_survivors:
            status = "DICHOTOMY_COUNTEREXAMPLE"
            result_values = values
            break
        for partition in select_survivors(
            pair_survivors, add_partitions, "pair", selection
        ):
            master.add_partition_obstruction(partition, encoding=encoding)
            pair_pool.add(partition)
        for partition in select_survivors(
            repair_survivors, add_repairs, "repair", selection
        ):
            add_repair_obstruction(master, partition)
            repair_pool.add(partition)

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    literal_count = (
        independent.count_complete_efx0(result_values)
        if result_values is not None
        else None
    )
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": raw_status,
        "reason_unknown": reason_unknown,
        "domain": (
            "strictly positive reals normalized per row"
            if integer_upper is None
            else f"integers in [1,{integer_upper}]"
        ),
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "threshold_encoding": threshold_encoding,
        "survivor_selection": selection,
        "favorite_pair_partition_count": len(pair_universe),
        "common_low_triple_candidate_count": len(triples),
        "favorite_pair_obstruction_encoding": encoding,
        "preloaded_all_obstructions": preload_all,
        "integer_upper": integer_upper,
        "favorite_pair_pool_size": len(pair_pool),
        "common_low_triple_repair_pool_size": len(repair_pool),
        "add_partitions_per_iteration": add_partitions,
        "add_repairs_per_iteration": add_repairs,
        "favorite_pair_pool": [
            [list(bundle) for bundle in partition]
            for partition in sorted(pair_pool)
        ],
        "common_low_triple_repair_pool": [
            [list(bundle) for bundle in partition]
            for partition in sorted(repair_pool)
        ],
        "iterations": iteration,
        "elapsed_seconds": time.time() - started,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "literal_complete_efx_count": literal_count,
        "trace": trace,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT_CANDIDATE would prove the favorite-pair/common-low-triple "
            "dichotomy subject to independent checking. "
            "DICHOTOMY_COUNTEREXAMPLE refutes only this two-normal-form "
            "statement unless its literal complete-EFX count is also zero."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--seed-values", type=Path, action="append", default=[])
    parser.add_argument("--resume-result", type=Path, action="append", default=[])
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--add-partitions", type=int, default=64)
    parser.add_argument("--add-repairs", type=int, default=32)
    parser.add_argument("--preload-all", action="store_true")
    parser.add_argument("--integer-upper", type=int)
    parser.add_argument(
        "--threshold-encoding",
        choices=("cardinal", "sorted"),
        default="cardinal",
    )
    parser.add_argument(
        "--encoding",
        choices=("matching_clauses", "inline_matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument(
        "--selection",
        choices=("first", "diverse"),
        default="first",
    )
    args = parser.parse_args()
    if (
        args.time_limit < 0
        or args.max_iterations < 1
        or args.add_partitions < 1
        or args.add_repairs < 1
        or (
            args.integer_upper is not None
            and args.integer_upper < 2
        )
    ):
        parser.error("invalid CEGAR limits")
    result = run(
        args.result,
        args.smt2,
        tuple(args.seed_values),
        tuple(args.resume_result),
        args.time_limit,
        args.max_iterations,
        args.add_partitions,
        args.add_repairs,
        args.encoding,
        args.preload_all,
        args.integer_upper,
        args.threshold_encoding,
        args.selection,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
