#!/usr/bin/env python3
"""Decide the any-root/any-cross-subset dichotomy in the full binary cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .decide_alternating_bottom_partition_dichotomy import ORDER, SIZES, owner
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        integerize,
        make_cell,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from decide_alternating_bottom_partition_dichotomy import ORDER, SIZES, owner
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        integerize,
        make_cell,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-any-cross-subset-dichotomy-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def menu(cell):
    tr, br, tq, bq = cell["packets"]
    x, y, floater = cell["x"], cell["y"], cell["floater"]
    xr = tr + br
    xq = tq + bq
    records = []

    for s_size in range(1, len(xq) + 1):
        for s_old in itertools.combinations(xq, s_size):
            remainder = xr + tuple(good for good in xq if good not in s_old)
            for q_size in range(len(remainder) + 1):
                for q_bundle in itertools.combinations(remainder, q_size):
                    records.append(
                        (
                            "root_subset",
                            owner(
                                cell,
                                {
                                    0: (x,),
                                    1: (y,),
                                    2: s_old + (floater,),
                                    3: q_bundle,
                                },
                            ),
                        )
                    )

    # The countermodel to the bottom-only menu requires a top good from T_q.
    # Permit every nonempty incoming subset of X_q and every release from X_r.
    for incoming_size in range(1, len(xq) + 1):
        for incoming in itertools.combinations(xq, incoming_size):
            q_bundle = tuple(good for good in xq if good not in incoming)
            for release_size in range(len(xr) + 1):
                for release in itertools.combinations(xr, release_size):
                    r_bundle = tuple(good for good in xr if good not in release) + incoming
                    records.append(
                        (
                            "cross_subset_to_r",
                            owner(cell, {0: (x,), 1: r_bundle, 2: (y,), 3: q_bundle}),
                        )
                    )

    deduplicated = []
    seen = set()
    for mode, allocation in records:
        if allocation not in seen:
            seen.add(allocation)
            deduplicated.append((mode, allocation))
    return deduplicated


def decide(timeout_seconds: float) -> dict:
    cell = make_cell(SIZES)
    records = menu(cell)
    solver, values, own = structural_solver(cell)
    solver.set(timeout=int(timeout_seconds * 1000))
    solver.add(*(rival_blocker(values, own, allocation, ORDER) for _, allocation in records))
    started = time.monotonic()
    status = solver.check()
    elapsed = time.monotonic() - started
    status_name = (
        "ALL_CROSS_DICHOTOMY_REFUTED"
        if status == z3.sat
        else "ALL_CROSS_DICHOTOMY_UNSAT_FULL_BINARY_CELL"
        if status == z3.unsat
        else "UNKNOWN"
    )
    result = {
        "schema": SCHEMA,
        "status": status_name,
        "packet_sizes": list(SIZES),
        "goods": list(cell["goods"]),
        "agent_order": list(ORDER),
        "agent_order_names": [AGENTS[agent] for agent in ORDER],
        "menu_size": len(records),
        "mode_counts": {
            mode: sum(candidate_mode == mode for candidate_mode, _ in records)
            for mode in sorted({mode for mode, _ in records})
        },
        "elapsed_seconds": elapsed,
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
            "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
        },
        "claim_boundary": {
            "sat": "refutes only the two-mode all-cross menu in the full binary cell",
            "unsat": "proves only that menu in the full binary cell until a cap-free proof is supplied",
            "not_proved": "the arbitrary-packet external-observer lemma or complete EFX",
        },
    }
    if status == z3.sat:
        result["values"] = [list(row) for row in integerize(solver.model(), values)]
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": sha256(script),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = decide(args.timeout_seconds)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in ("status", "menu_size", "mode_counts", "elapsed_seconds")
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
