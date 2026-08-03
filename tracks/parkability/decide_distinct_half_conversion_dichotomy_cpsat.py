#!/usr/bin/env python3
"""Bounded CP-SAT decision for the favorite-pair/common-low dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import (
        audit_branch,
        half_matching,
    )
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_distinct_half_pair_cover import (
        balanced_state_universe,
        favorite_pair_balanced_universe,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch, half_matching
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_distinct_half_pair_cover import (
        balanced_state_universe,
        favorite_pair_balanced_universe,
    )


SCHEMA = "distinct-half-conversion-dichotomy-cpsat-v1"
N = 4
M = 9
FAVORITE = 0


def equivalent_ge(model, variable, left, right):
    model.Add(left >= right).OnlyEnforceIf(variable)
    model.Add(left < right).OnlyEnforceIf(variable.Not())


def equivalent_gt(model, variable, left, right):
    model.Add(left > right).OnlyEnforceIf(variable)
    model.Add(left <= right).OnlyEnforceIf(variable.Not())


def add_branch(model, values):
    residual = tuple(range(1, M))
    for observer in range(N):
        favorite = values[observer][FAVORITE]
        for good in residual:
            model.Add(favorite > values[observer][good])
        model.Add(2 * values[observer][observer + 1] > favorite)

        for four_set in itertools.combinations(residual, 4):
            witnesses = []
            for removed in four_set:
                witness = model.NewBoolVar(
                    f"four_{observer}_{'_'.join(map(str, four_set))}_{removed}"
                )
                equivalent_gt(
                    model,
                    witness,
                    sum(
                        values[observer][good]
                        for good in four_set
                        if good != removed
                    ),
                    favorite,
                )
                witnesses.append(witness)
            model.AddBoolOr(witnesses)

        pair_edges = {}
        for left, right in itertools.combinations(residual, 2):
            edge = model.NewBoolVar(f"pair_{observer}_{left}_{right}")
            equivalent_gt(
                model,
                edge,
                values[observer][left] + values[observer][right],
                favorite,
            )
            pair_edges[left, right] = edge

        degree_six = []
        degree_four = []
        for good in residual:
            incident = [
                pair_edges[tuple(sorted((good, other)))]
                for other in residual
                if other != good
            ]
            at_least_six = model.NewBoolVar(f"degree6_{observer}_{good}")
            model.Add(sum(incident) >= 6).OnlyEnforceIf(at_least_six)
            model.Add(sum(incident) <= 5).OnlyEnforceIf(at_least_six.Not())
            degree_six.append(at_least_six)
            at_least_four = model.NewBoolVar(f"degree4_{observer}_{good}")
            model.Add(sum(incident) >= 4).OnlyEnforceIf(at_least_four)
            model.Add(sum(incident) <= 3).OnlyEnforceIf(at_least_four.Not())
            degree_four.append(at_least_four)

        six_branch = model.NewBoolVar(f"six_branch_{observer}")
        model.Add(sum(degree_six) >= 3).OnlyEnforceIf(six_branch)
        model.Add(sum(degree_six) <= 2).OnlyEnforceIf(six_branch.Not())
        four_branch = model.NewBoolVar(f"four_branch_{observer}")
        model.Add(sum(degree_four) >= 4).OnlyEnforceIf(four_branch)
        model.Add(sum(degree_four) <= 3).OnlyEnforceIf(four_branch.Not())
        model.AddBoolOr([six_branch, four_branch])


def add_favorite_pair_obstruction(
    model, values, partition, position, guard=None
):
    feasible = []
    for observer in range(N):
        row = []
        for own_bundle in range(N):
            own = sum(
                values[observer][good] for good in partition[own_bundle]
            )
            comparisons = []
            for target_bundle, target in enumerate(partition):
                if target_bundle == own_bundle:
                    continue
                for removed in target:
                    comparison = model.NewBoolVar(
                        f"efx_{position}_{observer}_{own_bundle}_"
                        f"{target_bundle}_{removed}"
                    )
                    equivalent_ge(
                        model,
                        comparison,
                        own,
                        sum(
                            values[observer][good]
                            for good in target
                            if good != removed
                        ),
                    )
                    comparisons.append(comparison)
            edge = model.NewBoolVar(
                f"feasible_{position}_{observer}_{own_bundle}"
            )
            model.AddBoolAnd(comparisons).OnlyEnforceIf(edge)
            model.AddBoolOr(
                comparison.Not() for comparison in comparisons
            ).OnlyEnforceIf(edge.Not())
            row.append(edge)
        feasible.append(row)
    for matching in itertools.permutations(range(N)):
        constraint = model.AddBoolOr(
            feasible[observer][matching[observer]].Not()
            for observer in range(N)
        )
        if guard is not None:
            constraint.OnlyEnforceIf(guard)


def add_repair_obstruction(model, values, partition, position):
    favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
    low_goods = tuple(good for good in favorite_bundle if good != FAVORITE)
    pairs = tuple(bundle for bundle in partition if bundle != favorite_bundle)
    violations = []
    for observer in range(N):
        for pair_index, pair in enumerate(pairs):
            pair_value = sum(values[observer][good] for good in pair)
            for low_good in low_goods:
                violation = model.NewBoolVar(
                    f"repair_reject_{position}_{observer}_{pair_index}_{low_good}"
                )
                equivalent_gt(
                    model,
                    violation,
                    values[observer][FAVORITE] + values[observer][low_good],
                    pair_value,
                )
                violations.append(violation)
    model.AddBoolOr(violations)


def load_and_canonicalize(path):
    payload = json.loads(path.read_text())
    raw = payload.get("values")
    if raw is None:
        raw = payload["trace"][-1]["values"]
    values = core.validate_values(raw, expected_n=N, expected_m=M, lower=1)
    representatives = half_matching(values)
    if representatives is None:
        raise ValueError("hint has no half-favorite matching")
    old_to_new = {FAVORITE: FAVORITE}
    for observer, good in enumerate(representatives):
        old_to_new[good] = observer + 1
    remaining = [good for good in range(1, M) if good not in representatives]
    for new_good, old_good in enumerate(remaining, start=N + 1):
        old_to_new[old_good] = new_good
    new_to_old = {new: old for old, new in old_to_new.items()}
    return tuple(
        tuple(row[new_to_old[good]] for good in range(M))
        for row in values
    )


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


def run(output, proto_output, cap, time_limit, workers, random_seed, hint_path,
        common_bottom):
    pair_universe = tuple(favorite_pair_balanced_universe())
    repair_universe = tuple(
        partition
        for partition in balanced_state_universe()
        if len(next(bundle for bundle in partition if FAVORITE in bundle)) == 3
    )
    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{observer}_{good}")
            for good in range(M)
        )
        for observer in range(N)
    )
    add_branch(model, values)
    if common_bottom is not None:
        for observer in range(N):
            for low_good in common_bottom:
                for other in range(1, M):
                    if other not in common_bottom:
                        model.Add(
                            values[observer][low_good]
                            <= values[observer][other]
                        )
    for position, partition in enumerate(pair_universe):
        add_favorite_pair_obstruction(model, values, partition, position)
    for position, partition in enumerate(repair_universe):
        add_repair_obstruction(model, values, partition, position)

    if hint_path is not None:
        hint = load_and_canonicalize(hint_path)
        if max(max(row) for row in hint) <= cap:
            for observer in range(N):
                for good in range(M):
                    model.AddHint(values[observer][good], hint[observer][good])

    proto_output.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_output)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_output.read_bytes()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    solver.parameters.log_search_progress = True
    started = time.time()
    status_code = solver.Solve(model)
    elapsed = time.time() - started
    status_name = solver.StatusName(status_code)

    result_values = None
    pair_survivors = None
    repairs = None
    literal_count = None
    if status_code in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        result_values = tuple(
            tuple(solver.Value(values[observer][good]) for good in range(M))
            for observer in range(N)
        )
        audit_branch(result_values)
        pair_survivors = sum(
            matching_rank(feasible_graph(result_values, partition)) == N
            for partition in pair_universe
        )
        repairs = sum(
            repair_holds(result_values, partition)
            for partition in repair_universe
        )
        if pair_survivors or repairs:
            raise AssertionError("CP-SAT model violates the encoded dichotomy failure")
        literal_count = independent.count_complete_efx0(result_values)

    result = {
        "schema": SCHEMA,
        "status": (
            "DICHOTOMY_COUNTEREXAMPLE"
            if result_values is not None
            else "FINITE_CAP_UNSAT_CANDIDATE"
            if status_code == cp_model.INFEASIBLE
            else "CP_SAT_UNKNOWN"
        ),
        "solver_status": status_name,
        "cap": cap,
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "fixed_common_bottom_pair": (
            list(common_bottom) if common_bottom is not None else None
        ),
        "favorite_pair_partition_count": len(pair_universe),
        "common_low_triple_candidate_count": len(repair_universe),
        "elapsed_seconds": elapsed,
        "workers": workers,
        "random_seed": random_seed,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "favorite_pair_efx_partition_count": pair_survivors,
        "common_low_triple_repair_partition_count": repairs,
        "literal_complete_efx_count": literal_count,
        "best_objective_bound": solver.BestObjectiveBound(),
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "wall_time_seconds": solver.WallTime(),
        "proto_path": str(proto_output.resolve()),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "warning": (
            "INFEASIBLE is only a finite-cap result and requires an "
            "independent replay before theorem status."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--cap", type=int, default=100)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--hint-values", type=Path)
    parser.add_argument("--common-bottom")
    args = parser.parse_args()
    common_bottom = None
    if args.common_bottom is not None:
        try:
            common_bottom = tuple(
                int(item) for item in args.common_bottom.split(",")
            )
        except ValueError:
            parser.error("common bottom must contain two comma-separated goods")
        if (
            len(common_bottom) != 2
            or len(set(common_bottom)) != 2
            or any(good <= FAVORITE or good >= M for good in common_bottom)
        ):
            parser.error("common bottom goods are invalid")
    if (
        args.cap < 2
        or args.time_limit <= 0
        or args.workers < 1
        or args.random_seed < 0
    ):
        parser.error("invalid bounded decision parameters")
    result = run(
        args.output,
        args.proto,
        args.cap,
        args.time_limit,
        args.workers,
        args.random_seed,
        args.hint_values,
        common_bottom,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
