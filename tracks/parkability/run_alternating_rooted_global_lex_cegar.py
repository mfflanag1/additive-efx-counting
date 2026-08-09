#!/usr/bin/env python3
"""Exact rooted-global-lex CEGAR for the seven-good alternating atom."""

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
        BASE_BUNDLES,
        BASE_OWNER,
        N,
        V_STAR,
        atomic_json,
        integerize_model,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_alternating_global_lex_cegar import (
        AGENTS,
        BASE_BUNDLES,
        BASE_OWNER,
        N,
        V_STAR,
        atomic_json,
        integerize_model,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-rooted-global-lex-cegar-v1"
POOL_SCHEMA = "alternating-rooted-global-lex-rival-pool-v1"
Owner = tuple[int | None, ...]


def rooted_owners(root: int) -> tuple[Owner, ...]:
    if len(BASE_BUNDLES[root]) != 1:
        raise ValueError("the priority root must own a singleton")
    root_good = BASE_BUNDLES[root][0]
    remaining_goods = tuple(good for good in range(len(BASE_OWNER)) if good != root_good)
    destinations: tuple[int | None, ...] = tuple(
        agent for agent in range(N) if agent != root
    ) + (None,)
    owners = []
    for assignments in itertools.product(destinations, repeat=len(remaining_goods)):
        owner: list[int | None] = [None] * len(BASE_OWNER)
        owner[root_good] = root
        for good, destination in zip(remaining_goods, assignments):
            owner[good] = destination
        owners.append(tuple(owner))
    return tuple(owners)


def dominating_rooted_rivals(
    values: tuple[tuple[int, ...], ...],
    order: tuple[int, ...],
    candidates: tuple[Owner, ...],
) -> tuple[list[tuple[tuple[int, ...], Owner]], int]:
    base_utility = numeric_utilities(values, BASE_OWNER)
    base_key = tuple(base_utility[agent] for agent in order)
    found = []
    efx_count = 0
    for owner in candidates:
        if not numeric_efx(values, owner):
            continue
        efx_count += 1
        utility = numeric_utilities(values, owner)
        key = tuple(utility[agent] for agent in order)
        if key > base_key:
            found.append((key, owner))
    found.sort(reverse=True, key=lambda record: (record[0], str(record[1])))
    return found, efx_count


def load_pool(path: Path, order: tuple[int, ...], root: int) -> list[Owner]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("agent_order") != list(order)
        or payload.get("root") != root
    ):
        raise ValueError("pool metadata mismatch")
    rivals = [tuple(owner) for owner in payload["rivals"]]
    if len(rivals) != len(set(rivals)):
        raise ValueError("duplicate rival in pool")
    return rivals


def save_pool(path: Path, order: tuple[int, ...], root: int, rivals: list[Owner]) -> None:
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "agent_order": list(order),
            "root": root,
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(
    order: tuple[int, ...],
    pool_path: Path,
    result_path: Path,
    max_iterations: int,
    add_per_iteration: int,
    timeout_seconds: int,
) -> dict:
    root = order[0]
    candidates = rooted_owners(root)
    solver, values, base_own = structural_solver()
    solver.set(timeout=timeout_seconds * 1000)
    rivals = load_pool(pool_path, order, root)
    rival_set = set(rivals)

    seed_rivals, _ = dominating_rooted_rivals(V_STAR, order, candidates)
    for _, owner in seed_rivals:
        if owner not in rival_set:
            rivals.append(owner)
            rival_set.add(owner)
    for owner in rivals:
        solver.add(rival_blocker(values, base_own, owner, order))
    save_pool(pool_path, order, root, rivals)

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_ROOTED_ATOMIC_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values = integerize_model(solver.model(), values)
        found, efx_count = dominating_rooted_rivals(model_values, order, candidates)
        unseen = [owner for _, owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "rooted_efx_count": efx_count,
                "dominating_rooted_rival_count": len(found),
                "new_rival_count": len(unseen),
                "values": [list(row) for row in model_values],
            }
        )
        print(
            f"iteration={iteration} pool={len(rivals)} rooted_efx={efx_count} "
            f"dominating={len(found)} new={len(unseen)}",
            flush=True,
        )
        if not found:
            status = "SAT_NO_ROOTED_LEX_ESCAPE_ATOM"
            final_values = model_values
            break
        if not unseen:
            raise AssertionError("a pooled rooted rival still dominates the model")
        for owner in unseen[:add_per_iteration]:
            solver.add(rival_blocker(values, base_own, owner, order))
            rivals.append(owner)
            rival_set.add(owner)
        save_pool(pool_path, order, root, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "claim_boundary": {
            "sat": "refutes the rooted external-observer escape in the exact seven-good atom only",
            "unsat": "proves the rooted escape only in the exact seven-good atom until a cap-free argument is supplied",
        },
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "root": root,
        "root_name": AGENTS[root],
        "root_good": BASE_BUNDLES[root][0],
        "candidate_assignment_count": len(candidates),
        "iterations": len(trace),
        "pool_size": len(rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason_unknown,
        "values": None if final_values is None else [list(row) for row in final_values],
        "trace": trace,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-order", required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=200)
    parser.add_argument("--add-per-iteration", type=int, default=64)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    order = tuple(int(field) for field in args.agent_order.split(","))
    if sorted(order) != list(range(N)):
        parser.error("agent order must be a permutation of 0,1,2,3")
    if order[0] not in (0, 2):
        parser.error("the first agent must be singleton owner p=0 or s=2")
    if args.result.exists():
        parser.error("result path must not exist")
    result = run(
        order,
        args.pool,
        args.result,
        args.max_iterations,
        args.add_per_iteration,
        args.timeout_seconds,
    )
    print(
        json.dumps(
            {key: result[key] for key in ("status", "iterations", "pool_size", "elapsed_seconds")},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
