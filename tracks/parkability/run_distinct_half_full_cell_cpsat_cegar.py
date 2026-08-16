#!/usr/bin/env python3
"""Bounded CP-SAT CEGAR for the conditional full-Hall-cell target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from ortools.sat.python import cp_model

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
        equivalent_ge,
    )
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_full_cell_cegar import (
        common_bottom_pairs,
        common_rr_uu_singleton_witness,
        common_rr_uu_singleton_witnesses,
        favorite_pair_universe,
        full_hall_cells,
        singleton_failure_cells,
        three_agent_bottom_pairs,
    )
    from .decide_distinct_half_terminal_exchange import TERMINAL_PARTITIONS
    from .run_distinct_half_two_core_cegar import perfect_pairings
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_conversion_dichotomy_cpsat import (
        add_branch,
        add_favorite_pair_obstruction,
        equivalent_ge,
    )
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_full_cell_cegar import (
        common_bottom_pairs,
        common_rr_uu_singleton_witness,
        common_rr_uu_singleton_witnesses,
        favorite_pair_universe,
        full_hall_cells,
        singleton_failure_cells,
        three_agent_bottom_pairs,
    )
    from decide_distinct_half_terminal_exchange import TERMINAL_PARTITIONS
    from run_distinct_half_two_core_cegar import perfect_pairings
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-full-cell-cpsat-cegar-v1"
N = 4
M = 9
FAVORITE = 0


def initial_seeded_partitions(universe, seed_supported, seed_mode, has_seed_sources):
    if not has_seed_sources:
        return set()
    if seed_mode == "union":
        return set(seed_supported)
    return set(universe).difference(seed_supported)


def add_no_full_hall_cells(
    model, values, cap, *, assumption_guards=None, low_pairs=None
):
    accept_literal_count = 0
    hall_witness_count = 0
    cells = (
        tuple(itertools.combinations(range(1, M), 2))
        if low_pairs is None
        else tuple(tuple(lows) for lows in low_pairs)
    )
    for lows in cells:
        residual = tuple(good for good in range(1, M) if good not in lows)
        accept = {}
        for agent in range(N):
            low_max = model.NewIntVar(
                1, cap, f"full_cell_lowmax_{lows[0]}_{lows[1]}_{agent}"
            )
            model.AddMaxEquality(
                low_max, [values[agent][low] for low in lows]
            )
            threshold = values[agent][FAVORITE] + low_max
            for edge in itertools.combinations(residual, 2):
                literal = model.NewBoolVar(
                    f"full_cell_accept_{lows[0]}_{lows[1]}_{agent}_"
                    f"{edge[0]}_{edge[1]}"
                )
                equivalent_ge(
                    model,
                    literal,
                    values[agent][edge[0]] + values[agent][edge[1]],
                    threshold,
                )
                accept[agent, edge] = literal
                accept_literal_count += 1

        witnesses = []
        for matching_position, matching in enumerate(perfect_pairings(residual)):
            witness_conditions = []
            witness_conditions.extend(
                tuple(accept[agent, edge].Not() for agent in range(N))
                for edge in matching
            )
            witness_conditions.extend(
                tuple(
                    accept[agent, edge].Not()
                    for edge in edge_pair
                    for agent in range(N)
                    if agent != possible_neighbor
                )
                for edge_pair in itertools.combinations(matching, 2)
                for possible_neighbor in range(N)
            )
            witness_conditions.extend(
                tuple(
                    accept[agent, edge].Not()
                    for edge in matching
                    for agent in range(N)
                    if agent not in possible_neighbors
                )
                for possible_neighbors in itertools.combinations(range(N), 2)
            )
            if len(witness_conditions) != 21:
                raise AssertionError("Hall-witness template count changed")
            for witness_position, conditions in enumerate(witness_conditions):
                witness = model.NewBoolVar(
                    f"full_cell_hall_failure_{lows[0]}_{lows[1]}_"
                    f"{matching_position}_{witness_position}"
                )
                model.AddBoolAnd(conditions).OnlyEnforceIf(witness)
                model.AddBoolOr(
                    condition.Not() for condition in conditions
                ).OnlyEnforceIf(witness.Not())
                witnesses.append(witness)
                hall_witness_count += 1
        constraint = model.AddBoolOr(witnesses)
        if assumption_guards is not None:
            guard = model.NewBoolVar(
                f"full_cell_obstruction_guard_{lows[0]}_{lows[1]}"
            )
            constraint.OnlyEnforceIf(guard)
            model.AddAssumption(guard)
            assumption_guards[guard.Index()] = lows
    return {
        "low_pair_cells": len(cells),
        "accept_literals": accept_literal_count,
        "hall_witness_literals": hall_witness_count,
        "hall_failure_templates_per_pairing": 21,
    }


def add_singleton_failure_cells(model, values, cap, low_pairs):
    witness_count = 0
    cells = tuple(low_pairs)
    for lows in cells:
        residual = tuple(good for good in range(1, M) if good not in lows)
        low_maxima = []
        for agent in range(N):
            low_max = model.NewIntVar(
                1, cap, f"singleton_cell_lowmax_{lows[0]}_{lows[1]}_{agent}"
            )
            model.AddMaxEquality(
                low_max, [values[agent][low] for low in lows]
            )
            low_maxima.append(low_max)
        witnesses = []
        for edge in itertools.combinations(residual, 2):
            witness = model.NewBoolVar(
                f"singleton_cell_bad_edge_{lows[0]}_{lows[1]}_"
                f"{edge[0]}_{edge[1]}"
            )
            for agent in range(N):
                model.Add(
                    values[agent][edge[0]] + values[agent][edge[1]]
                    < values[agent][FAVORITE] + low_maxima[agent]
                ).OnlyEnforceIf(witness)
            witnesses.append(witness)
            witness_count += 1
        model.AddBoolOr(witnesses)
    return {
        "low_pair_cells": len(cells),
        "candidate_singleton_witness_edges": witness_count,
    }


def add_all_cells_singleton_failures(model, values, cap):
    return add_singleton_failure_cells(
        model,
        values,
        cap,
        itertools.combinations(range(1, M), 2),
    )


def add_no_singleton_failure_cell(model, values, cap, lows):
    residual = tuple(good for good in range(1, M) if good not in lows)
    low_maxima = []
    for agent in range(N):
        low_max = model.NewIntVar(
            1, cap, f"nonsingleton_cell_lowmax_{lows[0]}_{lows[1]}_{agent}"
        )
        model.AddMaxEquality(low_max, [values[agent][low] for low in lows])
        low_maxima.append(low_max)
    accept_literal_count = 0
    for edge in itertools.combinations(residual, 2):
        accepted = []
        for agent in range(N):
            literal = model.NewBoolVar(
                f"nonsingleton_cell_accept_{lows[0]}_{lows[1]}_"
                f"{edge[0]}_{edge[1]}_{agent}"
            )
            equivalent_ge(
                model,
                literal,
                values[agent][edge[0]] + values[agent][edge[1]],
                values[agent][FAVORITE] + low_maxima[agent],
            )
            accepted.append(literal)
            accept_literal_count += 1
        model.AddBoolOr(accepted)
    return {
        "low_pair": list(lows),
        "required_nonempty_neighbor_edges": 15,
        "accept_literals": accept_literal_count,
    }


def add_common_rr_uu_singleton_witness(model, values, cap, edge=(5, 6)):
    constraint_count = 0
    for agent in range(N):
        for lows in itertools.combinations(range(1, 5), 2):
            low_max = model.NewIntVar(
                1,
                cap,
                f"common_uu_lowmax_{edge[0]}_{edge[1]}_"
                f"{agent}_{lows[0]}_{lows[1]}",
            )
            model.AddMaxEquality(
                low_max, [values[agent][low] for low in lows]
            )
            model.Add(
                values[agent][edge[0]] + values[agent][edge[1]]
                < values[agent][FAVORITE] + low_max
            )
            constraint_count += 1
    return {
        "edge": list(edge),
        "rr_low_pair_cells": 6,
        "rejection_constraints": constraint_count,
    }


def add_no_common_rr_uu_singleton_witness(model, values):
    for edge in itertools.combinations(range(5, M), 2):
        witnesses = []
        for agent in range(N):
            edge_value = values[agent][edge[0]] + values[agent][edge[1]]
            for lows in itertools.combinations(range(1, 5), 2):
                witness = model.NewBoolVar(
                    f"no_common_uu_{edge[0]}_{edge[1]}_"
                    f"{agent}_{lows[0]}_{lows[1]}"
                )
                for low in lows:
                    model.Add(
                        edge_value
                        >= values[agent][FAVORITE] + values[agent][low]
                    ).OnlyEnforceIf(witness)
                witnesses.append(witness)
        model.AddBoolOr(witnesses)
    return {
        "unmatched_edges": 6,
        "nonwitness_constraints": 6,
        "witness_literals": 144,
    }


def add_no_common_bottom_pair(model, values):
    witness_count = 0
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        witnesses = []
        for agent in range(N):
            for low in lows:
                for other in residual:
                    witness = model.NewBoolVar(
                        f"no_common_bottom_{lows[0]}_{lows[1]}_"
                        f"{agent}_{low}_{other}"
                    )
                    equivalent_ge(
                        model,
                        witness,
                        values[agent][low],
                        values[agent][other] + 1,
                    )
                    witnesses.append(witness)
                    witness_count += 1
        model.AddBoolOr(witnesses)
    return {
        "candidate_bottom_pairs": 28,
        "strict_nonbottom_witness_literals": witness_count,
        "strict_nonbottom_terms_per_pair": 48,
    }


def add_no_three_agent_bottom_pair(model, values):
    bottom_literals = 0
    violation_literals = 0
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        supported_by = []
        for agent in range(N):
            bottom = model.NewBoolVar(
                f"three_agent_bottom_{lows[0]}_{lows[1]}_{agent}"
            )
            violations = []
            for low in lows:
                for other in residual:
                    model.Add(
                        values[agent][low] <= values[agent][other]
                    ).OnlyEnforceIf(bottom)
                    violation = model.NewBoolVar(
                        f"three_agent_bottom_violation_{lows[0]}_{lows[1]}_"
                        f"{agent}_{low}_{other}"
                    )
                    equivalent_ge(
                        model,
                        violation,
                        values[agent][low],
                        values[agent][other] + 1,
                    )
                    violations.append(violation)
                    violation_literals += 1
            model.AddBoolOr(violations).OnlyEnforceIf(bottom.Not())
            supported_by.append(bottom)
            bottom_literals += 1
        model.Add(sum(supported_by) <= 2)
    return {
        "candidate_bottom_pairs": 28,
        "bottom_support_literals": bottom_literals,
        "strict_nonbottom_witness_literals": violation_literals,
        "maximum_agents_per_bottom_pair": 2,
    }


def add_partition_efx_requirement(model, values, partition):
    feasible = []
    for observer in range(N):
        row = []
        for own_bundle in range(N):
            own = sum(values[observer][good] for good in partition[own_bundle])
            comparisons = []
            for target_bundle, target in enumerate(partition):
                if target_bundle == own_bundle:
                    continue
                for removed in target:
                    comparison = model.NewBoolVar(
                        f"required_terminal_efx_{observer}_{own_bundle}_"
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
                f"required_terminal_feasible_{observer}_{own_bundle}"
            )
            model.AddBoolAnd(comparisons).OnlyEnforceIf(edge)
            model.AddBoolOr(
                comparison.Not() for comparison in comparisons
            ).OnlyEnforceIf(edge.Not())
            row.append(edge)
        feasible.append(row)
    matchings = []
    for position, matching in enumerate(itertools.permutations(range(N))):
        selected = model.NewBoolVar(f"required_terminal_matching_{position}")
        model.AddBoolAnd(
            feasible[observer][matching[observer]] for observer in range(N)
        ).OnlyEnforceIf(selected)
        matchings.append(selected)
    model.AddBoolOr(matchings)
    return {"matching_literals": len(matchings), "feasible_edges": N * N}


def run(
    output,
    proto_output,
    seed_paths,
    seed_mode,
    cap,
    time_limit,
    max_iterations,
    add_per_iteration,
    workers,
    random_seed,
    resume_path,
    pool_path,
    cell_obstruction,
    terminal_case,
    partition_family="all",
    require_common_uu_witness=False,
    forbid_common_uu_witness=False,
    forbid_common_bottom_pair=False,
    forbid_three_agent_bottom_pair=False,
):
    if require_common_uu_witness and forbid_common_uu_witness:
        raise ValueError("common-UU witness modes are mutually exclusive")
    model = cp_model.CpModel()
    values = tuple(
        tuple(
            model.NewIntVar(1, cap, f"value_{agent}_{good}")
            for good in range(M)
        )
        for agent in range(N)
    )
    add_branch(model, values)
    if cell_obstruction == "none":
        full_cell_encoding = None
    elif cell_obstruction == "full_hall":
        full_cell_encoding = add_no_full_hall_cells(model, values, cap)
    elif cell_obstruction == "singleton":
        full_cell_encoding = add_all_cells_singleton_failures(model, values, cap)
    elif cell_obstruction == "rr_singleton":
        full_cell_encoding = {
            "full_hall": add_no_full_hall_cells(model, values, cap),
            "rr_singleton": add_singleton_failure_cells(
                model,
                values,
                cap,
                itertools.combinations(range(1, 5), 2),
            ),
        }
    else:
        full_cell_encoding = {
            "full_hall": add_no_full_hall_cells(model, values, cap),
            "rr_nonsingleton_12": add_no_singleton_failure_cell(
                model, values, cap, (1, 2)
            ),
        }
    common_uu_witness_encoding = (
        add_common_rr_uu_singleton_witness(model, values, cap)
        if require_common_uu_witness
        else None
    )
    no_common_uu_witness_encoding = (
        add_no_common_rr_uu_singleton_witness(model, values)
        if forbid_common_uu_witness
        else None
    )
    no_common_bottom_pair_encoding = (
        add_no_common_bottom_pair(model, values)
        if forbid_common_bottom_pair
        else None
    )
    no_three_agent_bottom_pair_encoding = (
        add_no_three_agent_bottom_pair(model, values)
        if forbid_three_agent_bottom_pair
        else None
    )
    terminal_encoding = None
    if terminal_case is not None:
        terminal_encoding = add_partition_efx_requirement(
            model, values, TERMINAL_PARTITIONS[terminal_case]
        )
    if cell_obstruction != "rr_nonsingleton_12" and terminal_case is None:
        for agent in range(N - 1):
            model.Add(values[agent][FAVORITE] >= values[agent + 1][FAVORITE])
    if terminal_case is None:
        if require_common_uu_witness:
            model.Add(values[0][5] >= values[0][6])
            model.Add(values[0][7] >= values[0][8])
        else:
            for good in range(5, M - 1):
                model.Add(values[0][good] >= values[0][good + 1])

    universe = favorite_pair_universe(partition_family)
    positions = {partition: position for position, partition in enumerate(universe)}
    seed_supported = set()
    seed_sources = []
    for path in seed_paths:
        seed_supported.update(supported_partitions(load_values(path), list(universe)))
        seed_sources.append(
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    seeded = initial_seeded_partitions(
        universe,
        seed_supported,
        seed_mode,
        bool(seed_paths),
    )
    pool_source = None
    if pool_path is not None:
        pool_payload = json.loads(pool_path.read_text())
        selected = {
            tuple(tuple(bundle) for bundle in partition)
            for partition in pool_payload.get("core_partitions", [])
        }
        if not selected or not selected <= set(universe):
            raise ValueError("pool source does not contain valid partitions")
        seeded.update(selected)
        pool_source = {
            "path": str(pool_path),
            "sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(),
            "partition_count": len(selected),
        }
    pool = set()
    for partition in universe:
        if partition in seeded:
            add_favorite_pair_obstruction(
                model, values, partition, positions[partition]
            )
            pool.add(partition)

    trace = []
    resume_source = None
    resume_source_sha256 = None
    if resume_path is not None:
        resumed = json.loads(resume_path.read_text())
        if (
            resumed.get("schema") != SCHEMA
            or resumed.get("cap") != cap
            or resumed.get("seed_mode") != seed_mode
            or resumed.get("cell_obstruction", "full_hall") != cell_obstruction
            or resumed.get("required_terminal_case") != terminal_case
            or resumed.get("partition_family", "all") != partition_family
            or resumed.get("common_rr_uu_singleton_witness")
            != ([5, 6] if require_common_uu_witness else None)
            or resumed.get("common_rr_uu_singleton_witness_forbidden", False)
            != forbid_common_uu_witness
            or resumed.get("common_bottom_pair_forbidden", False)
            != forbid_common_bottom_pair
            or resumed.get("three_agent_bottom_pair_forbidden", False)
            != forbid_three_agent_bottom_pair
        ):
            raise ValueError("resume record is incompatible")
        for record in resumed["trace"]:
            decoded = tuple(tuple(row) for row in record["values"])
            audit_branch(decoded)
            if cell_obstruction != "none" and full_hall_cells(decoded):
                raise AssertionError("resumed model has a full Hall cell")
            if require_common_uu_witness and not common_rr_uu_singleton_witness(
                decoded
            ):
                raise AssertionError("resumed model lost the common UU witness")
            if forbid_common_uu_witness and common_rr_uu_singleton_witnesses(
                decoded
            ):
                raise AssertionError("resumed model gained a common UU witness")
            if forbid_common_bottom_pair and common_bottom_pairs(decoded):
                raise AssertionError("resumed model gained a common bottom pair")
            if (
                forbid_three_agent_bottom_pair
                and three_agent_bottom_pairs(decoded)
            ):
                raise AssertionError(
                    "resumed model gained a three-agent bottom pair"
                )
            if (
                cell_obstruction == "singleton"
                and len(singleton_failure_cells(decoded)) != 28
            ):
                raise AssertionError("resumed model lost a singleton witness")
            singleton_cells = {
                tuple(cell) for cell in singleton_failure_cells(decoded)
            }
            rr_cells = set(itertools.combinations(range(1, 5), 2))
            if (
                cell_obstruction == "rr_singleton"
                and not rr_cells <= singleton_cells
            ):
                raise AssertionError("resumed model lost an RR singleton witness")
            if (
                cell_obstruction == "rr_nonsingleton_12"
                and (1, 2) in singleton_cells
            ):
                raise AssertionError("resumed model gained a singleton witness")
            if terminal_case is not None and not supported_partitions(
                decoded, [TERMINAL_PARTITIONS[terminal_case]]
            ):
                raise AssertionError("resumed model lost required terminal EFX")
            survivors = tuple(
                partition
                for partition in supported_partitions(decoded, list(universe))
                if partition not in pool
            )
            if (
                record["pool_size_before"] != len(pool)
                or record["favorite_pair_efx_survivors"] != len(survivors)
            ):
                raise AssertionError("resume trace replay changed")
            trace.append(record)
            for partition in survivors[:add_per_iteration]:
                add_favorite_pair_obstruction(
                    model, values, partition, positions[partition]
                )
                pool.add(partition)
        resume_source = str(resume_path)
        resume_source_sha256 = hashlib.sha256(resume_path.read_bytes()).hexdigest()

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = random_seed
    status_code = cp_model.UNKNOWN
    status = "ITERATION_LIMIT"
    result_values = None
    started = time.time()
    iteration = len(trace)
    for iteration in range(len(trace) + 1, max_iterations + 1):
        status_code = solver.Solve(model)
        if status_code == cp_model.INFEASIBLE:
            status = "FINITE_CAP_UNSAT_CANDIDATE"
            break
        if status_code not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            status = "CP_SAT_UNKNOWN"
            break
        decoded = tuple(
            tuple(solver.Value(values[agent][good]) for good in range(M))
            for agent in range(N)
        )
        audit_branch(decoded)
        if cell_obstruction != "none" and full_hall_cells(decoded):
            raise AssertionError("decoded model violates no-full-cell encoding")
        if require_common_uu_witness and not common_rr_uu_singleton_witness(
            decoded
        ):
            raise AssertionError("decoded model lost the common UU witness")
        if forbid_common_uu_witness and common_rr_uu_singleton_witnesses(decoded):
            raise AssertionError("decoded model gained a common UU witness")
        if forbid_common_bottom_pair and common_bottom_pairs(decoded):
            raise AssertionError("decoded model gained a common bottom pair")
        if (
            forbid_three_agent_bottom_pair
            and three_agent_bottom_pairs(decoded)
        ):
            raise AssertionError("decoded model gained a three-agent bottom pair")
        if (
            cell_obstruction == "singleton"
            and len(singleton_failure_cells(decoded)) != 28
        ):
            raise AssertionError("decoded model lost a singleton witness")
        singleton_cells = {tuple(cell) for cell in singleton_failure_cells(decoded)}
        rr_cells = set(itertools.combinations(range(1, 5), 2))
        if cell_obstruction == "rr_singleton" and not rr_cells <= singleton_cells:
            raise AssertionError("decoded model lost an RR singleton witness")
        if (
            cell_obstruction == "rr_nonsingleton_12"
            and (1, 2) in singleton_cells
        ):
            raise AssertionError("decoded model gained a singleton witness")
        if terminal_case is not None and not supported_partitions(
            decoded, [TERMINAL_PARTITIONS[terminal_case]]
        ):
            raise AssertionError("decoded model lost required terminal EFX")
        survivors = tuple(
            partition
            for partition in supported_partitions(decoded, list(universe))
            if partition not in pool
        )
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(pool),
                "favorite_pair_efx_survivors": len(survivors),
                "values": [list(row) for row in decoded],
            }
        )
        print(
            f"iteration={iteration} pool={len(pool)} survivors={len(survivors)}",
            flush=True,
        )
        if not survivors:
            status = "FULL_CELL_SELECTION_COUNTEREXAMPLE"
            result_values = decoded
            break
        for partition in survivors[:add_per_iteration]:
            add_favorite_pair_obstruction(
                model, values, partition, positions[partition]
            )
            pool.add(partition)

    proto_output.parent.mkdir(parents=True, exist_ok=True)
    if not model.ExportToFile(str(proto_output)):
        raise RuntimeError("CP-SAT model export failed")
    proto = proto_output.read_bytes()
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": solver.StatusName(status_code),
        "cap": cap,
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "symmetry_breaking": [
            (
                "none on agents after fixing a labeled structural object"
                if cell_obstruction == "rr_nonsingleton_12"
                or terminal_case is not None
                else "nonincreasing favorite values by agent"
            ),
            (
                "none on unmatched goods after fixing a terminal partition"
                if terminal_case is not None
                else "within the fixed common edge and its complement"
                if require_common_uu_witness
                else "nonincreasing agent-0 values on goods 5..8"
            ),
        ],
        "favorite_pair_partition_count": len(universe),
        "partition_family": partition_family,
        "common_rr_uu_singleton_witness": (
            [5, 6] if require_common_uu_witness else None
        ),
        "common_rr_uu_singleton_witness_encoding": common_uu_witness_encoding,
        "common_rr_uu_singleton_witness_forbidden": forbid_common_uu_witness,
        "no_common_rr_uu_singleton_witness_encoding": (
            no_common_uu_witness_encoding
        ),
        "common_bottom_pair_forbidden": forbid_common_bottom_pair,
        "no_common_bottom_pair_encoding": no_common_bottom_pair_encoding,
        "three_agent_bottom_pair_forbidden": forbid_three_agent_bottom_pair,
        "no_three_agent_bottom_pair_encoding": (
            no_three_agent_bottom_pair_encoding
        ),
        "full_hall_cell_forbidden": cell_obstruction != "none",
        "cell_obstruction": cell_obstruction,
        "full_cell_encoding": full_cell_encoding,
        "required_terminal_case": terminal_case,
        "required_terminal_encoding": terminal_encoding,
        "seed_mode": seed_mode,
        "seed_sources": seed_sources,
        "seed_supported_union_size": len(seed_supported),
        "pool_source": pool_source,
        "pool_size": len(pool),
        "iterations": iteration,
        "add_per_iteration": add_per_iteration,
        "time_limit_seconds": time_limit,
        "elapsed_seconds": time.time() - started,
        "workers": workers,
        "random_seed": random_seed,
        "resume_source": resume_source,
        "resume_source_sha256": resume_source_sha256,
        "trace": trace,
        "values": [list(row) for row in result_values] if result_values else None,
        "literal_complete_efx_count": (
            independent.count_complete_efx0(result_values)
            if result_values is not None
            else None
        ),
        "proto_path": str(proto_output),
        "proto_sha256": hashlib.sha256(proto).hexdigest(),
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "warning": (
            "UNSAT is finite-cap only and needs independent replay. A "
            "terminal SAT model refutes only the conditional full-cell "
            "target unless literal complete-EFX enumeration is also zero."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proto", type=Path, required=True)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--seed-mode", choices=("union", "complement"), default="complement")
    parser.add_argument("--cap", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=120)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument("--add", type=int, default=128)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--pool", type=Path)
    parser.add_argument(
        "--cell-obstruction",
        choices=(
            "none",
            "full_hall",
            "singleton",
            "rr_singleton",
            "rr_nonsingleton_12",
        ),
        default="full_hall",
    )
    parser.add_argument("--require-terminal-case", choices=tuple(TERMINAL_PARTITIONS))
    parser.add_argument(
        "--partition-family",
        choices=("all", "six_orbit", "eight_orbit", "common_uu_fan"),
        default="all",
    )
    parser.add_argument("--require-common-uu-witness", action="store_true")
    parser.add_argument("--forbid-common-uu-witness", action="store_true")
    parser.add_argument("--forbid-common-bottom-pair", action="store_true")
    parser.add_argument(
        "--forbid-three-agent-bottom-pair", action="store_true"
    )
    args = parser.parse_args()
    if (
        args.cap < 2
        or args.time_limit <= 0
        or args.max_iterations < 1
        or args.add < 1
        or args.workers < 1
        or (not args.seed and args.pool is None)
        or (
            args.require_common_uu_witness
            and args.forbid_common_uu_witness
        )
    ):
        parser.error("invalid bounded CEGAR parameters")
    result = run(
        args.output,
        args.proto,
        tuple(args.seed),
        args.seed_mode,
        args.cap,
        args.time_limit,
        args.max_iterations,
        args.add,
        args.workers,
        args.random_seed,
        args.resume,
        args.pool,
        args.cell_obstruction,
        args.require_terminal_case,
        args.partition_family,
        args.require_common_uu_witness,
        args.forbid_common_uu_witness,
        args.forbid_common_bottom_pair,
        args.forbid_three_agent_bottom_pair,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
