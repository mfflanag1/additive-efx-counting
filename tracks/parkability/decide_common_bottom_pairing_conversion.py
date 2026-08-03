#!/usr/bin/env python3
"""Exact-real decision for the common-bottom Hall-pairing conversion lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        hall_failure,
        pairing_has_hall_matching,
    )
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )
except ImportError:
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import (
        add_acceptance_literals,
        hall_failure,
        pairing_has_hall_matching,
    )
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure,
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )


SCHEMA = "common-bottom-pairing-conversion-lra-v1"
N = 4
M = 9
FAVORITE = 0
LOWS = (7, 8)
RESIDUAL = tuple(range(1, 7))
MATCHING = ((1, 2), (3, 4), (5, 6))


def canonical_partition(*bundles):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in bundles))


def conversion_partitions(scope="all"):
    edges = (
        MATCHING[:1]
        if scope == "first_edge"
        else MATCHING[:2]
        if scope == "first_two_edges"
        else MATCHING
        if scope == "all"
        else None
    )
    if edges is None:
        raise ValueError("unknown conversion scope")
    return tuple(
        canonical_partition(
            (FAVORITE, high),
            (*edge, low),
            *(pair for pair in MATCHING if pair != edge),
        )
        for high, low in (LOWS, tuple(reversed(LOWS)))
        for edge in edges
    )


def run(
    result_path,
    smt2_path,
    time_limit,
    threshold_encoding="cardinal",
    hall_witness_type="all",
    conversion_scope="all",
    bottom_agents=None,
    near_bottom_agents=(),
    near_bottom_exception=None,
):
    bottom_agents = (
        tuple(range(N)) if bottom_agents is None else tuple(bottom_agents)
    )
    if not bottom_agents or any(agent not in range(N) for agent in bottom_agents):
        raise ValueError("bottom agents must be a nonempty subset of 0..3")
    near_bottom_agents = tuple(near_bottom_agents)
    if (
        any(agent not in range(N) for agent in near_bottom_agents)
        or set(bottom_agents) & set(near_bottom_agents)
        or (near_bottom_agents and near_bottom_exception not in RESIDUAL)
        or (not near_bottom_agents and near_bottom_exception is not None)
    ):
        raise ValueError("invalid near-bottom exception specification")
    conversions = conversion_partitions(conversion_scope)
    if len(conversions) != len(set(conversions)):
        raise AssertionError("conversion partition census changed")
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    if threshold_encoding == "cardinal":
        add_universal_threshold_failure_cardinal(master)
    elif threshold_encoding == "sorting":
        add_universal_threshold_failure(master)
    else:
        raise ValueError("threshold encoding must be cardinal or sorting")
    bottom_constraints = 0
    for agent in bottom_agents:
        for low in LOWS:
            for good in RESIDUAL:
                master.solver.add(
                    master.values[agent][low]
                    <= master.values[agent][good]
                )
                bottom_constraints += 1
    near_bottom_constraints = 0
    for agent in near_bottom_agents:
        for low in LOWS:
            for good in RESIDUAL:
                if good == near_bottom_exception:
                    continue
                master.solver.add(
                    master.values[agent][low]
                    <= master.values[agent][good]
                )
                near_bottom_constraints += 1
    accept = add_acceptance_literals(master, LOWS, RESIDUAL)
    if hall_witness_type == "all":
        master.solver.add(hall_failure(accept, MATCHING))
        hall_failure_template_count = 21
    elif hall_witness_type == "zero_neighbor":
        master.solver.add(
            *(z3.Not(accept[agent, MATCHING[0]]) for agent in range(N))
        )
        hall_failure_template_count = 1
    elif hall_witness_type == "two_edges_one_neighbor":
        master.solver.add(
            *(
                z3.Not(accept[agent, edge])
                for edge in MATCHING[:2]
                for agent in range(1, N)
            )
        )
        hall_failure_template_count = 1
    elif hall_witness_type == "three_edges_two_neighbors":
        master.solver.add(
            *(
                z3.Not(accept[agent, edge])
                for edge in MATCHING
                for agent in range(2, N)
            )
        )
        hall_failure_template_count = 1
    else:
        raise ValueError("unknown Hall-witness type")
    for partition in conversions:
        master.add_partition_obstruction(partition)

    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    elapsed = time.time() - started
    values = solved.values
    if values is not None:
        audit_threshold_failure(values)
        if any(
            row[low] > row[good]
            for agent, row in enumerate(values)
            if agent in bottom_agents
            for low in LOWS
            for good in RESIDUAL
        ):
            raise AssertionError("model lost a required bottom order")
        if any(
            values[agent][low] > values[agent][good]
            for agent in near_bottom_agents
            for low in LOWS
            for good in RESIDUAL
            if good != near_bottom_exception
        ):
            raise AssertionError("model lost a required near-bottom order")
        if pairing_has_hall_matching(values, LOWS, MATCHING):
            raise AssertionError("model lost the Hall-failed pairing")
        if supported_partitions(values, list(conversions)):
            raise AssertionError("model gained a converted EFX partition")
    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": (
            "UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "CONVERSION_COUNTEREXAMPLE"
            if solved.status == "SAT"
            else "MASTER_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "domain": "strictly positive reals normalized per row",
        "n": N,
        "m": M,
        "favorite": FAVORITE,
        "common_bottom_pair": list(LOWS),
        "fixed_residual_matching": [list(edge) for edge in MATCHING],
        "residual_matching_wlog": (
            "Every perfect matching of the six non-low residual goods is "
            "equivalent by a goods relabeling."
        ),
        "universal_owner_threshold_failure": True,
        "threshold_encoding": threshold_encoding,
        "bottom_order_constraint_count": bottom_constraints,
        "bottom_order_agents": list(bottom_agents),
        "near_bottom_order_agents": list(near_bottom_agents),
        "near_bottom_exception_good": near_bottom_exception,
        "near_bottom_order_constraint_count": near_bottom_constraints,
        "hall_witness_type": hall_witness_type,
        "hall_failure_template_count": hall_failure_template_count,
        "conversion_partition_count": len(conversions),
        "conversion_scope": conversion_scope,
        "conversion_partitions": [
            [list(bundle) for bundle in partition]
            for partition in conversions
        ],
        "values": [list(row) for row in values] if values else None,
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "smt2_path": str(smt2_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT proves the fixed-pairing lemma in this exact encoding; "
            "independent replay is required before theorem status."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument(
        "--threshold-encoding",
        choices=("cardinal", "sorting"),
        default="cardinal",
    )
    parser.add_argument(
        "--bottom-agents",
        default="0,1,2,3",
        help="comma-separated agents required to rank the lows bottom-two",
    )
    parser.add_argument(
        "--near-bottom-agents",
        default="",
        help="agents whose bottom comparisons may fail at one exception good",
    )
    parser.add_argument("--near-bottom-exception", type=int)
    parser.add_argument(
        "--hall-witness-type",
        choices=(
            "all",
            "zero_neighbor",
            "two_edges_one_neighbor",
            "three_edges_two_neighbors",
        ),
        default="all",
    )
    parser.add_argument(
        "--conversion-scope",
        choices=("all", "first_edge", "first_two_edges"),
        default="all",
    )
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    try:
        bottom_agents = tuple(int(item) for item in args.bottom_agents.split(","))
        near_bottom_agents = tuple(
            int(item)
            for item in args.near_bottom_agents.split(",")
            if item
        )
    except ValueError:
        parser.error("bottom agents must be comma-separated integers")
    if (
        not bottom_agents
        or len(set(bottom_agents)) != len(bottom_agents)
        or any(agent not in range(N) for agent in bottom_agents)
    ):
        parser.error("bottom agents must be a nonempty subset of 0..3")
    if (
        len(set(near_bottom_agents)) != len(near_bottom_agents)
        or any(agent not in range(N) for agent in near_bottom_agents)
        or set(bottom_agents) & set(near_bottom_agents)
        or (near_bottom_agents and args.near_bottom_exception not in RESIDUAL)
        or (not near_bottom_agents and args.near_bottom_exception is not None)
    ):
        parser.error("invalid near-bottom exception specification")
    result = run(
        args.result,
        args.smt2,
        args.time_limit,
        args.threshold_encoding,
        args.hall_witness_type,
        args.conversion_scope,
        bottom_agents,
        near_bottom_agents,
        args.near_bottom_exception,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
