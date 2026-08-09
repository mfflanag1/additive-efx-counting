#!/usr/bin/env python3
"""Exact motif-discovery CEGAR for the length-three two-large EFX atom."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import (
        ALL_OWNERS,
        N,
        atomic_json,
        bundles,
        desired_expression,
        integerize_model,
        numeric_efx,
        rival_blocker,
        subset_sum,
    )
except ImportError:
    from run_alternating_global_lex_cegar import (
        ALL_OWNERS,
        N,
        atomic_json,
        bundles,
        desired_expression,
        integerize_model,
        numeric_efx,
        rival_blocker,
        subset_sum,
    )


SCHEMA = "length-three-global-lex-atomic-cegar-v1"
POOL_SCHEMA = "length-three-global-lex-atomic-pool-v2"
AGENTS = ("p", "r", "q", "s")
GOODS = ("tr", "br", "tq", "bq", "x", "y", "f")
BASE_OWNER = (1, 1, 2, 2, 0, 3, None)
BASE_BUNDLES = ((4,), (0, 1), (2, 3), (5,))
def structural_solver(singleton_source: int, mode: str = "exact"):
    if singleton_source not in (0, 1, 2):
        raise ValueError("singleton champion source must be p, r, or q")
    if mode not in {"exact", "selected"}:
        raise ValueError("mode must be exact or selected")
    values = tuple(
        tuple(z3.Real(f"l3_v_{agent}_{good}") for good in range(7))
        for agent in range(N)
    )
    own = tuple(subset_sum(values, agent, BASE_BUNDLES[agent]) for agent in range(N))
    solver = z3.SolverFor("QF_LRA")
    expected_envy = {(2, 0), (singleton_source, 3)}
    for agent in range(N):
        solver.add(*(entry > 0 for entry in values[agent]))
        solver.add(z3.Sum(*values[agent]) == 1)
    for observer in range(N):
        solver.add(own[observer] > values[observer][6])
        for target in range(N):
            if observer != target and mode == "exact":
                target_value = subset_sum(values, observer, BASE_BUNDLES[target])
                solver.add(
                    target_value > own[observer]
                    if (observer, target) in expected_envy
                    else own[observer] > target_value
                )
            for removed in BASE_BUNDLES[target]:
                solver.add(
                    own[observer]
                    > subset_sum(
                        values,
                        observer,
                        tuple(g for g in BASE_BUNDLES[target] if g != removed),
                    )
                )

    if mode == "selected":
        solver.add(subset_sum(values, 2, BASE_BUNDLES[0]) > own[2])
        solver.add(subset_sum(values, singleton_source, BASE_BUNDLES[3]) > own[singleton_source])
        solver.add(own[0] > subset_sum(values, 0, BASE_BUNDLES[1]))
        solver.add(own[1] > subset_sum(values, 1, BASE_BUNDLES[2]))
    expected_desired = {
        (0, 1): (0, 6),
        (1, 2): (2, 6),
        (2, 0): (4,),
        (singleton_source, 3): (5,),
    }
    for source in range(N):
        for target in range(N):
            offer = BASE_BUNDLES[target] + (6,)
            expected = expected_desired.get((source, target))
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    relation = desired_expression(values, own, source, candidate)
                    if candidate == expected:
                        solver.add(relation)
                    elif mode == "exact" and (expected is None or candidate == offer):
                        solver.add(z3.Not(relation))
    return solver, values, own


def numeric_utilities(values, owner):
    assigned = bundles(owner)
    return tuple(
        sum(values[agent][good] for good in assigned[agent]) for agent in range(N)
    )


def dominating_rivals(values, order):
    base = numeric_utilities(values, BASE_OWNER)
    base_key = tuple(base[agent] for agent in order)
    found = []
    efx_count = 0
    for owner in ALL_OWNERS:
        if not numeric_efx(values, owner):
            continue
        efx_count += 1
        utility = numeric_utilities(values, owner)
        key = tuple(utility[agent] for agent in order)
        if key > base_key:
            found.append((key, owner))
    found.sort(reverse=True, key=lambda record: (record[0], str(record[1])))
    return found, efx_count


def load_pool(path, source, order, mode="exact"):
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("singleton_champion_source") != source
        or payload.get("agent_order") != list(order)
        or payload.get("structural_mode") != mode
    ):
        raise ValueError("pool metadata mismatch")
    owners = [tuple(owner) for owner in payload["rivals"]]
    if len(owners) != len(set(owners)):
        raise ValueError("duplicate rival")
    return owners


def save_pool(path, source, order, rivals, mode="exact"):
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "singleton_champion_source": source,
            "agent_order": list(order),
            "structural_mode": mode,
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(source, order, pool_path, output, iterations, batch, timeout, mode="exact"):
    solver, values, own = structural_solver(source, mode)
    solver.set(timeout=max(1, timeout * 1000))
    rivals = load_pool(pool_path, source, order, mode)
    rival_set = set(rivals)
    for owner in rivals:
        solver.add(rival_blocker(values, own, owner, order))
    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason = None
    for iteration in range(1, iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_ATOMIC_SOURCE_ORDER_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason = solver.reason_unknown()
            break
        model_values = integerize_model(solver.model(), values)
        found, efx_count = dominating_rivals(model_values, order)
        unseen = [owner for _key, owner in found if owner not in rival_set]
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
        print(
            f"iteration={iteration} pool={len(rivals)} efx={efx_count} "
            f"dominating={len(found)} new={len(unseen)}",
            flush=True,
        )
        if not found:
            status = "SAT_ATOMIC_GLOBAL_LEX_COUNTEREXAMPLE"
            final_values = model_values
            break
        if not unseen:
            raise AssertionError("master admitted a profile blocked by the current pool")
        for owner in unseen[:batch]:
            solver.add(rival_blocker(values, own, owner, order))
            rivals.append(owner)
            rival_set.add(owner)
        save_pool(pool_path, source, order, rivals, mode)
    result = {
        "schema": SCHEMA,
        "status": status,
        "singleton_champion_source": source,
        "structural_mode": mode,
        "agent_order": list(order),
        "iterations": len(trace),
        "pool_size": len(rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason,
        "values": None if final_values is None else [list(row) for row in final_values],
        "trace": trace,
        "claim_boundary": {
            "sat": "exact counterexample to this atomic structural source/order cell",
            "unsat": "motif discovery only; not a packet theorem",
            "unknown": "no mathematical decision",
        },
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--singleton-source", choices=AGENTS[:3], required=True)
    parser.add_argument("--order", required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--batch", type=int, default=128)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--mode", choices=("exact", "selected"), default="exact")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output path must not exist")
    source = AGENTS.index(args.singleton_source)
    order = tuple(AGENTS.index(name) for name in args.order.split(","))
    if sorted(order) != list(range(N)):
        parser.error("order must be a permutation of p,r,q,s")
    result = run(
        source,
        order,
        args.pool,
        args.output,
        args.iterations,
        args.batch,
        args.timeout_seconds,
        args.mode,
    )
    print(json.dumps({key: result[key] for key in ("status", "iterations", "pool_size")}, indent=2))


if __name__ == "__main__":
    main()
