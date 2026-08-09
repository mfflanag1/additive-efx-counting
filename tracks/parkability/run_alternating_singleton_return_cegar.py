#!/usr/bin/env python3
"""Exact CEGAR for the singleton-return rooted escape family."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        bundles,
        make_cell,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        bundles,
        make_cell,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-singleton-return-cegar-v1"
POOL_SCHEMA = "alternating-singleton-return-pool-v1"
SIZES = (2, 2, 2, 2)
ORDER = (0, 2, 1, 3)


def atomic_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def singleton_return_candidates(cell):
    x, y = cell["x"], cell["y"]
    remaining = tuple(good for good in range(cell["m"]) if good not in (x, y))
    seen = set()
    for fixed_agent, destinations in (
        (1, (2, 3, None)),
        (2, (1, 3, None)),
    ):
        for assignment in itertools.product(destinations, repeat=len(remaining)):
            owner = [None] * cell["m"]
            owner[x] = 0
            owner[y] = fixed_agent
            for good, destination in zip(remaining, assignment):
                owner[good] = destination
            allocation = tuple(owner)
            if allocation not in seen:
                seen.add(allocation)
                yield allocation


def rational(model, expression) -> Fraction:
    value = model.eval(expression, model_completion=True)
    return Fraction(value.numerator_as_long(), value.denominator_as_long())


def integerize(model, symbolic):
    rows = []
    for row in symbolic:
        fractions = [rational(model, expression) for expression in row]
        denominator = math.lcm(*(entry.denominator for entry in fractions))
        integers = [int(entry * denominator) for entry in fractions]
        divisor = math.gcd(*integers)
        rows.append(tuple(entry // divisor for entry in integers))
    return tuple(rows)


def dominates(values, cell, allocation) -> bool:
    base = numeric_utilities(values, cell["base_owner"])
    rival = numeric_utilities(values, allocation)
    return tuple(rival[agent] for agent in ORDER) > tuple(base[agent] for agent in ORDER)


def load_pool(path: Path, cell, candidates):
    candidate_set = set(candidates)
    pool = []
    if path.exists():
        data = json.loads(path.read_text())
        if data.get("schema") != POOL_SCHEMA:
            raise ValueError("pool schema mismatch")
        if tuple(data.get("packet_sizes", ())) != SIZES:
            raise ValueError("packet-size mismatch")
        for record in data.get("rivals", []):
            allocation = tuple(record)
            if allocation not in candidate_set:
                raise ValueError("pool contains a non-family allocation")
            if allocation not in pool:
                pool.append(allocation)
    return pool


def save_pool(path: Path, pool) -> None:
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "packet_sizes": list(SIZES),
            "agent_order": list(ORDER),
            "rivals": [list(allocation) for allocation in pool],
        },
    )


def run(pool_path: Path, result_path: Path, timeout_seconds: float, max_iterations: int, batch_size: int):
    cell = make_cell(SIZES)
    candidates = tuple(singleton_return_candidates(cell))
    pool = load_pool(pool_path, cell, candidates)
    solver, symbolic, own = structural_solver(cell)
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    solver.add(*(rival_blocker(symbolic, own, allocation, ORDER) for allocation in pool))
    started = time.monotonic()
    trace = []
    status_name = "ITERATION_LIMIT"
    terminal_values = None
    for iteration in range(1, max_iterations + 1):
        remaining = timeout_seconds - (time.monotonic() - started)
        if remaining <= 0:
            status_name = "TIME_LIMIT"
            break
        solver.set(timeout=max(1, int(remaining * 1000)))
        status = solver.check()
        if status == z3.unsat:
            status_name = "UNSAT_SINGLETON_RETURN_CELL"
            break
        if status == z3.unknown:
            status_name = "MASTER_UNKNOWN"
            break
        values = integerize(solver.model(), symbolic)
        escapes = [
            allocation
            for allocation in candidates
            if numeric_efx(values, allocation) and dominates(values, cell, allocation)
        ]
        if not escapes:
            status_name = "SINGLETON_RETURN_LEMMA_REFUTED"
            terminal_values = values
            break
        new = [allocation for allocation in escapes if allocation not in pool]
        new.sort(key=lambda allocation: (sum(item is not None for item in allocation), str(allocation)))
        selected = new[:batch_size]
        if not selected:
            raise AssertionError("model has escapes but no new blocker")
        before = len(pool)
        pool.extend(selected)
        solver.add(*(rival_blocker(symbolic, own, allocation, ORDER) for allocation in selected))
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": before,
                "escape_count": len(escapes),
                "new_count": len(new),
                "added_count": len(selected),
                "values": [list(row) for row in values],
            }
        )
        save_pool(pool_path, pool)

    result = {
        "schema": SCHEMA,
        "status": status_name,
        "packet_sizes": list(SIZES),
        "goods": list(cell["goods"]),
        "agent_order": list(ORDER),
        "agent_order_names": [AGENTS[agent] for agent in ORDER],
        "candidate_count": len(candidates),
        "pool_size": len(pool),
        "iterations": len(trace),
        "elapsed_seconds": time.monotonic() - started,
        "trace": trace,
        "values": None if terminal_values is None else [list(row) for row in terminal_values],
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
            "reason_unknown": solver.reason_unknown() if status_name == "MASTER_UNKNOWN" else None,
        },
        "claim_boundary": {
            "refuted": "only the singleton-return family in the full binary cell",
            "unsat": "only the singleton-return family in the full binary cell until cap-free conversion",
            "not_proved": "the arbitrary-packet external-observer lemma or complete EFX",
        },
    }
    atomic_json(result_path, result)
    save_pool(pool_path, pool)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=128)
    args = parser.parse_args()
    result = run(args.pool, args.output, args.timeout_seconds, args.max_iterations, args.batch_size)
    print(json.dumps({key: result[key] for key in ("status", "candidate_count", "pool_size", "iterations", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
