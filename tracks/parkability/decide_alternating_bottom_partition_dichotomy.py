#!/usr/bin/env python3
"""Decide a structured bottom-partition escape menu in the full binary cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        integerize,
        make_cell,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        integerize,
        make_cell,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-bottom-partition-dichotomy-v1"
SIZES = (2, 2, 2, 2)
ORDER = (0, 2, 1, 3)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner(cell, assigned_bundles) -> tuple[int | None, ...]:
    result = [None] * cell["m"]
    for agent, goods in assigned_bundles.items():
        for good in goods:
            if result[good] is not None:
                raise AssertionError((good, result[good], agent))
            result[good] = agent
    return tuple(result)


def menu(cell):
    tr, br, tq, bq = cell["packets"]
    x, y, floater = cell["x"], cell["y"], cell["floater"]
    xr = tr + br
    xq = tq + bq
    records = []

    # Promote s to its selected desired set and give q any subset of the
    # cross-bottom offer.  The other goods may remain charity.
    offer = xr + bq
    for size in range(len(offer) + 1):
        for q_bundle in itertools.combinations(offer, size):
            records.append(
                (
                    "promote_s",
                    owner(cell, {0: (x,), 1: (y,), 2: tq + (floater,), 3: q_bundle}),
                )
            )

    # Move a nonempty part of B_q to r, optionally releasing any part of
    # X_r, and leave q the complementary part of its old bundle.
    for incoming_size in range(1, len(bq) + 1):
        for incoming in itertools.combinations(bq, incoming_size):
            q_bundle = tuple(good for good in xq if good not in incoming)
            for release_size in range(len(xr) + 1):
                for release in itertools.combinations(xr, release_size):
                    r_bundle = tuple(good for good in xr if good not in release) + incoming
                    records.append(
                        (
                            "transfer_to_r",
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


def check(cell, records, timeout_ms: int):
    solver, values, own = structural_solver(cell)
    solver.set(timeout=timeout_ms)
    solver.add(*(rival_blocker(values, own, allocation, ORDER) for _, allocation in records))
    started = time.monotonic()
    status = solver.check()
    elapsed = time.monotonic() - started
    return solver, values, status, elapsed


def decide(timeout_seconds: float) -> dict:
    cell = make_cell(SIZES)
    records = menu(cell)
    solver, values, status, elapsed = check(cell, records, int(timeout_seconds * 1000))
    status_name = (
        "STRUCTURED_DICHOTOMY_REFUTED"
        if status == z3.sat
        else "STRUCTURED_DICHOTOMY_UNSAT_FULL_BINARY_CELL"
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
            mode: sum(record_mode == mode for record_mode, _ in records)
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
            "sat": "refutes only the structured two-mode menu in the full binary cell",
            "unsat": "proves only that structured menu in the full binary cell until a cap-free proof is supplied",
            "not_proved": "the arbitrary-packet external-observer lemma or complete EFX",
        },
    }
    if status == z3.sat:
        result["values"] = [list(row) for row in integerize(solver.model(), values)]
    elif status == z3.unsat:
        # Obtain and greedily shrink a deletion-minimal rival menu without
        # any further model-generation loop.
        core_solver, core_values, core_own = structural_solver(cell)
        assumptions = [z3.Bool(f"menu_{index}") for index in range(len(records))]
        core_solver.add(
            *(
                z3.Implies(
                    assumption,
                    rival_blocker(core_values, core_own, allocation, ORDER),
                )
                for assumption, (_, allocation) in zip(assumptions, records)
            )
        )
        if core_solver.check(*assumptions) != z3.unsat:
            raise AssertionError("UNSAT menu did not replay")
        indices = sorted(
            int(str(item).rsplit("_", 1)[1]) for item in core_solver.unsat_core()
        )
        active = [records[index] for index in indices]
        changed = True
        while changed:
            changed = False
            for index in range(len(active)):
                reduced = active[:index] + active[index + 1 :]
                _, _, reduced_status, _ = check(cell, reduced, 0)
                if reduced_status == z3.unsat:
                    active = reduced
                    changed = True
                    break
        result["minimal_core"] = [
            {"mode": mode, "owner_by_good": list(allocation)}
            for mode, allocation in active
        ]
        result["minimal_core_size"] = len(active)
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
    print(json.dumps({key: result.get(key) for key in ("status", "menu_size", "mode_counts", "minimal_core_size", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
