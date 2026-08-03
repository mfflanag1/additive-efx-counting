#!/usr/bin/env python3
"""Exact CEGAR for the conditional two-core/Tutte selection target."""

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
    from .decide_distinct_half_pair_cover import (
        favorite_pair_balanced_universe,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from decide_distinct_half_hall_layers import add_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-two-core-cegar-v1"
N = 4
M = 9
FAVORITE = 0


def perfect_pairings(goods):
    goods = tuple(goods)
    if not goods:
        yield ()
        return
    first = goods[0]
    for partner in goods[1:]:
        remaining = tuple(
            good for good in goods if good not in (first, partner)
        )
        for rest in perfect_pairings(remaining):
            yield ((first, partner),) + rest


def pair_is_safe(values, agent, lows, pair):
    row = values[agent]
    return (
        sum(row[good] for good in pair)
        >= row[FAVORITE] + max(row[good] for good in lows)
    )


def low_core_candidates(scope="all"):
    if scope == "all":
        return tuple(
            (lows, core_agents)
            for lows in itertools.combinations(range(1, M), 2)
            for core_agents in itertools.combinations(range(N), 2)
        )
    if scope == "canonical":
        return tuple(
            (
                lows,
                tuple(
                    agent for agent in range(N) if agent + 1 not in lows
                ),
            )
            for lows in itertools.combinations(range(1, N + 1), 2)
        )
    raise ValueError("two-core scope must be all or canonical")


def two_core_witnesses(values, scope="all"):
    witnesses = []
    for lows, core_agents in low_core_candidates(scope):
        residual = tuple(good for good in range(1, M) if good not in lows)
        edges = tuple(itertools.combinations(residual, 2))
        pairings = tuple(perfect_pairings(residual))
        if any(
            not pair_is_safe(values, agent, lows, edge)
            for agent in core_agents
            for edge in edges
        ):
            continue
        outsiders = tuple(
            agent for agent in range(N) if agent not in core_agents
        )
        bad_edges = {
            edge
            for edge in edges
            if all(
                not pair_is_safe(values, agent, lows, edge)
                for agent in outsiders
            )
        }
        if any(
            all(tuple(sorted(edge)) in bad_edges for edge in matching)
            for matching in pairings
        ):
            continue
        witnesses.append(
            {
                "low_goods": list(lows),
                "core_agents": list(core_agents),
                "bad_edges": [list(edge) for edge in sorted(bad_edges)],
            }
        )
    return witnesses


def rejection(master, agent, lows, pair):
    pair_value = master._sum(agent, pair)
    return z3.Or(
        *(
            pair_value
            < master.values[agent][FAVORITE] + master.values[agent][low]
            for low in lows
        )
    )


def add_no_two_core(master, scope="all"):
    cell_count = 0
    lost_core_literals = 0
    bad_matching_terms = 0
    for lows, core_agents in low_core_candidates(scope):
        residual = tuple(good for good in range(1, M) if good not in lows)
        edges = tuple(itertools.combinations(residual, 2))
        pairings = tuple(perfect_pairings(residual))
        outsiders = tuple(
            agent for agent in range(N) if agent not in core_agents
        )
        lost_core = tuple(
            rejection(master, agent, lows, edge)
            for agent in core_agents
            for edge in edges
        )
        bad_matchings = tuple(
            z3.And(
                *(
                    rejection(master, agent, lows, edge)
                    for edge in matching
                    for agent in outsiders
                )
            )
            for matching in pairings
        )
        master.solver.add(z3.Or(*lost_core, *bad_matchings))
        cell_count += 1
        lost_core_literals += len(lost_core)
        bad_matching_terms += len(bad_matchings)
    return {
        "encoding": "direct",
        "low_core_cells": cell_count,
        "lost_core_literals": lost_core_literals,
        "bad_perfect_matching_terms": bad_matching_terms,
    }


def add_no_two_core_reified(master, scope="all"):
    cell_count = 0
    accept_literals = 0
    lost_core_literals = 0
    bad_matching_terms = 0
    candidates = low_core_candidates(scope)
    for lows in dict.fromkeys(lows for lows, _ in candidates):
        residual = tuple(good for good in range(1, M) if good not in lows)
        edges = tuple(itertools.combinations(residual, 2))
        pairings = tuple(perfect_pairings(residual))
        accept = {}
        for agent in range(N):
            for edge in edges:
                literal = z3.Bool(
                    f"two_core_accept_lows_{lows[0]}_{lows[1]}_"
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
                accept_literals += 1
        for candidate_lows, core_agents in candidates:
            if candidate_lows != lows:
                continue
            outsiders = tuple(
                agent for agent in range(N) if agent not in core_agents
            )
            lost_core = tuple(
                z3.Not(accept[agent, edge])
                for agent in core_agents
                for edge in edges
            )
            bad_matchings = tuple(
                z3.And(
                    *(
                        z3.Not(accept[agent, edge])
                        for edge in matching
                        for agent in outsiders
                    )
                )
                for matching in pairings
            )
            master.solver.add(z3.Or(*lost_core, *bad_matchings))
            cell_count += 1
            lost_core_literals += len(lost_core)
            bad_matching_terms += len(bad_matchings)
    return {
        "encoding": "reified",
        "accept_literals": accept_literals,
        "low_core_cells": cell_count,
        "lost_core_literals": lost_core_literals,
        "bad_perfect_matching_terms": bad_matching_terms,
    }


def run(
    result_path,
    smt2_path,
    seed_paths,
    time_limit,
    max_iterations,
    add_per_iteration,
    preload_all,
    encoding,
    threshold_encoding,
    seed_mode,
    two_core_encoding_name,
    resume_path,
    two_core_scope,
):
    universe = tuple(favorite_pair_balanced_universe())
    master = ParkabilityLRAMaster(N, M)
    add_branch(master, None, threshold_encoding=threshold_encoding)
    two_core_encoding = (
        add_no_two_core(master, two_core_scope)
        if two_core_encoding_name == "direct"
        else add_no_two_core_reified(master, two_core_scope)
    )
    pool = set()

    if preload_all:
        for partition in universe:
            master.add_partition_obstruction(partition, encoding=encoding)
            pool.add(partition)

    seed_supported = set()
    seed_sources = []
    for seed_path in seed_paths:
        values = load_values(seed_path)
        seed_supported.update(supported_partitions(values, list(universe)))
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
    for partition in universe:
        if partition in seeded and partition not in pool:
            master.add_partition_obstruction(partition, encoding=encoding)
            pool.add(partition)

    trace = []
    resume_source = None
    if resume_path is not None:
        resumed = json.loads(resume_path.read_text())
        if (
            resumed.get("schema") != SCHEMA
            or resumed.get("seed_mode") != seed_mode
            or resumed.get("add_per_iteration") != add_per_iteration
            or resumed.get("favorite_pair_obstruction_encoding") != encoding
            or resumed.get("universal_threshold_encoding")
            != threshold_encoding
            or resumed.get("two_core_encoding", {}).get("encoding")
            != two_core_encoding_name
            or resumed.get("two_core_scope", "all") != two_core_scope
        ):
            raise ValueError("resume record is incompatible")
        for record in resumed["trace"]:
            values = core.validate_values(
                record["values"], expected_n=N, expected_m=M, lower=1
            )
            if two_core_witnesses(values, two_core_scope):
                raise AssertionError("resumed model has a two-core witness")
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
                master.add_partition_obstruction(partition, encoding=encoding)
                pool.add(partition)
        resume_source = str(resume_path.resolve())
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
            solved.values,
            expected_n=N,
            expected_m=M,
            lower=1,
        )
        witnesses = two_core_witnesses(values, two_core_scope)
        if witnesses:
            raise AssertionError("model violates the no-two-core encoding")
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
            status = "TWO_CORE_SELECTION_COUNTEREXAMPLE"
            result_values = values
            break
        for partition in survivors[:add_per_iteration]:
            master.add_partition_obstruction(partition, encoding=encoding)
            pool.add(partition)

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
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "fixed_half_favorite_representatives": [1, 2, 3, 4],
        "universal_owner_threshold_failure": True,
        "universal_threshold_encoding": threshold_encoding,
        "two_core_target_forbidden": True,
        "two_core_scope": two_core_scope,
        "two_core_encoding": two_core_encoding,
        "favorite_pair_partition_count": len(universe),
        "favorite_pair_obstruction_encoding": encoding,
        "preloaded_all_obstructions": preload_all,
        "seed_mode": seed_mode,
        "seed_sources": seed_sources,
        "seed_supported_union_size": len(seed_supported),
        "resume_source": resume_source,
        "pool_size": len(pool),
        "add_per_iteration": add_per_iteration,
        "iterations": iteration,
        "elapsed_seconds": time.time() - started,
        "trace": trace,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "literal_complete_efx_count": literal_count,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "A terminal counterexample refutes only the conditional "
            "two-core/Tutte selection lemma. UNSAT_CANDIDATE requires an "
            "independent encoding before theorem status."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--max-iterations", type=int, default=50)
    parser.add_argument("--add", type=int, default=32)
    parser.add_argument("--preload-all", action="store_true")
    parser.add_argument(
        "--encoding",
        choices=("matching_clauses", "hall_selectors"),
        default="matching_clauses",
    )
    parser.add_argument(
        "--threshold-encoding",
        choices=("cardinal", "sorting"),
        default="cardinal",
    )
    parser.add_argument(
        "--seed-mode",
        choices=("union", "complement"),
        default="union",
    )
    parser.add_argument(
        "--two-core-encoding",
        choices=("direct", "reified"),
        default="direct",
    )
    parser.add_argument("--resume", type=Path)
    parser.add_argument(
        "--two-core-scope",
        choices=("all", "canonical"),
        default="all",
    )
    args = parser.parse_args()
    if args.time_limit <= 0 or args.max_iterations < 1 or args.add < 1:
        parser.error("invalid CEGAR limits")
    result = run(
        args.result,
        args.smt2,
        tuple(args.seed),
        args.time_limit,
        args.max_iterations,
        args.add,
        args.preload_all,
        args.encoding,
        args.threshold_encoding,
        args.seed_mode,
        args.two_core_encoding,
        args.resume,
        args.two_core_scope,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
