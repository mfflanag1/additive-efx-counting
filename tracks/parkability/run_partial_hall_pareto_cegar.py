#!/usr/bin/env python3
"""CEGAR for a Pareto-maximal radius-one Hall obstruction."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .analyze_partial_state_potentials import enumerate_states
    from .decide_partial_hall_radius_one import (
        bundle_value,
        candidate_partitions,
        eligible_constraints,
        integerize,
        matching_failure,
    )
except ImportError:
    from anneal import atomic_json
    from analyze_partial_state_potentials import enumerate_states
    from decide_partial_hall_radius_one import (
        bundle_value,
        candidate_partitions,
        eligible_constraints,
        integerize,
        matching_failure,
    )


SCHEMA = "partial-hall-pareto-cegar-v1"


def masks_to_bundles(masks, m):
    return tuple(
        tuple(good for good in range(m) if mask & (1 << good)) for mask in masks
    )


def build_master(timeout_ms):
    n = 4
    m = 9
    floater = 8
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    values = [[z3.Real(f"v_{agent}_{good}") for good in range(m)] for agent in range(n)]
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    for row in values:
        solver.add(z3.Sum(row) == 1)
        solver.add(*(entry > 0 for entry in row))
    solver.add(*eligible_constraints(values, base, floater))
    partitions = list(candidate_partitions(base, floater))
    for move in partitions:
        for matching in itertools.permutations(range(n)):
            solver.add(matching_failure(values, move["partition"], matching))
    return solver, values, base, floater, partitions


def dominators(integer_values, base, floater):
    base_utilities = tuple(
        sum(integer_values[agent][good] for good in base[agent])
        for agent in range(4)
    )
    records = []
    for state in enumerate_states(integer_values):
        if all(
            state["utilities"][agent] >= base_utilities[agent]
            for agent in range(4)
        ) and state["utilities"] != base_utilities:
            records.append(state)
    records.sort(
        key=lambda state: (
            -sum(
                state["utilities"][agent] - base_utilities[agent]
                for agent in range(4)
            ),
            state["floater"],
            state["base_index"],
        )
    )
    return base_utilities, records


def pareto_blocker(values, base, rival):
    bundles = masks_to_bundles(rival["masks"], len(values[0]))
    rival_eligible = z3.And(
        *eligible_constraints(values, bundles, rival["floater"])
    )
    base_utilities = [
        bundle_value(values[agent], base[agent]) for agent in range(4)
    ]
    rival_utilities = [
        bundle_value(values[agent], bundles[agent]) for agent in range(4)
    ]
    dominates = z3.And(
        *(rival_utilities[agent] >= base_utilities[agent] for agent in range(4)),
        z3.Or(
            *(rival_utilities[agent] > base_utilities[agent] for agent in range(4))
        ),
    )
    return z3.Not(z3.And(rival_eligible, dominates))


def replay_trace(solver, values, base, trace, batch_size):
    learned = set()
    for record in trace:
        _, found = dominators(record["values"], base, 8)
        new = [
            state
            for state in found
            if (state["floater"], tuple(state["masks"])) not in learned
        ]
        if len(new) != record["new_dominator_count"]:
            raise ValueError(
                f"checkpoint replay mismatch at iteration {record['iteration']}"
            )
        for rival in new[:batch_size]:
            key = (rival["floater"], tuple(rival["masks"]))
            learned.add(key)
            solver.add(pareto_blocker(values, base, rival))
    return learned


def run(
    output,
    checkpoint,
    max_iterations,
    batch_size,
    timeout_seconds,
    resume_from=None,
):
    solver, values, base, floater, partitions = build_master(
        int(timeout_seconds * 1000)
    )
    trace = []
    learned = set()
    if resume_from is not None:
        saved = json.loads(resume_from.read_text())
        if saved.get("schema") != SCHEMA:
            raise ValueError(f"unsupported checkpoint schema: {saved.get('schema')}")
        if saved.get("batch_size", batch_size) != batch_size:
            raise ValueError("resume batch size must match checkpoint batch size")
        trace = saved["trace"]
        learned = replay_trace(solver, values, base, trace, batch_size)
        if saved.get("learned_rival_count") != len(learned):
            raise ValueError("checkpoint learned-rival count does not replay")
    started = time.time()
    terminal_values = None
    status = "ITERATION_LIMIT"
    iteration = len(trace)
    for iteration in range(iteration + 1, max_iterations + 1):
        verdict = solver.check()
        if verdict == z3.unsat:
            status = "UNSAT"
            break
        if verdict == z3.unknown:
            status = "MASTER_UNKNOWN"
            break
        integer_values = integerize(solver.model(), values)
        base_utilities, found = dominators(integer_values, base, floater)
        new = [
            state
            for state in found
            if (state["floater"], tuple(state["masks"])) not in learned
        ]
        record = {
            "iteration": iteration,
            "elapsed_seconds": round(time.time() - started, 6),
            "base_utilities": list(base_utilities),
            "dominator_count": len(found),
            "new_dominator_count": len(new),
            "learned_rival_count_before": len(learned),
            "values": integer_values,
        }
        trace.append(record)
        print(json.dumps(record, sort_keys=True), flush=True)
        if not found:
            terminal_values = integer_values
            status = "PARETO_RADIUS_ONE_COUNTEREXAMPLE"
            break
        if not new:
            raise AssertionError("model retains only already-blocked dominators")
        for rival in new[:batch_size]:
            key = (rival["floater"], tuple(rival["masks"]))
            learned.add(key)
            solver.add(pareto_blocker(values, base, rival))
        partial = {
            "schema": SCHEMA,
            "status": "RUNNING",
            "iteration": iteration,
            "batch_size": batch_size,
            "learned_rival_count": len(learned),
            "trace": trace,
        }
        atomic_json(checkpoint, partial)
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "A SAT counterexample refutes Pareto-maximal radius-one Hall "
            "completion, not complete additive EFX; UNSAT proves this fixed base cell."
        ),
        "n": 4,
        "m": 9,
        "floater": floater,
        "base_bundles": [list(bundle) for bundle in base],
        "candidate_partition_count": len(partitions),
        "max_iterations": max_iterations,
        "batch_size": batch_size,
        "timeout_seconds_per_master": timeout_seconds,
        "iterations_completed": iteration,
        "learned_rival_count": len(learned),
        "elapsed_seconds": round(time.time() - started, 6),
        "values": terminal_values,
        "trace": trace,
        "solver_reason_unknown": solver.reason_unknown() if status == "MASTER_UNKNOWN" else None,
        "solver_statistics": str(solver.statistics()),
    }
    atomic_json(output, result)
    atomic_json(checkpoint, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--resume-from", type=Path)
    args = parser.parse_args()
    result = run(
        args.output,
        args.checkpoint,
        args.max_iterations,
        args.batch_size,
        args.timeout_seconds,
        args.resume_from,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
