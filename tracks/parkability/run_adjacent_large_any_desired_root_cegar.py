#!/usr/bin/env python3
"""Exact CEGAR for anchored-or-any-base-desired adjacent root escapes."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .analyze_adjacent_large_packet_flow import desired_sources
    from .run_adjacent_large_unrestricted_owner_cegar import (
        concrete_owner,
        fixed_owner_solver,
    )
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        atomic_json,
        desired_expression,
        integerize,
        make_cell,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from analyze_adjacent_large_packet_flow import desired_sources
    from run_adjacent_large_unrestricted_owner_cegar import concrete_owner, fixed_owner_solver
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        atomic_json,
        desired_expression,
        integerize,
        make_cell,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "adjacent-large-any-desired-root-cegar-v1"
POOL_SCHEMA = "adjacent-large-any-desired-root-pool-v1"


def root_bundle(owner, root):
    return tuple(good for good, assigned in enumerate(owner) if assigned == root)


def fixed_bundle_formula(owner, root, bundle):
    selected = set(bundle)
    return z3.And(
        *(
            variable == root if good in selected else variable != root
            for good, variable in enumerate(owner)
        )
    )


def qualifying_bundles(values, cell, root):
    base = numeric_utilities(values, cell["base_owner"])
    anchored = tuple(cell["base_bundles"][root])
    bundles = {anchored}
    for mask in range(1, 1 << cell["m"]):
        bundle = tuple(good for good in range(cell["m"]) if mask & (1 << good))
        if root in desired_sources(values, base, bundle):
            bundles.add(bundle)
    return tuple(sorted(bundles, key=lambda item: (len(item), item)))


def find_rivals(values, cell, order, root, limit):
    solver, owner, _ = fixed_owner_solver(values, cell, order)
    bundles = qualifying_bundles(values, cell, root)
    solver.add(z3.Or(*(fixed_bundle_formula(owner, root, bundle) for bundle in bundles)))
    found = []
    for _ in range(limit):
        if solver.check() != z3.sat:
            return "unsat", found, len(bundles)
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
    return "sat", found, len(bundles)


def guarded_blocker(values, own, owner, order, cell, root):
    bundle = root_bundle(owner, root)
    if bundle == tuple(cell["base_bundles"][root]):
        guard = z3.BoolVal(True)
    elif not bundle:
        guard = z3.BoolVal(False)
    else:
        guard = desired_expression(values, own, root, bundle)
    return z3.Or(z3.Not(guard), rival_blocker(values, own, owner, order))


def load_pool(path, sizes, order, root):
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("packet_sizes") != list(sizes)
        or payload.get("agent_order") != list(order)
        or payload.get("root") != root
    ):
        raise ValueError("pool metadata mismatch")
    return [tuple(owner) for owner in payload["rivals"]]


def save_pool(path, sizes, order, root, rivals):
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "packet_sizes": list(sizes),
            "agent_order": list(order),
            "root": root,
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(sizes, order, pool_path, max_iterations, rivals_per_iteration, timeout_seconds):
    root = order[0]
    if root not in (0, 1):
        raise ValueError("the nontrivial root must be p=0 or r=1")
    cell = make_cell(sizes)
    master, values, own = structural_solver(cell)
    master.set(timeout=timeout_seconds * 1000)
    rivals = load_pool(pool_path, sizes, order, root)
    rival_set = set(rivals)
    for owner in rivals:
        master.add(guarded_blocker(values, own, owner, order, cell, root))
    save_pool(pool_path, sizes, order, root, rivals)
    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    started = time.time()
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        checked = master.check()
        if checked == z3.unsat:
            status = "UNSAT_ANY_DESIRED_ROOT_ESCAPE_COUNTEREXAMPLE"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = master.reason_unknown()
            break
        model_values = integerize(master.model(), values)
        finder_status, found, qualifying_count = find_rivals(
            model_values, cell, order, root, rivals_per_iteration
        )
        unseen = [owner for owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "finder_status": finder_status,
                "qualifying_root_bundle_count": qualifying_count,
                "found_count": len(found),
                "new_count": len(unseen),
                "values": [list(row) for row in model_values],
            }
        )
        if finder_status == "unsat":
            status = "SAT_ANY_DESIRED_ROOT_ESCAPE_REFUTED"
            final_values = model_values
            break
        if not unseen:
            raise AssertionError("finder returned no unseen qualifying rival")
        for owner in unseen:
            rivals.append(owner)
            rival_set.add(owner)
            master.add(guarded_blocker(values, own, owner, order, cell, root))
        save_pool(pool_path, sizes, order, root, rivals)
    result = {
        "schema": SCHEMA,
        "status": status,
        "packet_sizes": list(sizes),
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "root": root,
        "root_name": AGENTS[root],
        "family": "root keeps its exact base bundle or receives any bundle desired at the base; all other assignments unrestricted",
        "pool_size": len(rivals),
        "iterations": trace,
        "elapsed_seconds": time.time() - started,
        "claim_boundary": {
            "sat": "refutes this rooted family only; endogenous or changed-equal-utility roots remain unrestricted",
            "unsat": "fixed-cell theorem only; an arbitrary-packet analytic lift is still required",
            "unknown": "no mathematical decision",
        },
        "solver": {"name": "z3", "version": z3.get_version_string()},
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
    parser.add_argument("--rivals-per-iteration", type=int, default=32)
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
