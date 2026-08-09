#!/usr/bin/env python3
"""CEGAR proof miner for adjacent selected-root EFX completion."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import z3

try:
    from .decide_adjacent_large_selected_root_completion import candidates, selected_bundle
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        atomic_json,
        integerize,
        make_cell,
        numeric_efx,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from decide_adjacent_large_selected_root_completion import candidates, selected_bundle
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        atomic_json,
        integerize,
        make_cell,
        numeric_efx,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "adjacent-large-selected-root-completion-cegar-v1"
POOL_SCHEMA = "adjacent-large-selected-root-completion-pool-v1"


def load_pool(path, sizes, root):
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("packet_sizes") != list(sizes)
        or payload.get("root") != root
    ):
        raise ValueError("pool metadata mismatch")
    rivals = [tuple(owner) for owner in payload["rivals"]]
    if len(rivals) != len(set(rivals)):
        raise ValueError("duplicate rival in pool")
    return rivals


def save_pool(path, sizes, root, rivals):
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "packet_sizes": list(sizes),
            "root": root,
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(sizes, root, pool_path, max_iterations, add_per_iteration, timeout_seconds):
    cell = make_cell(sizes)
    menu = tuple(candidates(cell, root))
    order = (root,) + tuple(agent for agent in range(4) if agent != root)
    solver, values, own = structural_solver(cell)
    solver.set(timeout=timeout_seconds * 1000)
    rivals = load_pool(pool_path, sizes, root)
    rival_set = set(rivals)
    for owner in rivals:
        solver.add(rival_blocker(values, own, owner, order))
    save_pool(pool_path, sizes, root, rivals)

    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason_unknown = None
    started = time.time()
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_SELECTED_ROOT_ALWAYS_COMPLETES"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values = integerize(solver.model(), values)
        found = [owner for owner in menu if numeric_efx(model_values, owner)]
        unseen = [owner for owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "efx_completion_count": len(found),
                "new_count": len(unseen),
                "values": [list(row) for row in model_values],
            }
        )
        if not found:
            status = "SAT_SELECTED_ROOT_COMPLETION_REFUTED"
            final_values = model_values
            break
        if not unseen:
            raise AssertionError("pooled completion remains EFX")
        for owner in unseen[:add_per_iteration]:
            rivals.append(owner)
            rival_set.add(owner)
            solver.add(rival_blocker(values, own, owner, order))
        save_pool(pool_path, sizes, root, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "root": root,
        "root_name": AGENTS[root],
        "selected_root_bundle": [cell["goods"][good] for good in selected_bundle(cell, root)],
        "candidate_count": len(menu),
        "pool_size": len(rivals),
        "iterations": trace,
        "elapsed_seconds": time.time() - started,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
    }
    if final_values is not None:
        result["values"] = [list(row) for row in final_values]
    if reason_unknown is not None:
        result["reason_unknown"] = reason_unknown
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--root", type=int, choices=(0, 1), required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=40)
    parser.add_argument("--add-per-iteration", type=int, default=64)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    result = run(
        sizes,
        args.root,
        args.pool,
        args.max_iterations,
        args.add_per_iteration,
        args.timeout_seconds,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
