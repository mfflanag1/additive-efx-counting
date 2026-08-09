#!/usr/bin/env python3
"""Nested exact CEGAR for unrestricted adjacent-large global-lex escape."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import z3

try:
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        atomic_json,
        integerize,
        make_cell,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        atomic_json,
        integerize,
        make_cell,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "adjacent-large-unrestricted-owner-cegar-v1"
POOL_SCHEMA = "adjacent-large-unrestricted-owner-pool-v1"


def fixed_owner_solver(values, cell, order):
    m = cell["m"]
    owner = tuple(z3.Int(f"owner_{good}") for good in range(m))
    solver = z3.SolverFor("QF_LIA")
    solver.add(*(z3.And(variable >= 0, variable <= 4) for variable in owner))
    utilities = tuple(
        z3.Sum(*(z3.If(owner[good] == agent, values[agent][good], 0) for good in range(m)))
        for agent in range(4)
    )
    observed = tuple(
        tuple(
            z3.Sum(*(z3.If(owner[good] == target, values[observer][good], 0) for good in range(m)))
            for target in range(4)
        )
        for observer in range(4)
    )
    solver.add(
        *(
            z3.Implies(
                owner[removed] == target,
                utilities[observer]
                >= observed[observer][target] - values[observer][removed],
            )
            for observer in range(4)
            for target in range(4)
            for removed in range(m)
        )
    )
    base = numeric_utilities(values, cell["base_owner"])
    solver.add(
        z3.Or(
            *(
                z3.And(
                    *(utilities[order[prefix]] == base[order[prefix]] for prefix in range(index)),
                    utilities[agent] > base[agent],
                )
                for index, agent in enumerate(order)
            )
        )
    )
    return solver, owner, utilities


def concrete_owner(model, owner):
    return tuple(
        None if model.eval(variable).as_long() == 4 else model.eval(variable).as_long()
        for variable in owner
    )


def find_rivals(values, cell, order, limit):
    solver, owner, _ = fixed_owner_solver(values, cell, order)
    found = []
    for _ in range(limit):
        checked = solver.check()
        if checked != z3.sat:
            return str(checked), found
        concrete = concrete_owner(solver.model(), owner)
        found.append(concrete)
        solver.add(
            z3.Or(
                *(
                    variable != (4 if assigned is None else assigned)
                    for variable, assigned in zip(owner, concrete)
                )
            )
        )
    return "sat", found


def load_pool(path, sizes, order):
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("packet_sizes") != list(sizes)
        or payload.get("agent_order") != list(order)
    ):
        raise ValueError("pool metadata mismatch")
    rivals = [tuple(owner) for owner in payload["rivals"]]
    if len(rivals) != len(set(rivals)):
        raise ValueError("duplicate rival in pool")
    return rivals


def save_pool(path, sizes, order, rivals):
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "packet_sizes": list(sizes),
            "agent_order": list(order),
            "rivals": [list(owner) for owner in rivals],
        },
    )


def allocation_record(cell, owner):
    return {
        "allocation": {
            AGENTS[agent]: [
                cell["goods"][good]
                for good, assigned in enumerate(owner)
                if assigned == agent
            ]
            for agent in range(4)
        },
        "charity": [
            cell["goods"][good]
            for good, assigned in enumerate(owner)
            if assigned is None
        ],
    }


def run(sizes, order, pool_path, max_iterations, rivals_per_iteration, timeout_seconds):
    cell = make_cell(sizes)
    master, values, own = structural_solver(cell)
    master.set(timeout=timeout_seconds * 1000)
    rivals = load_pool(pool_path, sizes, order)
    rival_set = set(rivals)
    for owner in rivals:
        master.add(rival_blocker(values, own, owner, order))
    save_pool(pool_path, sizes, order, rivals)

    trace = []
    final_values = None
    status = "ITERATION_LIMIT"
    reason_unknown = None
    started = time.time()
    for iteration in range(1, max_iterations + 1):
        checked = master.check()
        if checked == z3.unsat:
            status = "UNSAT_ADJACENT_GLOBAL_LEX_COUNTEREXAMPLE"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = master.reason_unknown()
            break
        model_values = integerize(master.model(), values)
        finder_status, found = find_rivals(
            model_values, cell, order, rivals_per_iteration
        )
        unseen = [owner for owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "finder_status": finder_status,
                "found_count": len(found),
                "new_count": len(unseen),
                "values": [list(row) for row in model_values],
                "examples": [allocation_record(cell, owner) for owner in unseen[:3]],
            }
        )
        if finder_status == "unsat":
            status = "SAT_UNRESTRICTED_GLOBAL_LEX_COUNTEREXAMPLE"
            final_values = model_values
            break
        if not unseen:
            raise AssertionError("owner finder returned no unseen improving allocation")
        for owner in unseen:
            rivals.append(owner)
            rival_set.add(owner)
            master.add(rival_blocker(values, own, owner, order))
        save_pool(pool_path, sizes, order, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "basic_cycle": ["p-f->r", "r-f->q", "q->s", "s->p"],
        "rival_scope": "unrestricted owner-variable QF_LIA over all partial allocations",
        "pool_size": len(rivals),
        "iterations": trace,
        "elapsed_seconds": time.time() - started,
        "solver": {"name": "z3", "version": z3.get_version_string(), "master_logic": "QF_LRA", "finder_logic": "QF_LIA"},
        "claim_boundary": {
            "sat": "exact unrestricted global-lex counterexample in this fixed strict packet cell",
            "unsat": "exact exclusion only in this fixed packet cell; not a cap-free theorem",
            "unknown": "no mathematical decision",
        },
    }
    if final_values is not None:
        result["values"] = [list(row) for row in final_values]
    if reason_unknown is not None:
        result["reason_unknown"] = reason_unknown
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--order", required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--rivals-per-iteration", type=int, default=16)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    order = tuple(int(part) for part in args.order.split(","))
    result = run(
        sizes,
        order,
        args.pool,
        args.max_iterations,
        args.rivals_per_iteration,
        args.timeout_seconds,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
