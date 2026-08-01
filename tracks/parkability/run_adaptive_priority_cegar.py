#!/usr/bin/env python3
"""Exact CEGAR for a fixed all-priority lex-max obstruction cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .anneal_lexmax_all_orders import exact_all_orders
    from .lra_master import ParkabilityLRAMaster
    from .normalize_smt2_for_cvc5 import atomic_write
    from .run_lexmax_partial_cegar import (
        Base,
        add_candidate,
        add_rival_blocker,
        lex_rivals,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from anneal_lexmax_all_orders import exact_all_orders
    from lra_master import ParkabilityLRAMaster
    from normalize_smt2_for_cvc5 import atomic_write
    from run_lexmax_partial_cegar import (
        Base,
        add_candidate,
        add_rival_blocker,
        lex_rivals,
    )


SCHEMA = "adaptive-priority-lra-cegar-v1"
POOL_SCHEMA = "adaptive-priority-rival-pool-v1"
Cell = tuple[tuple[int, ...], Base]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive_unique_seed_cells(
    values: tuple[tuple[int, ...], ...],
) -> list[Cell]:
    n = len(values)
    candidates = []
    for floater in range(len(values[0])):
        for base in core.iter_efx_bases(values, floater):
            utilities = tuple(base["own_values"])
            if all(
                utilities[observer] >= values[observer][floater]
                for observer in range(n)
            ):
                candidates.append(
                    (
                        floater,
                        tuple(base["base_owner"]),
                        utilities,
                    )
                )
    if not candidates:
        raise ValueError("seed has no eligible one-unallocated EFX state")

    cells = []
    for order in itertools.permutations(range(n)):
        best_key = max(
            tuple(candidate[2][agent] for agent in order)
            for candidate in candidates
        )
        best = [
            (candidate[0], candidate[1])
            for candidate in candidates
            if tuple(candidate[2][agent] for agent in order) == best_key
        ]
        if len(best) != 1:
            raise ValueError(
                f"seed order {order} has {len(best)} lex-max states; "
                "a unique-state seed is required"
            )
        cells.append((order, best[0]))
    return cells


def cell_document(order: tuple[int, ...], candidate: Base) -> dict:
    return {
        "agent_order": list(order),
        "candidate": {
            "floater": candidate[0],
            "base_owner": list(candidate[1]),
        },
    }


def pool_document(
    n: int,
    m: int,
    cells: list[Cell],
    rivals_by_order: dict[tuple[int, ...], list[Base]],
) -> dict:
    return {
        "schema": POOL_SCHEMA,
        "n": n,
        "m": m,
        "cells": [
            {
                **cell_document(order, candidate),
                "rivals": [
                    {
                        "floater": floater,
                        "base_owner": list(base_owner),
                    }
                    for floater, base_owner in rivals_by_order[order]
                ],
            }
            for order, candidate in cells
        ],
    }


def load_pool(
    path: Path,
    n: int,
    m: int,
    cells: list[Cell],
) -> dict[tuple[int, ...], list[Base]]:
    empty = {order: [] for order, _ in cells}
    if not path.exists():
        return empty
    raw = json.loads(path.read_text())
    if (
        raw.get("schema") != POOL_SCHEMA
        or raw.get("n") != n
        or raw.get("m") != m
        or not isinstance(raw.get("cells"), list)
        or len(raw["cells"]) != len(cells)
    ):
        raise ValueError("adaptive-priority rival pool metadata mismatch")

    result: dict[tuple[int, ...], list[Base]] = {}
    for record, (order, candidate) in zip(raw["cells"], cells):
        if {
            "agent_order": record.get("agent_order"),
            "candidate": record.get("candidate"),
        } != cell_document(order, candidate):
            raise ValueError("adaptive-priority rival pool cell mismatch")
        if not isinstance(record.get("rivals"), list):
            raise ValueError("adaptive-priority rival list is missing")
        rivals = [
            (rival["floater"], tuple(rival["base_owner"]))
            for rival in record["rivals"]
        ]
        if len(rivals) != len(set(rivals)) or candidate in rivals:
            raise ValueError("adaptive-priority pool has duplicate rival")
        for floater, base_owner in rivals:
            core.validate_triple(
                {
                    "floater": floater,
                    "base_owner": list(base_owner),
                    "host": 0,
                },
                n,
                m,
            )
        result[order] = rivals
    return result


def run(
    *,
    seed_path: Path,
    pool_path: Path,
    result_path: Path,
    smt2_path: Path,
    add_per_cell: int,
    max_iterations: int,
    time_limit_s: float,
    require_distinct_item_values: bool,
) -> dict:
    if (
        result_path.exists()
        or smt2_path.exists()
        or add_per_cell < 1
        or max_iterations < 1
        or time_limit_s <= 0
    ):
        raise ValueError("new outputs and valid search parameters are required")
    raw_seed = json.loads(seed_path.read_text())
    raw_values = raw_seed.get("values", raw_seed.get("candidate_values"))
    if raw_values is None:
        raise ValueError("seed JSON contains no values")
    seed_values = core.validate_values(raw_values, lower=1)
    n = len(seed_values)
    m = len(seed_values[0])
    cells = derive_unique_seed_cells(seed_values)
    unique_candidates = list(dict.fromkeys(candidate for _, candidate in cells))

    rivals_by_order = load_pool(pool_path, n, m, cells)
    rival_sets = {
        order: set(rivals)
        for order, rivals in rivals_by_order.items()
    }
    atomic_json(
        pool_path,
        pool_document(n, m, cells, rivals_by_order),
    )

    master = ParkabilityLRAMaster(
        n,
        m,
        require_distinct_item_values=require_distinct_item_values,
    )
    candidate_utilities = {
        candidate: add_candidate(master, *candidate)
        for candidate in unique_candidates
    }
    for order, candidate in cells:
        for rival in rivals_by_order[order]:
            add_rival_blocker(
                master,
                candidate_utilities[candidate],
                candidate[1],
                rival,
                order,
                "exact",
            )

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    result_values = None
    exact_audit = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit_s)
        if solved.status == "UNSAT":
            status = "UNSAT_FIXED_CANDIDATE_CELL"
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            reason_unknown = solved.reason_unknown
            break
        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=n,
            expected_m=m,
            lower=1,
        )

        audits = []
        total_found = 0
        total_unseen = 0
        all_clear = True
        for order, candidate in cells:
            found, audit = lex_rivals(values, candidate, order)
            unseen = [
                rival
                for rival in found
                if rival not in rival_sets[order]
            ]
            if found:
                all_clear = False
            if found and not unseen:
                raise AssertionError("model satisfies a pooled rival blocker")
            total_found += len(found)
            total_unseen += len(unseen)
            audits.append(
                {
                    "agent_order": list(order),
                    "candidate_index": unique_candidates.index(candidate),
                    "nonlower_rival_count": len(found),
                    "new_nonlower_rival_count": len(unseen),
                    **audit,
                }
            )
            for rival in unseen[:add_per_cell]:
                add_rival_blocker(
                    master,
                    candidate_utilities[candidate],
                    candidate[1],
                    rival,
                    order,
                    "exact",
                )
                rivals_by_order[order].append(rival)
                rival_sets[order].add(rival)

        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": sum(
                    len(rivals) for rivals in rivals_by_order.values()
                )
                - sum(
                    min(
                        audit["new_nonlower_rival_count"],
                        add_per_cell,
                    )
                    for audit in audits
                ),
                "total_nonlower_rival_count": total_found,
                "new_nonlower_rival_count": total_unseen,
                "values": [list(row) for row in values],
                "cell_audits": audits,
            }
        )
        print(
            f"iteration={iteration} "
            f"pool={sum(len(rivals) for rivals in rivals_by_order.values())} "
            f"nonlower_rivals={total_found} new={total_unseen}",
            flush=True,
        )
        if all_clear:
            exact_audit = exact_all_orders([list(row) for row in values])
            if exact_audit["insertable_agent_order_count"] != 0:
                raise AssertionError(
                    "terminal adaptive counterexample failed all-order replay"
                )
            status = "ALL_ORDERS_BLOCKED_COUNTEREXAMPLE"
            result_values = values
            break
        atomic_json(
            pool_path,
            pool_document(n, m, cells, rivals_by_order),
        )

    atomic_json(
        pool_path,
        pool_document(n, m, cells, rivals_by_order),
    )
    atomic_write(smt2_path, master.to_smt2().encode())
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "a counterexample refutes only adaptive-priority lex-max direct "
            "completion, not complete EFX existence; UNSAT closes only the "
            "fixed candidate cell derived from the seed"
        ),
        "n": n,
        "m": m,
        "seed_path": str(seed_path.resolve()),
        "seed_sha256": sha256(seed_path),
        "candidate_count": len(unique_candidates),
        "candidates": [
            {
                "floater": floater,
                "base_owner": list(base_owner),
            }
            for floater, base_owner in unique_candidates
        ],
        "cells": [
            {
                **cell_document(order, candidate),
                "candidate_index": unique_candidates.index(candidate),
                "pool_size": len(rivals_by_order[order]),
            }
            for order, candidate in cells
        ],
        "require_distinct_item_values": require_distinct_item_values,
        "add_per_cell": add_per_cell,
        "iterations": len(trace),
        "pool_size": sum(
            len(rivals) for rivals in rivals_by_order.values()
        ),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason_unknown,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "exact_audit": exact_audit,
        "trace": trace,
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": sha256(pool_path),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": sha256(smt2_path),
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--add-per-cell", type=int, default=32)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--require-distinct-item-values", action="store_true")
    args = parser.parse_args()
    result = run(
        seed_path=args.seed,
        pool_path=args.pool,
        result_path=args.result,
        smt2_path=args.smt2,
        add_per_cell=args.add_per_cell,
        max_iterations=args.max_iterations,
        time_limit_s=args.time_limit,
        require_distinct_item_values=args.require_distinct_item_values,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
