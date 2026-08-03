#!/usr/bin/env python3
"""Mine sufficient subsets of the common-bottom order inequalities."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_common_bottom_pairing_conversion import (
        FAVORITE,
        LOWS,
        MATCHING,
        M,
        N,
        RESIDUAL,
        conversion_partitions,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import add_acceptance_literals
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
    )
except ImportError:
    from anneal import atomic_json
    from decide_common_bottom_pairing_conversion import (
        FAVORITE,
        LOWS,
        MATCHING,
        M,
        N,
        RESIDUAL,
        conversion_partitions,
    )
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import add_acceptance_literals
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
    )


SCHEMA = "common-bottom-conversion-order-core-v1"


def add_canonical_hall_witness(master, accept, witness_type):
    if witness_type == "zero_neighbor":
        master.solver.add(
            *(z3.Not(accept[agent, MATCHING[0]]) for agent in range(N))
        )
        return
    if witness_type == "two_edges_one_neighbor":
        master.solver.add(
            *(
                z3.Not(accept[agent, edge])
                for edge in MATCHING[:2]
                for agent in range(1, N)
            )
        )
        return
    if witness_type == "three_edges_two_neighbors":
        master.solver.add(
            *(
                z3.Not(accept[agent, edge])
                for edge in MATCHING
                for agent in range(2, N)
            )
        )
        return
    raise ValueError("unknown Hall-witness type")


def run(output: Path, formula_output: Path, witness_type: str, time_limit: float):
    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    add_universal_threshold_failure_cardinal(master)

    assumptions = []
    records = {}
    for agent in range(N):
        for low in LOWS:
            for good in RESIDUAL:
                literal = z3.Bool(f"bottom_order_{agent}_{low}_{good}")
                master.solver.add(
                    z3.Implies(
                        literal,
                        master.values[agent][low]
                        <= master.values[agent][good],
                    )
                )
                assumptions.append(literal)
                records[literal] = {
                    "agent": agent,
                    "low": low,
                    "dominating_good": good,
                }

    accept = add_acceptance_literals(master, LOWS, RESIDUAL)
    add_canonical_hall_witness(master, accept, witness_type)
    for partition in conversion_partitions():
        master.add_partition_obstruction(partition)

    master.solver.set(timeout=max(1, round(1000 * time_limit)))
    started = time.time()
    initial_status = master.solver.check(*assumptions)
    initial_elapsed = time.time() - started
    initial_core = (
        list(master.solver.unsat_core()) if initial_status == z3.unsat else []
    )
    core = list(initial_core)

    deletion_trace = []
    if initial_status == z3.unsat:
        for literal in tuple(core):
            trial = [candidate for candidate in core if candidate is not literal]
            check_started = time.time()
            status = master.solver.check(*trial)
            deletion_trace.append(
                {
                    "removed_candidate": records[literal],
                    "solver_status": str(status),
                    "elapsed_seconds": time.time() - check_started,
                }
            )
            if status == z3.unsat:
                core = trial

    formula = master.solver.sexpr()
    formula += "\n"
    formula += "".join(f"(assert {literal})\n" for literal in core)
    formula += "(check-sat)\n"
    formula_output.parent.mkdir(parents=True, exist_ok=True)
    formula_output.write_text(formula)
    minimized = [records[literal] for literal in core]
    result = {
        "schema": SCHEMA,
        "status": (
            "DELETION_MINIMAL_SUFFICIENT_ORDER_CORE"
            if initial_status == z3.unsat
            and all(
                record["solver_status"] != "unknown"
                for record in deletion_trace
            )
            else "UNSAT_CORE_WITH_UNKNOWN_DELETIONS"
            if initial_status == z3.unsat
            else "MASTER_UNKNOWN"
            if initial_status == z3.unknown
            else "UNEXPECTED_SAT"
        ),
        "solver_status": str(initial_status),
        "reason_unknown": (
            master.solver.reason_unknown()
            if initial_status == z3.unknown
            else None
        ),
        "hall_witness_type": witness_type,
        "initial_order_inequality_count": len(assumptions),
        "initial_core_count": (
            len(initial_core) if initial_status == z3.unsat else None
        ),
        "minimized_order_inequality_count": len(core),
        "minimized_order_inequalities": minimized,
        "order_counts_by_agent": {
            str(agent): sum(item["agent"] == agent for item in minimized)
            for agent in range(N)
        },
        "deletion_trace": deletion_trace,
        "initial_elapsed_seconds": initial_elapsed,
        "elapsed_seconds": time.time() - started,
        "time_limit_seconds_per_check": time_limit,
        "formula_path": str(formula_output),
        "formula_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "The retained order inequalities are sufficient for the fixed "
            "canonical Hall-witness cell and six-conversion obstruction. "
            "This is proof-mining evidence until independently replayed."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument(
        "--hall-witness-type",
        choices=(
            "zero_neighbor",
            "two_edges_one_neighbor",
            "three_edges_two_neighbors",
        ),
        required=True,
    )
    parser.add_argument("--time-limit", type=float, default=120)
    args = parser.parse_args()
    if args.time_limit <= 0:
        parser.error("time limit must be positive")
    result = run(
        args.output,
        args.formula,
        args.hall_witness_type,
        args.time_limit,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
