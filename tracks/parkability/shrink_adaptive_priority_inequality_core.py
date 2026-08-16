#!/usr/bin/env python3
"""Shrink an adaptive-priority obstruction to individual candidate constraints."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster
    from .normalize_smt2_for_cvc5 import atomic_write
    from .run_adaptive_priority_cegar import derive_unique_seed_cells
    from .run_lexmax_partial_cegar import (
        bundles_of,
        candidate_constraint_records,
        rival_blocker_expression,
        subset_sum,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster
    from normalize_smt2_for_cvc5 import atomic_write
    from run_adaptive_priority_cegar import derive_unique_seed_cells
    from run_lexmax_partial_cegar import (
        bundles_of,
        candidate_constraint_records,
        rival_blocker_expression,
        subset_sum,
    )


SCHEMA = "adaptive-priority-inequality-core-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assumption_records(
    master: ParkabilityLRAMaster,
    cells: list,
    compact_core: dict,
) -> list[dict]:
    unique_candidates = list(dict.fromkeys(candidate for _, candidate in cells))
    utilities = {}
    for candidate in unique_candidates:
        bundles = bundles_of(candidate[1], master.n)
        utilities[candidate] = tuple(
            subset_sum(master, observer, bundles[observer])
            for observer in range(master.n)
        )

    records = []
    candidate_indices = {
        core_record["candidate_index"]
        for core_record in compact_core["core"]
        if core_record["kind"] == "candidate"
    } | set(compact_core.get("dependency_candidate_indices", []))
    for candidate_index in sorted(candidate_indices):
        candidate = unique_candidates[candidate_index]
        _, constraints = candidate_constraint_records(master, *candidate)
        for constraint_index, constraint in enumerate(constraints):
            metadata = {
                key: value
                for key, value in constraint.items()
                if key != "constraint"
            }
            constraint_kind = metadata.pop("kind")
            records.append(
                {
                    "kind": "candidate_constraint",
                    "constraint_kind": constraint_kind,
                    "candidate_index": candidate_index,
                    "constraint_index": constraint_index,
                    **metadata,
                    "expression": constraint["constraint"],
                }
            )

    for compact_index, core_record in enumerate(compact_core["core"]):
        if core_record["kind"] != "rival":
            continue
        cell_index = core_record["cell_index"]
        order, candidate = cells[cell_index]
        rival = (
            core_record["rival"]["floater"],
            tuple(core_record["rival"]["base_owner"]),
        )
        records.append(
            {
                "kind": "rival_blocker",
                "compact_core_index": compact_index,
                "cell_index": cell_index,
                "agent_order": list(order),
                "candidate_index": core_record["candidate_index"],
                "rival": core_record["rival"],
                "expression": rival_blocker_expression(
                    master,
                    utilities[candidate],
                    candidate[1],
                    rival,
                    order,
                    "exact",
                ),
            }
        )
    return records


def public_record(record: dict) -> dict:
    return {
        key: value
        for key, value in record.items()
        if key != "expression"
    }


def run(
    *,
    seed_path: Path,
    compact_core_path: Path,
    output_path: Path,
    smt2_path: Path,
    time_limit_s: float,
) -> dict:
    if (
        output_path.exists()
        or smt2_path.exists()
        or time_limit_s <= 0
    ):
        raise ValueError("new outputs and a positive time limit are required")
    raw_seed = json.loads(seed_path.read_text())
    raw_values = raw_seed.get("values", raw_seed.get("candidate_values"))
    if raw_values is None:
        raise ValueError("seed JSON contains no values")
    seed_values = core.validate_values(raw_values, lower=1)
    n = len(seed_values)
    m = len(seed_values[0])
    cells = derive_unique_seed_cells(seed_values)
    compact_core = json.loads(compact_core_path.read_text())
    if (
        compact_core.get("schema") != "adaptive-priority-rival-core-v1"
        or compact_core.get("status")
        != "UNSAT_DELETION_MINIMAL_RIVAL_CORE"
        or compact_core.get("n") != n
        or compact_core.get("m") != m
    ):
        raise ValueError("invalid compact adaptive-priority core")

    master = ParkabilityLRAMaster(n, m)
    records = assumption_records(master, cells, compact_core)
    selectors = [
        z3.Bool(f"active_inequality_{index}")
        for index in range(len(records))
    ]
    for selector, record in zip(selectors, records):
        master.solver.add(z3.Implies(selector, record["expression"]))
    master.solver.set(timeout=round(time_limit_s * 1000))

    started = time.time()
    verdict = master.solver.check(*selectors)
    if verdict != z3.unsat:
        raise RuntimeError(
            f"expanded inequality formula is {verdict}: "
            f"{master.solver.reason_unknown()}"
        )
    by_name = {
        selector.decl().name(): index
        for index, selector in enumerate(selectors)
    }
    initial_core = [
        by_name[item.decl().name()]
        for item in master.solver.unsat_core()
    ]
    active = initial_core[:]
    checks = 1
    for index in initial_core:
        trial = [other for other in active if other != index]
        result = master.solver.check(*(selectors[other] for other in trial))
        checks += 1
        if result == z3.unsat:
            active = trial
        elif result != z3.sat:
            raise RuntimeError(
                f"inequality-core shrink is {result}: "
                f"{master.solver.reason_unknown()}"
            )
    necessity = []
    for index in active:
        trial = [other for other in active if other != index]
        result = master.solver.check(*(selectors[other] for other in trial))
        checks += 1
        necessity.append(
            {
                "assumption_index": index,
                "status_without": str(result),
            }
        )
        if result != z3.sat:
            raise AssertionError("inequality core is not deletion-minimal")

    frozen = ParkabilityLRAMaster(n, m)
    frozen_records = assumption_records(frozen, cells, compact_core)
    if [
        public_record(record) for record in frozen_records
    ] != [
        public_record(record) for record in records
    ]:
        raise AssertionError("frozen inequality records changed")
    for index in active:
        frozen.solver.add(frozen_records[index]["expression"])
    frozen_result = frozen.solve(time_limit_s=time_limit_s)
    if frozen_result.status != "UNSAT":
        raise AssertionError("frozen inequality core is not UNSAT")
    atomic_write(smt2_path, frozen.to_smt2().encode())

    active_records = [records[index] for index in active]
    result = {
        "schema": SCHEMA,
        "status": "UNSAT_DELETION_MINIMAL_INEQUALITY_CORE",
        "meaning": (
            "this is a local logical handoff certificate for one fixed "
            "4x9 candidate cell, not a general EFX existence proof"
        ),
        "n": n,
        "m": m,
        "seed_path": str(seed_path.resolve()),
        "seed_sha256": sha256(seed_path),
        "compact_core_path": str(compact_core_path.resolve()),
        "compact_core_sha256": sha256(compact_core_path),
        "initial_assumption_count": len(records),
        "solver_unsat_core_count": len(initial_core),
        "deletion_minimal_assumption_count": len(active),
        "candidate_constraint_count": sum(
            record["kind"] == "candidate_constraint"
            for record in active_records
        ),
        "rival_blocker_count": sum(
            record["kind"] == "rival_blocker"
            for record in active_records
        ),
        "solver_checks": checks,
        "elapsed_seconds": time.time() - started,
        "core": [
            {
                "assumption_index": index,
                **public_record(records[index]),
            }
            for index in active
        ],
        "necessity_replay": necessity,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": sha256(smt2_path),
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--compact-core", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    args = parser.parse_args()
    result = run(
        seed_path=args.seed,
        compact_core_path=args.compact_core,
        output_path=args.output,
        smt2_path=args.smt2,
        time_limit_s=args.time_limit,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
