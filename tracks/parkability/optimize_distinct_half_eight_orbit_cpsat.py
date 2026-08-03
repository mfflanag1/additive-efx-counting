#!/usr/bin/env python3
"""Optimize the bounded eight-orbit/full-Hall selection gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_full_cell_cegar import (
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
        three_agent_bottom_pairs,
    )
    from .run_distinct_half_full_cell_cpsat_cegar import (
        add_no_full_hall_cells,
        add_no_three_agent_bottom_pair,
    )
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
    )
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_full_cell_cegar import (
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
        three_agent_bottom_pairs,
    )
    from run_distinct_half_full_cell_cpsat_cegar import (
        add_no_full_hall_cells,
        add_no_three_agent_bottom_pair,
    )
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-eight-orbit-cpsat-optimization-v1"
N = 4
M = 9


def canonicalize_hint(values):
    agent_order = sorted(range(N), key=lambda agent: (-values[agent][0], agent))
    representative_order = tuple(agent + 1 for agent in agent_order)
    relabeled = tuple(
        (values[agent][0],)
        + tuple(values[agent][good] for good in representative_order)
        + tuple(values[agent][good] for good in range(5, M))
        for agent in agent_order
    )
    unmatched_order = sorted(
        range(5, M), key=lambda good: (-relabeled[0][good], good)
    )
    return tuple(
        row[:5] + tuple(row[good] for good in unmatched_order)
        for row in relabeled
    )


def run(
    result_path,
    proto_path,
    cap,
    time_limit,
    workers,
    random_seed,
    hint_path=None,
    hard_six_orbit=False,
    hard_hint_complement=False,
    partition_family="eight_orbit",
    required_agent_bottom_pattern=None,
    forbid_three_agent_bottom_pair=False,
):
    target_family = favorite_pair_universe(partition_family)
    hint_values = (
        (
            load_values(hint_path)
            if required_agent_bottom_pattern is not None
            else canonicalize_hint(load_values(hint_path))
        )
        if hint_path is not None
        else None
    )
    if hint_values is not None and max(map(max, hint_values)) > cap:
        hint_values = None
    if hard_hint_complement and hint_values is None:
        raise ValueError(
            "hard hint-complement mode requires a within-cap hint profile"
        )
    hint_repairs = (
        tuple(supported_partitions(hint_values, list(target_family)))
        if hard_hint_complement
        else ()
    )
    if hard_hint_complement:
        hint_repair_set = set(hint_repairs)
        hard_partitions = tuple(
            partition
            for partition in eight_orbit
            if partition not in hint_repair_set
        )
    elif hard_six_orbit:
        hard_partitions = favorite_pair_universe("six_orbit")
    else:
        hard_partitions = ()
    targets = tuple(
        partition
        for partition in target_family
        if partition not in hard_partitions
    )
    all_favorite_pair = favorite_pair_universe("all")
    positions = {
        partition: position
        for position, partition in enumerate(all_favorite_pair)
    }

    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{agent}_{good}")
            for good in range(M)
        )
        for agent in range(N)
    )
    add_branch(model, values)
    for agent in range(N - 1):
        model.Add(values[agent][0] >= values[agent + 1][0])
    if required_agent_bottom_pattern is None:
        for good in range(5, M - 1):
            model.Add(values[0][good] >= values[0][good + 1])
    else:
        for agent, lows in enumerate(required_agent_bottom_pattern):
            for low in lows:
                for good in range(1, M):
                    if good not in lows:
                        model.Add(values[agent][low] <= values[agent][good])
    full_cell_encoding = add_no_full_hall_cells(model, values, cap)
    no_three_agent_bottom_encoding = (
        add_no_three_agent_bottom_pair(model, values)
        if forbid_three_agent_bottom_pair
        else None
    )

    for partition in hard_partitions:
        add_favorite_pair_obstruction(
            model,
            values,
            partition,
            positions[partition],
        )
    obstruction_guards = []
    for partition in targets:
        guard = model.NewBoolVar(f"obstruct_{positions[partition]}")
        add_favorite_pair_obstruction(
            model,
            values,
            partition,
            positions[partition],
            guard=guard,
        )
        obstruction_guards.append(guard)
    model.Maximize(sum(obstruction_guards))

    if hint_values is not None:
        for agent in range(N):
            for good in range(M):
                model.AddHint(values[agent][good], hint_values[agent][good])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    started = time.time()
    status_code = solver.Solve(model)
    elapsed = time.time() - started

    decoded = None
    target_repairs = ()
    hard_repairs = ()
    all_repairs = ()
    if status_code in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        decoded = tuple(
            tuple(solver.Value(values[agent][good]) for good in range(M))
            for agent in range(N)
        )
        audit_branch(decoded)
        if full_hall_cells(decoded):
            raise AssertionError("decoded profile has a full Hall cell")
        if required_agent_bottom_pattern is not None and any(
            max(decoded[agent][low] for low in lows)
            > min(
                decoded[agent][good]
                for good in range(1, M)
                if good not in lows
            )
            for agent, lows in enumerate(required_agent_bottom_pattern)
        ):
            raise AssertionError("decoded profile lost its bottom pattern")
        if (
            forbid_three_agent_bottom_pair
            and three_agent_bottom_pairs(decoded)
        ):
            raise AssertionError("decoded profile gained a three-agent bottom pair")
        target_repairs = tuple(
            partition
            for partition in targets
            if matching_rank(feasible_graph(decoded, partition)) == N
        )
        hard_repairs = tuple(
            partition
            for partition in hard_partitions
            if matching_rank(feasible_graph(decoded, partition)) == N
        )
        if hard_repairs:
            raise AssertionError("decoded profile violates a hard obstruction")
        all_repairs = tuple(
            supported_partitions(decoded, list(all_favorite_pair))
        )

    histogram = Counter(
        favorite_pair_orbit_signature(partition) for partition in all_repairs
    )
    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    encoded_targets = json.dumps(
        [[list(bundle) for bundle in partition] for partition in targets],
        separators=(",", ":"),
    ).encode()
    semantic_obstructions = (
        len(targets) - len(target_repairs) if decoded is not None else None
    )
    objective = solver.ObjectiveValue() if decoded is not None else None
    bound = solver.BestObjectiveBound() if decoded is not None else None
    if decoded is not None and int(round(objective)) != semantic_obstructions:
        raise AssertionError("guard objective disagrees with semantic replay")

    result = {
        "schema": SCHEMA,
        "status": (
            (
                "FULL_CELL_SELECTION_COUNTEREXAMPLE"
                if partition_family == "all"
                else "EIGHT_ORBIT_SELECTOR_COUNTEREXAMPLE"
            )
            if decoded is not None and not target_repairs
            else (
                "FINITE_CAP_FAVORITE_PAIR_FULL_CELL_THEOREM"
                if partition_family == "all"
                else "FINITE_CAP_EIGHT_ORBIT_THEOREM"
            )
            if status_code == cp_model.OPTIMAL and bound < len(targets)
            else "OPTIMIZATION_CHECKPOINT"
            if decoded is not None
            else "CP_SAT_UNKNOWN"
        ),
        "solver_status": solver.StatusName(status_code),
        "cap": cap,
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "symmetry_breaking": (
            ["nonincreasing favorite values by agent"]
            + (
                ["nonincreasing agent-0 values on goods 5..8"]
                if required_agent_bottom_pattern is None
                else []
            )
        ),
        "partition_family": partition_family,
        "required_agent_bottom_pairs": (
            [list(pair) for pair in required_agent_bottom_pattern]
            if required_agent_bottom_pattern is not None
            else None
        ),
        "three_agent_bottom_pair_forbidden": forbid_three_agent_bottom_pair,
        "no_three_agent_bottom_pair_encoding": (
            no_three_agent_bottom_encoding
        ),
        "hard_partition_family": (
            "hint_eight_orbit_complement"
            if hard_hint_complement
            else "six_orbit"
            if hard_six_orbit
            else None
        ),
        "hard_partition_count": len(hard_partitions),
        "hint_eight_orbit_repair_count": (
            len(hint_repairs) if hard_hint_complement else None
        ),
        "hard_partition_repair_count": (
            len(hard_repairs) if decoded is not None else None
        ),
        "target_partition_count": len(targets),
        "target_partitions_sha256": hashlib.sha256(encoded_targets).hexdigest(),
        "obstruction_objective": objective,
        "obstruction_objective_bound": bound,
        "semantic_obstruction_count": semantic_obstructions,
        "target_repair_count": (
            len(target_repairs) if decoded is not None else None
        ),
        "full_hall_cell_forbidden": True,
        "full_cell_encoding": full_cell_encoding,
        "full_hall_cells": full_hall_cells(decoded) if decoded is not None else None,
        "values": [list(row) for row in decoded] if decoded is not None else None,
        "favorite_pair_efx_partition_count": (
            len(all_repairs) if decoded is not None else None
        ),
        "favorite_pair_efx_orbit_histogram": (
            {
                repr(signature): count
                for signature, count in sorted(
                    histogram.items(), key=lambda item: repr(item[0])
                )
            }
            if decoded is not None
            else None
        ),
        "literal_complete_efx_count": (
            independent.count_complete_efx0(decoded)
            if decoded is not None
            else None
        ),
        "hint_path": str(hint_path) if hint_path is not None else None,
        "time_limit_seconds": time_limit,
        "elapsed_seconds": elapsed,
        "workers": workers,
        "random_seed": random_seed,
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "proto_path": str(proto_path),
        "proto_sha256": hashlib.sha256(proto_path.read_bytes()).hexdigest(),
        "warning": (
            (
                "A zero-repair profile refutes the favorite-pair/full-cell "
                "selector, not EFX existence unless literal complete-EFX "
                "enumeration is also zero."
                if partition_family == "all"
                else "A zero-repair profile refutes only the eight-orbit "
                "selector, not EFX existence unless literal complete-EFX "
                "enumeration is also zero."
            )
            + " Any positive optimum is a finite-cap theorem only."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--cap", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--hard-six-orbit", action="store_true")
    parser.add_argument("--hard-hint-complement", action="store_true")
    parser.add_argument(
        "--partition-family", choices=("eight_orbit", "all"), default="eight_orbit"
    )
    parser.add_argument("--forbid-three-agent-bottom-pair", action="store_true")
    parser.add_argument(
        "--require-agent-bottom-pairs",
        help="semicolon-separated pair per agent, e.g. 5,7;3,7;5,7;3,7",
    )
    args = parser.parse_args()
    if (
        args.cap < 2
        or args.time_limit <= 0
        or args.workers < 1
        or args.random_seed < 0
        or args.hard_six_orbit and args.hard_hint_complement
        or args.hard_hint_complement and args.hint is None
        or args.partition_family == "all"
        and (args.hard_six_orbit or args.hard_hint_complement)
    ):
        parser.error("invalid optimization parameters")
    required_agent_bottom_pattern = None
    if args.require_agent_bottom_pairs is not None:
        try:
            from anneal_distinct_half_eight_orbit import (
                parse_agent_bottom_pattern,
            )
        except ImportError:
            from .anneal_distinct_half_eight_orbit import (
                parse_agent_bottom_pattern,
            )
        try:
            required_agent_bottom_pattern = parse_agent_bottom_pattern(
                args.require_agent_bottom_pairs
            )
        except ValueError as error:
            parser.error(str(error))
    result = run(
        args.result,
        args.proto,
        args.cap,
        args.time_limit,
        args.workers,
        args.random_seed,
        args.hint,
        args.hard_six_orbit,
        args.hard_hint_complement,
        args.partition_family,
        required_agent_bottom_pattern,
        args.forbid_three_agent_bottom_pair,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
