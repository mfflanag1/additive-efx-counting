#!/usr/bin/env python3
"""Exact unrestricted global-lex CEGAR for split adjacent-large packets."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .run_adjacent_large_global_lex_atomic_cegar import (
        strict_desired_expression,
        strict_not_desired_expression,
    )
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        N,
        atomic_json,
        desired_expression,
        integerize,
        lex_gt,
        make_cell,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        subset_sum,
    )
except ImportError:
    from run_adjacent_large_global_lex_atomic_cegar import (
        strict_desired_expression,
        strict_not_desired_expression,
    )
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        N,
        atomic_json,
        desired_expression,
        integerize,
        lex_gt,
        make_cell,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        subset_sum,
    )


SCHEMA = "adjacent-large-variable-packet-global-lex-cegar-v1"
POOL_SCHEMA = "adjacent-large-variable-packet-global-lex-pool-v1"
Owner = tuple[int | None, ...]


def structural_solver(cell):
    m = cell["m"]
    tr, _, tq, _ = cell["packets"]
    x, y, floater = cell["x"], cell["y"], cell["floater"]
    base_bundles = cell["base_bundles"]
    values = tuple(
        tuple(z3.Real(f"v_{agent}_{good}") for good in range(m))
        for agent in range(N)
    )
    own = tuple(subset_sum(values, agent, base_bundles[agent]) for agent in range(N))
    solver = z3.SolverFor("QF_LRA")
    for agent in range(N):
        solver.add(*(entry > 0 for entry in values[agent]))
        solver.add(z3.Sum(*values[agent]) == 1)
    for packet in cell["packets"]:
        for left, right in zip(packet, packet[1:]):
            solver.add(values[0][left] < values[0][right])

    expected_envy = {(3, 2), (2, 0)}
    for observer in range(N):
        solver.add(own[observer] > values[observer][floater])
        for target in range(N):
            if observer != target:
                comparison = subset_sum(values, observer, base_bundles[target])
                solver.add(
                    comparison > own[observer]
                    if (observer, target) in expected_envy
                    else own[observer] > comparison
                )
            for removed in base_bundles[target]:
                remainder = tuple(
                    good for good in base_bundles[target] if good != removed
                )
                solver.add(own[observer] > subset_sum(values, observer, remainder))

    expected_desired = {
        (0, 1): tr + (floater,),
        (1, 3): tq + (floater,),
        (3, 2): (y,),
        (2, 0): (x,),
    }
    for source in range(N):
        for target in range(N):
            offer = base_bundles[target] + (floater,)
            expected = expected_desired.get((source, target))
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    if candidate == expected:
                        solver.add(strict_desired_expression(values, own, source, candidate))
                    elif candidate == base_bundles[source]:
                        continue
                    elif expected is None or candidate == offer:
                        solver.add(strict_not_desired_expression(values, own, source, candidate))
    return solver, values, own


def iter_owners(m: int):
    for raw in itertools.product(range(N + 1), repeat=m):
        yield tuple(None if assigned == N else assigned for assigned in raw)


def dominating(values, cell, order):
    base = numeric_utilities(values, cell["base_owner"])
    base_key = tuple(base[agent] for agent in order)
    found = []
    efx_count = 0
    for owner in iter_owners(cell["m"]):
        if not numeric_efx(values, owner):
            continue
        efx_count += 1
        utility = numeric_utilities(values, owner)
        key = tuple(utility[agent] for agent in order)
        if key > base_key:
            found.append((key, owner))
    found.sort(reverse=True, key=lambda record: (record[0], str(record[1])))
    return found, efx_count


def load_pool(path: Path, cell, order):
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("packet_sizes") != list(cell["sizes"])
        or payload.get("agent_order") != list(order)
    ):
        raise ValueError("pool metadata mismatch")
    rivals = [tuple(owner) for owner in payload["rivals"]]
    if len(rivals) != len(set(rivals)):
        raise ValueError("duplicate rival in pool")
    return rivals


def save_pool(path: Path, cell, order, rivals) -> None:
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "packet_sizes": list(cell["sizes"]),
            "agent_order": list(order),
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(sizes, order, pool_path, max_iterations, add_per_iteration, timeout_seconds):
    cell = make_cell(sizes)
    solver, values, own = structural_solver(cell)
    solver.set(timeout=timeout_seconds * 1000)
    rivals = load_pool(pool_path, cell, order)
    rival_set = set(rivals)
    for owner in rivals:
        solver.add(rival_blocker(values, own, owner, order))
    save_pool(pool_path, cell, order, rivals)

    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason_unknown = None
    started = time.time()
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_ADJACENT_SPLIT_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values = integerize(solver.model(), values)
        found, efx_count = dominating(model_values, cell, order)
        unseen = [owner for _, owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "efx_assignment_count": efx_count,
                "dominating_count": len(found),
                "new_count": len(unseen),
                "values": [list(row) for row in model_values],
            }
        )
        if not found:
            status = "SAT_UNRESTRICTED_GLOBAL_LEX_COUNTEREXAMPLE"
            final_values = model_values
            break
        if not unseen:
            raise AssertionError("pooled rival still improves current model")
        for owner in unseen[:add_per_iteration]:
            rivals.append(owner)
            rival_set.add(owner)
            solver.add(rival_blocker(values, own, owner, order))
        save_pool(pool_path, cell, order, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "base_owner": list(cell["base_owner"]),
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "basic_cycle": ["p-f->r", "r-f->q", "q->s", "s->p"],
        "rival_scope": f"all 5^{cell['m']} partial allocations",
        "pool_size": len(rivals),
        "iterations": trace,
        "elapsed_seconds": time.time() - started,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "claim_boundary": {
            "sat": "exact unrestricted counterexample in this fixed packet cell",
            "unsat": "exact theorem only in this fixed packet cell; not an arbitrary-packet theorem",
            "unknown": "no mathematical decision",
        },
    }
    if final_values is not None:
        result["values"] = [list(row) for row in final_values]
    if reason_unknown is not None:
        result["reason_unknown"] = reason_unknown
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--order", required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--add-per-iteration", type=int, default=64)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    order = tuple(int(part) for part in args.order.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        raise ValueError("--sizes must contain four positive integers")
    if sorted(order) != list(range(N)):
        raise ValueError("--order must be a permutation of 0,1,2,3")
    result = run(
        sizes,
        order,
        args.pool,
        args.max_iterations,
        args.add_per_iteration,
        args.timeout_seconds,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
