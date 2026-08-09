#!/usr/bin/env python3
"""Shrink all-order adjacent-large atomic rival pools to exact UNSAT cores."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_adjacent_large_global_lex_atomic_cegar import (
        AGENTS,
        BASE_OWNER,
        GOODS,
        load_pool,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_adjacent_large_global_lex_atomic_cegar import (
        AGENTS,
        BASE_OWNER,
        GOODS,
        load_pool,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "adjacent-large-global-lex-atomic-core-extraction-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shrink(order: tuple[int, ...], rivals):
    solver, values, own = structural_solver()
    tags = []
    by_name = {}
    for index, owner in enumerate(rivals):
        tag = z3.Bool(f"rival_{index}")
        solver.add(z3.Implies(tag, rival_blocker(values, own, owner, order)))
        tags.append(tag)
        by_name[str(tag)] = owner
    if solver.check(*tags) != z3.unsat:
        raise AssertionError((order, "pool is not UNSAT"))
    core = list(solver.unsat_core())
    for tag in tuple(core):
        trial = [candidate for candidate in core if candidate is not tag]
        if solver.check(*trial) == z3.unsat:
            core = trial
    if any(
        solver.check(*(candidate for candidate in core if candidate is not tag))
        != z3.sat
        for tag in core
    ):
        raise AssertionError((order, "core is not deletion-minimal"))
    return [by_name[str(tag)] for tag in core]


def extract(pool_directory: Path) -> dict:
    records = []
    for order in itertools.permutations(range(4)):
        tag = "".join(map(str, order))
        pool_path = pool_directory / f"adjacent-{tag}-pool.json"
        rivals = load_pool(pool_path, order)
        core = shrink(order, rivals)
        records.append(
            {
                "agent_order": list(order),
                "agent_order_names": [AGENTS[agent] for agent in order],
                "pool_size": len(rivals),
                "core_size": len(core),
                "rival_allocations": [list(owner) for owner in core],
            }
        )
    script = Path(__file__).resolve()
    search = script.with_name("run_adjacent_large_global_lex_atomic_cegar.py")
    return {
        "schema": SCHEMA,
        "status": "ALL_24_ADJACENT_ATOMIC_ORDERS_UNSAT",
        "agents": list(AGENTS),
        "goods": list(GOODS),
        "base_owner_by_good": list(BASE_OWNER),
        "priority_order_count": len(records),
        "single_rival_order_count": sum(record["core_size"] == 1 for record in records),
        "maximum_core_size": max(record["core_size"] for record in records),
        "total_order_specific_rivals": sum(record["core_size"] for record in records),
        "orders": records,
        "claim_boundary": {
            "proved_exactly": "no globally lexicographically maximal state exists in the strict seven-good adjacent-large structural atom",
            "not_proved": "the adjacent-large escape for arbitrary packet sizes or complete four-agent EFX",
        },
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
            "search_script": str(search.relative_to(search.parents[2])),
            "search_script_sha256": sha256(search),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool-directory", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = extract(args.pool_directory)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
