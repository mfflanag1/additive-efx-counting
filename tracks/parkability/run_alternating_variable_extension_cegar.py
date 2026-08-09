#!/usr/bin/env python3
"""Exact variable-packet CEGAR for the strict anchored-or-any-offer lemma."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import atomic_json
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        N,
        bundles,
        integerize,
        make_cell,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_alternating_global_lex_cegar import atomic_json
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        N,
        bundles,
        integerize,
        make_cell,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-variable-extension-cegar-v1"
POOL_SCHEMA = "alternating-variable-extension-pool-v1"
ORDER = (0, 2, 3, 1)


def find_rivals(values, cell, timeout_seconds, limit):
    m = cell["m"]
    root = 0
    root_good = cell["x"]
    offer = cell["base_bundles"][1] + (cell["floater"],)
    base = numeric_utilities(values, cell["base_owner"])
    owner = tuple(z3.Int(f"extension_owner_{good}") for good in range(m))
    solver = z3.SolverFor("QF_LIA")
    solver.set(timeout=max(1, timeout_seconds * 1000))
    solver.add(*(z3.And(variable >= 0, variable <= N) for variable in owner))
    utilities = tuple(
        z3.Sum(
            *(z3.If(owner[good] == agent, values[agent][good], 0) for good in range(m))
        )
        for agent in range(N)
    )
    targets = tuple(
        tuple(
            z3.Sum(
                *(z3.If(owner[good] == target, values[observer][good], 0) for good in range(m))
            )
            for target in range(N)
        )
        for observer in range(N)
    )
    anchored = z3.And(
        owner[root_good] == root,
        *(owner[good] != root for good in range(m) if good != root_good),
    )
    promoted = z3.And(
        *(owner[good] != root for good in range(m) if good not in offer),
        utilities[root] > base[root],
        *(
            z3.Implies(
                owner[removed] == root,
                targets[observer][root] - values[observer][removed] <= base[observer],
            )
            for observer in range(N)
            for removed in offer
        ),
    )
    solver.add(z3.Or(anchored, promoted))
    solver.add(
        *(
            z3.Implies(
                owner[removed] == target,
                utilities[observer]
                >= targets[observer][target] - values[observer][removed],
            )
            for observer in range(N)
            for target in range(N)
            for removed in range(m)
        )
    )
    solver.add(
        z3.Or(
            *(
                z3.And(
                    *(utilities[ORDER[prefix]] == base[ORDER[prefix]] for prefix in range(index)),
                    utilities[agent] > base[agent],
                )
                for index, agent in enumerate(ORDER)
            )
        )
    )

    found = []
    modes = []
    while len(found) < limit:
        checked = solver.check()
        if checked == z3.unsat:
            return ("unsat" if not found else "sat"), found, modes, None
        if checked != z3.sat:
            return ("unknown" if not found else "sat"), found, modes, solver.reason_unknown()
        model = solver.model()
        concrete = tuple(
            None if model.eval(variable).as_long() == N else model.eval(variable).as_long()
            for variable in owner
        )
        assigned = bundles(concrete)
        mode = "anchored" if assigned[root] == (root_good,) else "promoted"
        if not numeric_efx(values, concrete):
            raise AssertionError("finder returned non-EFX rival")
        found.append(concrete)
        modes.append(mode)
        solver.add(
            z3.Or(
                *(variable != (N if assigned is None else assigned)
                  for variable, assigned in zip(owner, concrete))
            )
        )
    return "sat", found, modes, None


def load_pool(path, sizes):
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if payload.get("schema") != POOL_SCHEMA or payload.get("packet_sizes") != list(sizes):
        raise ValueError("pool metadata mismatch")
    rivals = [tuple(owner) for owner in payload["rivals"]]
    if len(rivals) != len(set(rivals)):
        raise ValueError("duplicate pool rival")
    return rivals


def save_pool(path, sizes, rivals):
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "packet_sizes": list(sizes),
            "agent_order": list(ORDER),
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(sizes, pool_path, output, iterations, master_timeout, rival_timeout, batch):
    cell = make_cell(sizes)
    solver, values, own = structural_solver(cell)
    solver.set(timeout=max(1, master_timeout * 1000))
    rivals = load_pool(pool_path, sizes)
    rival_set = set(rivals)
    for owner in rivals:
        solver.add(rival_blocker(values, own, owner, ORDER))
    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason = None
    for iteration in range(1, iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_STRICT_EXTENSION_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason = solver.reason_unknown()
            break
        model_values = integerize(solver.model(), values)
        rival_status, found, modes, rival_reason = find_rivals(
            model_values, cell, rival_timeout, batch
        )
        unseen = [owner for owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "rival_status": rival_status,
                "anchored_count": modes.count("anchored"),
                "promoted_count": modes.count("promoted"),
                "new_count": len(unseen),
                "rival_reason_unknown": rival_reason,
                "values": [list(row) for row in model_values],
            }
        )
        print(
            f"iteration={iteration} pool={len(rivals)} "
            f"anchored={modes.count('anchored')} "
            f"promoted={modes.count('promoted')} new={len(unseen)}",
            flush=True,
        )
        if rival_status == "unsat":
            status = "SAT_STRICT_EXTENSION_COUNTEREXAMPLE"
            final_values = model_values
            break
        if rival_status == "unknown":
            status = "RIVAL_UNKNOWN"
            final_values = model_values
            reason = rival_reason
            break
        if not unseen:
            raise AssertionError("finder returned only pooled rivals")
        for owner in unseen:
            solver.add(rival_blocker(values, own, owner, ORDER))
            rivals.append(owner)
            rival_set.add(owner)
        save_pool(pool_path, sizes, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "packet_sizes": list(sizes),
        "agent_order": list(ORDER),
        "iterations": len(trace),
        "pool_size": len(rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason,
        "values": None if final_values is None else [list(row) for row in final_values],
        "trace": trace,
        "claim_boundary": {
            "sat": "exactly refutes the unrestricted strict dichotomy",
            "unsat": "proves only this fixed packet-size cell",
            "unknown": "no mathematical decision",
        },
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--master-timeout-seconds", type=int, default=120)
    parser.add_argument("--rival-timeout-seconds", type=int, default=60)
    parser.add_argument("--batch", type=int, default=64)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    if args.output.exists():
        parser.error("output path must not exist")
    result = run(
        sizes,
        args.pool,
        args.output,
        args.iterations,
        args.master_timeout_seconds,
        args.rival_timeout_seconds,
        args.batch,
    )
    print(json.dumps({key: result[key] for key in ("status", "iterations", "pool_size")}, indent=2))


if __name__ == "__main__":
    main()
