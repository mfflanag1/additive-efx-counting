#!/usr/bin/env python3
"""Exact unrestricted CEGAR for the adjacent-large 2+2+1+1 atom.

The basic cycle is p -f-> r -f-> q -> s -> p.  Agents r and q own the
adjacent two-good bundles; p and s own singletons.  Every rival partial
allocation is allowed, so a SAT endpoint is an exact counterexample to the
global-lex escape statement in this structural atom.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import (
        AGENTS,
        ALL_OWNERS,
        BASE_BUNDLES,
        BASE_OWNER,
        M,
        N,
        atomic_json,
        desired_expression,
        dominating_rivals,
        integerize_model,
        rival_blocker,
        subset_sum,
    )
except ImportError:
    from run_alternating_global_lex_cegar import (
        AGENTS,
        ALL_OWNERS,
        BASE_BUNDLES,
        BASE_OWNER,
        M,
        N,
        atomic_json,
        desired_expression,
        dominating_rivals,
        integerize_model,
        rival_blocker,
        subset_sum,
    )


SCHEMA = "adjacent-large-global-lex-atomic-cegar-v1"
POOL_SCHEMA = "adjacent-large-global-lex-atomic-pool-v1"
GOODS = ("tr", "br", "tq", "bq", "x", "y", "f")
EXPECTED_ENVY = {(3, 2), (2, 0)}
EXPECTED_DESIRED = {
    (0, 1): {(0, 6)},
    (1, 3): {(2, 6)},
    (3, 2): {(5,)},
    (2, 0): {(4,)},
}


Owner = tuple[int | None, ...]


def strict_desired_expression(values, own, source, candidate):
    return z3.And(
        subset_sum(values, source, candidate) > own[source],
        *(
            own[observer]
            > subset_sum(
                values,
                observer,
                tuple(good for good in candidate if good != removed),
            )
            for observer in range(N)
            for removed in candidate
        ),
    )


def strict_not_desired_expression(values, own, source, candidate):
    return z3.Or(
        subset_sum(values, source, candidate) < own[source],
        *(
            subset_sum(
                values,
                observer,
                tuple(good for good in candidate if good != removed),
            )
            > own[observer]
            for observer in range(N)
            for removed in candidate
        ),
    )


def structural_solver():
    values = tuple(
        tuple(z3.Real(f"v_{agent}_{good}") for good in range(M))
        for agent in range(N)
    )
    own = tuple(
        subset_sum(values, agent, BASE_BUNDLES[agent]) for agent in range(N)
    )
    solver = z3.SolverFor("QF_LRA")
    for agent in range(N):
        solver.add(*(entry > 0 for entry in values[agent]))
        solver.add(z3.Sum(*values[agent]) == 1)

    for observer in range(N):
        solver.add(own[observer] > values[observer][6])
        for target in range(N):
            if observer != target:
                comparison = subset_sum(values, observer, BASE_BUNDLES[target])
                solver.add(
                    comparison > own[observer]
                    if (observer, target) in EXPECTED_ENVY
                    else own[observer] > comparison
                )
            for removed in BASE_BUNDLES[target]:
                remainder = tuple(
                    good for good in BASE_BUNDLES[target] if good != removed
                )
                solver.add(own[observer] > subset_sum(values, observer, remainder))

    for source in range(N):
        for target in range(N):
            offer = BASE_BUNDLES[target] + (6,)
            expected = EXPECTED_DESIRED.get((source, target), set())
            for size in range(1, len(offer) + 1):
                for candidate in itertools.combinations(offer, size):
                    if candidate in expected:
                        solver.add(strict_desired_expression(values, own, source, candidate))
                    elif candidate == BASE_BUNDLES[source]:
                        # This candidate equals the source's current bundle,
                        # so failure of the strict improvement condition is
                        # an algebraic identity, not a degeneracy tie.
                        continue
                    elif not expected or candidate == offer:
                        solver.add(strict_not_desired_expression(values, own, source, candidate))
    return solver, values, own


def load_pool(path: Path, order: tuple[int, ...]) -> list[Owner]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("agent_order") != list(order)
        or payload.get("base_owner") != list(BASE_OWNER)
    ):
        raise ValueError("pool metadata mismatch")
    rivals = [tuple(owner) for owner in payload["rivals"]]
    if len(rivals) != len(set(rivals)):
        raise ValueError("duplicate rival in pool")
    return rivals


def save_pool(path: Path, order: tuple[int, ...], rivals: list[Owner]) -> None:
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "agent_order": list(order),
            "base_owner": list(BASE_OWNER),
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(
    order: tuple[int, ...],
    pool_path: Path,
    max_iterations: int,
    add_per_iteration: int,
    timeout_seconds: int,
) -> dict:
    solver, values, own = structural_solver()
    solver.set(timeout=timeout_seconds * 1000)
    rivals = load_pool(pool_path, order)
    rival_set = set(rivals)
    for owner in rivals:
        solver.add(rival_blocker(values, own, owner, order))
    save_pool(pool_path, order, rivals)

    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason_unknown = None
    started = time.time()
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_ADJACENT_ATOMIC_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values = integerize_model(solver.model(), values)
        found, efx_count = dominating_rivals(model_values, order)
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
        save_pool(pool_path, order, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "basic_cycle": ["p-f->r", "r-f->q", "q->s", "s->p"],
        "goods": list(GOODS),
        "base_owner": list(BASE_OWNER),
        "rival_scope": "all 5^7 partial allocations",
        "pool_size": len(rivals),
        "iterations": trace,
        "elapsed_seconds": time.time() - started,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "claim_boundary": {
            "sat": "exact unrestricted counterexample in the displayed strict seven-good adjacent-large atom",
            "unsat": "exact theorem only in the displayed atom; arbitrary packets still require an analytic lift",
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
    parser.add_argument("--order", default="0,1,2,3")
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=30)
    parser.add_argument("--add-per-iteration", type=int, default=64)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    order = tuple(int(part) for part in args.order.split(","))
    if sorted(order) != list(range(N)):
        raise ValueError("--order must be a permutation of 0,1,2,3")
    result = run(
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
