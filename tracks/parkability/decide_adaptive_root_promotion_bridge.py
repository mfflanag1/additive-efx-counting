#!/usr/bin/env python3
"""Decide whether both promoted root rotations can fail in the atomic cell."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

from run_alternating_global_lex_cegar import (
    AGENTS,
    ALL_OWNERS,
    BASE_OWNER,
    N,
    Owner,
    bundles,
    integerize_model,
    numeric_efx,
    numeric_utilities,
    structural_solver,
    subset_sum,
)


SCHEMA = "alternating-adaptive-root-promotion-bridge-v1"
ROOT_OWNERS: dict[str, Owner] = {
    "p_anchored": (2, None, 3, 3, 0, 1, 2),
    "p_promoted": (0, None, 2, 2, 3, 1, 0),
    "s_anchored": (1, 1, 0, None, 3, 2, 0),
    "s_promoted": (0, 0, 2, None, 3, 1, 2),
    "q_bottom_for_charity": (1, 1, 3, 1, 0, 2, 3),
    "r_bottom_for_charity": (1, 3, 3, 3, 0, 2, 1),
    "cross_bottom_swap": (1, 3, 3, 1, 0, 2, None),
}
SURVIVING_ORDERS = ((0, 2, 1, 3), (2, 0, 3, 1))


def efx_failure(values, owner: Owner):
    assigned = bundles(owner)
    own = tuple(subset_sum(values, agent, assigned[agent]) for agent in range(N))
    failures = []
    for observer in range(N):
        for target in range(N):
            for removed in assigned[target]:
                remainder = tuple(good for good in assigned[target] if good != removed)
                failures.append(own[observer] < subset_sum(values, observer, remainder))
    return z3.Or(*failures)


def smallest_lex_escape(values, order):
    base = numeric_utilities(values, BASE_OWNER)
    base_key = tuple(base[agent] for agent in order)
    records = []
    for owner in ALL_OWNERS:
        if not numeric_efx(values, owner):
            continue
        utility = numeric_utilities(values, owner)
        if tuple(utility[agent] for agent in order) <= base_key:
            continue
        changed = sum(left != right for left, right in zip(owner, BASE_OWNER))
        records.append((changed, owner, utility))
    if not records:
        return None
    changed, owner, utility = min(records, key=lambda record: (record[0], str(record[1])))
    return {
        "changed_goods": changed,
        "owner": list(owner),
        "utility": list(utility),
        "delta": [right - left for left, right in zip(base, utility)],
    }


def decide(timeout_seconds, block_bottom_swaps, block_cross_bottom_swap):
    solver, symbolic, _ = structural_solver()
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(efx_failure(symbolic, ROOT_OWNERS["p_promoted"]))
    solver.add(efx_failure(symbolic, ROOT_OWNERS["s_promoted"]))
    if block_bottom_swaps:
        solver.add(efx_failure(symbolic, ROOT_OWNERS["q_bottom_for_charity"]))
        solver.add(efx_failure(symbolic, ROOT_OWNERS["r_bottom_for_charity"]))
    if block_cross_bottom_swap:
        solver.add(efx_failure(symbolic, ROOT_OWNERS["cross_bottom_swap"]))
    status = solver.check()
    result = {
        "schema": SCHEMA,
        "solver_status": str(status),
        "block_bottom_swaps": block_bottom_swaps,
        "block_cross_bottom_swap": block_cross_bottom_swap,
        "claim_boundary": {
            "sat": (
                "refutes only the selected finite root/exchange menu; it does not "
                "refute adaptive escape with broader anchored suffix operations"
            ),
            "unsat": "would prove the canonical promoted-root alternative only in the atomic cell",
        },
    }
    if status == z3.sat:
        values = integerize_model(solver.model(), symbolic)
        base = numeric_utilities(values, BASE_OWNER)
        root_records = {}
        for name, owner in ROOT_OWNERS.items():
            utility = numeric_utilities(values, owner)
            root_records[name] = {
                "owner": list(owner),
                "efx": numeric_efx(values, owner),
                "utility": list(utility),
                "delta": [right - left for left, right in zip(base, utility)],
            }
        if root_records["p_promoted"]["efx"] or root_records["s_promoted"]["efx"]:
            raise AssertionError("promoted bridge countermodel did not replay")
        result.update(
            {
                "status": (
                    "SAT_AUGMENTED_ROOT_MENU_FAILS"
                    if block_bottom_swaps or block_cross_bottom_swap
                    else "SAT_BOTH_PROMOTED_ROOTS_FAIL"
                ),
                "values": [list(row) for row in values],
                "base_owner": list(BASE_OWNER),
                "base_utility": list(base),
                "root_allocations": root_records,
                "smallest_surviving_order_escapes": [
                    {
                        "agent_order": list(order),
                        "agent_order_names": [AGENTS[agent] for agent in order],
                        "escape": smallest_lex_escape(values, order),
                    }
                    for order in SURVIVING_ORDERS
                ],
            }
        )
    elif status == z3.unsat:
        result["status"] = "UNSAT_SELECTED_ADAPTIVE_ROOT_MENU"
    else:
        result.update({"status": "UNKNOWN", "reason_unknown": solver.reason_unknown()})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--block-bottom-swaps", action="store_true")
    parser.add_argument("--block-cross-bottom-swap", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = decide(
        args.timeout_seconds,
        args.block_bottom_swaps,
        args.block_cross_bottom_swap,
    )
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps({key: result[key] for key in ("status", "solver_status")}, indent=2))


if __name__ == "__main__":
    main()
