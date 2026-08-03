#!/usr/bin/env python3
"""Bounded decision for the rank-one triple conversion dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from collections import Counter
from pathlib import Path

import ortools

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        CONTESTED,
        FAVORITE,
        M,
        N,
        OWNER,
        RESIDUAL,
        conversion_partitions,
        resident_graph,
    )
    from .decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from .decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )
    from .integer_partition_master import IntegerPartitionMaster
    from .master import add_lex_ge
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        CONTESTED,
        FAVORITE,
        M,
        N,
        OWNER,
        RESIDUAL,
        conversion_partitions,
        resident_graph,
    )
    from decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )
    from integer_partition_master import IntegerPartitionMaster
    from master import add_lex_ge


SCHEMA = "common-favorite-rank1-triple-conversion-cpsat-v1"
UPPER_HIT_GROUPS = {
    "f": (FAVORITE,),
    "a": RESIDUAL[0],
    "b": RESIDUAL[1],
    "c": RESIDUAL[2],
}


def add_zero_neighbor_obstruction(master, partition, partition_index):
    bundles = tuple(sorted(tuple(sorted(bundle)) for bundle in partition))
    masks = tuple(sum(1 << good for good in bundle) for bundle in bundles)
    selectors = []
    for bundle_index in range(N):
        selector = master.model.NewBoolVar(
            f"zero_neighbor_{partition_index}_{bundle_index}"
        )
        selectors.append(selector)
        for observer in range(N):
            violations = master._edge_violations(
                observer,
                bundle_index,
                bundles,
                masks,
            )
            master.model.AddBoolOr(violations).OnlyEnforceIf(selector)
    master.model.AddBoolOr(selectors)


def add_cell_symmetry(master):
    for resident in range(1, N - 1):
        add_lex_ge(
            master.model,
            master.values[resident],
            master.values[resident + 1],
            f"resident_{resident}_{resident + 1}",
        )
    for group_index, group in enumerate(RESIDUAL):
        for left, right in zip(group, group[1:]):
            add_lex_ge(
                master.model,
                [master.values[observer][left] for observer in range(N)],
                [master.values[observer][right] for observer in range(N)],
                f"group_{group_index}_good_{left}_{right}",
            )


def add_rank_one_premise(master):
    masks = tuple(sum(1 << good for good in bundle) for bundle in RESIDUAL)
    for resident in range(1, N):
        for bundle_index in range(len(RESIDUAL)):
            violations = master._edge_violations(
                resident,
                bundle_index,
                RESIDUAL,
                masks,
            )
            if bundle_index == 0:
                master.model.AddBoolAnd(
                    [violation.Not() for violation in violations]
                )
            else:
                master.model.AddBoolOr(violations)


def cell_symmetric(values):
    if any(values[left] < values[left + 1] for left in range(1, N - 1)):
        return False
    return all(
        all(
            tuple(values[observer][left] for observer in range(N))
            >= tuple(values[observer][right] for observer in range(N))
            for left, right in zip(group, group[1:])
        )
        for group in RESIDUAL
    )


def canonicalize_cell(values):
    candidates = []
    for residents in itertools.permutations(range(1, N)):
        row_order = (OWNER,) + residents
        for first in itertools.permutations(RESIDUAL[0]):
            for second in itertools.permutations(RESIDUAL[1]):
                for third in itertools.permutations(RESIDUAL[2]):
                    good_order = (FAVORITE,) + first + second + third
                    transformed = tuple(
                        tuple(values[row][good] for good in good_order)
                        for row in row_order
                    )
                    if cell_symmetric(transformed):
                        candidates.append(transformed)
    if not candidates:
        raise AssertionError("cell orbit has no symmetry representative")
    return max(candidates)


def run(
    upper,
    conversion_scope,
    hall_obstruction,
    obstruction_encoding,
    cell_symmetry,
    identical_residents,
    resident_collision,
    resident_equality_pair,
    require_upper_used,
    required_upper_hit,
    cegar_singletons,
    add_per_iteration,
    max_iterations,
    time_limit,
    workers,
    seed_paths,
    result_path,
    proto_path,
):
    if (
        upper < 1
        or conversion_scope not in {
            "first",
            "all",
            "radius2",
            "radius2_contested",
            "radius2_bridge",
            "radius2_extended_bridge",
            "orbit_aab",
            "orbit_bcc",
        }
        or hall_obstruction not in {"any", "zero_neighbor"}
        or obstruction_encoding
        not in {
            "matching_clauses",
            "hall_selectors",
            "duplicate_matching_clauses",
            "duplicate_hall_selectors",
        }
        or type(cell_symmetry) is not bool
        or type(identical_residents) is not bool
        or type(resident_collision) is not bool
        or type(require_upper_used) is not bool
        or resident_equality_pair not in {None, "12", "23"}
        or required_upper_hit not in {
            None,
            *(f"{observer}{group}" for observer in range(N) for group in UPPER_HIT_GROUPS),
        }
        or sum(
            (identical_residents, resident_collision, resident_equality_pair is not None)
        )
        > 1
        or (
            obstruction_encoding
            in {"duplicate_matching_clauses", "duplicate_hall_selectors"}
            and resident_equality_pair is None
        )
        or add_per_iteration < 1
        or max_iterations < 1
        or time_limit <= 0
        or workers < 1
        or result_path.exists()
        or proto_path.exists()
    ):
        raise ValueError("valid bounds and new output paths are required")
    master = IntegerPartitionMaster(N, M, upper, require_upper_used=require_upper_used)
    if required_upper_hit is not None:
        observer = int(required_upper_hit[0])
        group = required_upper_hit[1]
        upper_hits = []
        for good in UPPER_HIT_GROUPS[group]:
            hit = master.model.NewBoolVar(
                f"required_upper_hit_{observer}_{group}_{good}"
            )
            master.model.Add(
                master.values[observer][good] == upper
            ).OnlyEnforceIf(hit)
            master.model.Add(
                master.values[observer][good] <= upper - 1
            ).OnlyEnforceIf(hit.Not())
            upper_hits.append(hit)
        master.model.AddBoolOr(upper_hits)
    if cell_symmetry:
        add_cell_symmetry(master)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    favorite = master.values[OWNER][FAVORITE]
    for bundle in RESIDUAL:
        for removed in bundle:
            master.model.Add(
                favorite
                >= sum(
                    master.values[OWNER][good]
                    for good in bundle
                    if good != removed
                )
            )
    add_rank_one_premise(master)
    if identical_residents:
        for resident in range(2, N):
            for good in range(M):
                master.model.Add(
                    master.values[1][good] == master.values[resident][good]
                )
    elif resident_collision:
        adjacent_equal = []
        for resident in range(1, N - 1):
            selector = master.model.NewBoolVar(
                f"resident_rows_{resident}_{resident + 1}_equal"
            )
            adjacent_equal.append(selector)
            for good in range(M):
                master.model.Add(
                    master.values[resident][good]
                    == master.values[resident + 1][good]
                ).OnlyEnforceIf(selector)
        master.model.AddBoolOr(adjacent_equal)
    elif resident_equality_pair is not None:
        first = int(resident_equality_pair[0])
        second = int(resident_equality_pair[1])
        for good in range(M):
            master.model.Add(
                master.values[first][good] == master.values[second][good]
            )

    def add_partition_obstruction(partition):
        if obstruction_encoding in {
            "duplicate_matching_clauses",
            "duplicate_hall_selectors",
        }:
            duplicate_observers = tuple(map(int, resident_equality_pair))
            master.add_duplicate_row_partition_obstruction(
                partition,
                duplicate_observers,
                encoding=obstruction_encoding,
            )
        else:
            master.add_partition_obstruction(
                partition,
                encoding=obstruction_encoding,
            )

    singleton_partitions = tuple(
        ((FAVORITE,),) + partition for partition in residual_partitions()
    )
    singleton_pool = []
    singleton_pool_set = set()
    if not cegar_singletons:
        for partition in singleton_partitions:
            add_partition_obstruction(partition)
            singleton_pool.append(partition)
            singleton_pool_set.add(tuple(sorted(partition)))
    all_conversions = conversion_partitions()
    radius_two = balanced_transfer_neighborhood(RESIDUAL, 2)
    contested_partner = tuple(
            partition
            for partition in radius_two
            for favorite_bundle in [
                next(bundle for bundle in partition if FAVORITE in bundle)
            ]
            if len(favorite_bundle) == 2
            and next(
                good for good in favorite_bundle if good != FAVORITE
            )
            in CONTESTED
        )
    bridge_orbit = tuple(
        partition
        for partition in radius_two
        for favorite_bundle in [
            next(bundle for bundle in partition if FAVORITE in bundle)
        ]
        for triple in [next(bundle for bundle in partition if len(bundle) == 3)]
        if len(favorite_bundle) == 2
        and next(good for good in favorite_bundle if good != FAVORITE)
        in RESIDUAL[1]
        and (
            sum(good in RESIDUAL[0] for good in triple),
            sum(good in RESIDUAL[1] for good in triple),
            sum(good in RESIDUAL[2] for good in triple),
        )
        == (1, 2, 0)
    )
    extended_bridge_orbits = tuple(
        partition
        for partition in radius_two
        for favorite_bundle in [
            next(bundle for bundle in partition if FAVORITE in bundle)
        ]
        for triple in [next(bundle for bundle in partition if len(bundle) == 3)]
        if len(favorite_bundle) == 2
        and (
            (
                next(good for good in favorite_bundle if good != FAVORITE)
                in RESIDUAL[2]
                and (
                    sum(good in RESIDUAL[0] for good in triple),
                    sum(good in RESIDUAL[1] for good in triple),
                    sum(good in RESIDUAL[2] for good in triple),
                )
                == (0, 3, 0)
            )
            or (
                next(good for good in favorite_bundle if good != FAVORITE)
                in RESIDUAL[1]
                and (
                    sum(good in RESIDUAL[0] for good in triple),
                    sum(good in RESIDUAL[1] for good in triple),
                    sum(good in RESIDUAL[2] for good in triple),
                )
                == (1, 0, 2)
            )
        )
    )
    if conversion_scope == "radius2":
        blocked_partitions = radius_two
    elif conversion_scope == "radius2_contested":
        blocked_partitions = contested_partner
    elif conversion_scope == "radius2_bridge":
        blocked_partitions = tuple(sorted(set(contested_partner) | set(bridge_orbit)))
    elif conversion_scope == "radius2_extended_bridge":
        blocked_partitions = tuple(sorted(
            set(contested_partner) | set(bridge_orbit) | set(extended_bridge_orbits)
        ))
    elif conversion_scope in {"orbit_aab", "orbit_bcc"}:
        target_counts = (
            (2, 1, 0) if conversion_scope == "orbit_aab" else (0, 1, 2)
        )
        blocked_partitions = tuple(
            partition
            for partition in contested_partner
            for triple in [next(bundle for bundle in partition if len(bundle) == 3)]
            if (
                sum(good in RESIDUAL[0] for good in triple),
                sum(good in RESIDUAL[1] for good in triple),
                sum(good in RESIDUAL[2] for good in triple),
            )
            == target_counts
        )
    else:
        blocked_partitions = conversion_partitions(conversion_scope)
    for partition_index, partition in enumerate(blocked_partitions):
        if hall_obstruction == "any":
            add_partition_obstruction(partition)
        else:
            add_zero_neighbor_obstruction(master, partition, partition_index)

    seed_imports = []
    for seed_path in seed_paths:
        seed = json.loads(seed_path.read_text())
        if not cegar_singletons:
            raise ValueError("singleton seeds require CEGAR mode")
        value_domain_matches = seed.get("upper") == upper
        candidates = []
        if value_domain_matches:
            candidates.extend(
                tuple(tuple(row) for row in record["values"])
                for record in seed.get("cegar_trace", [])
            )
            if seed.get("values") is not None:
                candidates.append(tuple(tuple(row) for row in seed["values"]))
            if seed.get("best_values") is not None:
                candidates.append(tuple(tuple(row) for row in seed["best_values"]))
        imported = 0
        direct_imported = 0
        singleton_keys = {
            tuple(sorted(partition)) for partition in singleton_partitions
        }
        direct_singleton_field = (
            "singleton_obstruction_core_partitions"
            if "singleton_obstruction_core_partitions" in seed
            else "singleton_obstruction_partitions"
        )
        for raw_partition in seed.get(direct_singleton_field, []):
            partition = tuple(
                sorted(tuple(sorted(bundle)) for bundle in raw_partition)
            )
            key = tuple(sorted(partition))
            if key not in singleton_keys:
                raise ValueError("direct seed partition left the singleton universe")
            if key in singleton_pool_set:
                continue
            add_partition_obstruction(partition)
            singleton_pool.append(partition)
            singleton_pool_set.add(key)
            direct_imported += 1
        for raw_values in candidates:
            values = core.validate_values(
                raw_values,
                expected_n=N,
                expected_m=M,
                lower=1,
                upper=upper,
            )
            if cell_symmetry:
                values = canonicalize_cell(values)
            for partition in singleton_partitions:
                key = tuple(sorted(partition))
                if (
                    key not in singleton_pool_set
                    and matching_rank(feasible_graph(values, partition)) == N
                ):
                    add_partition_obstruction(partition)
                    singleton_pool.append(partition)
                    singleton_pool_set.add(key)
                    imported += 1
        seed_imports.append({
            "source": str(seed_path),
            "source_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
            "model_count": len(candidates),
            "new_singleton_count": imported,
            "direct_singleton_partition_count": direct_imported,
            "direct_singleton_field": direct_singleton_field,
            "import_mode": "singleton_obstructions_only",
            "source_conversion_scope": seed.get("conversion_scope"),
            "source_schema": seed.get("schema"),
            "source_hall_obstruction": seed.get("hall_obstruction", "any"),
            "value_domain_matches": value_domain_matches,
            "canonicalized_for_cell_symmetry": cell_symmetry,
        })

    started = time.time()
    trace = []
    solved = None
    candidate = None
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(
            time_limit_s=time_limit,
            workers=workers,
            random_seed=1,
        )
        if solved.status != "SAT":
            break
        values = solved.values
        assert values is not None
        if not cegar_singletons:
            candidate = values
            break
        survivors = []
        for partition in singleton_partitions:
            key = tuple(sorted(partition))
            if key in singleton_pool_set:
                continue
            if matching_rank(feasible_graph(values, partition)) == N:
                survivors.append(partition)
        trace.append({
            "iteration": iteration,
            "singleton_pool_size_before": len(singleton_pool),
            "supported_unpooled_singleton_partition_count": len(survivors),
            "solver_status": solved.raw_status,
            "solver_wall_seconds": solved.wall_time_seconds,
            "values": [list(row) for row in values],
        })
        if not survivors:
            candidate = values
            break
        for partition in survivors[:add_per_iteration]:
            add_partition_obstruction(partition)
            singleton_pool.append(partition)
            singleton_pool_set.add(tuple(sorted(partition)))
    if solved is None:
        raise AssertionError("CP-SAT performed no solve")
    elapsed = time.time() - started
    values = candidate
    candidate_audit = None
    if values is not None:
        singleton_support = sum(
            matching_rank(feasible_graph(values, partition)) == N
            for partition in singleton_partitions
        )
        conversion_ranks = [
            matching_rank(feasible_graph(values, partition))
            for partition in all_conversions
        ]
        if (
            any(row[FAVORITE] <= max(row[1:]) for row in values)
            or not threshold_passes(values, OWNER, RESIDUAL)
            or resident_graph(values) != ((True, False, False),) * 3
            or (
                identical_residents
                and any(values[1] != values[resident] for resident in range(2, N))
            )
            or (
                resident_collision
                and len({values[resident] for resident in range(1, N)}) == N - 1
            )
            or (
                resident_equality_pair is not None
                and values[int(resident_equality_pair[0])]
                != values[int(resident_equality_pair[1])]
            )
            or (
                required_upper_hit is not None
                and not any(
                    values[int(required_upper_hit[0])][good] == upper
                    for good in UPPER_HIT_GROUPS[required_upper_hit[1]]
                )
            )
            or singleton_support
            or any(
                matching_rank(feasible_graph(values, partition)) == N
                for partition in blocked_partitions
            )
            or (
                hall_obstruction == "zero_neighbor"
                and any(
                    all(any(row[bundle] for row in graph) for bundle in range(N))
                    for partition in blocked_partitions
                    for graph in [feasible_graph(values, partition)]
                )
            )
        ):
            raise AssertionError("decoded CP-SAT model left the decision cell")
        support_shapes = Counter()
        support_count = 0
        for partition in core.iter_unlabeled_nonempty_partitions(N, M):
            if matching_rank(feasible_graph(values, partition)) != N:
                continue
            support_count += 1
            support_shapes[
                "".join(map(str, sorted(map(len, partition), reverse=True)))
            ] += 1
        candidate_audit = {
            "selected_owner_threshold_pass": True,
            "resident_graph": [list(row) for row in resident_graph(values)],
            "favorite_singleton_supporting_partition_count": 0,
            "all_three_conversion_ranks": conversion_ranks,
            "blocked_partition_supporting_count": 0,
            "all_supporting_partition_count": support_count,
            "supporting_partition_count_by_shape": dict(sorted(support_shapes.items())),
            "complete_efx_allocation_count": independent.count_complete_efx0(values),
        }

    proto_path.parent.mkdir(parents=True, exist_ok=True)
    if not master.model.ExportToFile(str(proto_path)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_path.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": (
            "RANK1_TRIPLE_DICHOTOMY_COUNTEREXAMPLE"
            if values is not None
            else "BOUNDED_RANK1_TRIPLE_DICHOTOMY_UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "ITERATION_LIMIT"
            if solved.status == "SAT"
            else "MASTER_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "n": N,
        "m": M,
        "domain": f"positive integers in [1,{upper}]",
        "upper": upper,
        "strict_common_favorite": FAVORITE,
        "selected_owner": OWNER,
        "selected_residual_partition": [list(bundle) for bundle in RESIDUAL],
        "resident_rank_one_common_bundle": list(CONTESTED),
        "conversion_scope": conversion_scope,
        "hall_obstruction": hall_obstruction,
        "obstruction_encoding": obstruction_encoding,
        "cell_symmetry": cell_symmetry,
        "identical_residents": identical_residents,
        "resident_collision": resident_collision,
        "resident_equality_pair": resident_equality_pair,
        "require_upper_used": require_upper_used,
        "required_upper_hit": required_upper_hit,
        "blocked_partition_count": len(blocked_partitions),
        "favorite_singleton_partition_count": len(singleton_partitions),
        "cegar_singletons": cegar_singletons,
        "singleton_obstruction_pool_size": len(singleton_pool),
        "singleton_obstruction_partitions": [
            [list(bundle) for bundle in partition]
            for partition in singleton_pool
        ],
        "cegar_iterations": len(trace),
        "cegar_trace": trace,
        "seed_imports": seed_imports,
        "values": [list(row) for row in values] if values else None,
        "candidate_audit": candidate_audit,
        "solver_wall_seconds": solved.wall_time_seconds,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "max_iterations": max_iterations,
        "add_per_iteration": add_per_iteration,
        "comparison_variables": len(master._comparison_variables),
        "matching_clauses": master.matching_clauses,
        "hall_selectors": master.hall_selectors,
        "hall_edge_clauses": master.hall_edge_clauses,
        "conflicts": solved.conflicts,
        "branches": solved.branches,
        "proto": str(proto_path),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "proto_bytes": len(proto),
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools.__version__,
        },
        "claim_boundary": (
            "SAT refutes only the selected local conversion-or-singleton "
            "implication under the recorded Hall-obstruction strength; it is "
            "not an EFX counterexample. UNSAT is bounded and requires "
            "independent replay."
        ),
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upper", type=int, default=20)
    parser.add_argument(
        "--conversion-scope",
        choices=(
            "first",
            "all",
            "radius2",
            "radius2_contested",
            "radius2_bridge",
            "radius2_extended_bridge",
            "orbit_aab",
            "orbit_bcc",
        ),
        default="first",
    )
    parser.add_argument("--time-limit", type=float, default=60)
    parser.add_argument(
        "--hall-obstruction",
        choices=("any", "zero_neighbor"),
        default="any",
    )
    parser.add_argument(
        "--obstruction-encoding",
        choices=(
            "matching_clauses",
            "hall_selectors",
            "duplicate_matching_clauses",
            "duplicate_hall_selectors",
        ),
        default="matching_clauses",
    )
    parser.add_argument("--cell-symmetry", action="store_true")
    parser.add_argument("--identical-residents", action="store_true")
    parser.add_argument("--resident-collision", action="store_true")
    parser.add_argument("--resident-equality-pair", choices=("12", "23"))
    parser.add_argument("--require-upper-used", action="store_true")
    parser.add_argument(
        "--required-upper-hit",
        choices=tuple(
            f"{observer}{group}"
            for observer in range(N)
            for group in UPPER_HIT_GROUPS
        ),
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--cegar-singletons", action="store_true")
    parser.add_argument("--add-per-iteration", type=int, default=256)
    parser.add_argument("--max-iterations", type=int, default=3)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.upper,
        args.conversion_scope,
        args.hall_obstruction,
        args.obstruction_encoding,
        args.cell_symmetry,
        args.identical_residents,
        args.resident_collision,
        args.resident_equality_pair,
        args.require_upper_used,
        args.required_upper_hit,
        args.cegar_singletons,
        args.add_per_iteration,
        args.max_iterations,
        args.time_limit,
        args.workers,
        args.seed,
        args.result,
        args.proto,
    )


if __name__ == "__main__":
    main()
