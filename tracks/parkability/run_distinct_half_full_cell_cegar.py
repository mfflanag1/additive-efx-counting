#!/usr/bin/env python3
"""Exact CEGAR for the conditional full favorite-triple Hall-cell target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from . import core, independent
    from .anneal import atomic_json
    from .decide_distinct_half_hall_layers import add_branch
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_two_core_cegar import perfect_pairings
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from decide_distinct_half_hall_layers import add_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_two_core_cegar import perfect_pairings
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-full-cell-cegar-v1"
N = 4
M = 9
FAVORITE = 0
REPRESENTATIVE_GOODS = frozenset(range(1, 5))
SIX_ORBIT_SIGNATURES = frozenset(
    {
        ("R", 0, ("RR", "RU")),
        ("R", 1, ("RR", "UU")),
        ("R", 1, ("RU", "RU")),
        ("R", 2, ("RU", "UU")),
        ("U", 2, ("RR", "UU")),
        ("U", 2, ("RU", "RU")),
    }
)
EIGHT_ORBIT_SIGNATURES = SIX_ORBIT_SIGNATURES | {
    ("U", 0, ("RR", "RR")),
    ("U", 1, ("RR", "RU")),
}


def common_uu_fan_universe(edge=(5, 6)):
    """The 54 terminal-orbit states canonically attached to a fixed UU edge."""
    edge = tuple(edge)
    if (
        len(edge) != 2
        or len(set(edge)) != 2
        or any(good not in range(5, M) for good in edge)
    ):
        raise ValueError("common-UU fan edge must contain two unmatched goods")
    complement = tuple(good for good in range(5, M) if good not in edge)
    partitions = set()
    for partner in complement:
        other = next(good for good in complement if good != partner)
        for pivot in edge:
            third_candidates = tuple(REPRESENTATIVE_GOODS) + tuple(
                good for good in edge if good != pivot
            )
            for third in third_candidates:
                triple = tuple(sorted((other, pivot, third)))
                residual = tuple(
                    good
                    for good in range(1, M)
                    if good != partner and good not in triple
                )
                for pairing in perfect_pairings(residual):
                    partitions.add(
                        tuple(
                            sorted(
                                ((FAVORITE, partner), triple, *pairing)
                            )
                        )
                    )
    result = tuple(sorted(partitions))
    if len(result) != 54:
        raise AssertionError("common-UU fan census changed")
    return result


def favorite_pair_orbit_signature(partition):
    favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
    partner = next(good for good in favorite_bundle if good != FAVORITE)
    triple = next(bundle for bundle in partition if len(bundle) == 3)
    pairs = tuple(
        bundle
        for bundle in partition
        if len(bundle) == 2 and FAVORITE not in bundle
    )

    def pair_type(bundle):
        representatives = sum(good in REPRESENTATIVE_GOODS for good in bundle)
        return "R" * representatives + "U" * (2 - representatives)

    return (
        "R" if partner in REPRESENTATIVE_GOODS else "U",
        sum(good in REPRESENTATIVE_GOODS for good in triple),
        tuple(sorted(pair_type(bundle) for bundle in pairs)),
    )


def favorite_pair_universe(partition_family):
    if partition_family == "common_uu_fan":
        return common_uu_fan_universe()
    universe = tuple(favorite_pair_balanced_universe())
    if partition_family == "all":
        return universe
    if partition_family == "six_orbit":
        return tuple(
            partition
            for partition in universe
            if favorite_pair_orbit_signature(partition) in SIX_ORBIT_SIGNATURES
        )
    if partition_family == "eight_orbit":
        return tuple(
            partition
            for partition in universe
            if favorite_pair_orbit_signature(partition) in EIGHT_ORBIT_SIGNATURES
        )
    raise ValueError("unknown favorite-pair partition family")


def add_acceptance_literals(master, lows, residual):
    accept = {}
    for agent in range(N):
        for edge in itertools.combinations(residual, 2):
            literal = z3.Bool(
                f"full_cell_accept_lows_{lows[0]}_{lows[1]}_"
                f"agent_{agent}_edge_{edge[0]}_{edge[1]}"
            )
            pair_value = master._sum(agent, edge)
            master.solver.add(
                literal
                == z3.And(
                    *(
                        pair_value
                        >= master.values[agent][FAVORITE]
                        + master.values[agent][low]
                        for low in lows
                    )
                )
            )
            accept[agent, edge] = literal
    return accept


def hall_failure(accept, matching):
    zero_neighbor = tuple(
        z3.And(*(z3.Not(accept[agent, edge]) for agent in range(N)))
        for edge in matching
    )
    two_at_most_one = tuple(
        z3.And(
            *(
                z3.Not(accept[agent, edge])
                for edge in edge_pair
                for agent in range(N)
                if agent != possible_neighbor
            )
        )
        for edge_pair in itertools.combinations(matching, 2)
        for possible_neighbor in range(N)
    )
    three_at_most_two = tuple(
        z3.And(
            *(
                z3.Not(accept[agent, edge])
                for edge in matching
                for agent in range(N)
                if agent not in possible_neighbors
            )
        )
        for possible_neighbors in itertools.combinations(range(N), 2)
    )
    return z3.Or(*zero_neighbor, *two_at_most_one, *three_at_most_two)


def add_no_full_hall_cell(master, low_pairs=None):
    low_pair_cells = 0
    accept_literals = 0
    pairing_failure_terms = 0
    cells = (
        tuple(itertools.combinations(range(1, M), 2))
        if low_pairs is None
        else tuple(tuple(lows) for lows in low_pairs)
    )
    for lows in cells:
        residual = tuple(good for good in range(1, M) if good not in lows)
        accept = add_acceptance_literals(master, lows, residual)
        failures = tuple(
            hall_failure(accept, matching)
            for matching in perfect_pairings(residual)
        )
        master.solver.add(z3.Or(*failures))
        low_pair_cells += 1
        accept_literals += len(accept)
        pairing_failure_terms += len(failures)
    return {
        "low_pair_cells": low_pair_cells,
        "accept_literals": accept_literals,
        "pairing_failure_terms": pairing_failure_terms,
        "hall_failure_templates_per_pairing": 21,
    }


def add_singleton_failure_cells(master, low_pairs):
    """Require a universally rejected residual edge in selected cells."""
    bad_edges = 0
    cells = tuple(low_pairs)
    for lows in cells:
        residual = tuple(good for good in range(1, M) if good not in lows)
        cell_bad_edges = []
        for edge in itertools.combinations(residual, 2):
            rejected_by_all = z3.And(
                *(
                    z3.Or(
                        master._sum(agent, edge)
                        < master.values[agent][FAVORITE]
                        + master.values[agent][low]
                        for low in lows
                    )
                    for agent in range(N)
                )
            )
            cell_bad_edges.append(rejected_by_all)
        master.solver.add(z3.Or(*cell_bad_edges))
        bad_edges += len(cell_bad_edges)
    return {
        "low_pair_cells": len(cells),
        "candidate_singleton_witness_edges": bad_edges,
    }


def add_all_cells_singleton_failure(master):
    """Require a universally rejected residual edge in every low-pair cell."""
    return add_singleton_failure_cells(
        master, itertools.combinations(range(1, M), 2)
    )


def common_rr_uu_singleton_witness(values, edge=(5, 6)):
    return all(
        all(
            sum(row[good] for good in edge)
            < row[FAVORITE] + max(row[low] for low in lows)
            for row in values
        )
        for lows in itertools.combinations(range(1, 5), 2)
    )


def common_rr_uu_singleton_witnesses(values):
    return tuple(
        edge
        for edge in itertools.combinations(range(5, M), 2)
        if common_rr_uu_singleton_witness(values, edge)
    )


def common_bottom_pairs(values):
    return tuple(
        lows
        for lows in itertools.combinations(range(1, M), 2)
        if all(
            max(row[good] for good in lows)
            <= min(row[good] for good in range(1, M) if good not in lows)
            for row in values
        )
    )


def three_agent_bottom_pairs(values):
    return tuple(
        lows
        for lows in itertools.combinations(range(1, M), 2)
        if sum(
            max(row[good] for good in lows)
            <= min(
                row[good]
                for good in range(1, M)
                if good not in lows
            )
            for row in values
        )
        >= 3
    )


def add_no_common_bottom_pair(master):
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        master.solver.add(
            z3.Or(
                *(
                    master.values[agent][low]
                    > master.values[agent][other]
                    for agent in range(N)
                    for low in lows
                    for other in residual
                )
            )
        )
    return {
        "candidate_bottom_pairs": 28,
        "strict_nonbottom_terms_per_pair": 48,
    }


def add_no_three_agent_bottom_pair(master):
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        for agents in itertools.combinations(range(N), 3):
            master.solver.add(
                z3.Or(
                    *(
                        master.values[agent][low]
                        > master.values[agent][other]
                        for agent in agents
                        for low in lows
                        for other in residual
                    )
                )
            )
    return {
        "candidate_bottom_pairs": 28,
        "candidate_agent_triples_per_pair": 4,
        "strict_nonbottom_terms_per_agent_triple": 36,
    }


def split_bottom_pattern(pattern):
    if pattern == "disjoint":
        return (((0, 1), (7, 8)), ((2, 3), (5, 6)))
    if pattern == "overlap":
        return (((0, 1), (7, 8)), ((2, 3), (6, 8)))
    raise ValueError("unknown split-bottom pattern")


def split_bottom_pattern_holds(values, pattern):
    return all(
        max(values[agent][low] for low in lows)
        <= min(
            values[agent][good]
            for good in range(1, M)
            if good not in lows
        )
        for agents, lows in split_bottom_pattern(pattern)
        for agent in agents
    )


def add_split_bottom_pattern(master, pattern):
    requirements = split_bottom_pattern(pattern)
    constraint_count = 0
    for agents, lows in requirements:
        residual = tuple(good for good in range(1, M) if good not in lows)
        for agent in agents:
            for low in lows:
                for good in residual:
                    master.solver.add(
                        master.values[agent][low]
                        <= master.values[agent][good]
                    )
                    constraint_count += 1
    return {
        "pattern": pattern,
        "requirements": [
            {"agents": list(agents), "bottom_pair": list(lows)}
            for agents, lows in requirements
        ],
        "bottom_order_constraint_count": constraint_count,
    }


def second_smallest_representative_map_holds(values, mapping):
    return all(
        row[representative] == sorted(row[1:5])[1]
        for row, representative in zip(values, mapping)
    )


def add_second_smallest_representative_map(master, mapping):
    mapping = tuple(mapping)
    if len(mapping) != N or any(good < 1 or good > 4 for good in mapping):
        raise ValueError(
            "second-smallest map must name one representative per agent"
        )
    comparison_count = 0
    for agent, representative in enumerate(mapping):
        selected = master.values[agent][representative]
        others = tuple(
            master.values[agent][good]
            for good in range(1, 5)
            if good != representative
        )
        master.solver.add(z3.Or(*(value <= selected for value in others)))
        comparison_count += 1
        for left, right in itertools.combinations(others, 2):
            master.solver.add(z3.Or(left >= selected, right >= selected))
            comparison_count += 1
    return {
        "representative_map": list(mapping),
        "order_constraints": comparison_count,
    }


def add_common_rr_uu_singleton_witness(master, edge=(5, 6), mapping=None):
    if (
        len(edge) != 2
        or len(set(edge)) != 2
        or any(good < 5 or good >= M for good in edge)
    ):
        raise ValueError("common RR-cell witness must be an unmatched-good pair")
    edge = tuple(sorted(edge))
    if mapping is not None:
        order_encoding = add_second_smallest_representative_map(master, mapping)
        for agent, representative in enumerate(mapping):
            master.solver.add(
                master._sum(agent, edge)
                < master.values[agent][FAVORITE]
                + master.values[agent][representative]
            )
        return {
            "edge": list(edge),
            "rr_low_pair_cells": 6,
            "rejection_constraints": N,
            "second_smallest_map_encoding": order_encoding,
        }
    constraint_count = 0
    for lows in itertools.combinations(range(1, 5), 2):
        for agent in range(N):
            master.solver.add(
                z3.Or(
                    *(
                        master._sum(agent, edge)
                        < master.values[agent][FAVORITE]
                        + master.values[agent][low]
                        for low in lows
                    )
                )
            )
            constraint_count += 1
    return {
        "edge": list(edge),
        "rr_low_pair_cells": 6,
        "rejection_constraints": constraint_count,
    }


def add_no_common_rr_uu_singleton_witness(master):
    constraint_count = 0
    for edge in itertools.combinations(range(5, M), 2):
        master.solver.add(
            z3.Or(
                *(
                    z3.And(
                        *(
                            master._sum(agent, edge)
                            >= master.values[agent][FAVORITE]
                            + master.values[agent][low]
                            for low in lows
                        )
                    )
                    for agent in range(N)
                    for lows in itertools.combinations(range(1, 5), 2)
                )
            )
        )
        constraint_count += 1
    return {
        "unmatched_edges": 6,
        "nonwitness_constraints": constraint_count,
    }


def add_no_singleton_failure_cell(master, lows):
    """Require every residual edge to have a threshold-accepting agent."""
    residual = tuple(good for good in range(1, M) if good not in lows)
    for edge in itertools.combinations(residual, 2):
        master.solver.add(
            z3.Or(
                *(
                    z3.And(
                        *(
                            master._sum(agent, edge)
                            >= master.values[agent][FAVORITE]
                            + master.values[agent][low]
                            for low in lows
                        )
                    )
                    for agent in range(N)
                )
            )
        )
    return {
        "low_pair": list(lows),
        "required_nonempty_neighbor_edges": 15,
    }


def pairing_has_hall_matching(values, lows, matching):
    masks = []
    for edge in matching:
        mask = 0
        for agent, row in enumerate(values):
            threshold = row[FAVORITE] + max(row[low] for low in lows)
            if sum(row[good] for good in edge) >= threshold:
                mask |= 1 << agent
        masks.append(mask)
    return any(
        all(masks[index] & (1 << agent) for index, agent in enumerate(agents))
        for agents in itertools.permutations(range(N), 3)
    )


def full_hall_cells(values):
    cells = []
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        if all(
            pairing_has_hall_matching(values, lows, matching)
            for matching in perfect_pairings(residual)
        ):
            cells.append(list(lows))
    return cells


def singleton_failure_cells(values):
    cells = []
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        if any(
            all(
                sum(row[good] for good in edge)
                < row[FAVORITE] + max(row[low] for low in lows)
                for row in values
            )
            for edge in itertools.combinations(residual, 2)
        ):
            cells.append(list(lows))
    return cells


def run(
    result_path,
    smt2_path,
    seed_paths,
    time_limit,
    max_iterations,
    add_per_iteration,
    seed_mode,
    resume_path,
    threshold_encoding,
    partition_family,
    require_common_uu_witness,
    forbid_common_uu_witness=False,
    rank_branch=None,
    second_smallest_map=None,
    forbid_full_hall=True,
    forbid_common_bottom_pair=False,
    forbid_three_agent_bottom_pair=False,
    required_split_bottom_pattern=None,
):
    if require_common_uu_witness and forbid_common_uu_witness:
        raise ValueError("common-UU witness modes are mutually exclusive")
    if second_smallest_map is not None and not require_common_uu_witness:
        raise ValueError("a second-smallest map requires the common-UU branch")
    universe = favorite_pair_universe(partition_family)
    master = ParkabilityLRAMaster(N, M)
    add_branch(master, rank_branch, threshold_encoding=threshold_encoding)
    full_cell_encoding = add_no_full_hall_cell(master) if forbid_full_hall else None
    common_uu_witness_encoding = (
        add_common_rr_uu_singleton_witness(
            master, mapping=second_smallest_map
        )
        if require_common_uu_witness
        else None
    )
    no_common_uu_witness_encoding = (
        add_no_common_rr_uu_singleton_witness(master)
        if forbid_common_uu_witness
        else None
    )
    no_common_bottom_pair_encoding = (
        add_no_common_bottom_pair(master)
        if forbid_common_bottom_pair
        else None
    )
    no_three_agent_bottom_pair_encoding = (
        add_no_three_agent_bottom_pair(master)
        if forbid_three_agent_bottom_pair
        else None
    )
    split_bottom_pattern_encoding = (
        add_split_bottom_pattern(master, required_split_bottom_pattern)
        if required_split_bottom_pattern is not None
        else None
    )

    seed_supported = set()
    seed_sources = []
    for seed_path in seed_paths:
        seed_supported.update(
            supported_partitions(load_values(seed_path), list(universe))
        )
        seed_sources.append(
            {
                "path": str(seed_path),
                "sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
            }
        )
    seeded = (
        seed_supported
        if seed_mode == "union"
        else set(universe).difference(seed_supported)
    )
    pool = set()
    for partition in universe:
        if partition in seeded:
            master.add_partition_obstruction(partition)
            pool.add(partition)

    trace = []
    resume_source = None
    resume_source_sha256 = None
    if resume_path is not None:
        resumed = json.loads(resume_path.read_text())
        if (
            resumed.get("schema") != SCHEMA
            or resumed.get("seed_mode") != seed_mode
            or resumed.get("partition_family", "all") != partition_family
            or resumed.get("common_rr_uu_singleton_witness")
            != ([5, 6] if require_common_uu_witness else None)
            or resumed.get("common_rr_uu_singleton_witness_forbidden", False)
            != forbid_common_uu_witness
            or resumed.get("rank_disjunct_branch") != rank_branch
            or resumed.get("second_smallest_representative_map")
            != (list(second_smallest_map) if second_smallest_map else None)
            or resumed.get("full_hall_cell_forbidden", True) != forbid_full_hall
            or resumed.get("common_bottom_pair_forbidden", False)
            != forbid_common_bottom_pair
            or resumed.get("three_agent_bottom_pair_forbidden", False)
            != forbid_three_agent_bottom_pair
            or resumed.get("required_split_bottom_pattern")
            != required_split_bottom_pattern
        ):
            raise ValueError("resume record is incompatible")
        for record in resumed["trace"]:
            values = core.validate_values(
                record["values"], expected_n=N, expected_m=M, lower=1
            )
            if forbid_full_hall and full_hall_cells(values):
                raise AssertionError("resumed model has a full Hall cell")
            if require_common_uu_witness and not common_rr_uu_singleton_witness(
                values
            ):
                raise AssertionError("resumed model lost the common UU witness")
            if second_smallest_map is not None and not (
                second_smallest_representative_map_holds(
                    values, second_smallest_map
                )
            ):
                raise AssertionError("resumed model changed second-smallest map")
            if forbid_common_uu_witness and common_rr_uu_singleton_witnesses(
                values
            ):
                raise AssertionError("resumed model gained a common UU witness")
            if forbid_common_bottom_pair and common_bottom_pairs(values):
                raise AssertionError("resumed model gained a common bottom pair")
            if (
                forbid_three_agent_bottom_pair
                and three_agent_bottom_pairs(values)
            ):
                raise AssertionError(
                    "resumed model gained a three-agent bottom pair"
                )
            if required_split_bottom_pattern is not None and not (
                split_bottom_pattern_holds(
                    values, required_split_bottom_pattern
                )
            ):
                raise AssertionError("resumed model lost its split-bottom pattern")
            survivors = tuple(
                partition
                for partition in supported_partitions(values, list(universe))
                if partition not in pool
            )
            if (
                record["pool_size_before"] != len(pool)
                or record["favorite_pair_efx_survivors"] != len(survivors)
            ):
                raise AssertionError("resume trace replay changed")
            trace.append(record)
            for partition in survivors[:add_per_iteration]:
                master.add_partition_obstruction(partition)
                pool.add(partition)
        resume_source = str(resume_path)
        resume_source_sha256 = hashlib.sha256(resume_path.read_bytes()).hexdigest()
    status = "ITERATION_LIMIT"
    raw_status = None
    reason_unknown = None
    result_values = None
    started = time.time()
    iteration = len(trace)
    for iteration in range(len(trace) + 1, max_iterations + 1):
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
            solved.values, expected_n=N, expected_m=M, lower=1
        )
        cells = full_hall_cells(values)
        if forbid_full_hall and cells:
            raise AssertionError("model violates the no-full-cell encoding")
        if require_common_uu_witness and not common_rr_uu_singleton_witness(
            values
        ):
            raise AssertionError("model lost the common UU witness")
        if second_smallest_map is not None and not (
            second_smallest_representative_map_holds(values, second_smallest_map)
        ):
            raise AssertionError("model changed second-smallest map")
        if forbid_common_uu_witness and common_rr_uu_singleton_witnesses(values):
            raise AssertionError("model gained a common UU witness")
        if forbid_common_bottom_pair and common_bottom_pairs(values):
            raise AssertionError("model gained a common bottom pair")
        if forbid_three_agent_bottom_pair and three_agent_bottom_pairs(values):
            raise AssertionError("model gained a three-agent bottom pair")
        if required_split_bottom_pattern is not None and not (
            split_bottom_pattern_holds(values, required_split_bottom_pattern)
        ):
            raise AssertionError("model lost its split-bottom pattern")
        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(pool),
                "favorite_pair_efx_survivors": len(survivors),
                "values": [list(row) for row in values],
            }
        )
        print(
            f"iteration={iteration} pool={len(pool)} survivors={len(survivors)}",
            flush=True,
        )
        if not survivors:
            status = "FULL_CELL_SELECTION_COUNTEREXAMPLE"
            result_values = values
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(partition)
            pool.add(partition)

    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": raw_status,
        "reason_unknown": reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "universal_threshold_encoding": threshold_encoding,
        "rank_disjunct_branch": rank_branch,
        "second_smallest_representative_map": (
            list(second_smallest_map) if second_smallest_map else None
        ),
        "full_hall_cell_forbidden": forbid_full_hall,
        "full_cell_encoding": full_cell_encoding,
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
        "required_split_bottom_pattern": required_split_bottom_pattern,
        "split_bottom_pattern_encoding": split_bottom_pattern_encoding,
        "favorite_pair_partition_count": len(universe),
        "partition_family": partition_family,
        "seed_mode": seed_mode,
        "seed_sources": seed_sources,
        "seed_supported_union_size": len(seed_supported),
        "resume_source": resume_source,
        "resume_source_sha256": resume_source_sha256,
        "pool_size": len(pool),
        "add_per_iteration": add_per_iteration,
        "time_limit_seconds": time_limit,
        "max_iterations": max_iterations,
        "iterations": iteration,
        "elapsed_seconds": time.time() - started,
        "trace": trace,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "literal_complete_efx_count": (
            independent.count_complete_efx0(result_values)
            if result_values is not None
            else None
        ),
        "smt2_path": str(smt2_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "A terminal model refutes only the conditional full-cell "
            "selection target. UNSAT_CANDIDATE requires an independent "
            "encoding before theorem status."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--seed", type=Path, action="append", required=True)
    parser.add_argument("--time-limit", type=float, default=120)
    parser.add_argument("--max-iterations", type=int, default=5)
    parser.add_argument("--add", type=int, default=128)
    parser.add_argument("--seed-mode", choices=("union", "complement"), default="complement")
    parser.add_argument("--resume", type=Path)
    parser.add_argument(
        "--partition-family",
        choices=("all", "six_orbit", "eight_orbit", "common_uu_fan"),
        default="all",
    )
    parser.add_argument(
        "--threshold-encoding",
        choices=("cardinal", "sorting"),
        default="cardinal",
    )
    parser.add_argument("--require-common-uu-witness", action="store_true")
    parser.add_argument("--forbid-common-uu-witness", action="store_true")
    parser.add_argument("--rank-branch")
    parser.add_argument("--second-smallest-map")
    parser.add_argument("--allow-full-hall-cells", action="store_true")
    parser.add_argument("--forbid-common-bottom-pair", action="store_true")
    parser.add_argument(
        "--forbid-three-agent-bottom-pair", action="store_true"
    )
    parser.add_argument(
        "--require-split-bottom-pattern",
        choices=("disjoint", "overlap"),
    )
    args = parser.parse_args()
    if args.time_limit <= 0 or args.max_iterations < 1 or args.add < 1:
        parser.error("invalid CEGAR limits")
    if args.require_common_uu_witness and args.forbid_common_uu_witness:
        parser.error("common-UU witness modes are mutually exclusive")
    if args.rank_branch is not None and (
        len(args.rank_branch) != N or set(args.rank_branch) - {"B", "C"}
    ):
        parser.error("rank branch must be a four-character B/C string")
    second_smallest_map = None
    if args.second_smallest_map is not None:
        try:
            second_smallest_map = tuple(
                int(item) for item in args.second_smallest_map.split(",")
            )
        except ValueError:
            parser.error(
                "second-smallest map must be four comma-separated goods"
            )
        if (
            len(second_smallest_map) != N
            or any(good < 1 or good > 4 for good in second_smallest_map)
            or not args.require_common_uu_witness
        ):
            parser.error(
                "second-smallest map requires four goods 1..4 and the "
                "common-UU branch"
            )
    result = run(
        args.result,
        args.smt2,
        tuple(args.seed),
        args.time_limit,
        args.max_iterations,
        args.add,
        args.seed_mode,
        args.resume,
        args.threshold_encoding,
        args.partition_family,
        args.require_common_uu_witness,
        args.forbid_common_uu_witness,
        args.rank_branch,
        second_smallest_map,
        not args.allow_full_hall_cells,
        args.forbid_common_bottom_pair,
        args.forbid_three_agent_bottom_pair,
        args.require_split_bottom_pattern,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
