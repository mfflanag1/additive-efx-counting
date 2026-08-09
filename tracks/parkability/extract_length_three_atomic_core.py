#!/usr/bin/env python3
"""Extract a deletion-minimal rival core from a length-three atomic pool."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import bundles, rival_blocker
    from .run_length_three_global_lex_atomic_cegar import (
        AGENTS,
        GOODS,
        load_pool,
        structural_solver,
    )
except ImportError:
    from run_alternating_global_lex_cegar import bundles, rival_blocker
    from run_length_three_global_lex_atomic_cegar import (
        AGENTS,
        GOODS,
        load_pool,
        structural_solver,
    )


def named(owner):
    return [
        [GOODS[good] for good in bundle]
        for bundle in bundles(owner)
    ]


def extract(source, order, pool_path):
    rivals = load_pool(pool_path, source, order)
    solver, values, own = structural_solver(source)
    active = []
    for index, owner in enumerate(rivals):
        guard = z3.Bool(f"rival_{index}")
        solver.add(z3.Implies(guard, rival_blocker(values, own, owner, order)))
        active.append((guard, owner))
    if solver.check(*(guard for guard, _owner in active)) != z3.unsat:
        raise AssertionError("pool is not UNSAT")
    core_names = set(solver.unsat_core())
    core = [record for record in active if record[0] in core_names]
    changed = True
    while changed:
        changed = False
        for record in tuple(core):
            trial = [other for other in core if other != record]
            if solver.check(*(guard for guard, _owner in trial)) == z3.unsat:
                core = trial
                changed = True
                break
    return {
        "schema": "length-three-global-lex-atomic-core-v1",
        "singleton_champion_source": source,
        "singleton_champion_source_name": AGENTS[source],
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "pool_size": len(rivals),
        "core_size": len(core),
        "rivals": [
            {"owner": list(owner), "bundles": named(owner)}
            for _guard, owner in core
        ],
        "claim_boundary": "atomic proof-mining core only; not a packet theorem",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--singleton-source", choices=AGENTS[:3], required=True)
    parser.add_argument("--order", required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = AGENTS.index(args.singleton_source)
    order = tuple(AGENTS.index(name) for name in args.order.split(","))
    result = extract(source, order, args.pool)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
